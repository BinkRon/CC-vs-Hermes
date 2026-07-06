#!/usr/bin/env python3
# 装配脚本：把 findings/ 下分章 HTML 合并成一份带左侧栏的 index.html。
# 源仍是分章（契约7：单章可 review/重生成）；成品是 index.html。
# 新增章节只需往 CHAPTERS 里加一行、重跑本脚本。
import re, json, sys, os

ROOT = os.path.dirname(os.path.abspath(__file__))
FIND = os.path.join(ROOT, "findings")

# 章节清单（顺序即阅读顺序；group 用于左栏分组）
CHAPTERS = [
    {"file": "01-inside-control-loop.html", "group": "轴一 · Loop 之内", "label": "01 控制侧",     "id": "ch-01"},
    {"file": "02-inside-input.html",        "group": "轴一 · Loop 之内", "label": "02 输入侧",     "id": "ch-02"},
    {"file": "03-inside-output.html",       "group": "轴一 · Loop 之内", "label": "03 输出行动侧", "id": "ch-03"},
    {"file": "SYN-inside-story.html",        "group": "综合",            "label": "综合① 一个 Loop 怎么设计", "id": "ch-syn1"},
    # 轴二各篇完成后在此追加：
    {"file": "04-outside-time-trigger.html", "group": "轴二 · Loop 之外", "label": "04 Loop 与时间", "id": "ch-04"},
    {"file": "05-outside-programmability.html", "group": "轴二 · Loop 之外", "label": "05 Loop 与用户·上", "id": "ch-05"},
    {"file": "05b-outside-user-adaptation.html", "group": "轴二 · Loop 之外", "label": "05 Loop 与用户·下", "id": "ch-05b"},
    {"file": "06-outside-environment.html", "group": "轴二 · Loop 之外", "label": "06 Loop 与环境", "id": "ch-06"},
    {"file": "07-outside-multiagent.html", "group": "轴二 · Loop 之外", "label": "07 Loop 与其他 Agent", "id": "ch-07"},
    {"file": "08-outside-self-improvement.html", "group": "轴二 · Loop 之外", "label": "08 Loop 与自己", "id": "ch-08"},
    {"file": "SYN-outside-story.html", "group": "综合", "label": "综合② Loop 之外怎么设计", "id": "ch-syn2"},
]

# ---------- 样式：组件 CSS 从 _design-system.html 读取（单一真相，契约2）；此处仅放合订本专属的壳/布局 ----------
# 契约2：设计系统只认一处 = findings/_design-system.html 的 <style>。build.py 构建时抽取它，
# 再叠加下面这段"合订本才需要"的侧栏/多章框架 CSS（单章不需要，故不进设计系统）。
SHELL_CSS = r"""
/* —— 合订本专属：左侧栏 + 多章框架 —— */
body{display:flex}
.sidebar{width:252px;flex:0 0 252px;position:sticky;top:0;align-self:flex-start;height:100vh;overflow-y:auto;
  border-right:1px solid var(--border);padding:22px 0;background:#0b0e14}
.sidebar .brand{font-weight:700;font-size:14px;padding:0 20px 14px;color:var(--text);border-bottom:1px solid var(--border);margin-bottom:6px}
.sidebar .brand small{display:block;color:var(--faint);font-weight:400;font-size:12px;margin-top:4px}
.sidebar .grp{color:var(--faint);font-size:12px;letter-spacing:.5px;padding:15px 20px 6px}
.navitem{display:block;padding:7px 20px;font-size:14px;color:var(--muted);cursor:pointer;border-left:2px solid transparent}
.navitem:hover{color:var(--text);background:var(--surface)}
.navitem.on{color:var(--blue);border-left-color:var(--blue);background:color-mix(in srgb,var(--blue) 10%,transparent)}
.content{flex:1;min-width:0}
.chwrap{max-width:var(--maxw);margin:0 auto;padding:44px 40px 120px}
.chapter{display:none}
.chapter.active{display:block;animation:fade .25s ease}
@media(max-width:800px){body{flex-direction:column}.sidebar{width:100%;height:auto;position:static;flex:none}}
"""

def extract_design_css():
    """从 _design-system.html 抽取 <style> 内容作为组件 CSS（单一真相）。"""
    p = os.path.join(FIND, "_design-system.html")
    html = open(p, encoding="utf-8").read()
    m = re.search(r'<style>(.*?)</style>', html, re.S)
    if not m:
        raise SystemExit("无法从 _design-system.html 提取 <style>")
    return m.group(1)

def extract_bespoke_css(html):
    """收集某章自带的 <style class="bespoke"> —— 定制章专属样式（须 scoped 在本章根 class 下，
    如 .syn2，防泄漏别章）。共享设计系统仍单一真相，这里只搬各章显式声明的定制块进合订本 head。"""
    return "\n".join(re.findall(r'<style class="bespoke">(.*?)</style>', html, re.S))

