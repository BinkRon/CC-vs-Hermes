# 视觉脚本 · Ch05 第 2 节「它学你」重设计

> 依据：新版 `design-principles.md` Part 2.1 五问 + Part 1 全序梯度。
> 范围：聚焦第 2 节内部重构，但全序表覆盖整章（梯度须在整章尺度算）。
> 素材：`scratchpad/ch-a2r-05/`（cc-extract.json / hm-extract.json，五问结构，含 file:line）。

---

## 问1 · 一句话论点（读者只能带走这一句）

> **「越用越懂你」不是一个温柔功能，是一条布满防御的流水线——两家在"什么时候偷偷记你、记什么、记了凭什么信"上下了不同的赌注：Claude Code 撒网（多时机、分主体、夜里整理、还跨人共享），Hermes 定期复盘（攒一阵子回看一次、整块管）。**

回指章脊：这条学习线沉淀出的东西（画像/记忆/技能）**住哪、跟谁走**，正是章末"定位 verdict"要用的弹药。深挖服务于 verdict，不是自足的记忆专论。

---

## 问2 · 最大卡壳点（决定重档给谁）

PM 读者的默认心智：「它就是把我说的话存了下来」。三个它想不到的真相 = 三个卡壳点，按落差排序：

1. **【最大】提取不是一个动作，是一条多时机、多主体、后台的流水线。** CC 在 5 个时刻由不同角色（主 agent 顺手 / 回合末 fork / 会话中 fork / 夜里做梦 fork / 小模型扫技能）分头做；Hermes 攒到阈值起一个复盘分身一次管完。→ **重档 hero**。
2. **【次大】记忆是攻击面、也会把 agent 养成固执。** 记忆会过时误导、会被投毒注入、会让 agent"越记越畏手畏脚"。PM 根本不会想到"存点偏好"需要安检。→ **重档**。
3. 记什么的判据反直觉：**成功也要记**（只记纠正会让它变胆小）、**越会过时的越不该记**。→ 中档，靠真实原文打钉。

---

## 问3 · 叙事顺序（按本节论证逻辑，不按模板）

第 2 节内部走「**一条记忆/技能的一生**」时间线，三拍：

- **拍1 什么时候记、谁来记**（防：打扰你 / 抢你算力）→ 承接现有 lead「记忆记你是谁、技能记怎么为你做事」，进入写入侧节奏 hero。
- **拍2 记什么、凭什么筛**（防：记脏 / 记成教条）→ 该记/不该记二分 + 杀手原文。
- **拍3 记了之后凭什么信**（防：记死误导 / 被投毒 / 卡死回复）→ 安检门。
- 收尾接「用户建模分野」（USER.md 一等公民 vs 揉进记忆）→ 顺势交棒给第 3 节「你改它」。

每拍先抛**产品问题**（先行句），机制只作证据；正文不出现函数/类名。

---

## 问4 · 全序重量分配表（覆盖研究 JSON 全部机制，谁都不许静默消失）

| 名次 | 块 | 档 | 凭什么这档 / 卡壳点 |
|---|---|---|---|
| **1** | 拍1 hero「写入侧节奏」双泳道时间轴 | **重** | 全章最大卡壳点：黑箱化的"它就是存了点东西" |
| **2** | 拍3「安检门」记忆守卫流程 | **重** | 次大卡壳点：记忆是攻击面/会变固执，PM 想不到 |
| 3 | 拍2「该记 vs 不该记」二分 + 原文制品 | 中 | 制品即可视化，硬上图反稀释 |
| 4 | 用户建模分野（USER.md vs 揉进记忆）matrix | 中 | 逐维并置足够；本节收尾 |
| 5 | 现第 5 节「逐维对照」matrix | 中 | 现成，不动 |
| **基线·安静** | 第 1 节定义空表 / 第 4 节懂≠顺闸 / 第 6 节防夸大 / 各段连接散文 | 轻·裸文 | 梯度靠这些裸文安静挣来；thesis 才进绿框 |

**机制清点（防静默丢弃，逐条须在稿中有归宿）：**

