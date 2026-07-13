══════════ 05-outside-user.html ══════════
〈title〉轴二 · Loop 之外 · Loop 与用户：它该多懂用户，这份「懂」谁说了算

`第 5 篇 · 轴二 · Loop 之外 Loop 与用户 · 用户建模`

# Loop 与用户：它该多懂用户，这份「懂」谁说了算

*和 agent 打交道，是一场双重让渡——它记得住你交出去的东西吗？*

> **【TL;DR / 核心洞察】**
> 你跟一个 agent 打交道，本质是一场 双重让渡 ——你交出意图（想要什么，说给它听），也交出 行动权 （让它替你改文件、跑命令）。
> 让渡内生两个期望：它得 懂 你的意图、它的行动得 顺 你的心意。所以「懂用户」不是锦上添花的功能，是委托关系里长出来的内生需求。这一章拆两家怎么定义「懂用户」、用什么手段做到、以及懂了之后凭什么不无条件照办。

## 00 · 问题：第二次打交道，它还得从头认识你吗

【问题框】
  你昨天花十分钟跟它交代过你是谁：后端出身、第一次碰前端；讨厌它擅自 mock 数据库；这个项目的规矩是所有改动 合成一个 PR 、别拆；还嫌它答得太啰嗦。今天你新开一个对话—— 它还记得吗？还是又得从头认识你一遍？ 这四句话，正好对应它该「懂」你的四个方面：你是谁、你的边界、你的规矩、你的口味。可一旦它真开始记你，问题就不止「记不记得」，而是： 该由谁来决定它记什么、记多深、记了之后归谁、又凭什么信 ？

## 01 · 定义「懂用户」：看两家给记忆预设了什么样的空表

_想知道一家怎么定义「懂用户」，别看它记住了什么，要看它为记忆预留了 什么样的空表 ——源码里写死的是记忆的分类和填写须知，不是填好的内容。两家的记忆结构长得完全不同。_
Claude Code · 一张装下四类记忆的通表
「你」是这四类记忆之一，跟项目、外部资源同表登记

  ┌─ 制品 · user 类的填表须知 · 原文
  │ Great user memories help you tailor your future behavior to the user's preferences and perspective ... you should collaborate with a senior software engineer differently than a student who is coding for the very first time.
  └─

  ┌─ 制品 · 还有一道强门：What NOT to save · 逐字原文
  │ ## What NOT to save in memory
  │ - Code patterns, conventions, architecture, file paths ... can be derived by reading the current project state.
  │ - Git history, recent changes ... `git log` / `git blame` are authoritative.
  │ - Anything already documented in CLAUDE.md files.
  │ These exclusions apply even when the user explicitly asks you to save. If they ask you to save a PR list ... ask what was *surprising* or *non-obvious* about it — that is the part worth keeping.
  └─
