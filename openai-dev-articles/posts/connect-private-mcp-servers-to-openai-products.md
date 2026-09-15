---
title: "Making private MCP servers reachable without making them public"
date: 2026-06-26
source: https://developers.openai.com/blog/connect-private-mcp-servers-to-openai-products/
crawled: 2026-09-14
---

We built [Secure MCP Tunnel](https://developers.openai.com/api/docs/guides/secure-mcp-tunnels) because the MCP servers teams care about most are often the ones they least want to expose to the Internet.

We wanted to share how we approached that constraint: keeping private servers private while still giving ChatGPT, Codex, and other OpenAI products a normal MCP request path.

The [Model Context Protocol](https://modelcontextprotocol.io/) has made it easier for AI systems to connect to external tools and data. But many of the most valuable MCP servers run inside enterprise networks, private service meshes, developer laptops, and other environments designed to reject inbound public traffic. Connecting these servers to hosted AI products has often required teams to create public endpoints, deploy additional proxy infrastructure, or introduce new network operators into sensitive paths.

Secure MCP Tunnel provides a simpler approach:
Customers run a small client inside their private environment that establishes an outbound HTTPS connection to OpenAI. The client:

1. Receives MCP requests
2. Forwards them to an approved local server
3. Returns responses and notifications through the same connection.

OpenAI products can use the standard MCP request and response model, while the underlying server remains behind the customer’s existing network controls.

Making that work reliably and securely meant solving several engineering problems at once: preserving the server’s private network boundary, supporting MCP’s streaming and authentication flows, and giving teams a client they can inspect and operate. This post walks through those decisions.

We designed the tunnel around a small set of principles: outbound-only connectivity, explicit destination configuration, compatibility with MCP streaming and notifications, and a customer-run client that teams can inspect and operate themselves.

Together, these make it possible to easily connect private tools and data to OpenAI products without turning private MCP servers into public services.

## The wrong defaults

Today, teams typically make a private service reachable in one of three ways: expose a public endpoint, run a third-party tunnel, or extend the network with a VPN or peering connection.

- A public endpoint makes access easy by weakening the boundary.
- A third-party tunnel provider can make a private server reachable quickly, but it also adds another vendor to review, contract with, operate, and trust in the connectivity path. For enterprise teams, that is not a small detail: the tunnel provider becomes part of the security review, procurement process, operational runbook, and metadata surface for a system whose purpose is to keep private tools private.
- VPNs and network peering solve reachability by creating broad network connectivity, which is often too much machinery for a narrow MCP integration.

Secure MCP Tunnel takes a more focused approach. Instead of asking customers to move the MCP server, expand the network perimeter, or introduce another connectivity vendor, Secure MCP Tunnel puts a small, inspectable open-source client next to the private server and lets that client initiate and control the connection to OpenAI.

Secure MCP Tunnel turns reachability inside out: the private side makes the first move. OpenAI products send MCP requests to an OpenAI-hosted tunnel endpoint. The tunnel service queues work for a specific tunnel, and the customer-run client, already running next to the private MCP server, picks it up over outbound HTTPS. The client forwards the request locally and returns the response through the same path.

This gives OpenAI products a normal MCP request path without requiring the private server to accept inbound public traffic or creating broader network connectivity.

Figure 1. Secure MCP Tunnel request lifecycle.

## Why start with long-poll?

We deliberately started with a transport that is operationally boring. Outbound HTTPS is already familiar to enterprise firewalls, proxy environments, and platform teams. Long-polling lets the tunnel client ask only for the amount of work it can process, which gives the client-side queue a natural backpressure point instead of encouraging unbounded buffering.

That choice also kept the shipped shape easy to reason about:

1. A product sends MCP JSON-RPC to the OpenAI-hosted endpoint.
2. The tunnel service holds or streams that request until the customer-run client returns a final response
3. When asked for streamed results, the tunnel can forward intermediate server-sent events.

The result is a normal MCP request/response path for the product while the MCP server and its address remain private. Requests, responses, and intermediate events are relayed through the OpenAI-hosted tunnel endpoint.

## Keeping the security boundary explicit

The tunnel is not a way to erase the network boundary; it is a way to make that boundary explicit. The customer-run tunnel client authenticates to the tunnel control plane, the product side uses the OpenAI-hosted tunnel endpoint, and the private MCP address is only used from inside the customer environment. Tunnel access is tied to the customer’s existing OpenAI organization and workspace context and configured tunnel identity, instead of becoming a separate network path with its own access model.

The design depends on more than choosing the right network direction. Because the tunnel client runs inside the customer environment, its behavior has to be inspectable and intentionally narrow: customers should be able to understand what code is running, what outbound path it opens, and what private services it is allowed to reach.

Figure 2. The MCP server stays behind the customer boundary.

## Making MCP development feel local

We wanted the tunnel client to feel like a developer tool, not a network project. A developer should be able to run an MCP server on a laptop, start the tunnel client next to it, and connect that server to ChatGPT or Codex without creating a public endpoint or waiting on a VPN, firewall rule, or peering change.

That same flow should carry forward as the server moves from a laptop to Kubernetes, a VM, or another customer-controlled environment. The important part is that the mental model stays the same: run the client near the private MCP server, validate that the client can reach it, and let the client initiate the OpenAI-facing path. Health checks, readiness, logs, and the local admin UI exist to make that loop inspectable when something does not work, not to turn the tunnel into an operations project.

The developer experience also lives in Codex itself. The tunnel client includes a [Codex plugin](https://github.com/openai/tunnel-client/tree/master/plugins/tunnel-mcp) that turns setup into a guided workflow instead of asking developers to learn every tunnel-client flag, profile, and control-plane detail up front. The goal is not to create a one-off local shortcut: the plugin should produce the same configuration shape a team can carry forward when the server moves from a laptop to Kubernetes, a VM, or another production environment.

The same idea shows up in the assistant workflow packaged with tunnel-client: because the assistant can read the local tunnel context exposed by tunnel-client, it can help a developer reason from the actual setup instead of generic instructions – which profile is active, what config was generated, whether the local MCP server is reachable, and where the tunnel client is in its startup path.
That makes troubleshooting part of the developer loop rather than a separate escalation path.

Figure 3. The same tunnel-client loop works from laptop to production.

## Why an open-source tunnel client matters

The tunnel client is open-source, customer-run software that sits inside the customer boundary, next to private MCP servers. That gives customers and security reviewers a way to inspect the code running inside their environment. Customers and security reviewers can inspect what the client does, what outbound connection it opens, how it forwards MCP requests locally, and what configuration controls its reach.

That transparency keeps the trust model aligned with the architecture: OpenAI hosts the tunnel service, but the code running inside the customer environment is small, reviewable, and under the customer’s control.

## Enterprise auth without broad network access

Private MCP servers are rarely just anonymous internal HTTP endpoints. They may depend on OAuth, private certificate authorities, outbound proxies, or client certificates on the MCP hop. Supporting those servers meant treating enterprise network assumptions as part of the tunnel design, not as exceptions customers have to work around.

The key constraint is that the MCP server still stays private. OAuth discovery for the MCP server travels through the tunnel path, so the hosted product can learn how to authenticate without requiring the MCP server to listen on the public internet. On the customer side, the tunnel client can be configured for the local environment: custom CA bundles, proxy settings, and MCP-side mTLS.

We also kept the boundary explicit. The tunnel does not automatically make every related enterprise endpoint reachable from OpenAI. If an authorization server is private, it must still be reachable by the component performing the OAuth flow. That boundary is intentional: Secure MCP Tunnel provides a narrow path to configured private tools, not a general-purpose network bridge.

## Beyond MCP

MCP is the primary shape for model tools, but early alpha testing with customers showed that there was a closely related issue as well: not every customer-private workflow is already packaged as an MCP server. Some important workflows are existing REST APIs behind the same firewall boundary. If Secure MCP Tunnel only solved MCP reachability, teams would still need a separate public endpoint, tunnel provider, VPN path, or peering project for those adjacent private APIs.

Harpoon extends the same narrow-connectivity model to approved REST targets. Instead of exposing arbitrary URLs, the customer registers labeled targets on the tunnel client. OpenAI-side callers invoke those labels through Secure MCP Tunnel, and the actual HTTP request still originates from inside the customer environment, next to the private service.

The important constraint is that labels are not a general-purpose network bridge. Calls stay bounded by customer-owned target registration, allowed methods, response-size limits, timeouts, redirect behavior, and tunnel access controls. That gives approved OpenAI workflows a controlled path to customer-private APIs without asking the customer to open inbound network access or giving OpenAI a VPN-like identity.

## Resources

- [tunnel-client on GitHub](https://github.com/openai/tunnel-client)
- [Secure MCP Tunnel guide](https://developers.openai.com/api/docs/guides/secure-mcp-tunnels)
