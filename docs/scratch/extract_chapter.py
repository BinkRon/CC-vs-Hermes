#!/usr/bin/env python3
"""把 findings/*.html 抽成可读 Markdown —— 只保留内容，剥掉设计系统的 <style>/<script>。

用法：
    python3 docs/scratch/extract_chapter.py                     # 抽全部轴二章 + 综合 → 打印
    python3 docs/scratch/extract_chapter.py findings/05-*.html  # 抽指定文件
    python3 docs/scratch/extract_chapter.py --out docs/scratch/extracted/  # 落盘

设计：按语义 class 分派（.thesis/.problem/h2.num/.matrix/.artifact/.verdict/
.compare/.mermaid/.stepper/.open），保留真实制品原文与 mermaid 图规格，
丢掉 .foot 溯源块（file:line 另存）与导航条。
"""
import sys
import re
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Tag

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_FILES = [
    "findings/04-outside-time-trigger.html",
    "findings/05-outside-user.html",
    "findings/06-outside-environment.html",
    "findings/07-outside-multiagent.html",
    "findings/08-outside-self-improvement.html",
    "findings/SYN-outside-story.html",
]


def txt(node) -> str:
    """内联文本：折叠空白，保留字面内容（去掉 span/b/code 等标签只留字）。"""
    s = node.get_text(" ", strip=True) if isinstance(node, Tag) else str(node)
    return re.sub(r"\s+", " ", s).strip()


def has(node, *classes) -> bool:
    cl = node.get("class", []) if isinstance(node, Tag) else []
    return any(c in cl for c in classes)