# ---------- 共享脚本（组件化 stepper + 侧栏导航 + mermaid 按需渲染） ----------
SHARED_JS = r"""
/* 离线守卫：CDN 掉线时 mermaid 未定义。不加守卫会抛 ReferenceError 掐死整段脚本，
   导致 show() 不执行、所有章节停在 display:none → 侧栏在、正文全空白。加守卫后：图退化为原始文字，正文照常可读。 */
var MERMAID_OK = (typeof mermaid !== 'undefined');
if(MERMAID_OK){
  mermaid.initialize({startOnLoad:false,theme:"dark",
    flowchart:{nodeSpacing:30,rankSpacing:38,padding:10,useMaxWidth:true},
    themeVariables:{background:"#1e2531",primaryColor:"#161b26",primaryBorderColor:"#2a3342",
      primaryTextColor:"#e6edf3",lineColor:"#8b98a9",fontSize:"13.5px"}});
}

/* 每个 .stepper 自带状态，互不干扰 */
document.querySelectorAll('.stepper').forEach(function(st){
  var frames=[].slice.call(st.querySelectorAll('.frame'));
  var caps=[]; var cj=st.querySelector('.captions'); if(cj){try{caps=JSON.parse(cj.textContent);}catch(e){}}
  var cap=st.querySelector('.caption'), cnt=st.querySelector('.count'), dots=st.querySelector('.dots');
  var cur=0;
  if(dots){frames.forEach(function(_,i){var d=document.createElement('span');d.className='dot'+(i?'':' on');dots.appendChild(d);});}
  function render(){
    frames.forEach(function(f,i){f.classList.toggle('on',i===cur);});
    if(cap&&caps[cur]!=null)cap.innerHTML=caps[cur];
    if(cnt)cnt.textContent=(cur+1)+' / '+frames.length;
    if(dots)[].slice.call(dots.querySelectorAll('.dot')).forEach(function(d,i){d.classList.toggle('on',i===cur);});
  }
  var p=st.querySelector('.prev'), n=st.querySelector('.next');
  if(p)p.onclick=function(){cur=Math.max(0,cur-1);render();};
  if(n)n.onclick=function(){cur=Math.min(frames.length-1,cur+1);render();};
  render();
});

/* 侧栏导航 + mermaid 按需渲染（隐藏 tab 里画会算错尺寸，故切到才画） */
var chapters=[].slice.call(document.querySelectorAll('.chapter'));
function show(id){
  chapters.forEach(function(c){c.classList.toggle('active',c.id===id);});
  [].slice.call(document.querySelectorAll('.navitem')).forEach(function(n){n.classList.toggle('on',n.dataset.t===id);});
  var sec=document.getElementById(id);
  if(sec&&MERMAID_OK){
    var nodes=[].slice.call(sec.querySelectorAll('.mermaid:not([data-processed])'));
    if(nodes.length){try{mermaid.run({nodes:nodes});}catch(e){}}
  }
  if(location.hash!=='#'+id){history.replaceState(null,'','#'+id);}
  window.scrollTo(0,0);
}
[].slice.call(document.querySelectorAll('.navitem')).forEach(function(n){n.onclick=function(){show(n.dataset.t);};});
var start=(location.hash||'').replace('#','');
show(chapters.some(function(c){return c.id===start;})?start:chapters[0].id);
"""

def extract_body(html):
    m = re.search(r'<body>\s*<div class="wrap">(.*)</div>\s*<script>', html, re.S)
    if not m:
        raise SystemExit("无法提取 body: 结构不符")
    body = m.group(1)
    body = re.sub(r'\s*<nav\b[^>]*>.*?</nav>', '', body, flags=re.S)  # 去掉旧的页脚导航
    return body

def extract_captions(html):
    m = re.search(r'const CAPTIONS\s*=\s*(\[.*?\]);', html, re.S)
    if not m:
        return None
    raw = m.group(1)
    json.loads(raw)  # 校验是有效 JSON，否则报错（防未转义引号）
    return raw

