# vLLM Blog English Archive

Complete English archive of the official vLLM blog ([vllm.ai/blog](https://vllm.ai/blog)), crawled 2026-09-12/13 from the sitemap: **134 posts**, 2023-06-20 (founding PagedAttention post) through 2026-09-10.

- `posts/<slug>.md` — one file per post, frontmatter with title/date/source/crawled
- `meta.json` — machine-readable index (slug, title, date, url, description)
- `html/` — raw HTML cache of every post page
- `mathjax_report.json` — posts containing MathJax formulas (math restored into the markdown as `$...$`)

Chinese translations: [`vllm-articles-zh/`](../vllm-articles-zh/) · Translation guide & glossary: [`TRANSLATION_GUIDE_VLLM.md`](../TRANSLATION_GUIDE_VLLM.md)

Archive tooling (this repo): `crawl_vllm.py` (fetch + HTML→Markdown, with MathJax-SVG→LaTeX reconstruction and iframe/video placeholders), `scan_vllm_math.py` (HTML cache + formula census), `regen_vllm_math.py` (regenerate formula-bearing posts), `verify_vllm_zh.py` (zh completeness checks + zh README builder).

Note: images are referenced by absolute URL (`https://vllm.ai/blog-assets/...`), not downloaded. A few interactive figures / demo videos that ship as `<iframe>`/`<video>` on the site are kept as `[Interactive figure](url)` / `[Video](url)` placeholder links pointing at the original assets.
