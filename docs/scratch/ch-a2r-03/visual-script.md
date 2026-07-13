# CH-A2R-03 视觉脚本 v2（报告化重构 · 渲染依据）

> **PM 重定骨架 2026-07-09**：弃「三处分岔并列」叙事骨架，改**产品报告化**——事实清晰＋高可视化＋**信息架构驱动**（不是论点驱动）。
> **定性校正**：本章非整章弱信号；**产品判断浓度全集中在「何时拆」这一层**，机制盘点层才弱（趋同、像功能清单）。
> **主线＝任务生命周期流：拆 → 派 → 协调 → 合。** PM 最省认知的读法，不需要「三分岔」这种作者视角。
> 依据 `fact-map.md`。切片 CC 真源码 / Hermes @8e734810d。**须继承 DSN-04 开篇范式**（H1「Loop 与其他 Agent：论断」+ TL;DR 绿标 + `00·问题`叙述框），别推翻。

---

## 一句话（报告的封面结论，非要证明的轴）

多 agent 是 single-agent 上下文极限逼出的一套**升级阶梯**（从派一个干净分身，到一支共享看板的团队）。两家的阶梯几乎一一对得上——**真正的产品判断不在「有哪些档」，而在「何时该爬这个阶梯、爬到第几级、谁来决定」**。这一层，两家分道。

---

## 三个视觉重点（其余安静基线，防盒子疲劳）

1. **门面：协作能力升级阶梯全景图**（bespoke·让 PM 10 秒拿到地图）
2. **核心节：「何时拆」决策块**（决策光谱 + 两家 WHEN TO USE/NOT 原文并排）
3. **Hero：§04 协调拓扑双流程图**（消息网 vs 共享状态板·唯一 mermaid 重档·保留旧稿对的那个）

> **配色纪律**：**趋同用证据（原文并排）说话，分野用可视化说话**。别把趋同做成重图（会显得"没差异"），也别把分野埋进文字。

---

## 骨架（7 节 · 生命周期流）

- **00 · 问题（继承 DSN-04 `00·问题`叙述框）**：一个 agent 干不完的活——一个大重构 / 大调研，单个 agent 的上下文和时间都扛不下。拆开之后，谁跟谁怎么管？**为什么非拆不可（趋同·并进本节）**：核心不是"人手不够"，是**上下文是稀缺资源**——中间原始输出会把父窗口塞满，委派把"不再需要的原始输出"挡在父窗口外。
- **01 · 全景：协作能力的升级阶梯【门面图】**：多 agent 到底有哪些档。单 agent → 隔离委派 → 并行 fan-out → 嵌套编排 → 共享看板团队，代价（token / 协调 / 跑偏风险）逐级递增。两家骨架一一对得上，**只有两处一方有一方无**：CC 的 fork（第 1 级旁支）、Hermes 的 profiles（横切）。
- **02 · ★何时拆【核心节 / 脊】**：三个刻度——① **拆不拆**（趋同·两家逐字重合划"别滥用"红线）② **拆多重 / 何时升级**（分野：CC 提示词鼓励主动组队 vs HM 不教择时、靠显式入口）③ **谁来判断**（分野：模型临场 vs 壳写死；原"同步/异步"归此）。
- **03 · 派出去之后：分身带着什么代价干活**：隔离（各自沙箱？防互踩）· 信任（信不信它自报"我做完了"）· 成本（token 怎么省）· 都够不到用户（趋同）。紧凑三联对照。
- **04 · 分身之间怎么协调【Hero】**：一张互发消息的同事网，还是一块只读写的共享状态板。双流程图对比。
- **05 · 干完怎么合回来（fan-in）**：成果怎么回流 · **谁来汇聚成一个连贯结果**（父不可外包 vs synthesizer 角色卡）· 落到哪 · 持久化。**补回原被 §05 拓扑吃掉的 F 组料。**
- **06 · 悬而未决 · 边界与降位说明**。

---

## 载体规格（渲染员照此实现）

### 【门面图 · 01】协作能力升级阶梯 —— bespoke（本章唯一 bespoke 额度，scoped 本章根 class、只引 tokens）