def render_block(el, out: list):
    """把一个块级元素渲染成 markdown 追加进 out。"""
    if not isinstance(el, Tag):
        return
    name = el.name

    # —— 跳过的东西 ——
    if name in ("style", "script"):
        return
    if name == "nav" or has(el, "foot"):          # 导航条 + 代码溯源脚
        return

    # —— 标题 ——
    if name == "h1":
        out.append(f"\n# {txt(el)}\n")
        return
    if name == "h2":
        num = el.find(class_="num")
        n = txt(num) if num else ""
        # 去掉编号后的正文
        body = txt(el)
        if n and body.startswith(n):
            body = body[len(n):].strip()
        out.append(f"\n## {n + ' · ' if n else ''}{body}\n")
        return
    if name in ("h3", "h4"):
        out.append(f"\n### {txt(el)}\n")
        return

    # —— 顶部 eyebrow / subtitle ——
    if has(el, "eyebrow"):
        out.append(f"`{txt(el)}`")
        return
    if has(el, "subtitle"):
        out.append(f"*{txt(el)}*")
        return

    # —— thesis（TL;DR 核心洞察）——
    if has(el, "thesis"):
        out.append("\n> **【TL;DR / 核心洞察】**")
        tag = el.find(class_="thesis-tag")
        if tag:
            tag.extract()
        ps = el.find_all("p", recursive=False)
        if ps:
            for p in ps:
                out.append(f"> {txt(p)}")
        else:                                # 文本直挂 div、无 <p>：按 <br> 断段
            for seg in re.split(r"\n\s*\n", el.get_text("\n", strip=True)):
                seg = re.sub(r"\s+", " ", seg).strip()
                if seg:
                    out.append(f"> {seg}")
        out.append("")
        return

    # —— problem（00·问题 叙事框）——
    if has(el, "problem"):
        out.append("\n【问题框】")
        for p in el.find_all("p", recursive=False):
            out.append(f"  {txt(p)}")
        out.append("")
        return

    # —— story 叙事块 ——
    if has(el, "story"):
        out.append(f"\n【故事】{txt(el)}\n")
        return

    # —— lead 分节引言 ——
    if has(el, "lead"):
        out.append(f"_{txt(el)}_")
        return

    # —— 真实制品原文 ——
    if has(el, "artifact"):
        lbl = el.find(class_="lbl")
        label = txt(lbl) if lbl else "制品"
        # 取标签之外的正文（保留换行）
        if lbl:
            lbl.extract()
        body = el.get_text("\n", strip=True)
        body = "\n".join(line.rstrip() for line in body.splitlines() if line.strip())
        out.append(f"\n  ┌─ 制品 · {label}")
        for line in body.splitlines():
            out.append(f"  │ {line}")
        out.append("  └─")
        return

    # —— verdict 定论 ——
    if has(el, "verdict"):
        out.append("\n【VERDICT】")
        ps = el.find_all("p", recursive=False)
        if ps:
            for p in ps:
                out.append(f"  {txt(p)}")
        else:                                # 文本直挂 div、无 <p>
            out.append(f"  {txt(el)}")
        out.append("")
        return

    # —— compare 双栏对比 ——
    if has(el, "compare"):
        for side in el.find_all(class_="side", recursive=False):
            who = "Claude Code" if has(side, "cc") else ("Hermes" if has(side, "hm") else "")
            h = side.find(["h3", "h4"])
            head = txt(h) if h else who
            out.append(f"\n[{who}] {head}")
            for child in side.children:
                if not isinstance(child, Tag):
                    continue
                if child is h:
                    continue
                if has(child, "artifact"):
                    render_block(child, out)
                elif child.name == "p":
                    out.append(f"  {txt(child)}")
                elif child.name in ("ul", "ol"):
                    for li in child.find_all("li", recursive=False):
                        out.append(f"  - {txt(li)}")
        out.append("")
        return

    # —— matrix 多维对照矩阵 ——
    if has(el, "matrix"):
        render_matrix(el, out)
        return

    # —— cov 覆盖网（损失类型 × 防线阶段，06 章专用）——
    if has(el, "cov"):
        render_cov(el, out)
        return

    # —— diagram（mermaid 图 + 说明）——
    if has(el, "diagram"):
        for merm in el.find_all(class_="mermaid"):
            code = merm.get_text("\n", strip=True)
            out.append("\n```mermaid")
            out.append(code)
            out.append("```")
        for cap in el.find_all(class_=["cap", "dlead", "decode"]):
            out.append(f"  〔图注〕{txt(cap)}")
        # flow2 里每个 diagram 有 h3 标题
        out.append("")
        return
    if has(el, "flow2"):
        for d in el.find_all(class_="diagram", recursive=False):
            render_block(d, out)
        return

    # —— stepper 分步演示 ——
    if has(el, "stepper"):
        render_stepper(el, out)
        return

    # —— open 悬而未决 ——
    if has(el, "open"):
        out.append("\n【悬而未决 / 防夸大】")
        for li in el.find_all("li"):
            out.append(f"  - {txt(li)}")
        out.append("")
        return

    # —— 普通段落 ——
    if name == "p":
        t = txt(el)
        if t:
            out.append(t)
        return
    if name in ("ul", "ol"):
        for li in el.find_all("li", recursive=False):
            out.append(f"  - {txt(li)}")
        return

    # —— 容器：递归子块 ——
    if name in ("div", "section", "body"):
        for child in el.children:
            render_block(child, out)
        return


def render_matrix(el, out):
    """.matrix 用 grid 三列铺平：一个 .mh 空 + CC + Hermes 表头，随后每行 .dim + 两格。"""
    cells = [c for c in el.children if isinstance(c, Tag)]
    # 表头：前三个（mh 空、mh cc、mh hm）
    headers = []
    i = 0
    while i < len(cells) and has(cells[i], "mh"):
        headers.append(txt(cells[i]))
        i += 1
    # 剩下按 dim + (列数-1) 分组
    ncol = max(len(headers), 3)
    out.append("")
    if headers:
        out.append("  【矩阵】 " + " | ".join(h or "—" for h in headers))
    rest = cells[i:]
    row = []
    for c in rest:
        if has(c, "band"):           # 全宽分组分隔条：单独成行、不进 3 列分组
            if row:                  # 冲掉残行防串位
                out.append("  · " + " | ".join(row))
                row = []
            out.append(f"  —— {txt(c)} ——")
            continue
        row.append(txt(c))
        if len(row) == ncol:
            dim = row[0]
            out.append(f"  · {dim}")
            for h, v in zip(headers[1:] or ["CC", "Hermes"], row[1:]):
                out.append(f"      [{h}] {v}")
            row = []
    if row:  # 收尾残行
        out.append("  · " + " | ".join(row))
    out.append("")


