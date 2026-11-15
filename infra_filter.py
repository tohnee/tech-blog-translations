#!/usr/bin/env python3
"""知乎库 LLM infra / AI infra 文章筛选器 v2（精准优先）。

输入：zhihu-articles/posts/*.md（frontmatter + 正文）
输出：
  1) zhihu-articles/INFRA_INDEX.md —— 按 7 个子类分组的全量索引
  2) 命中文章 frontmatter 注入 infra: <子类> 标签（幂等）

判定规则（精准优先）：
  A. 标题含强词（vLLM/SGLang/CUDA/量化部署/推理框架/分布式训练…）→ 收
  B. 标题无强词但含应用/教程类排除词（上下文工程/提示工程/MCP/应用/价格/选型…）→ 不收
  C. 弱词 ≥2 且正文 infra 术语 ≥10 处 → 收
  D. 正文强词命中 ≥3 且 infra 密度 ≥12/千字 → 收
分类：标题强词 > 正文强词 > 弱词，按子类得分取最大。
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
POSTS = ROOT / "zhihu-articles" / "posts"
INDEX = ROOT / "zhihu-articles" / "INFRA_INDEX.md"

CATS = {
    "推理服务与优化": [
        "vllm", "sglang", "tensorrt", "trt-llm", "推理引擎", "推理框架", "推理优化", "推理加速",
        "推理服务", "kv cache", "kvcache", "pagedattention", "投机解码", "speculative",
        "连续批处理", "prefill", "decode 阶段", "吞吐", "ttft", "tpot", "推理成本",
        "llm 服务", "serving", "推理系统", "量化推理",
    ],
    "训练系统与并行": [
        "分布式训练", "deepspeed", "megatron", "fsdp", "张量并行", "流水线并行", "数据并行",
        "专家并行", "并行策略", "训练框架", "混合精度", "梯度累积", "多机多卡",
        "通信优化", "rl 训练", "预训练系统", "训练效率", "训练加速", "checkpoint",
    ],
    "算力与芯片": [
        "gpu", "npu", "tpu", "昇腾", "寒武纪", "ai 芯片", "h100", "h800", "a100", "h200",
        "blackwell", "nvlink", "infiniband", "rdma", "算力集群", "gpu 集群", "超算",
        "国产芯片", "显存", "hbm", "光模块", "液冷", "芯片架构", "互联", "算力",
    ],
    "编译与算子": [
        "cuda", "triton", "编译器", "算子", "flashattention", "tilelang", "cutlass",
        "kernel", "ptx", "算子融合", "图编译", "torch.compile", "mlir", "tvm", "指令集",
    ],
    "部署与运维": [
        "模型部署", "服务化", "kubernetes", "k8s", "mlops", "推理平台", "容器", "镜像",
        "扩缩容", "弹性", "运维", "网关", "负载均衡", "调度系统", "调度",
    ],
    "端侧与边缘": [
        "端侧", "手机端", "边缘推理", "llama.cpp", "gguf", "嵌入式", "树莓派",
        "apple silicon", "本地部署", "端上", "移动端", "npu 推理",
    ],
    "存储与数据": [
        "向量数据库", "向量检索", "分布式存储", "缓存系统", "对象存储", "数据管道",
        "数据加载", "数据集构建", "标注平台", "数据清洗", "存储系统",
    ],
}

STRONG = [
    "vllm", "sglang", "tensorrt", "trt-llm", "llama.cpp", "pagedattention", "flashattention",
    "cuda", "triton", "tilelang", "cutlass", "deepspeed", "megatron", "fsdp",
    "kv cache", "kvcache", "投机解码", "speculative decoding", "推理优化", "推理加速",
    "推理引擎", "推理框架", "推理服务", "推理系统", "分布式训练", "张量并行", "流水线并行",
    "专家并行", "显存优化", "算子融合", "kernel 优化", "gpu 集群", "算力集群",
    "ai 芯片", "芯片架构", "昇腾", "模型部署", "端侧推理", "量化推理", "推理成本",
    "训练加速", "训练效率", "mlops",
]
WEAK = [
    "gpu", "npu", "tpu", "量化", "显存", "算力", "集群", "推理", "部署", "训练",
    "并行", "编译", "算子", "调度", "存储", "芯片", "端侧", "边缘", "吞吐", "延迟",
    "加速", "缓存", "框架", "工程",
]
# 应用/教程/视角类排除（仅在标题无强词时生效）
EXCLUDE_TITLE = re.compile(
    r"(上下文工程|提示工程|提示词|mcp|智能体开发|agent 开发|应用落地|商业化|赚钱|变现|价格战|选型|哪家|推荐|测评|排行榜|榜单|面试|简历|写论文|读书|调研|综述|趋势|前沿|全景|年报|月报|周报|日报)",
    re.I,
)


def read_doc(p: Path):
    text = p.read_text(encoding="utf-8", errors="replace")
    meta = {}
    body = text
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, _, v = line.partition(":")
                meta[k.strip()] = v.strip().strip('"')
        body = text[m.end():]
    return meta.get("title", ""), body, meta


def classify(title: str, body: str):
    t = title.lower()
    b = body[:15000].lower()
    t_strong = [w for w in STRONG if w in t]
    t_weak = [w for w in WEAK if w in t]
    b_strong = [w for w in STRONG if w in b]
    b_hits = {cat: sum(1 for w in words if w in b) for cat, words in CATS.items()}
    t_hits = {cat: sum(1 for w in words if w in t) for cat, words in CATS.items()}
    body_terms = sum(b_hits.values())
    density = body_terms / max(len(b), 1) * 1000

    # 判定（召回优先）
    if t_strong:
        ok = True
    elif EXCLUDE_TITLE.search(title) and len(b_strong) < 3:
        ok = False
    elif len(t_weak) >= 1 and body_terms >= 12:
        ok = True
    elif len(t_weak) >= 2 and body_terms >= 8:
        ok = True
    elif len(b_strong) >= 4:
        ok = True
    elif len(b_strong) >= 2 and density >= 10:
        ok = True
    else:
        ok = False
    if not ok:
        return None

    # 分类：标题强词（权重 5）> 正文强词命中（2）> 弱词（1）
    score = {}
    for cat, words in CATS.items():
        ts = sum(1 for w in words if w in t)
        bs = sum(1 for w in words if w in b)
        score[cat] = t_hits[cat] * 5 + ts * 3 + bs * 2 + b_hits[cat]
    cat = max(score, key=score.get)
    return cat, body_terms


def add_tag(p: Path, cat: str) -> None:
    text = p.read_text(encoding="utf-8", errors="replace")
    if re.search(r"^infra:", text, re.M):
        text2 = re.sub(r"^infra:.*$", f"infra: {cat}", text, count=1, flags=re.M)
    else:
        parts = text.split("---", 2)
        if len(parts) >= 3:
            text2 = parts[0] + "---" + parts[1].rstrip() + f"\ninfra: {cat}\n---" + parts[2]
        else:
            text2 = text
    p.write_text(text2, encoding="utf-8")


def clear_tags() -> None:
    """清除旧的 infra: 标签（支持重复跑的幂等前提）。"""
    for p in POSTS.glob("*.md"):
        text = p.read_text(encoding="utf-8", errors="replace")
        if re.search(r"^infra:", text, re.M):
            p.write_text(re.sub(r"^infra:.*\n?", "", text, count=1, flags=re.M), encoding="utf-8")


def main() -> None:
    clear_tags()
    rows = []
    for p in sorted(POSTS.glob("*.md")):
        title, body, meta = read_doc(p)
        res = classify(title, body)
        if not res:
            continue
        cat, terms = res
        rows.append({
            "file": p.name, "title": title, "cat": cat, "terms": terms,
            "author": meta.get("author", ""), "date": meta.get("created", meta.get("date", "")),
        })
    for r in rows:
        add_tag(POSTS / r["file"], r["cat"])
    groups = {}
    for r in rows:
        groups.setdefault(r["cat"], []).append(r)
    lines = ["# 知乎库 LLM infra / AI infra 文章索引", "",
             f"从知乎全量归档中筛出 **{len(rows)} 篇** infra 相关文章（强词命中 → 排除词过滤 → 弱词+正文密度双阈值，精准优先）。",
             "分类为启发式单标签；frontmatter 已加 `infra:` 字段，可据此二次检索。", ""]
    for cat in CATS:
        items = groups.get(cat, [])
        lines += [f"## {cat}（{len(items)} 篇）", "", "| 标题 | 作者 | 日期 | 文件 |", "|---|---|---|---|"]
        for r in sorted(items, key=lambda x: (x["date"] or "", x["title"]), reverse=True):
            t = r["title"].replace("|", "｜")
            lines.append(f"| [{t}](https://zhuanlan.zhihu.com/p/{r['file'][:-3]}) | {r['author']} | {r['date']} | [{r['file']}](posts/{r['file']}) |")
        lines.append("")
    INDEX.write_text("\n".join(lines), encoding="utf-8")
    print(f"infra articles: {len(rows)} / {len(list(POSTS.glob('*.md')))}")
    for cat in CATS:
        print(f"  {cat}: {len(groups.get(cat, []))}")


if __name__ == "__main__":
    main()
