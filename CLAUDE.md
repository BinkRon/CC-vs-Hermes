# Claude Code vs Hermes Agent —— Harness 设计对比研究

> **语言铁律**：与用户对话一律用中文。

研究两个主流 agent 在 **harness**（包在模型外的控制脚手架）设计上的差异，产出一份**给产品经理看的、可视化的产品逻辑**对比文档。交付物是合订本 `index.html`（由 `build.py` 从 `findings/` 各章装配而成）。

---

## 🚀 新 session 上手顺序（务必按序）

1. **读本文件**（CLAUDE.md）——理解项目是什么、怎么干、有哪些铁律。
2. **读 `docs/progress.md`**——运行态仪表盘：做到哪、下一步、活跃待办。**这是"现在该干什么"的唯一真相。**
3. **读 `docs/contract.md`**——强制规则（"怎么干"的宪法）。每次调研+渲染前必读。**渲染/排版另须读 `docs/design-principles.md`（设计宪法：三档重量+视觉脚本+设计门）。**
4. **领活先绑需求 ID（契约 8）**：推进交付物的 session，在 `docs/backlog.csv` 选一个 `依赖` 全 `done` **且 `状态=draft`（无人认领）**的需求，**领取即把 `状态` 切出 draft 占位**、在 `progress.md`「🔴 在做」区建任务块起一棒，本 session 只推进这一个；接**在制品**则读该 ID 在 progress 任务块的最新一棒续做。纯讨论/流程 session 不绑。**独立需求可由不同 session 并行**（有依赖的按序；共享工作树时并合订本那步串行，契约 8.6）。
5. 按需：框架/为什么 → `docs/framework-and-plan.md`；已完成的详细结论与整改史 → `docs/archive.md`；某章原文 → `findings/`。

被对比的代码（只读）：
- Claude Code：`/Users/luohuibin/cursor_project/claude-code-main`
- Hermes Agent：`/Users/luohuibin/cursor_project/hermes-agent`（@ `daf4f1a7a`）

---

## 🗺️ 项目地图

| 路径 | 性质 | 何时用 |
|---|---|---|
| **`CLAUDE.md`** | **入口（本文件）** | 每个 session 第一个读 |
| **`index.html`** | **成品合订本** | 最终交付物：左侧栏切章。由 `build.py` 从 `findings/` 装配，**勿手改** |
| `build.py` | 装配脚本 | 某章过门后跑 `python3 build.py` 重生成 `index.html`；加新章改脚本顶部 `CHAPTERS` 清单 |
| `findings/` | 章节源 | 每章一个自包含 HTML（可单独 review）+ `_design-system.html`（设计系统单一真相）|
| **`docs/backlog.csv`** | **需求清单** | 该做什么、能不能领（`依赖`全 done 才可领）；**开工先绑一个 ID**（契约 8）|
| `docs/progress.md` | **运行态 + 接棒** | 每次干活**前看 / 后更新**（契约 4：在做/等谁/接下来，接棒住任务块；与 backlog 状态同步）|
| `docs/contract.md` | **契约（规则）** | 调研+渲染前必读 |
| `docs/framework-and-plan.md` | 稳定参考 | 共识框架 + 调研计划（两轴顺序）|
| `docs/archive.md` | 归档（已完成）| 各章结论（回审后准确版）+ 整改/审计史；**与旧记忆冲突以它为准** |
| `assets/` | 杂物 | 历史截图等 |

---

## 🔬 怎么产出一篇（单篇流水线）

**框架**：两条正交轴 —— 轴一「Loop 之内」（输入/计算/输出/控制四侧）、轴二「Loop 之外」（时间触发/可编程性/环境/多智能体）。大顺序：整条轴一→综合①→整条轴二→综合②，不跳轴不并轴。

**分析仪器**：轴一每篇问「**改模型 vs 改壳**」；轴二每篇问「**什么世界/人/部署现实逼出了它**」。

**流水线**（契约 7，串行单篇、≤3 agent）：
1. **研究**：每个代码库 1 个研究员（Opus max effort）各啃一库 → 结构化 JSON（产品逻辑 + 图规格 + `file:line`）。
2. **综合**：**我**把 JSON 收敛成产品论点（这是核心，也是最易出错处，见下）。
3. **渲染**：1 个渲染员套 `_design-system.html` 出单章 HTML。
4. **过四道门**（见下）→ 修正 → 同步 `backlog.csv` 状态 + `progress.md` 任务块（契约 4；done 则删块并把结论沉 `archive.md`）→ `python3 build.py` 并入合订本。

---

## 🚦 四道质量门（不可跳）

