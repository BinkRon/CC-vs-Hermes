# CH-A2R-03 视觉脚本（渲染依据 · 五问 + 全序重量表）

> 定性：产品**手段章**，全五章最弱产品观信号。收尾**不拔统一轴**，三处分岔并列，**不碰「在场」**（留综合②）。
> 依据 `fact-map.md`。切片 CC 真源码 / Hermes @8e734810d。

---

## 问 1 · 一句话论点
多 agent 是 single-agent 上下文极限逼出的手段；两家为**几乎相同的理由**拆开，真差异在拆开之后的三处——**谁决定怎么委派**（模型判断 vs 壳的默认）、**信不信分身的自报**（默认信任 vs 默认复核）、**分身之间靠什么协调**（互发消息的同事网 vs 只读写共享状态板）。

## 问 2 · 最大卡壳点（→ 决定唯一重档）
**「分身之间靠什么联系」的拓扑差异。** PM 若不画，会把两家的团队/看板笼统当成「都是多 agent 协作」，看不出根本形状差异：CC 的分身**互相发消息**（有 agent↔agent 的连线），Hermes 的分身**彼此不说话、只各自读写一块共享状态板**（没有 agent 间连线，全连到中央 DB）。这处具体、有原文、且不碰「在场」——旧稿本来就抓对了，是本章唯一重档。

## 问 3 · 叙事顺序（问题→机制→三分岔→收尾，差异段把最戏剧的拓扑压在末尾当 Hero）
- **开篇**：thesis 框（绿左规·≤2 段）+ story 框（single-agent 撞墙的具体故事：一个大重构/大调研，一个 agent 的上下文和时间扛不下）。
- **§01【趋同·基石】** 为什么非拆不可：两家拆开 agent 的理由几乎相同——防中间原始输出淹没父上下文。
- **§02【趋同骨架 + 两处非对称】** 拆出来的分身有哪些种类：委派层趋同，例外是 CC 独有 fork、Hermes 独有 profiles-as-roster。
- **§03【分岔一】** 谁决定怎么委派：CC 交给模型运行时判断，Hermes 写进壳的默认（委派即后台、模型不能选）。
- **§04【分岔二·接轴一】** 信不信分身说的「我做完了」：CC 默认信任，Hermes 默认复核。
- **§05【分岔三·重档 Hero】** 分身之间靠什么联系：互发消息的同事网 vs 只读写共享状态板。
- **§06【收尾】** 三处分野各自的取舍（并列，不拔统一轴，不碰在场；统一变量明说留综合②）。
- **§07** 悬而未决与边界。

## 问 4 · 全序重量分配表（覆盖研究 JSON 全部机制，无一静默消失）

| 排名 | 块 | 档 | 承载/归入的机制（CC ｜ Hermes） | 形式 |
|---|---|---|---|---|
| 1（第一名） | §05 协调拓扑：消息网 vs 共享状态板 | **重** | teammates 团队·共享 TaskList·SendMessage·peer(存疑) ｜ kanban·swarm·profiles-as-roster·黑板·依赖图·原子认领 | 两图对比 `.flow2` + 制品 |
| 2 | §02 范式盘点对照 | 中 | subagent·并行 fanout·coordinator·**fork(独有)** ｜ delegate_task·并行批量·orchestrator 嵌套·**profiles(独有)** | `.matrix` 三列（范式｜CC｜HM｜同/异） |
| 3 | §04 信任自报 | 中 | 完成通知「trust it」·coordinator 才加 verifier ｜「SELF-REPORTS」父亲自复核 | 两家原文并排（制品，王牌） |
| 4 | §03 委派控制 | 中 | 前台默认+模型选前后台·background-agent·fork 恒后台 ｜ **async_delegation**·委派默认后台·background 参数废弃 | 原文对照（制品）+ 一句裸文 |
| 5 | §01 问题定义（趋同） | 轻 | fork/subagent「防上下文淹没」 ｜ delegate WHEN TO USE 原文 | 裸文 + 两段原文行内 |
| 6 | §06 三分岔取舍收尾 | 中 | —（回指上文三处） | 手工三行收束（`88px 标签列+正文列`两栏，无卡） |
| 7 | §03 附「何时不该拆」（趋同） | 轻 | 目标已知用 Read/Glob·单任务别开清单 ｜ 机械活用 execute_code·别 pass-through | 行内对照一句 + 原文 |
| 8 | §03/§04 附 成本敏感（趋同·手法异） | 轻 | fork byte-identical 复用 prompt cache·别设 model ｜ 按父剩余上下文×0.5 裁剪 summary·并发默认 3 | 裸文一句 + 数字 |
| 9 | §02 附 隔离档位（趋同·默认弱可升级强） | 轻 | 同 cwd→worktree→remote 沙箱(ant) ｜ 同进程线程→kanban worker 独立进程 | 行内对照，可并进 §02 表脚 |
| 10 | §07 悬而未决·边界 | 轻 | peer=impl-missing·可监督两家趋同·observer/DreamTask(支线) ｜ ACP 仅出向·MoA(多模型非多agent)·batch_runner(离线非运行态) | 悬而未决列表 |

