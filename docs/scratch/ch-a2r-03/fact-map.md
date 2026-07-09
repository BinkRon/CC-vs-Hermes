# CH-A2R-03 事实梳理（按调研脉络平铺·不预设轴）

> 切片：CC=`/Users/bink/cc_project/claude-code-main`（真源码树·无 git 版本）｜Hermes=`/Users/bink/.hermes/hermes-agent`@`8e734810d`（2026-07-08）。
> 方法：先按脉络老实摊事实、每节标「趋同 / 分岔」，收尾定位那节的轴单列、待 PM 定。原文（英文）是证据，保留逐字。
> 源：`research-cc.json` / `research-hermes.json`。

---

## 脉络 0 · 起点：single-agent 撞什么墙

两家在提示词里自认的「为什么要多 agent」几乎逐字重合——**这是趋同，不是分岔**：核心是**上下文窗口会被中间原始输出塞满**，委派把「不再需要的原始输出」挡在父窗口外。

- CC：`Fork yourself when the intermediate tool output isn't worth keeping in your context. The criterion is qualitative — "will I need this output again" — not task size.`（`AgentTool/prompt.ts:83-88`）
- Hermes：`Only the final summary is returned -- intermediate tool results never enter your context window.`（`delegate_tool.py:3213`）+ WHEN TO USE：`Reasoning-heavy subtasks / Tasks that would flood your context with intermediate data / Parallel independent workstreams`（`:3226-3229`）

连「**何时不该拆**」也趋同：机械活别派、单个 tool 调用直接调、目标已知直接读（CC `prompt.ts:234-240`、Hermes `:3231-3232`）。

**判断**：问题定义层是两家最趋同的地方。本章不能在这一层制造分歧。

---

## 脉络 1 · 有哪些协作范式，各解决什么【趋同的骨架 + 两处非对称】

| 范式 | CC | Hermes | 同/异 |
|---|---|---|---|
| fresh 隔离委派 | subagent（`prompt.ts:202`，零共享） | delegate_task（`delegate_tool.py:3211`，fresh 无父历史） | **趋同** |
| 并行 fan-out | 一条消息多个 Agent 调用 | tasks 数组批量 | 趋同 |
| 嵌套编排 | coordinator 模式（`coordinatorMode.ts`，双门控默认关） | orchestrator role（`delegate_tool.py:3313`，MAX_DEPTH=1 默认扁平） | 趋同（都默认关/浅） |
| 共享看板协作 | teammates + 共享 TaskList（`TeamCreateTool`，灰度门控） | kanban / swarm（`kanban*.py`，需显式进入） | 形态分岔（见脉络 4/5） |
| 监督单分身 | teams panel + TaskStop | TUI /agents overlay + RPC | 趋同（都能） |
| **继承父上下文的 fork** | **有**（`forkSubagent.ts`，复用 prompt cache） | **无对应物**（一律 fresh，靠 context 字段手搬） | **非对称①** |
| **角色=独立实例花名册** | 无（teammate 是同套下的 agent 类型） | **profiles**：每角色一个完全独立 HERMES_HOME（`profiles.py`） | **非对称②** |
| 多模型集成 MoA | 无 | 有（`moa_config.py`，默认关） | 非对称③（弱相关，多模型非多 agent） |
| peer 跨会话/跨机器 | 提示词/寻址在，**传输层实现缺失**（见脉络 5） | 仅出向 ACP 驱 Copilot 当子后端 | 都非既成 |

**判断**：范式骨架高度趋同。两处真非对称：CC 的 **fork**（解决「要个接着我上下文干、又不让它的原始输出污染我」）、Hermes 的 **profiles-as-roster**（角色=隔离实例，接住它自托管多实例的底色）。

---

## 脉络 2 · 何时触发哪种协作【金矿·出现真分岔】

### 分岔 A：轻委派的「同步/异步」控制默认——留给模型 vs 写死壳里
- **CC：留给模型按依赖判断。** `Foreground (default) when you need the agent's results before you can proceed ... background when you have genuinely independent work to do in parallel.`（`prompt.ts:264`）。fork 要不要用也是模型质性判断（`prompt.ts:83`）。
- **Hermes：委派=默认后台，模型不能选。** `BOTH MODES RUN IN THE BACKGROUND. delegate_task returns immediately ... Do NOT wait or poll`（`:3220-3225`）；`background` 参数 `DEPRECATED / IGNORED`（`:3405-3415`），`run_agent.py:5664` 硬编码 `background=(not _is_subagent)`。唯一同步例外＝orchestrator 子（depth>0）。