1. **自审**：产品逻辑清楚？设计系统合规？结论有 `file:line`？
2. **Codex soundness 门**：把事实性论断交 Codex 对着真实代码核验"claim 是否属实"，**并额外问一句 completeness**（有没有漏/低估重要机制）。对 Codex 反馈**先形成自己判断再采纳**，误报驳回并记录。
3. **完整性/忠实度门**：独立 agent 读"该维度真实代码 + 成稿"，逐条标记每个机制「如实/忠实合并/静默丢弃/**以偏概全**」，凡"会改变读者结论"的必修。
4. **设计门（2026-07-04 起，DSN-01）**：按 `docs/design-principles.md` Part 2.2 过（门 = 过 Part 1 规则全表 + 10 秒重点测试 / 梯度自查（全序排名+安静基线）/ 对照全序重量分配表防机制静默丢失）。前三道保真实，这道保表达。

> **⚠️ 血泪根因**：我有一个**系统性偏差**——为追求"一个干净故事"，会把"默认行为"写成"绝对/全局特征"，把不合主线的机制压掉（subagent 事故、5 篇的"默认→绝对"夸大都源于此）。Codex 只查 soundness、查不出遗漏。**所以靠独立的完整性门兜，不靠"我下次更仔细"。** 收敛论点前，先把研究列出的机制逐条过一遍"有没有被主线吞掉/以偏概全"。

---

## ⛔ 铁律（最高频踩坑，全量见 contract.md）

- **产品逻辑，不是技术细节**：受众是不懂代码的 PM。正文一律不出现函数名/类名/数据结构；代码只在页脚 `file:line` 溯源。（但真实文案原文/错误消息/阈值数字是**证据**，该展示——见契约 1 附注 + 契约 3 深潜"必须含真实制品"。）
- **出稿机械检查**：HTML 写出必两关——① 抽内联脚本 `node --check`；② 浏览器 smoke（0 error + **真的点一次 stepper** + 图为深色）。只截静态首帧不算验收。
- **绝不在 JS 字符串里用英文双引号 `"`**：会掐断整个 `<script>`。强调用中文「」或全角。
- **设计系统两层制**：复用样式只写进 `_design-system.html`（单一真相，别往 build.py 拷第二份）；每章重档可视化允许 ≤1 处 `<style class="bespoke">`（scoped 本章根 class、只引用 tokens）。**排版/可视化按 `docs/design-principles.md` 执行（渲染前必读）：三档视觉重量、统一 1080 版心（一章内所有块同边缘、禁窄列）、正文裸文、粗体每段 ≤2、标题必须是论断。**
- **合订本离线守卫**：`SHARED_JS` 所有 mermaid 调用裹 `MERMAID_OK`，否则 CDN 掉线整页白屏。
- **流程图** `flowchart TD`（纵向），两图对比用 `.flow2` **且必须高亮差异节点**（语义配色：判断=amber、终点=green）；多维对照用 `.matrix`。

---

## 📁 文档维护机制（每个 session 都要遵守）

**职责分离——"什么变了，就更新对应的那一份"：**

| 变化 | 更新哪个 |
|---|---|
| 领活开工 | 先绑 `backlog.csv` 一个需求 ID，`progress.md`「在做」区建任务块起一棒（契约 8）|
| 完成一篇 / 进度推进 / 交棒 | `backlog.csv`（状态）+ `progress.md`（任务块/接棒）**两处**同步（契约 4/8：不同步不算完成）|
| 一篇彻底完成、结论定稿 | 一句话结论写进 `archive.md`；**删** `progress.md` 该任务块；`backlog.csv` 状态置 `done`——**仅当无任何活跃需求的 `依赖` 列还引用它**才移走该行，否则留 `done` 行（契约 8.2）|
| 规则/流程改变 | `contract.md` |
| 框架/共识/计划改变 | `framework-and-plan.md` |
| 产出章节内容 | `findings/`（源）→ `build.py` → `index.html`（成品，勿手改）|

**两条机制原则：**
1. **progress 只装"运行态"，膨胀就归档**：`progress.md` 是仪表盘，只留"现在该干什么、还欠什么"。已完成的详细结论、历次整改/审计记录一律沉到 `archive.md`，保持 progress 一屏可读。
2. **归档是"回审后的准确版"**：往 `archive.md` 沉淀时，用最新校正过的措辞，不要把过时/被证伪的旧口径也归档进去。archive 与任何旧记忆冲突时，以 archive 为准。

**常用命令：**
- Codex 核实：`codex exec -C /Users/luohuibin/cursor_project --sandbox read-only --skip-git-repo-check -o <out> "<prompt>" </dev/null`
- 重建合订本：`python3 build.py`
