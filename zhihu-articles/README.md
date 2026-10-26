# 知乎 AI 专栏文章归档

知乎专栏（zhuanlan.zhihu.com）AI 主题文章归档。**中文原创内容，仅归档不翻译**（同 [苏剑林《科学空间》](../sujianlin-articles/) 先例）。

## 抓取范围与口径

- **主题**：AI 相关专栏文章，按 25 组关键词搜索发现（大模型 / LLM / 深度学习 / AI Agent / 智能体 / 多模态 / RAG / 强化学习 / 生成式AI / AIGC / DeepSeek / GPT / Claude / Gemini / 具身智能等）。
- **仅收专栏文章**（`/p/<id>`），问答体（question/answer）暂不收录。
- 每批下载上限 200–500 篇（防风控）；请求间隔 3.5–6.5 秒随机抖动；连续 5 次失败自动停轮。

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
