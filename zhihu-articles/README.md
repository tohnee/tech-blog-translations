# 知乎 AI 专栏文章归档

知乎专栏（zhuanlan.zhihu.com）AI 主题文章归档。**中文原创内容，仅归档不翻译**（同 [苏剑林《科学空间》](../sujianlin-articles/) 先例）。

> **LLM infra / AI infra 专题**：从全量库中筛出的 1628 篇基础设施文章，见 **[INFRA_INDEX.md](INFRA_INDEX.md)**（按推理服务与优化 / 训练系统与并行 / 算力与芯片 / 编译与算子 / 部署与运维 / 端侧与边缘 / 存储与数据 七类分组；命中文章 frontmatter 带 `infra:` 标签）。

## 抓取范围与口径

- **主题**：AI 相关专栏文章，按 65 组关键词搜索发现：25 组通用 AI 词（大模型 / LLM / Agent / RAG / DeepSeek / GPT / Claude 等）+ 40 组 LLM/AI infra 专项词（vLLM / SGLang / 推理优化 / KV Cache / 投机解码 / 分布式训练 / DeepSpeed / Megatron / CUDA / Triton / 算子 / FlashAttention / GPU 集群 / 昇腾 / 端侧推理 / llama.cpp 等）。
- **仅收专栏文章**（`/p/<id>`），问答体（question/answer）暂不收录。
- 每批下载上限 200–500 篇（防风控）；请求间隔 3.5–6.5 秒随机抖动；连续 5 次失败自动停轮。
- **infra 筛选**：`infra_filter.py`——强词命中 → 排除词过滤 → 弱词+正文密度双阈值 → 发现关键词信号（四重判定，召回优先）；结果写 `INFRA_INDEX.md` 并给命中文件打 `infra: <子类>` 标签（幂等，可重跑）。

## 工具链

- CLI：[zhihu-toolkit](https://github.com/KrisTHL181/zhihu-cli)（装于 `/tmp/zhihu-venv`，Python 3.12+；`/tmp` 重启即清，重建见 `../DAILY_SYNC_SOP.md` 第 12 节）。
- 管线：仓库根 [`crawl_zhihu.py`](../crawl_zhihu.py)——库直调（`search_articles` + `ContentDownloader.fetch_article`），零子进程；断点续传状态在 [`_state.json`](_state.json)。
- **登录必需**：`zhihu auth import`（本地 Chrome 导入，需钥匙串授权）/ `zhihu auth paste`（cURL 粘贴）/ `zhihu auth login`（扫码）。

## 运行

```bash
/tmp/zhihu-venv/bin/python3 crawl_zhihu.py                 # 发现 + 下载（默认上限 200）
/tmp/zhihu-venv/bin/python3 crawl_zhihu.py --download-only --limit 300   # 只清剩余清单
```

## 文件规范

`posts/<文章id>.md`，frontmatter：`title / source / crawled / author / created`，正文为知乎编辑器 HTML 转换的 Markdown（图片外链保留 zhimg.com 原图）。