Hermes · 给用户单开一份记忆档案
它记自己的教训、它记你这个人——分成两本，各自独立预算

  ┌─ 制品 · 开机第一句话就主动提议给你建档 · 原文关键句
  │ [This is the user's very first message ever. After a one-sentence introduction ... OFFER — do not assume — to build a short profile of them ... they can decline or do it later. Never read their connected accounts (email, calendar, etc.) silently — ask each time. If they decline at any point, stop immediately.]
  └─

  ┌─ 制品 · 还专门盯着你的挫败信号 · 原文
  │ Frustration signals like 'stop doing X', 'this is too verbose', 'just give me the answer', 'you always do Y and I hate it' ... are FIRST-CLASS skill signals, not just memory signals.
  └─
_半秒就看得出的差别： CC 把用户 塞进一张四类记忆通表 的其中一栏； Hermes 干脆给用户 单开一份记忆档案 、配一份专属字数预算。_
从这两张表的栏目，能把「懂用户」拆成四个方面。逐个看两家分别登记在哪：
你是谁。 「后端出身、第一次碰前端」—— CC 的 user 类专管这个，须知里写明「对资深工程师和第一次写代码的学生，要用不同方式协作」； Hermes 干脆给你单开的 USER.md 就是这本画像。
你的规矩。 「所有改动合成一个 PR」这种项目怪规矩—— CC 分给 project 类（记代码里读不出来的项目决策）和 feedback 类（记你纠正过的走法）； Hermes 把它塞进 MEMORY.md 的项目惯例。
你的口味。 「嫌它啰嗦」这种风格偏好—— CC 收进 feedback； Hermes 更进一步，把挫败信号列为 一等信号 ，要求把教训写进「管这类任务的技能」正文里，下次开局就已经懂。
你的边界。 这一维要分两层说，别写成一句话。软性的做法边界（「别擅自 mock 数据库」） 确实进记忆的暗通道 —— CC 的 feedback 分类里逐字写着 don't mock the database 这个例子， Hermes 记忆的第一优先级也正是「用户偏好与反复纠正」。但记忆里的边界只是被注入系统提示的 建议性文本、没有强制力 ；真正有牙的硬授权（哪些工具/命令能不能跑）走的是独立的权限/审批系统，结构上就进不了记忆。

  ┌─ 制品 · 软性边界进记忆的直接证据（CC feedback 类举的例子）· 原文
  │ user: don't mock the database in these tests — we got burned last quarter when mocked tests passed but the prod migration failed
  │ assistant: [saves team feedback memory: integration tests must hit a real database, not mocks ...]
  └─
一句话记住这一维： 边界分两层 ，软的走记忆（它学你）、硬的走权限（你来规定）——是四维里唯一横跨「记忆」和「你规定它」两侧的方面，后面两节正好分别拆这两侧。

## 02 · 它学你：什么时候记、记什么、记了怎么不翻车

_上一节的四维「懂用户」，大部分落进 记忆 ——但不全是：「你的口味」这一维， Hermes 就写进 技能 正文。记忆记「你是谁」，技能记「怎么为你做这类任务」。这条学习线主要靠它自动学、趁你不在时在后台沉淀（你也能亲手编辑记忆、手写技能，但那是补充）。_
_而「 自动学 」这件听起来温柔的事，拆开看是在小心翼翼地做三件难事：什么时候记、记什么、记了怎么不翻车。下面就按这三件事，看两家怎么下注。_

### 2.1 记你这件事，它撒在四个时间尺度上、还派不同的角色去做

_你可能以为它就是把你说的话存下来。其实「存」不是一个动作：从你还在说话时顺手记，到答完你之后派个后台分身补记，再到夜里趁机整理、甚至跨人同步——越往右越慢、越少人在场。横看一整行，看的是这家把「记你」摊成了 多少个机制、又有多少是默认就转的 。_
同一条学习线，两家沉淀出的 产物 也不止记忆： Hermes 的复盘被硬性要求「要主动」——每次都该产出至少一次技能更新，什么都不做算错过学习、不是中性结果；而且它把「用户偏好该写进 技能正文 、不只进记忆」讲得很明白。记忆记「你是谁」，技能记「为你这个人怎么做这一类任务」。

  ┌─ 制品 · 复盘被要求「要 ACTIVE」· 原文
  │ Be ACTIVE — most sessions produce at least one skill update, even if small. A pass that does nothing is a missed learning opportunity, not a neutral outcome.
  └─

  ┌─ 制品 · 记忆 vs 技能的分工原话
  │ Memory captures 'who the user is and what the current situation and state of your operations are'; skills capture 'how to do this class of task for this user'.
  └─

### 2.2 哪句话值得记一辈子？最反直觉的一条是——连你成功的选择也要记

_不是你说的每句都往长期记忆里塞。两家都有一套「该记 / 不该记」的判据——真正拉开认知的，是那条大多数人想不到的：只记你的纠正是不够的， 你点头认可的做法也得记 ，否则它会越用越畏手畏脚。_
  - 你是谁、你的规矩、你验证过的偏好
  - 你纠正它的走法（「别这么做」）
  - 连你 成功接受 的选择也要记——只记纠正，它会慢慢躲开你其实认可过的做法、变得过度谨慎
  - 能从代码 / 项目现状直接读出来的（架构、文件结构、谁改了什么）
  - 一周后就过时的：PR 号、任务进度、「Phase N 做完了」、「修好了 X」
  - 连你 明说 「把这个存下来」，若属上面两类它也会反问：这里面真正意外、非显然的点是什么？

  ┌─ 制品 · CC · 为什么「成功也要记」（原文）
  │ Record from failure AND success: if you only save corrections, you will avoid past mistakes but drift away from approaches the user has already validated, and may grow overly cautious.
  └─
另一头， Hermes 给「不该记」下了一条很硬的时间线判据： 一周后就会过时的事实，根本不该进记忆 ——那些该用历史检索去找，不该沉淀成长期记忆。

  ┌─ 制品 · Hermes · 一周会过时的别进记忆（原文）
  │ Do NOT save task progress, session outcomes, completed-work logs, or temporary TODO state... If a fact will be stale in a week, it does not belong in memory.
  └─

### 2.3 记进去这一步本身，会不会被人塞毒、或者卡住你回复

_自动写记忆有两个你想不到的坑：记忆文件可能被人动手脚（供应链、别的进程），成了往它脑子里 注入指令 的通道；反复整理记忆又可能陷进死循环，把该给你的回复 卡住 。 Hermes 在写入这一步筑了三道墙，其中两道直接带着 issue 号、是被真实线上事故逼出来的。_
写入 / 加载时逐条扫威胁模式，命中就在系统提示里换成 [BLOCKED] 占位，但保留原文让你能看见并删——不静默吞掉，免得瞒住攻击。
字数超预算要先合并再写；同一轮连败 3 次就停手、先把话回给你——记忆的副作用 绝不能卡住 给你的回复。
改写 / 删除前若发现磁盘上的记忆被外部手改过、对不上，先备份再 拒绝这次写 ，防止一次自动整理静默吞掉你手动加的内容。

  ┌─ 制品 · 投毒命中后的占位（原文）
  │ [BLOCKED: {filename} entry contained threat pattern(s)... Removed from system prompt; use memory(action=remove) to delete the original.]
  └─
CC 写入这侧更薄（best-effort，失败就静默、下次再来）——它把防线主要放在 使用记忆的时候 ：记忆天然会过期，用前先核实。至于「记好之后该不该无条件照办」，那是另一道闸，本章后面单说。

### 2.4 用户建模：单开一个子系统，还是揉进记忆？

_上面这条学习线，落到「你是谁」这一维时，两家分野最大——它决定了下一节「你能改它多深」的起点，别抹平。_
Hermes 把「你是谁」做成一等公民： 独立的用户档案 （USER.md，跟它记自己教训的那份记忆文件分开、两套预算、系统提示里分两块渲染）＋开机就 主动提议建档 （你有史以来第一条消息就触发，还带一道「先问你同不同意」的门）＋每轮请求前由外接组件现取现注一份画像。 （但要诚实标注：USER.md 内部，你手写的偏好与它自学的混在同一本、无来源标记。）
CC 没有独立画像文件，也 从不主动访谈 你——它把「记你偏好」和「记你反馈」当成通用记忆的两类揉进四类记忆里，每一轮再用一个小模型从所有记忆标题里 挑不超过 5 条 注入当前对话。（你手动造技能的流程里它确会访谈你，但那是你触发、且为造技能，不是为了给你这个人建档。）

## 03 · 不止让它懂你——你还能直接改它，改多深？

_记忆让它 懂 你（被动理解你是谁）；但你也能反过来 主动规定 它——从写一句指令，到教它一个可复用技能、设权限、挂钩子，一路到改它的源码。这条线不为「懂」，为的是让它的行为直接 顺 你，正好接上开篇那个「顺」的期望。关键看两家让你能走 多深 ——而这条光谱的尽头，就是本章反复要问的那句： 谁拥有代码 。_
Claude Code · 止于官方插槽
Hermes · 尽头是源码
_半秒看到的差别：两家都给你一排从浅到深的配置口， 但光谱尽头不同 —— CC 止于官方插槽（改不到源码）， Hermes 一路通到源码。这就是「谁拥有代码」的落点。 （词条悬停可见一句话解释。）_

## 04 · 懂了，不等于就该无条件照办

_这是最容易被忽略、也最值得单拎的一点：一个会自己攒记忆的 agent， 不只越用越懂你，也会越用越固执 ——把一次临时故障硬记成永久规则。所以两家都在「懂」和「顺」之间设了一道闸，正好呼应开篇那两个期望。姿态却相反。_

[Claude Code] Claude Code · 预防式：把「不信任记忆」焊进出厂设计
  系统提示里专门有一段召回纪律：记忆提到某文件就先确认它还在、要据此行动就 必须先核实 ；「记忆说 X 存在」不等于「X 现在存在」。夜间做梦（非默认）也内建「删掉被现场推翻的旧事实」。它把「记忆天然会过期」当默认前提来设计。

  ┌─ 制品 · 用前必核实 · 原文
  │ A memory that names a specific function, file, or flag is a claim that it existed *when the memory was written* ... "The memory says X exists" is not the same as "X exists now."
  └─

[Hermes] Hermes · 事后式：被真实投诉后才补的护栏
  后台复盘出过真实事故：把「这工具没装好」误记成「这工具坏了」，几个月后还拿这条错误结论拒绝干活—— 用户抱怨了 。整改两手：复盘指令加一段「不要捕获」黑名单，再加一道记忆写入的审批闸（默认关、可开成暂存待审）。

  ┌─ 制品 · 「不要捕获」黑名单（直击事故）· 原文
  │ Do NOT capture ... Negative claims about tools or features ('X tool is broken'). These harden into refusals the agent cites against itself for months after the actual problem was fixed.
  └─

Hermes 还有一条更细的纪律：把偏好 写成声明、不写成命令 ，防止「懂」硬化成机械的「顺」——这条是它独有的， CC 靠的是上面那套用前核实。

  ┌─ 制品 · Hermes 声明非命令的写法规范 · 原文
  │ 'User prefers concise responses'  ✓   —   'Always respond concisely'  ✗
  │ Imperative phrasing gets re-read as a directive in later sessions and can cause repeated work or override the user's current request.
  └─
在 Hermes 那侧，这道闸还露在 UI 上：它学到一条就在聊天里提示「💾 Memory updated」（默认开），你随时可以用 /memory 审查、撤回它学的每一条—— 学习不是黑箱 。 CC 的对应物是记忆本身就是你机器上可读可删的明文文件。

## 05 · 拼起来看：从「学你」的三个层次，照见它眼里的「用户是谁」

_把前面拆开讲的拼回一张表——但别平着读。它其实分 三层 ：记什么（内容）、怎么记（机制）、记了之后归谁·信不信（所有权与信任）。前两层是手段， 第三层才通向「它把你当谁」 。_

  【矩阵】 — | Claude Code | Hermes
  —— ① 记什么 内容——你交出去的那部分「你」 ——
  · 你是谁
      [Claude Code] user 类记忆里的一类（角色 / 目标 / 偏好 / 知识水平）。
      [Hermes] 单开一本 USER.md 画像。
  · 你的规矩
      [Claude Code] project 类记「项目为什么这么做」＋ feedback 类记「你纠正过的走法」。
      [Hermes] 塞进 MEMORY.md（环境事实 · 项目惯例 · 工具怪癖）。
  · 你的口味
      [Claude Code] feedback 类收你的风格反馈。
      [Hermes] 挫败信号列一等信号，还要求写进管这类任务的技能正文。
  · 你的边界 （软 / 硬分层）
      [Claude Code] 软边界进 feedback 记忆（建议性、 无牙 ）；硬授权走 settings 权限规则。
      [Hermes] 软边界进记忆（建议性、 无牙 ）；硬边界走 approvals 审批系统。
  —— ② 怎么记进来 学习机制——趁你不在时怎么运转 ——
  · 什么时候记 · 谁来记
      [Claude Code] 主 agent 即时写（ 默认开 ）＋ 回合末补写 / 会话笔记 / 夜间做梦（ 均特性门控 ）。
      [Hermes] 边聊边写 ＋ 每约 10 轮复盘分身（ 出厂默认开 ）＋ 技能自造。
  · 什么才值得记
      [Claude Code] 连你 成功接受 的做法也记（只记纠正会变得过度谨慎）。
      [Hermes] 一周会过时的 不记 （PR 号 / 进度交给历史检索）。
  · 记得安不安全
      [Claude Code] 写入 best-effort、失败静默；防线主要放在 使用时 （用前核实）。
      [Hermes] 写入侧 三道墙 ：投毒占位 / 防死循环 / 漂移拒写。
  —— ③ 记了之后归谁、信不信 所有权与信任——本章 verdict 的落点 ——
  · 记忆归谁 · 跟谁走
      [Claude Code] 你机器上的明文文件，但可经团队记忆同步 跨人共享 （组织维度）。
      [Hermes] 你的单机、单人、两份记忆文件， 不跨人 。
  · 懂了就照办吗
      [Claude Code] 预防式 ：用前必核实（默认常驻）、做梦删被推翻的（非默认）。
      [Hermes] 事后式 ：「不要捕获」黑名单 ＋ 记忆写入审批闸。

别停在"谁的表更全"。退一步看，上面第 ③ 层的每处设计，都在悄悄回答一个更根本的问题—— 在它眼里，「用户」到底是谁？ 答案就藏在它们「学你」的方式里。

> **【TL;DR / 核心洞察】**
> CC ：你是 组织里的一个专业角色 ——它把记忆做成 org 能治理的明文、还建了一套可跨组织成员共享的基础设施（可开启的能力，非默认全队直通），且从不给你单独建个人画像。它优化的是「一群人协作时的生产力」，落点是 多租户生产力工具 。
> Hermes ：你是 它专属服务的那一个人 ——开机就主动给你建档、单机单人不跨人，画像只属于你。它优化的是「长期陪一个人」，落点是 单人自托管陪伴 。 （这只是「与用户」这一维照见的判断；与「自己」「时间」两维合起来，才是完整答案。）

## 06 · 悬而未决 · 防夸大红线

【悬而未决 / 防夸大】
  - [默认口径要锚定] CC ：auto-memory 默认开（opt-out）、skillImprovement 默认关、skillify 仅内部用户开放； Hermes ：文中「默认开」一律指 出厂发行版 口径，裸库无配置键时兜底是关。
  - [CC 夜间做梦非默认] 夜间做梦 / KAIROS 助手日志是 特性门控·非默认 ，是「另一形态」而非出厂常态，别当主线支柱。
  - [CC 后台记忆通路多为特性门控] 除「顺手写」（auto-memory，出厂默认开）外，CC 的 会话笔记 / 回合末补写 / 每轮召回 ≤5 / 团队记忆同步 都在特性开关之后（GrowthBook flag，代码兜底关）——是可开启的能力，非无条件常态。尤其 团队记忆同步 （tengu_herring_clock）别写成「装上即全队共享」；文中「跨人共享」按 能力 / 架构 口径读：CC 建了这套 org 可共享的基础设施（＋团队上传专设密钥扫描）、且从不给你单独建个人画像，而 Hermes 单机结构上做不到跨人——这层对比与门控开没开无关，成立。
  - [边界维措辞] 软边界进记忆，但只是被注入的建议性文本、 没有强制拦截力 ——别写成「记忆能拦住它」。真正能阻断危险动作的是独立的权限 / 审批系统。
  - [Hermes 不是防火墙] USER.md 内部，你手写的与它自学的是 混同 的、无来源标记——别把「文件写权限隔离」夸成「Hermes 也有 CC 那种去重防火墙」。它的隔离是按「谁能写哪个文件」划界，不是「同层区分来源、显式压过学习」。
  - [不评优劣 · 时间切片] 本篇讲「懂用户」与「你改它」的 形态 ，不评孰优——取决于你要的是托管多租户产品，还是自托管的长期单人陪伴。切片：CC main / Hermes @daf4f1a7a。