> ⚠️ 防以偏概全：别写成「CC 全留模型 vs Hermes 全固化」。CC 也有强制（fork 模式所有 spawn 恒后台 `forkSubagent.ts:26`）；Hermes 也给模型择时指引（WHEN TO USE/NOT）。**准确差异＝在「委派该不该后台异步」这个具体决策上，CC 默认前台+模型选，Hermes 默认后台+模型不能选。**

### 分岔 B：升级到重协作的触发在哪一层
- **CC：在提示词层引导模型。** TeamCreate `Use this tool proactively whenever ... When in doubt about whether a task warrants a team, prefer spawning a team.`（`TeamCreateTool/prompt.ts:5-12`）——鼓励模型主动组队（但能力灰度门控）。
- **Hermes：不在提示词层教「何时升级」，重协作是结构性显式入口。** 没有「何时从 delegate 升级到 kanban」的择时语句；kanban/swarm 靠 `hermes kanban`/profile 显式进入（`toolsets.py:70-77`）。

**判断**：触发层是本章第一处真分岔。CC 倾向把「用哪种协作、同步异步」当模型的运行时判断并鼓励主动组队；Hermes 把「委派即后台」固化进壳，把「重协作」放在一条要人显式走进去的独立路径。

---

## 脉络 3 · 协作的代价：信任与成本【信任分岔 + 成本/隔离趋同】

### 分岔 C：信不信分身的自报（接轴一）
- **CC：默认信任。** `You get a completion notification; trust it.`（`prompt.ts:91`）、`The agent's outputs should generally be trusted`（`:268`）。**只有** coordinator 模式才加独立核验层：`Verification means proving the code works, not confirming it exists. A verifier that rubber-stamps weak work undermines everything.`（`coordinatorMode.ts:220-227`）
- **Hermes：默认不信，写进委派工具本身。** `Subagent summaries are SELF-REPORTS, not verified facts ... require the subagent to return a verifiable handle (URL, ID, absolute path, HTTP status) and verify it yourself`（`delegate_tool.py:3248-3254`）——常态，不是某个模式才开。

**判断**：真分岔，且呼应轴一（Hermes 对任何自报不全信）。CC 默认信任、按需在编排模式加核验；Hermes 默认怀疑、把「亲自复核」焊进委派常态。

### 趋同：两家分身都够不到用户
CC：ASYNC_AGENT_ALLOWED_TOOLS 白名单无 AskUserQuestion/Agent，结果对用户不可见须父转达（`prompt.ts:257`、`constants/tools.ts:55-71`）。Hermes：clarify 被硬 block（连同 delegate/memory/send_message/execute_code/cronjob，`delegate_tool.py:45-54`）。

### 趋同（手法不同）：都对成本敏感 + 都「默认弱隔离、可升级强隔离」
- 成本：CC 优化**缓存命中**（fork byte-identical 前缀复用 prompt cache、别设 model，`forkSubagent.ts:44-58`）；Hermes 优化**上下文预算**（按父剩余 headroom×0.5÷批量裁剪 summary、并发默认 3、>10 警告线性成本，`delegate_tool.py:D3`）。
- 隔离：CC 四档（同 cwd→cwd 覆盖→worktree→remote 沙箱）；Hermes 三档（同进程线程+独立终端会话→kanban worker 独立 OS 进程按 profile 隔离→无默认沙箱共享宿主 FS）。都默认弱、可升级。

---

## 脉络 4 · 成果怎么用：回流 / 汇聚 / 落地 / 交接 / 持久化【第二处形态分岔】