FILL = {"full": "●满", "half": "◐半", "none": "○空"}


def render_cov(el, out):
    """.cov 覆盖网：ch 表头(4) + 每行 rl 行名 + 3 格(cell/na)，每格含 CC/HM 两条 mrow。"""
    cells = [c for c in el.children if isinstance(c, Tag)]
    headers = [txt(c) for c in cells if has(c, "ch")]
    stage_cols = [h for h in headers if h]      # 去掉首个空表头
    out.append("\n  【覆盖网 · 损失类型 × 防线阶段】列： " + " / ".join(stage_cols))

    def mrow_str(cell):
        parts = []
        for mr in cell.find_all(class_="mrow"):
            who = txt(mr.find(class_="who"))
            mk = mr.find(class_="mk")
            level = "?"
            if mk:
                for k in ("full", "half", "none"):
                    if k in mk.get("class", []):
                        level = FILL[k]
            lab = txt(mr.find(class_="lab"))
            parts.append(f"{who}={level} {lab}".strip())
        return " ; ".join(parts)

    # 按 rl 分组：rl 之后的 cell/na 是该行三列
    row_name = None
    col_i = 0
    for c in cells:
        if has(c, "ch"):
            continue
        if has(c, "rl"):
            row_name = txt(c)
            col_i = 0
            out.append(f"  · {row_name}")
            continue
        stage = stage_cols[col_i] if col_i < len(stage_cols) else f"列{col_i+1}"
        col_i += 1
        if has(c, "na"):
            out.append(f"      〔{stage}〕{txt(c)}")
        else:
            out.append(f"      〔{stage}〕{mrow_str(c)}")
    out.append("")


def render_stepper(el, out):
    out.append("\n【分步演示 stepper】")
    frames = el.find_all(class_="frame")
    for idx, fr in enumerate(frames, 1):
        # 帧正文：抽 box 标题/内容，或整体文本
        body = txt(fr)
        out.append(f"  〈帧 {idx}〉{body}" if body else f"  〈帧 {idx}〉")
    for cap in el.find_all(class_="caption"):
        out.append(f"  〔字幕〕{txt(cap)}")
    out.append("")


def extract(path: Path) -> str:
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    title = txt(soup.title) if soup.title else path.name
    wrap = soup.find(class_="wrap") or soup.body
    out = [f"══════════ {path.name} ══════════", f"〈title〉{title}", ""]
    for child in wrap.children:
        render_block(child, out)
    # 折叠多余空行
    text = "\n".join(out)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def main():
    argv = sys.argv[1:]
    outdir = None
    if "--out" in argv:
        oi = argv.index("--out")
        outdir = Path(argv[oi + 1])
        outdir.mkdir(parents=True, exist_ok=True)
        del argv[oi:oi + 2]
    args = [a for a in argv if not a.startswith("--")]
    files = args or DEFAULT_FILES
    for f in files:
        p = (ROOT / f) if not Path(f).is_absolute() else Path(f)
        if not p.exists():
            print(f"!! 不存在: {p}", file=sys.stderr)
            continue
        md = extract(p)
        if outdir:
            dst = outdir / (p.stem + ".md")
            dst.write_text(md, encoding="utf-8")
            print(f"→ {dst}  ({len(md)} 字)")
        else:
            print(md)
            print()


if __name__ == "__main__":
    main()