**形状**：横向阶梯，从左（轻）到右（重）5 阶，每阶一张卡；卡内 CC / HM 对应物上下并排；卡底一条贯穿的「代价 / 协调开销 → 递增」轴。

| 阶 | 级别 | CC | Hermes | 备注 |
|---|---|---|---|---|
| 0 | 不拆·单 agent | 目标已知直接 Read/Glob | 机械活直接 execute_code | 阶梯起点（呼应 §02 何时不该拆） |
| 1 | 隔离委派（1 个干净分身） | subagent（零共享·fresh） | delegate_task（fresh·无父历史） | **旁支徽章：CC 独有 fork**（继承父上下文的分身） |
| 2 | 并行 fan-out（委派×N） | 一条消息发多个 Agent 调用 | tasks 数组批量 | |
| 3 | 嵌套编排（委派套委派） | coordinator 模式（双门控·默认关） | orchestrator 角色（层深≤1·默认扁平） | 都默认关/浅 |
| 4 | 共享看板团队（分身共用土台） | teammates ＋ 共享 TaskList（灰度门控） | kanban / swarm（需显式进入） | 协调形态大分岔→详见 §04 |

- **横切徽章（不在阶梯某一级、贯穿全阶）**：**HM 独有 profiles**——每个角色一个完全独立实例目录（配置/记忆/会话各自隔离）；**默认隔离档位**：CC 同 cwd→独立工作树→远程沙箱 / HM 同进程线程→独立 OS 进程（都默认弱、可升级强）。
- **读法注（图下一句裸文）**：两家的阶梯几乎逐级对得上；真正一方有一方无只有 fork / profiles 两处。骨架不是差异所在——差异在"何时爬、爬多高、谁决定"（→ §02）。
- **关键原文（钉在图下 artpair）**：
  - CC fork：`it inherits your full conversation context ... keeps its tool output out of your context`（forkSubagent.ts）
  - HM profiles：`Each profile is a fully independent HERMES_HOME directory with its own config.yaml, .env, memory, sessions, skills, gateway, cron, and logs.`（profiles.py:1-9）

### 【核心节 · 02】何时拆 —— 三刻度，趋同用原文、分野用对照

**刻度① 拆不拆（趋同·逐字重合）** —— 载体：「该拆的信号 vs 不该拆的信号」双栏决策卡 + 两家原文并排证趋同。
- 该拆：中间产物会淹没父上下文 / 有真正独立可并行的活 / 推理密集子任务。
- 不该拆：机械活别派 / 单个 tool 调用直接调 / 目标已知直接读。
- 原文：CC `Fork yourself when the intermediate tool output isn't worth keeping in your context. The criterion is qualitative — "will I need this output again" — not task size.`（prompt.ts:83-88）｜HM WHEN TO USE：`Reasoning-heavy subtasks / Tasks that would flood your context with intermediate data / Parallel independent workstreams`（delegate_tool.py:3226-3229）+ 何时不该拆（CC prompt.ts:234-240 / HM :3231-3232）。
- **一句点题（裸文）**：两家逐字重合地划"别滥用"红线，因为背后是同一个物理约束——上下文稀缺、协调有代价。多 agent 不是越多越好，这是设计者的共识，不是随意设计。

**刻度② 拆多重 / 何时升级（分野）** —— 载体：两家原文对照。
- CC：提示词层**鼓励模型主动组队**——`Use this tool proactively whenever ... When in doubt about whether a task warrants a team, prefer spawning a team.`（TeamCreateTool/prompt.ts:5-12）（但能力灰度门控）。
- HM：**不在提示词层教"何时升级"**，重协作是结构性显式入口——没有"何时从 delegate 升级到 kanban"的择时语句，靠 `hermes kanban`/profile 显式进入（toolsets.py:70-77）。