**支线机制去向（不静默丢，明确降位）**：CC observer/AgentSummary/DreamTask、Hermes MoA、batch_runner、in-process teammate、CC remote 沙箱——均非本章主线分岔，进 §07 边界或页脚一句交代（标明是什么、为何不入主线），不进重/中档。

**安静基线**（占全章大部分）：§01、§03 附条、§08 成本、§09 隔离、§07 边界——全轻档/裸文/行内对照。全章唯一重档＝§05。

## 问 5 · 重档草案（§05 Hero）
**两图并排 `.flow2`，`flowchart TD`，同一套图形词汇，差异靠高亮：**
- **左·Claude Code（blue）**：`队长/协调者` → 三个具名队友（研究/实现/验证）；**队友节点之间有双向消息箭头**（SendMessage）；一块「共享任务看板」所有人连。**差异高亮节点＝agent↔agent 消息箭头**（blue 粗描边）。图注：具名队友 · 邮箱互发消息 · 人当队长在同一张消息网。
- **右·Hermes（purple）**：三个独立 worker 进程，**彼此之间无连线**；全部连到中央「共享状态板 · kanban.db（依赖图 / 黑板评论 / 原子认领）」。**差异高亮节点＝中央共享状态板 +「worker 间无消息」**（purple 粗描边）。图注：独立进程 · 不互发消息 · 只读写共享状态板协调。
- **3 秒差异测试**：遮标题，左图 agent 之间有箭头、右图 agent 之间没有（只连中央板）——差异＝「有没有 agent 间消息」，一眼可辨。
- **真实制品并排**（图下）：
  - CC：`Your team cannot hear you if you do not use the SendMessage tool.`（`TeamCreateTool/prompt.ts:107`）
  - Hermes：`The shared blackboard is also deliberately low-tech: structured JSON comments on the root task.`（`kanban_swarm.py:47`）+ `Put cross-worker notes on the root task using structured comments.`（`:66-74`）
- **对照卡**（图下一段裸文，不进框）：点明 CC 团队层「消息网 + 共享看板」并存、Hermes「纯共享状态、分身不互发消息」；且两家都能旁观/暂停/打断单分身（趋同，别写成一方黑盒）。

## 关键制品清单（每个抽象主张钉一件真实原文）
- §01 CC：`The criterion is qualitative — "will I need this output again" — not task size`（prompt.ts:83-88）｜HM：`Only the final summary is returned -- intermediate tool results never enter your context window`（delegate_tool.py:3213）
- §02 fork：`it inherits your full conversation context ... keeps its tool output out of your context`（forkSubagent.ts）｜profiles：`Each profile is a fully independent HERMES_HOME directory`（profiles.py:1-9）
- §03 CC：`Foreground (default) when you need the agent's results before you can proceed ... background when you have genuinely independent work`（prompt.ts:264）｜HM：`BOTH MODES RUN IN THE BACKGROUND ... Do NOT wait or poll`（delegate_tool.py:3220-3225）+ background `DEPRECATED / IGNORED`（:3405-3415）
- §04 CC：`You get a completion notification; trust it.`（prompt.ts:91）｜HM：`Subagent summaries are SELF-REPORTS, not verified facts ... verify it yourself`（delegate_tool.py:3248-3254）
- §05 见重档草案。

## 硬边界（写进渲染员提示，防翻车）
1. **不碰「在场/人在不在环」**——收尾只落「对协作手段的取舍」，不写「CC 假设人在场 / Hermes 无人值守」。
2. **委派层是趋同**——§01/§02 老实呈现趋同，别制造分歧。
3. **peer 跨机=impl-missing**——别当既成能力；提到就标「当前代码树未闭环」。
4. **可监督性趋同**——两家都能旁观/暂停/打断，别写成「CC 能盯、Hermes 黑盒」。
5. 标题用专业术语、禁俏皮比喻、**禁「X 秒就懂 / 一眼看穿」夸张**（改「这张图读法很直接：…」）。
6. 版本切片：Hermes @8e734810d（成稿页脚标注，与前 11 章 daf4f1a7a 不同基线）。