- **回流形式**（趋同）：都只回摘要不回轨迹。CC fork 强制固定格式 `Scope:/Result:/Key files:/Files changed:/Issues:` ≤500 词（`forkSubagent.ts:171-198`）；Hermes 回数组每任务一条 {status,summary,...}。
- **谁来汇聚**（分岔）：
  - CC：**父/coordinator 亲自 synthesize，明令不可外包**——`Always synthesize — your most important job ... You never hand off understanding to another worker.`（`coordinatorMode.ts:255-259`）+ `Never delegate understanding.`（`prompt.ts:112`）。
  - Hermes：swarm 把 synthesis 做成**拓扑里一个专职角色卡**（verifier 卡 gate:pass/block + synthesizer 卡，`kanban_swarm.py:8-9,175-185`）；orchestrator 也自己综合。
- **成果落哪**（分岔·重现「父的脑子 vs 共享的板子」）：
  - CC：→父上下文（`<task-notification>` user-role 消息）；worktree 改动→git 分支；团队→共享 TaskList。
  - Hermes：delegate→父上下文；kanban/swarm→**共享 kanban.db 黑板**（`[swarm:blackboard]` 结构化 JSON 评论 + completion metadata，`kanban_swarm.py:11-13,66-74`）。
- **跨子交接**（分岔）：
  - CC：经**父这个中心**——父综合后写新 prompt（fresh 重述 / continue 复用 loaded context），团队用 TaskList blocks/blockedBy。
  - Hermes：靠**共享 DB 依赖图**——todo 待依赖满足→ready、原子认领防抢；swarm 固定依赖链 workers→verifier→synthesizer + root 黑板；`Read sibling/parent handoffs from Kanban context before working.`（`kanban_swarm.py:70`）。
- **持久化**（分岔）：CC 全轨迹落盘 5GB + transcript 可 resume + worktree→分支；Hermes delegate/async **不持久**（/new 或退出即丢），但 **kanban.db 持久沉淀**、dispatcher 重启仍在可续跑。

**判断**：第二处真分岔在「成果与协调的重心」——CC 一切经过**父/队长这个中心节点**（fork 是父的延伸、synthesis 焊在父、消息网以父为队长）；Hermes 的重协作外化到**一块共享持久状态（kanban.db 黑板 + 依赖图）**，可脱离具体父自转。

---

## 脉络 5 · 边界与待查证

- **CC peer 跨会话/跨机器＝impl-missing**：提示词层（`SendMessageTool/prompt.ts:6-20`）+ 寻址解析层（`peerAddress.ts:8-21`）齐全，但传输层（`bridge/peerSessions.js`、`utils/udsClient.js`）与发现层（`ListPeersTool.js`）在源码树中缺失、全树 grep 未命中——**不可端到端闭环，别当既成能力写**。（另有跨机安全门：`Cross-machine bridge message requires explicit user consent`、bypass-immune，`SendMessageTool.ts:586-602`。）
- **ACP/外来 agent**：CC not-found（跨会话仅 UDS/bridge，且见上）；Hermes 有但仅**出向** provider（config 驱动、对模型隐藏，`delegate_tool.py:3443-3462`）——不是通用入向 agent 互通花名册。
- **可监督性**：两家都能旁观/暂停/打断单分身（趋同，别写成「CC 能盯、Hermes 黑盒」）。

---

## 脉络 6 · 收尾定位【轴·待 PM 定·标在场红线】

事实摊完，三处真分岔集中在：**A 委派控制默认（模型选/壳固化）· C 信任自报（默认信/默认疑）· 成果重心（父中心/共享板）**。若要收一个「两家对协作手段的定位」：

- **候选轴（观察，非预设）**：CC 把协作组织成**围绕一个中心 agent（父/队长）的延伸**——委派保护父上下文、synthesis 焊在父、消息网以父为节点、默认信任子；Hermes 把重协作外化成**一套可脱离父自转的共享结构**——默认后台、默认复核、成果沉进持久 DB 黑板、靠依赖图去中心协调。

- ⚠️ **在场红线**：这个候选轴离「父/人是否在场盯着」很近，但那是综合②独占的总变量。收尾**只能落到「协作手段围绕什么组织（中心 agent 的延伸 vs 外化的共享状态机）」**，不得写成「CC 假设人在场 / Hermes 无人值守」。措辞需 PM 一起把关。

- **备选**：也可更保守——收尾不拔一个统一轴，只并列三处分岔 + 各自一句「这照见对协作手段的什么取舍」，把总变量完全留给综合②。
