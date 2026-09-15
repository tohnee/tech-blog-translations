---
title: "工作负载身份联合（WIF）现已在 Claude Platform 正式发布"
title_en: "Workload Identity Federation (WIF) is now generally available on the Claude Platform."
source: https://claude.com/blog/workload-identity-federation/
crawled: 2026-09-14
translated: 2026-09-14
---

# 工作负载身份联合（WIF）现已在 Claude Platform 正式发布

> 原文：[Workload Identity Federation (WIF) is now generally available on the Claude Platform.](https://claude.com/blog/workload-identity-federation/) · Claude 博客

工作负载身份联合（workload identity federation，WIF）现已在 Claude Platform 正式发布。WIF 兼容任何符合 OIDC 标准的身份提供方，覆盖所有 Claude API 端点，包括通过我们的第一方 SDK 和 Claude Code 访问这些端点的场景。

工作负载用 WIF、交互式会话用 [ant auth login](https://platform.claude.com/docs/en/cli-sdks-libraries/cli/quickstart#authentication)，开发者在使用 Claude Platform 构建时就再也不必接触静态 API 密钥。

## 工作负载身份联合的运作方式

WIF 用在请求时签发的短时效、限定范围的凭证取代了静态 API 密钥。无论你是运行 GitHub Actions 的两人初创团队，还是拥有细致凭证策略的企业，现在都可以用与接入技术栈其他部分相同的方式向 Claude Platform 完成身份验证。

有了 WIF，就不再有需要创建、轮换或可能泄露的静态 Anthropic 凭证。工作负载用它本已拥有的身份完成验证：AWS IAM 角色、GCP 或 Kubernetes 服务账户、Azure 托管标识（managed identity）、GitHub Actions 令牌、Okta，或其他符合 OIDC 标准的提供方。

我们还向 Claude Platform 引入了服务账户（service account），让每个工作负载都可以拥有自己的身份、角色和审计轨迹，而不必共用一个 API 密钥。首先，一条联合规则（federation rule）把外部身份绑定到某个服务账户。随后，当工作负载请求访问时，Claude Platform 会验证该工作负载经过签名的 OIDC 令牌，将其声明（claims）与你的联合规则进行匹配，并签发一个以该服务账户角色为边界的短时效访问令牌。每一次交换和每一个请求，都会记入审计日志中对应的服务账户名下。

## 几分钟配置好你的第一个工作负载

[Claude Console](https://platform.claude.com/) 提供了一条引导式配置流程，用于设置工作负载身份。配置过程会逐步校验每个环节，并以一条测试命令收尾，确认你的工作负载能够完成身份验证。

## 让整个组织摆脱静态密钥运转

WIF 与用于组织管理的 [Admin API](https://platform.claude.com/docs/en/build-with-claude/administration-api) 兼容。联合规则可以通过细粒度作用域（scope）配置为最小权限访问。

对于大规模运营的组织，联合配置也完全支持以编程方式管理。新增的 Admin API 端点让你可以创建和更新签发方（issuer）、服务账户与联合规则。

## 开始使用

API 密钥与 WIF 可以并行使用，因此你可以一次迁移一个工作负载。请阅读针对每种身份提供方的配置[指南](https://platform.claude.com/docs/en/build-with-claude/workload-identity-federation)，或者打开 [Claude Console](https://platform.claude.com/)，接入你的第一个工作负载。

FAQ（常见问题）