**刻度③ 谁来判断（分野·原"同步/异步"归此）** —— 载体：两家原文对照 + 一句裸文。
- CC：**交给模型临场判断**——`Foreground (default) when you need the agent's results before you can proceed ... background when you have genuinely independent work to do in parallel.`（prompt.ts:264）。
- HM：**写进壳的默认，模型不能选**——`BOTH MODES RUN IN THE BACKGROUND. delegate_task returns immediately ... Do NOT wait or poll`（delegate_tool.py:3220-3225）；老 background 参数 `DEPRECATED / IGNORED`（:3405-3415）；run_agent.py:5664 硬编码 `background=(not _is_subagent)`。
- **防以偏概全（必写）**：别读成"CC 全交模型 / HM 全固化"。CC 也有硬规则（fork 模式所有 spawn 恒后台 forkSubagent.ts:26）；HM 也给模型择时指引（WHEN TO USE/NOT 清单）。准确差异＝在"委派该不该后台异步"这个具体决策上，CC 默认前台+模型选、HM 默认后台+模型不能选。

### 【Hero · 04】协调拓扑双流程图 —— `.flow2` `flowchart TD`（沿用旧稿，已验证对）

- **左·CC（blue）**：队长/协调者 → 三个具名队友（研究/实现/验证）；**队友节点之间有双向消息箭头**（SendMessage）；一块共享任务看板所有人连。高亮＝agent↔agent 消息箭头（blue 粗）。
- **右·HM（purple）**：三个独立 worker 进程，**彼此无连线**；全部连中央「共享状态板 · kanban.db（依赖图/黑板评论/原子认领）」。高亮＝中央共享状态板 +「worker 间无消息」（purple 粗描边）。
- **读法（禁"X 秒就懂"夸张，改）**："这张图读法很直接：看分身之间有没有直接连线。"左有箭头、右没有（只连中央板）。
- **原文并排**：CC `Your team cannot hear you if you do not use the SendMessage tool.`（TeamCreateTool/prompt.ts:107）｜HM `The shared blackboard is also deliberately low-tech: structured JSON comments on the root task.`（kanban_swarm.py:47）+ `Put cross-worker notes on the root task using structured comments.`（:66-74）。
- **术语悬停**：SendMessage / 共享任务看板 / kanban.db / 依赖图 / 黑板评论 / 原子认领（沿用旧稿 data-tip）。

### 【新增 · 05】干完怎么合回来（fan-in）—— 补回原被吃掉的 F 组，载体：小标对照，不进重图

- **回流形式（趋同）**：都只回摘要不回轨迹。CC fork 强制固定格式 `Scope:/Result:/Key files:/Files changed:/Issues:` ≤500 词（forkSubagent.ts:171-198）；HM 回数组每任务一条 {status,summary,...}。
- **谁来汇聚（分野·王牌对比·原稿丢了这块）**：
  - CC：**父/coordinator 亲自 synthesize，明令不可外包**——`Always synthesize — your most important job ... You never hand off understanding to another worker.`（coordinatorMode.ts:255-259）+ `Never delegate understanding.`（prompt.ts:112）。
  - HM：swarm 把 synthesis 做成**拓扑里一个专职角色卡**（verifier gate:pass/block + synthesizer 卡，kanban_swarm.py:8-9,175-185）；orchestrator 也自综合。
- **落到哪（分野·呼应 §04 中心 vs 外化）**：CC→父上下文（`<task-notification>` user-role 消息）/ worktree→git 分支 / 团队→共享 TaskList；HM delegate→父上下文，kanban/swarm→**共享 kanban.db 黑板**（结构化 JSON 评论，kanban_swarm.py:11-13,66-74）。
- **交接 & 持久化**：CC 经父这个中心（父综合后写新 prompt）+ 全轨迹落盘可 resume + worktree→分支；HM 靠共享 DB 依赖图（`Read sibling/parent handoffs from Kanban context before working.` kanban_swarm.py:70）+ delegate/async 不持久（退出即丢）但 **kanban.db 持久沉淀、dispatcher 重启可续跑**。
- **一句点题**：fan-out 是"怎么拆"，fan-in 是"怎么合"——成果的去向恰好照见 §04 的形状：CC 一切回流到**父这个中心节点**，HM 沉进一块**可脱离父自转的共享状态板**。

---

## 全序重量分配表（覆盖研究 JSON / fact-map 全部机制，无一静默消失）