def transform_stepper(body, caps_raw, fname):
    """两种 stepper 约定（契约 2）：
    - 旧约定（01~07 存量章，不回改）：唯一 id="stepper" + 全局 CAPTIONS + onclick="step(±1)" → 此处自动转成组件化；
    - 组件化约定（2026-07-02 起的新章）：.stepper 内嵌 captions JSON + .prev/.next 按钮 → 原样直通。
    一章只能用一种约定；混用直接报错（防第二个 stepper 在合订本里静默变死按钮）。"""
    if 'class="stepper"' not in body:
        return body
    old = 'id="stepper"' in body
    new = '<script type="application/json" class="captions">' in body
    if old and new:
        raise SystemExit('%s: 混用两种 stepper 约定（id="stepper" 与内嵌 captions 并存）。'
                         '契约 2：出现第二个 stepper 时该章须整体改用组件化约定。' % fname)
    if not old:
        return body  # 组件化章节直通，交给 validate_steppers 把关
    # 旧约定 → 组件化：注入 captions JSON，改 id 为 class，改按钮
    if caps_raw:
        body = body.replace('<div class="stepper" id="stepper">',
                            '<div class="stepper"><script type="application/json" class="captions">' + caps_raw + '</script>', 1)
    else:
        body = body.replace('<div class="stepper" id="stepper">', '<div class="stepper">', 1)
    body = re.sub(r'<div class="caption" id="cap">.*?</div>', '<div class="caption"></div>', body, flags=re.S)
    body = re.sub(r'<div class="dots" id="dots">\s*</div>', '<div class="dots"></div>', body)
    body = re.sub(r'<span class="count" id="count">.*?</span>', '<span class="count"></span>', body, flags=re.S)
    body = body.replace('onclick="step(-1)"', 'class="prev"').replace('onclick="step(1)"', 'class="next"')
    return body

def validate_steppers(body, fname):
    """构建期守卫：转换后每个 .stepper 必须是组件化形态，否则在合订本里是死按钮——宁可构建失败也不静默出货。"""
    leftover = [m for m in ('id="stepper"', 'onclick="step(', 'id="cap"', 'id="dots"', 'id="count"') if m in body]
    if leftover:
        raise SystemExit('%s: 转换后仍残留旧约定 stepper 标记 %s（多半是一章塞了不止一个旧式 stepper）。'
                         '契约 2：多 stepper 章节须整体改用组件化约定。' % (fname, leftover))
    segs = body.split('<div class="stepper"')[1:]  # 每段 = 一个 stepper 到下一个 stepper 之间
    for i, seg in enumerate(segs, 1):
        if 'class="prev"' not in seg or 'class="next"' not in seg:
            raise SystemExit('%s: 第 %d 个 stepper 缺 class="prev"/"next" 按钮，合订本里会是死按钮。' % (fname, i))
        m = re.search(r'<script type="application/json" class="captions">(.*?)</script>', seg, re.S)
        if m:
            try:
                caps = json.loads(m.group(1))
            except ValueError as e:
                raise SystemExit('%s: 第 %d 个 stepper 的 captions JSON 无效（%s）——检查文案里是否混入未转义的英文双引号。' % (fname, i, e))
            n_frames = seg.count('class="frame')
            if isinstance(caps, list) and caps and n_frames and len(caps) != n_frames:
                print('  警告: %s 第 %d 个 stepper captions 条数(%d) != 帧数(%d)' % (fname, i, len(caps), n_frames))
        else:
            raise SystemExit('%s: 第 %d 个 stepper 未内嵌 captions JSON（组件化约定必备；确需无字幕请显式写 []）。' % (fname, i))

def build_sidebar():
    out = ['<aside class="sidebar">',
           '<div class="brand">Claude Code vs Hermes<small>Harness 设计对比</small></div>']
    last = None
    for c in CHAPTERS:
        if c["group"] != last:
            out.append('<div class="grp">%s</div>' % c["group"])
            last = c["group"]
        out.append('<div class="navitem" data-t="%s">%s</div>' % (c["id"], c["label"]))
    out.append('</aside>')
    return "\n".join(out)

def main():
    sections = []
    bespoke = []
    for c in CHAPTERS:
        path = os.path.join(FIND, c["file"])
        html = open(path, encoding="utf-8").read()
        caps = extract_captions(html)
        body = extract_body(html)
        body = transform_stepper(body, caps, c["file"])
        validate_steppers(body, c["file"])
        bespoke.append(extract_bespoke_css(html))
        sections.append('<section class="chapter" id="%s"><div class="chwrap">%s</div></section>' % (c["id"], body))
    bespoke_css = "\n".join(b for b in bespoke if b)
    doc = (
        '<!DOCTYPE html>\n<html lang="zh">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<link rel="icon" href="data:,">\n'
        '<title>Claude Code vs Hermes · Harness 设计对比</title>\n'
        '<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>\n'
        '<style>' + extract_design_css() + SHELL_CSS + bespoke_css + '</style>\n</head>\n<body>\n'
        + build_sidebar() + '\n<main class="content">\n'
        + "\n".join(sections)
        + '\n</main>\n<script>' + SHARED_JS + '</script>\n</body>\n</html>\n'
    )
    out = os.path.join(ROOT, "index.html")
    open(out, "w", encoding="utf-8").write(doc)
    print("wrote", out, "(%d chapters, %d bytes)" % (len(CHAPTERS), len(doc)))

if __name__ == "__main__":
    main()
