---
title: "Scaling PostgreSQL to power 800 million ChatGPT users"
date: 2026-01-22
source: https://openai.com/index/scaling-postgresql/
crawled: 2026-09-13
category: engineering
---

For years, PostgreSQL has been one of the most critical, under-the-hood data systems powering core products like ChatGPT and OpenAI’s API. As our user base grows rapidly, the demands on our databases have increased exponentially, too. Over the past year, our PostgreSQL load has grown by more than 10x, and it continues to rise quickly.

Our efforts to advance our production infrastructure to sustain this growth revealed a new insight: PostgreSQL can be scaled to reliably support much larger read-heavy workloads than many previously thought possible. The system (initially created by a team of scientists at University of California, Berkeley) has enabled us to support massive global traffic with a single primary [Azure PostgreSQL flexible server instance](https://learn.microsoft.com/en-us/azure/postgresql/overview) and nearly 50 read replicas spread over multiple regions globally. This is the story of how we’ve scaled PostgreSQL at OpenAI to support millions of queries per second for 800 million users through rigorous optimizations and solid engineering; we’ll also cover key takeaways we learned along the way.

## Cracks in our initial design

After the launch of ChatGPT, traffic grew at an unprecedented rate. To support it, we rapidly implemented extensive optimizations at both the application and PostgreSQL database layers, scaled up by increasing the instance size, and scaled out by adding more read replicas. This architecture has served us well for a long time. With ongoing improvements, it continues to provide ample runway for future growth.

It may sound surprising that a single-primary architecture can meet the demands of OpenAI’s scale; however, making this work in practice isn’t simple. We’ve seen several SEVs caused by Postgres overload, and they often follow the same pattern: an upstream issue causes a sudden spike in database load, such as widespread cache misses from a caching-layer failure, a surge of expensive multi-way joins saturating CPU, or a write storm from a new feature launch. As resource utilization climbs, query latency rises and requests begin to time out. Retries then further amplify the load, triggering a vicious cycle with the potential to degrade the entire ChatGPT and API services.

Although PostgreSQL scales well for our read-heavy workloads, we still encounter challenges during periods of high write traffic. This is largely due to PostgreSQL’s multiversion concurrency control (MVCC) implementation, which makes it less efficient for write-heavy workloads. For example, when a query updates a tuple or even a single field, the entire row is copied to create a new version. Under heavy write loads, this results in significant write amplification. It also increases read amplification, since queries must scan through multiple tuple versions (dead tuples) to retrieve the latest one. MVCC introduces additional challenges such as table and index bloat, increased index maintenance overhead, and complex autovacuum tuning. (You can find a deep-dive on these issues in a blog I wrote with Prof. Andy Pavlo at Carnegie Mellon University called [*The Part of PostgreSQL We Hate the Most*](https://www.cs.cmu.edu/~pavlo/blog/2023/04/the-part-of-postgresql-we-hate-the-most.html), [cited](https://en.wikipedia.org/wiki/PostgreSQL#cite_note-37) in the PostgreSQL Wikipedia page.)

## Scaling PostgreSQL to millions of QPS

To mitigate these limitations and reduce write pressure, we’ve migrated, and continue to migrate, shardable (i.e. workloads that can be horizontally partitioned), write-heavy workloads to sharded systems such as Azure Cosmos DB, optimizing application logic to minimize unnecessary writes. We also no longer allow adding new tables to the current PostgreSQL deployment. New workloads default to the sharded systems.

Even as our infrastructure has evolved, PostgreSQL has remained unsharded, with a single primary instance serving all writes. The primary rationale is that sharding existing application workloads would be highly complex and time-consuming, requiring changes to hundreds of application endpoints and potentially taking months or even years. Since our workloads are primarily read-heavy, and we’ve implemented extensive optimizations, the current architecture still provides ample headroom to support continued traffic growth. While we’re not ruling out sharding PostgreSQL in the future, it’s not a near-term priority given the sufficient runway we have for current and future growth.

In the following sections, we’ll dive into the challenges we faced and the extensive optimizations we implemented to address them and prevent future outages, pushing PostgreSQL to its limits and scaling it to millions of queries per second (QPS).

### Reducing load on the primary

*Challenge: With only one writer, a single-primary setup can’t scale writes. Heavy write spikes can quickly overload the primary and impact services like ChatGPT and our API.*

Solution: We minimize load on the primary as much as possible—both reads and writes—to ensure it has sufficient capacity to handle write spikes. Read traffic is offloaded to replicas wherever possible. However, some read queries must remain on the primary because they’re part of write transactions. For those, we focus on ensuring they’re efficient and avoid slow queries. For write traffic, we’ve migrated shardable, write-heavy workloads to sharded systems such as Azure CosmosDB. Workloads that are harder to shard but still generate high write volume take longer to migrate, and that process is still ongoing. We also aggressively optimized our applications to reduce write load; for example, we’ve fixed application bugs that caused redundant writes and introduced lazy writes, where appropriate, to smooth traffic spikes. In addition, when backfilling table fields, we enforce strict rate limits to prevent excessive write pressure.

### Query optimization

*Challenge: We identified several expensive queries in PostgreSQL. In the past, sudden volume spikes in these queries would consume large amounts of CPU, slowing both ChatGPT and API requests.*

Solution: A few expensive queries, such as those joining many tables together, can significantly degrade or even bring down the entire service. We need to continuously optimize PostgreSQL queries to ensure they’re efficient and avoid common Online Transaction Processing (OLTP) anti-patterns. For example, we once identified an extremely costly query that joined 12 tables, where spikes in this query were responsible for past high-severity SEVs. We should avoid complex multi-table joins whenever possible. If joins are necessary, we learned to consider breaking down the query and move complex join logic to the application layer instead. Many of these problematic queries are generated by Object-Relational Mapping frameworks (ORMs), so it’s important to carefully review the SQL they produce and ensure it behaves as expected. It’s also common to find long-running idle queries in PostgreSQL. Configuring timeouts like idle_in_transaction_session_timeout is essential to prevent them from blocking autovacuum.

### Single point of failure mitigation

*Challenge: If a read replica goes down, traffic can still be routed to other replicas. However, relying on a single writer means having a single point of failure—if it goes down, the entire service is affected.*

Solution: Most critical requests only involve read queries. To mitigate the single point of failure in the primary, we offloaded those reads from the writer to replicas, ensuring those requests can continue serving even if the primary goes down. While write operations would still fail, the impact is reduced; it’s no longer a SEV0 since reads remain available.

To mitigate primary failures, we run the primary in High-Availability (HA) mode with a hot standby, a continuously synchronized replica that is always ready to take over serving traffic. If the primary goes down or needs to be taken offline for maintenance, we can quickly promote the standby to minimize downtime. The Azure PostgreSQL team has done significant work to ensure these failovers remain safe and reliable even under very high load. To handle read replica failures, we deploy multiple replicas in each region with sufficient capacity headroom, ensuring that a single replica failure doesn’t lead to a regional outage.

### Workload isolation

*Challenge: We often encounter situations where certain requests consume a disproportionate amount of resources on PostgreSQL instances. This can lead to degraded performance for other workloads running on the same instances. For example, a new feature launch can introduce inefficient queries that heavily consume PostgreSQL CPU, slowing down requests for other critical features.*

Solution: To mitigate the “noisy neighbor” problem, we isolate workloads onto dedicated instances to ensure that sudden spikes in resource-intensive requests don’t impact other traffic. Specifically, we split requests into low-priority and high-priority tiers and route them to separate instances. This way, even if a low-priority workload becomes resource-intensive, it won’t degrade the performance of high-priority requests. We apply the same strategy across different products and services as well, so that activity from one product does not affect the performance or reliability of another.

### Connection pooling

*Challenge: Each instance has a maximum connection limit (5,000 in Azure PostgreSQL). It’s easy to run out of connections or accumulate too many idle ones. We’ve previously had incidents caused by connection storms that exhausted all available connections.*

Solution: We deployed PgBouncer as a proxy layer to pool database connections. Running it in statement or transaction pooling mode allows us to efficiently reuse connections, greatly reducing the number of active client connections. This also cuts connection setup latency: in our benchmarks, the average connection time dropped from 50 milliseconds (ms) to 5 ms. Inter-region connections and requests can be expensive, so we co-locate the proxy, clients, and replicas in the same region to minimize network overhead and connection use time. Moreover, PgBouncer must be configured carefully. Settings like idle timeouts are critical to prevent connection exhaustion.

Each read replica has its own Kubernetes deployment running multiple PgBouncer pods. We run multiple Kubernetes deployments behind the same Kubernetes Service, which load-balances traffic across pods.

### Caching

*Challenge: A sudden spike in cache misses can trigger a surge of reads on the PostgreSQL database, saturating CPU and slowing user requests.*

Solution: To reduce read pressure on PostgreSQL, we use a caching layer to serve most of the read traffic. However, when cache hit rates drop unexpectedly, the burst of cache misses can push a large volume of requests directly to PostgreSQL. This sudden increase in database reads consumes significant resources, slowing down the service. To prevent overload during cache-miss storms, we implement a cache locking (and leasing) mechanism so that only a single reader that misses on a particular key fetches the data from PostgreSQL. When multiple requests miss on the same cache key, only one request acquires the lock and proceeds to retrieve the data and repopulate the cache. All other requests wait for the cache to be updated rather than all hitting PostgreSQL at once. This significantly reduces redundant database reads and protects the system from cascading load spikes.

### Scaling read replicas

*Challenge: The primary streams Write Ahead Log (WAL) data to every read replica. As the number of replicas increases, the primary must ship WAL to more instances, increasing pressure on both network bandwidth and CPU. This causes higher and more unstable replica lag, which makes the system harder to scale reliably.*

Solution: We operate nearly 50 read replicas across multiple geographic regions to minimize latency. However, with the current architecture, the primary must stream WAL to every replica. Although it currently scales well with very large instance types and high-network bandwidth, we can’t keep adding replicas indefinitely without eventually overloading the primary. To address this, we’re collaborating with the Azure PostgreSQL team on [cascading replication](https://www.postgresql.org/docs/current/warm-standby.html#CASCADING-REPLICATION), where intermediate replicas relay WAL to downstream replicas. This approach allows us to scale to potentially over a hundred replicas without overwhelming the primary. However, it also introduces additional operational complexity, particularly around failover management. The feature is still in testing; we’ll ensure it’s robust and can fail over safely before rolling it out to production.

### Rate limit

*Challenge: A sudden traffic spike on specific endpoints, a surge of expensive queries, or a retry storm can quickly exhaust critical resources such as CPU, I/O, and connections, which causes widespread service degradation.*

Solution: We implemented rate-limiting across multiple layers—application, connection pooler, proxy, and query—to prevent sudden traffic spikes from overwhelming database instances and triggering cascading failures. It’s also crucial to avoid overly short retry intervals, which can trigger retry storms. We also enhanced the ORM layer to support rate limiting and when necessary, fully block specific query digests. This targeted form of load shedding enables rapid recovery from sudden surges of expensive queries.

### Schema Management

*Challenge: Even a small schema change, such as altering a column type, can trigger*[*a full table rewrite*](https://www.crunchydata.com/blog/when-does-alter-table-require-a-rewrite)*. We therefore apply schema changes cautiously—limiting them to lightweight operations and avoiding any that rewrite entire tables.*

Solution: Only lightweight schema changes are permitted, such as adding or removing certain columns that do not trigger a full table rewrite. We enforce a strict 5-second timeout on schema changes. Creating and dropping indexes concurrently is allowed. Schema changes are restricted to existing tables. If a new feature requires additional tables, they must be in alternative sharded systems such as Azure CosmosDB rather than PostgreSQL. When backfilling a table field, we apply strict rate limits to prevent write spikes. Although this process can sometimes take over a week, it ensures stability and avoids any production impact.

## Results and the road ahead

This effort demonstrates that with the right design and optimizations, Azure PostgreSQL can be scaled to handle the largest production workloads. PostgreSQL handles millions of QPS for read-heavy workloads, powering OpenAI’s most critical products like ChatGPT and the API platform. We added nearly 50 read replicas, while keeping replication lag near zero, maintained low-latency reads across geo-distributed regions, and built sufficient capacity headroom to support future growth.

This scaling works while still minimizing latency and improving reliability. We consistently deliver low double-digit millisecond p99 client-side latency and five-nines availability in production. And over the past 12 months, we’ve had only one SEV-0 PostgreSQL incident (it occurred during the [viral launch](https://newsletter.pragmaticengineer.com/p/chatgpt-images) of ChatGPT ImageGen, when write traffic suddenly surged by more than 10x as over 100 million new users signed up within a week.)

While we’re happy with how far PostgreSQL has taken us, we continue to push its limits to ensure we have sufficient runway for future growth. We’ve already migrated the shardable write-heavy workloads to our sharded systems like CosmosDB. The remaining write-heavy workloads are more challenging to shard—we’re actively migrating those as well to further offload writes from the PostgreSQL primary. We’re also working with Azure to enable cascading replication so we can safely scale to significantly more read replicas.

Looking ahead, we’ll continue to explore additional approaches to further scale, including sharded PostgreSQL or alternative distributed systems, as our infrastructure demands continue to grow.