*拍1 写入侧节奏（时机+主体+去向）*
- CC：主 agent 顺手写（prompts.ts:5-8）｜回合末补写 fork·主/后台每回合互斥（extractMemories.ts:296-337；stopHooks.ts:141-153）｜会话笔记 fork·阈值 10000/5000token+3工具（sessionMemory.ts:134-181；sessionMemoryUtils.ts:31-36）｜夜间做梦·24h+5会话·**非默认**（autoDream.ts:122-190；config.ts:13-21）｜召回每轮 Sonnet 挑≤5（findRelevantMemories.ts:18-24）｜团队跨人同步·2s debounce（teamMemorySync/index.ts:1-24）｜**分模型**：fork 用主模型 warm、召回用 Sonnet、技能扫用小模型（skillImprovement.ts getSmallFastModel）
- HM：即时写盘·不改本 session 系统提示（memory_tool.py:11-14,1058-1081）｜记忆复盘 nudge 每~10 轮（turn_context.py:294-301；agent_init.py:1203-1211）｜技能复盘 nudge 每~10 工具迭代（conversation_loop.py:688-692；turn_finalizer.py:435-441）｜两触发**合并成一次复盘**（background_review.py _COMBINED_REVIEW_PROMPT）｜复盘用**主模型 warm 重放**·PR#17276 降本~26%（background_review.py:34-37）｜冻结快照 session start 注入·本 session 只落盘不改提示（memory_tool.py:615-626）｜空闲策展 7 天·min_idle 2h·consolidate 出厂关（curator.py；config.py:2236-2253）｜**无跨人**（自托管单机）

*拍2 角度（提什么/不提什么）*
- CC：四类记忆信号 user/feedback/project/reference（memoryTypes.ts:46-94）｜**feedback 成功 AND 失败都记**（memoryTypes.ts:60-62,134-135）｜What NOT to save·连"显式让存"也拦（memoryTypes.ts:183-195）
- HM：复盘两问（background_review.py:163-166）｜记忆优先级 偏好&纠正 > 环境 > 流程（memory_tool.py:1073）｜**会一周内过时的别进记忆**（prompt_builder.py:155-159）｜技能侧 Do NOT capture·环境错误别记否则变自我设限（background_review.py:250-269）｜挫败信号"太啰嗦/别这么格式化"= 一等技能信号（background_review.py:181-187）

*拍3 容错（凭什么信/怎么不记脏）*
- CC：三段召回护栏 用前核实/ignore 语义/漂移警告（memoryTypes.ts:200-256）｜best-effort 静默失败·游标不推进下次重来（extractMemories.ts:429-435）｜去重 update 优先（prompts.ts:32,65）
- HM：投毒扫描·命中替 `[BLOCKED]` 占位（memory_tool.py:168-241）｜字数预算防死循环·连败 3 次终止免卡回复 #42405（memory_tool.py:124-166）｜漂移守卫·外部手改先快照再拒写 #26045（memory_tool.py:83-110）｜write_approval 审批闸·出厂关（memory_tool.py:823-924；config.py:2047-2059）｜声明非命令措辞（prompt_builder.py:162-167）

*用户建模分野*
- HM：USER.md 独立画像·两套预算·系统提示分块（memory_tool.py:55-59）｜开机主动提议建档·consent-gated（onboarding.py:134-183）｜每轮活注入画像
- CC：无独立画像文件·揉进四类记忆·每轮 Sonnet 挑≤5（findRelevantMemories.ts）

---

## 问5 · 重档草案

### 重档 A · 拍1 hero「一条记忆的一生·写入侧节奏」——手工 HTML 时间轴（非 mermaid）

- **图式依据**：Part 3 §3A「隔离/派生（主线 vs 支线）→ 双泳道、末端回传箭头」；横向时间轴+定位标记 flowchart TD 画不了 → 手工 HTML（比照综合② "在场之脊" 先例）。躲开离线守卫。
- **结构**：横轴 = 一场对话从左到右。每家一组"上下泳道"：**上 = 主对话**；提取事件从主对话**向下掉进"记忆库"**，召回**向上回注**。CC / Hermes 上下并置（同一图形词汇，差异靠疏密高亮）。
  - **CC 那条又密又杂**：边聊边记（多个下掉点·中性色）＋回合末补写（一个下掉点）＋每轮 Sonnet 挑≤5 回注（细上箭头）＋一枚 🌙 标夜里做梦整理（**灰/虚线 = 非默认**）＋一枚 👥 标跨人同步。
  - **Hermes 那条又疏又整**：约每 10 轮**一次复盘**下掉（单个粗点）＋开会话"冻结快照"整块注入（一根粗上箭头）＋**无 👥**（单机不跨人）。
