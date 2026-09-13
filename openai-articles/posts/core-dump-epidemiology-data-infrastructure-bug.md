---
title: "Epidemiology bug in data infrastructure | OpenAI Core Dump"
date: 2026-07-08
source: https://openai.com/index/core-dump-epidemiology-data-infrastructure-bug/
crawled: 2026-09-13
category: engineering
---

Welcome back to Core Dump, our series sharing interesting bugs from the team at OpenAI. In this edition: an epidemiological bug in data infrastructure.

Sometimes the bugs we find are about code. Sometimes they are about how information spreads. This one was both.

## The symptom

A data engineer noticed that a dashboard in our internal analytics platform was showing incorrect counts for one of our experiments. The numbers were not just slightly off; they were wrong in a patterned way, as if a fraction of events had been duplicated across specific shard boundaries.

The dashboard query ran over a table that aggregated events by experiment variant. Counts for variant A looked correct. Counts for variant B were inflated by roughly 12%, and the excess events were all attached to a handful of ingestion timestamps, spaced almost exactly one hour apart.

## The investigation

The first hypothesis was a retry loop: if a client retries a failed ingestion request without an idempotency key, the server counts the event twice. But the event pipeline required idempotency keys on every write, and deduplication was enforced at the storage layer. Retries, therefore, should have been absorbed.

Digging into the ingestion logs, we found that the duplicated events were not retries. They were _replays_—entire batches re-emitted by a stream processor after a checkpoint restore. Replays are normal and safe in an exactly-once architecture: the downstream deduplication layer should discard any event it has already seen.

The bug was in how deduplication keys were generated. The key was composed of the event ID and a time bucket derived from the ingestion timestamp, truncated to the hour. Normally this is harmless: an event arrives once, its key is stable, and replays produce the same key.

But the ingestion timestamp was assigned by the producer before the event entered the queue. When the producer’s clock drifted and was then corrected by NTP, events queued just before the correction could be assigned timestamps that straddled an hour boundary. On replay, the stream processor regenerated the bucket from the event’s stored timestamp—which was the same—so the key should still have matched.

It did not. The stored timestamp was normalized during the first write: the pipeline truncated the raw timestamp to the hour and stored the truncated value in the event payload, but the deduplication layer compared the stored truncated bucket against a bucket computed from the _untruncated_ payload field it read from the replayed batch. When the two disagreed—exactly for events whose raw timestamp had been within the clock-correction window—the deduplication layer treated a replayed event as new, and the event was counted twice.

## The fix

The fix was small: compute the deduplication key from the same normalized timestamp that was stored, rather than re-deriving it from the raw payload. We also added an invariant check that fails ingestion loudly if a replayed batch produces keys not seen in the original write, and a metric that reports the rate of key mismatches per hour bucket.

The dashboard recovered after a backfill that re-derived the affected buckets. Total duplicate events: about 1.4 million out of 12 billion, or 0.012%—enough to distort an experiment readout, not enough to trigger any of the coarse-grained data-quality alarms we had in place.

## What we learned

- __Normalize once, key from the normalized value.__ Any time a pipeline normalizes a field for storage but derives other artifacts from the raw value, the two representations can silently diverge.
- __Clock corrections are an epidemiological event.__ They propagate through every component that consumes timestamps, and the blast radius is bounded only by the accuracy of the correction and the sensitivity of downstream bucketing.
- __Fine-grained invariants beat coarse-grained alarms.__ Our dashboards watched totals and rates; the bug lived in the join between representations. Asserting representational consistency at write time is cheaper than debugging it from a skewed histogram.

If you enjoy this kind of debugging, we are hiring for the data infrastructure team.