| 排名 | 块 | 档 | 承载的机制（CC ｜ HM） | 形式 |
|---|---|---|---|---|
| 1 | §04 协调拓扑 | **重** | teammates·共享 TaskList·SendMessage·peer(存疑) ｜ kanban·swarm·黑板·依赖图·原子认领 | 双流程图 `.flow2` + 原文 |
| 2 | 01 升级阶梯门面 | **重** | subagent·fanout·coordinator·teammates·**fork(独有)**·隔离档 ｜ delegate·批量·orchestrator·kanban/swarm·**profiles(独有)**·隔离档 | bespoke 阶梯图 + artpair |
| 3 | 02 何时拆·刻度① 拆不拆 | 中 | fork/subagent「防上下文淹没」+ 何时不该拆 ｜ delegate WHEN TO USE/NOT 原文 | 双栏决策卡 + 原文并排 |
| 4 | 02 何时拆·刻度②③ 升级/谁判断 | 中 | TeamCreate 主动组队·前台默认+模型选·fork 恒后台 ｜ 无择时语句·委派恒后台·background 废弃·硬编码 | 两家原文对照 ×2 + 裸文 |
| 5 | 03 派后·信任自报 | 中 | 完成通知「trust it」·coordinator 才加 verifier ｜「SELF-REPORTS」父亲自复核 | 两家原文并排（王牌） |
| 6 | 05 fan-in·谁汇聚 | 中 | `Never delegate understanding`·父亲自 synthesize ｜ swarm synthesizer/verifier 角色卡 | 小标对照 + 原文 |
| 7 | 00 问题+为什么拆（趋同） | 轻 | fork/subagent 防上下文淹没 ｜ delegate WHEN TO USE | DSN-04 叙述框 + 行内原文 |
| 8 | 03 派后·成本+隔离+够不到用户（趋同/手法异） | 轻 | fork 复用 prompt cache·四档隔离·白名单无 AskUser ｜ 按父 headroom×0.5 裁剪·三档隔离·clarify 硬 block | 紧凑三联对照 + 数字 |
| 9 | 05 fan-in·回流/落哪/持久化 | 轻 | fork 固定格式≤500词·父上下文·全轨迹落盘 ｜ 数组摘要·kanban.db 黑板·async 不持久 DB 持久 | 小标对照行内 |
| 10 | 06 悬而未决·边界 | 轻 | peer=impl-missing·可监督两家趋同·observer/DreamTask(支线) ｜ ACP 仅出向·MoA(多模型非多agent)·batch_runner(离线) | 悬而未决列表 |

**支线机制去向（不静默丢·明确降位到 §06 或页脚）**：CC observer / AgentSummary / DreamTask、Hermes MoA（多模型≠多 agent·默认关）、batch_runner（离线非运行态）、in-process teammate、CC remote 沙箱。

**安静基线**（占全章大部分）：00 问题、02 刻度①点题、03 成本/隔离、05 回流/落哪/持久化、06 边界——全轻档/裸文/行内。**重档只有两处＝01 阶梯门面 + §04 拓扑 Hero；中档集中在 02 何时拆（核心节）。**

---

## 硬边界（写进渲染员提示，防翻车）

1. **「何时拆」是全章的脊**——产品判断浓度在这，别当垫场句；机制盘点（阶梯）是为它服务的坐标系。
2. **趋同用证据、分野用可视化**——拆不拆/成本/隔离/够不到用户是趋同，用原文并排呈现（别做重图显得没差异）；升级择时/谁判断/信任/协调/谁汇聚是分野，才配可视化。
3. **不碰「在场/人在不在环」**——fan-in「落哪」可说"回流到父中心 vs 沉进共享板"，但**不得**写成"CC 假设人在场 / HM 无人值守"（综合②独占）。
4. **防「默认→绝对」**——嵌套/团队都标"默认关/需显式进入"；谁判断那处必写防以偏概全段。
5. **peer 跨机=impl-missing**——别当既成能力，提到标"当前代码树未闭环"。
6. **可监督性趋同**——两家都能旁观/暂停/打断，别写成"CC 能盯、HM 黑盒"。
7. **继承 DSN-04 开篇**——H1「Loop 与其他 Agent：<论断>」+ TL;DR 绿标 + `00·问题`叙述框，别推翻。
8. **标题用专业术语**、禁俏皮比喻、**禁「X 秒就懂/一眼看穿」夸张**。
9. **版本切片**：Hermes @8e734810d（页脚标注，与前 11 章 daf4f1a7a 不同基线）。