- **读者 0.5 秒该看到**：CC = 高频撒网 + 夜间批处理 + 跨人；Hermes = 低频复盘 + 整块管 + 留在你机器上。差异 = **疏密与节奏**，不是文字。
- **高亮纪律**：只有"疏 vs 密"和"CC 独有的 🌙/👥"上色/描边，其余全灰（Part 1B 明线：遮住标题 3 秒指得出差异）。
- **词条解码**：🌙「夜里做梦」、👥「跨人同步」、"冻结快照"须配 `data-tip` 一句话（Part 1B 明线）；🌙 图注标"特性门控·非出厂默认"防"默认→绝对"夸大。
- **不装什么（防过密）**：召回"怎么挑≤5 / 冻结 vs 活注入"的细节**不进 hero**，留给拍3 前段或一条小 matrix。hero 只讲一件事——"它多勤快地趁你不在偷偷记"。
- **制品钉**：图下附 CC 会话笔记阈值「10000 / 5000 token + 3 工具」、HM 复盘间隔「每 ~10 轮 / ~10 工具迭代」、策展「7 天 · 空闲 2h」——真实数字作证据。

### 重档 B · 拍3「安检门」——记忆从写入到被采纳要过几道闸

- **图式依据**：Part 3 §3A「过程/状态 → 分步」或简洁 `flowchart TD`；语义配色强制（闸=amber 描边、通过=green）。
- **结构**：一条记忆两段旅程——
  - **写入侧闸**：投毒扫描 →（命中）`[BLOCKED]` 占位不删原文｜字数超预算 → 先合并再写·连败 3 次终止免卡回复｜外部手改 → 先快照再拒写。
  - **读取侧闸（召回前）**：用前核实（"记忆说 X 存在" ≠ "X 现在还在"）｜用户说 ignore → 当记忆为空｜漂移 → 信你眼见的、改陈旧记忆。
  - 两侧之间标：CC 偏**读取侧三段护栏**、HM 偏**写入侧硬闸（投毒/预算/漂移）**——顺手带出一个分野。
- **读者 0.5 秒该看到**：记忆不是"存了就信"，中间站着一排安检——而两家把安检重心放在了不同端。
- **制品钉**：`[BLOCKED: {filename} entry contained threat pattern(s)…]` 原文（HM，memory_tool.py:234-238）；「'The memory says X exists' is not the same as 'X exists now.'」原文（CC，memoryTypes.ts:200-256）。

### 中档 · 拍2「该记 vs 不该记」

- 二分对照（正例绿点 / 反例灰），**不上大图**。核心两条杀手原文：
  - 成功也要记：「if you only save corrections, you will … drift away from approaches the user has already validated, and may grow overly cautious」（CC，memoryTypes.ts:134-135）
  - 越会过时越不该记：「If a fact will be stale in a week, it does not belong in memory」（HM，prompt_builder.py:155-159）；技能侧「环境错误别记，否则硬化成 agent 月复一月拿来拒绝自己的借口」（HM，background_review.py:250-269）

### 中档 · 用户建模分野

- 现有 `.matrix` 保留：USER.md 独立画像 + 主动建档（HM）vs 无画像文件 + 揉进四类 + 每轮挑≤5（CC）。诚实标注 USER.md 内手写与自学**混在同一本、无来源标记**（amber caveat）。

---

## 设计门自查预挂（Part 2.2）

- [ ] 10 秒重点测试：滚一遍能指出"拍1 hero 是本节最重的图"。
- [ ] 梯度：全序表已排、第 1 名已论证、基线（1/4/6 节裸文）已点名；两个重档各自点名卡壳点、非凑数。
- [ ] 完整性挂钩：上方机制清点逐条在稿中有归宿，无静默丢弃（夜梦"非默认"、USER.md"混同无标记"、CC 无独立画像三处防夸大 caveat 必须在）。
- [ ] 机械两关：抽脚本 `node --check` + 浏览器 smoke（真点交互 / 图深色 / mermaid 实体）。
