#!/usr/bin/env python3
"""为 10 个厂商源生成 README 索引并校验中英文件一一对应（含 papers/ 子目录）。"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

VENDORS = {
    'qwen': ('Qwen 通义千问', '阿里通义千问（GitHub Pages 博客 + arXiv 报告）；官方双语，中文侧为官方译本（zh_source: official）'),
    'deepseek': ('DeepSeek 深度求索', 'api-docs.deepseek.com/news + arXiv 报告；官方双语'),
    'thinkingmachines': ('Thinking Machines Lab', 'Mira Murati 创办实验室官方博客'),
    'minimax': ('MiniMax 稀宇科技', 'minimax.io 官方技术博客 + arXiv 报告'),
    'zhipu': ('智谱 Z.ai / THUDM', 'HF zai-org 模型卡 + THUDM GitHub 仓库 + arXiv 报告；ChatGLM 早期仓库为中文原文'),
    'xiaomi': ('小米 MiMo', 'GitHub XiaomiMiMo 模型卡/发布日志 + arXiv 报告'),
    'stepfun': ('阶跃星辰 StepFun', 'GitHub stepfun-ai 模型卡 + arXiv 报告'),
    'ling': ('蚂蚁集团 InclusionAI（Ling 系列）', 'GitHub inclusionAI 仓库 + arXiv 报告'),
    'xai': ('xAI', 'x.ai/news（经 Wayback Machine 存档；直连受 Cloudflare 拦截）'),
    'meta-ai': ('Meta AI（FAIR）', 'ai.meta.com/blog（经 Wayback Machine 存档）+ arXiv 旗舰论文'),
}

def cjk_count(p):
    return len(re.findall(r'[\u4e00-\u9fff]', p.read_text(errors='replace')))

def main():
    rc = 0
    for src, (label, desc) in VENDORS.items():
        en_dir = ROOT / f'{src}-articles'
        zh_dir = ROOT / f'{src}-articles-zh'
        if not en_dir.exists():
            print(f'!! {src}: no archive dir'); continue
        en_files = sorted([p for p in en_dir.rglob('*.md') if p.name != 'README.md'])
        zh_files = sorted([p for p in zh_dir.rglob('*.md') if p.name != 'README.md']) if zh_dir.exists() else []
        en_rel = {str(p.relative_to(en_dir)) for p in en_files}
        zh_rel = {str(p.relative_to(zh_dir)) for p in zh_files}
        missing = en_rel - zh_rel
        orphan = zh_rel - en_rel
        lines = [
            f'# {label} 文章中文索引',
            '',
            f'> {desc}',
            f'> 英文归档 `{src}-articles/`（{len(en_files)} 篇），中文 `{src}-articles-zh/`（{len(zh_files)} 篇）。',
            f'> 翻译规范：`TRANSLATION_GUIDE_AI_VENDORS.md`；arXiv 论文在 `papers/` 子目录（译文同样在 `*-zh/papers/`）。',
            '',
        ]
        if missing:
            lines.append(f'> ⚠️ 未翻译：{len(missing)} 篇')
            rc = 1
        if orphan:
            lines.append(f'> ⚠️ 多余译文：{len(orphan)} 篇')
            rc = 1
        lines.append(f'| 篇数 | {len(en_files)} EN → {len(zh_files)} ZH |')
        lines.append('|---|---|')
        for p in en_files:
            rel = str(p.relative_to(en_dir))
            zh_p = zh_dir / rel
            if zh_p.exists():
                link = f'[译文]({str(zh_p.relative_to(ROOT / (src + "-articles-zh")))})' if False else f'[译文]({rel})'
            text = p.read_text(errors='replace')
            t = re.search(r'^title: "?([^"\n]+)"?', text, re.M)
            date = re.search(r'^date: (\S+)', text, re.M)
            arx = re.search(r'^arxiv: (\S+)', text, re.M)
            title = t.group(1) if t else rel
            meta = date.group(1) if date else (arx.group(1) if arx else '')
            status = '✅' if zh_p.exists() else '❌'
            kind = '📄' if 'papers/' in rel else '📝'
            lines.append(f'| {status} {kind} | {meta} | {title} | `{rel}` |')
        (zh_dir if zh_dir.exists() else en_dir).mkdir(parents=True, exist_ok=True)
        out_dir = zh_dir if zh_dir.exists() else en_dir
        (out_dir / 'README.md').write_text('\n'.join(lines) + '\n')
        print(f'{src}: EN {len(en_files)} / ZH {len(zh_files)} | missing {len(missing)} | README -> {out_dir.name}/README.md')
    sys.exit(rc)

if __name__ == '__main__':
    main()
