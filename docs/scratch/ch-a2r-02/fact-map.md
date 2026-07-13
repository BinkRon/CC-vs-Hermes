# CH-A2R-02 环境章 · 综合归位事实图（渲染前的单一真相）

> 切片：CC=`claude-code-main`（本地树·无版本标识）｜Hermes=`hermes-agent-8e734810`@`8e734810d`（2026-07-08，比旧基线新 4778 commit）。
> 源：`research-cc.json`（17 机制+A/B/D 全答）/ `research-hermes.json`（19 机制+12 问全答）。
> 仪器：损失类型（5 行）× 防线阶段（3 列）。**纪律：先落格、misfit 原样陈列、空格报告为空——不为矩阵漂亮压事实。**

---

## 一、矩阵落格（默认形态，非门控/非 opt-in 优先）

### Claude Code

| 损失类型＼阶段 | 事前（拦） | 事中（隔） | 事后（兜） |
|---|---|---|---|
| 1 资产毁损 | 四档模式弹窗；Bash 删危险路径**软拦**（bypass 可放行）；PowerShell 删**硬拒**（不对称） | 沙箱（**默认关**）；worktree（opt-in） | ★文件检查点/rewind（**交互默认开**·仅覆盖结构化编辑工具改的文件·bash 删除不入） |
| 2 机密外泄 | 近空白：仅 teamMemSecretGuard（**feature-flag 门控**·只堵写团队记忆） | 沙箱网络闸（**默认关**） | 空 |
| 3 失控·二阶 | ★**文件写入安全检查·bypass-immune**（.git/.claude/shell 启动/IDE 配置·连全放行也拦）；组织级 killswitch 远程锁 bypass 档 | — | 空 |
| 4 机器失能 | 删根落入 Bash 软拦/PS 硬拒；关机/fork 炸弹**无专项** | 空 | 空 |
| 5 外部世界后果 | 无硬闸：force push 仅信息提示、publish 靠用户自配规则、"不主动 push"是 prompt 纪律非闸门 | 空 | 空（已推/已发不可撤） |

**贯穿所有格**：allow/deny/ask 规则、被拒后训诫（DENIAL_WORKAROUND_GUIDANCE）。
**misfit**：破坏性命令提示语＝零强制力 UI 文案（非防线）；harness 内部目录仓外静默可写＝放行非防线（caveat）；Auto 分类器＝多重门控默认不可达（勿当产品）。

### Hermes

| 损失类型＼阶段 | 事前（拦） | 事中（隔） | 事后（兜） |
|---|---|---|---|
| 1 资产毁损 | ★**硬禁地板**（删根/删系统目录/删家目录·无条件·yolo 压不过）；危险模式软清单（yolo 可绕）；文件陈旧守卫 | 容器后端整链跳过（结构性·默认 local 不跳）；原子替换（崩溃安全非备份） | 文件快照/rollback（**默认关**·v2 从 True 翻 False·仅工作目录文件） |
| 2 机密外泄 | Tirith 内容扫描（默认开·**默认 fail-open**）；读密钥文件 terminal 侧**无拦** | ★**凭据剥离**（**默认开**·多面·GATEWAY 令牌无条件剥）；输出脱敏（展示层） | 空 |
| 3 失控·二阶 | sudo 猜密码地板（无条件）；改自己 config／杀网关在**软清单**（yolo 可绕）；Skills Guard／MCP 配置校验（spawn 期·review aid） | — | 空 |
| 4 机器失能 | ★**硬禁地板**（mkfs/dd 裸设备/fork 炸弹/kill -1/shutdown 类·无条件）；防自尽（**软清单**·yolo 可绕） | 空 | 空 |
| 5 外部世界后果 | 近空：force push 被 shell 模式偶然覆盖；发消息/发邮件/publish**零审批**；外部面 allowlist 只管入口不管出口 | 空 | 空 |

**贯穿**：审批模式（默认 manual）、被拒/超时训诫（"Silence is not consent"）、cron 无人默认拒。
**misfit/缺口**：D1 诚实漏洞＝非交互非网关非 cron 无人会话对软危险命令**静默 fail-open 放行**（主路径连 warning 都不打）；smart 审批＝opt-in；外部面授权闸＝入口非出口。

---

## 二、三条被数据改写的论断（旧稿/我的假设 → 修正）

### R1. 「事后兜底整个外包给 git」——不成立，改为「两家都有原生撤销、但都只兜自己动笔改的文件、都刻意边缘化」
- CC：文件检查点/rewind，**交互默认开**，但只覆盖结构化编辑工具（FileEdit/Write/Notebook）+ 模拟 edit 的 `sed -i`；**任意 bash 破坏性命令（rm/mv/dd/重定向/git）不进检查点**；只管文件、不管会话/已推 commit/外发。
- Hermes：文件快照/rollback（影子 git 库），**默认关**（v2 把默认 True→False，注释"most users never use /rollback"）；只覆盖工作目录内文件。
- 修正论断：**事后列不是空的，是"半格对半格"**——两家都只给"自己结构化改动的文件"做了撤销，对真正的灾难面（bash 删除、外泄、机器失能、已推/已发）事后都只能靠 git/OS/厂商。差异：**CC 把撤销做成默认体验，Hermes 做成 opt-in**（因为"多数人从不用"）。

### R2. ★「生存前提」假设——被证伪，换成「两家用两套不同判据划绝对地板」（本轮最重要的诚实修正）
- 我上一轮假设：CC 地板护治理层(row3)、Hermes 地板护机器(row4)，各护"自己治理模式的生存前提"。
- **数据证伪了统一解释**：
  - Hermes 的地板判据是**纯粹的可逆性**——代码注释写死"硬地板只收 no recovery path 的；可恢复但代价大的（git reset --hard、rm -rf /tmp/x、curl|sh）留软清单交给 yolo"。连"杀自己网关"都因为"可重来（terminate agents mid-work，重启即可）"而留在软清单——**哪怕它伤及"机器活着"这个所谓生存前提**。所以 Hermes 不是按"护生存前提"设计，是按"可不可逆"。
  - CC 的地板判据是**是否触及治理层**——bypass-immune 的是 .git/.claude/shell/IDE 配置；而可逆性上最该硬拒的 `rm -rf /`（不可逆）反因走 Bash 只是软拦、bypass 能放行（A2 反例）。CC 的判据**不是**可逆性，是"动没动管着 agent 的那层"。
- 修正论断（更锋利、有 file:line 铁证、且不需要我编的中间假设）：**两家的绝对地板用了两套不同判据——Hermes 按"物理可不可挽回"（护机器），CC 按"动没动治理层"（护规则本身）。一个防物理不可逆，一个防元级失控。** 各自把对方设成地板的那类，恰好留在自己的软层（旧稿"各自把对方留软层的升格成硬地板"的观察成立，但要用"两套判据"来解释，别用"生存前提"）。
- ⚠️ 完整性门要点：这是我"为干净故事编中间假设"偏差的现行案例。研究员 A1c/A2 定向题救回来了。渲染时**不得**复活"生存前提"叙事。

### R3. 硬拒不对称坐实，但地基换了
- 「PowerShell 删除才真硬拒、Bash 删根只是 bypass 可放行的软拦」属实；全仓无硬编码危险命令黑名单。
- 修正：CC 护栏强度**不按可逆性排，按"走哪个 shell／碰没碰治理层"排**——这是护栏不一致（PS/Bash 不对称），不是设计美学。写章要如实呈现这处不对称，别美化成"CC 按可逆性设计"。

---

## 三、两个共同盲区（"空即发现"·对 PM 有产品含义）

### B1. 行 5「外部世界后果」两家事前近乎真空——环境治理是**机器中心**的
- 强推共享分支、发消息/发邮件、发布包、MCP 对外调用——两家事前几乎都无硬闸。
- CC：force push 仅信息提示、publish 靠用户自配、"不主动 push"是 prompt 纪律。Hermes：出口发消息零审批、publish 无拦、只 force push 被 shell 模式偶然覆盖。
- 产品含义：**两家都把防线画在"别毁了这台机器/这个仓库"，对"祸落在别人头上"几乎不设防。** 环境治理 ≈ 本机资产治理，社会性/外部后果不在射程。

### B2. 工具面覆盖缺口——护栏只长在「shell 命令」这一个面
- CC：MCP/自定义工具 passthrough，完全不过环境侧闸（危险删除/文件保护/沙箱只覆盖 Bash/PowerShell/文件编辑）。
- Hermes：治理几乎只在 shell 字符串；MCP/发消息/发布靠一个**默认关**的通用钩子兜、仓内无自带插件启用＝实际无人接。
- 产品含义：**一个用 MCP 工具删数据/联网外传的 agent，绕开两家几乎全部环境护栏。** 两家惊人一致的结构性盲区。

---

## 四、两张王牌（保真·逐字制品已重取）

- **§被拒后训诫双语并排**（矩阵"事前·贯穿"格里最有趣的一条——唯一对着**行为者**而非行为的闸）：
  - CC `DENIAL_WORKAROUND_GUIDANCE`（messages.ts:226）：允许换等价工具、禁止恶意绕过意图、真需要就 STOP 问人。
  - Hermes（approval.py:2839·issue #24912）：`Do NOT retry / do NOT rephrase / do NOT attempt the same outcome via a different command … Silence is not consent.`（本切片比旧版更强，新增"换命令达成同一效果"堵口）。
- **诚实度自白**（长在 row2 机密外泄）：Hermes 主动剥密钥（默认开）却在 SECURITY.md §2.3 亲口"This reduces casual exfiltration. **It is not containment.**"；§2.2"The only security boundary … is the operating system. Nothing inside the agent process constitutes containment"；§2.4"They are useful. They are not boundaries."——对照 CC row2 基本敞开（赌你在可信仓库、你在场）。**诚实度是风险归属的下游**：越是你自担（Hermes 无 bug bounty、后果归运维），越被逼坦白真边界在哪。

---

## 五、保留的 caveat（防「默认→绝对」·完整性门清单）

- CC 沙箱**默认关**、开沙箱反而命令免逐条问（换范式非加层）｜Hermes 后端**默认 local 裸主机**、隔离全 opt-in。
- Hermes D1 诚实漏洞仍在且主路径更安静（非 cron 无人静默放行软危险命令）——不得被"无人更保守"压掉；cron 无人默认拒与之不一致，两个无人路径处理不同。
- Tirith 默认 fail-open、smart/off opt-in——硬禁地板是全篇唯一无条件机制。
- CC Auto 分类器 ant-only/门控、teamMemSecretGuard feature-flag、harness 仓外静默写——均非通用产品面。
- 沙箱/worktree 隔离两家默认都不开，子代理不自动隔离。
- 不评优劣；时间切片（CC main / Hermes @8e734810d）。

---

## 六、脊与结构（渲染前待 PM 确认）

**问题定义**：兜底不是让模型更聪明，是让「模型不聪明」不致命。机制惊人趋同＝弹簧（下限设计被"可错性"这个物理事实收敛，不由品味决定），不是内容。
**脊**：环境是"祸真落在某人头上"的一侧 → 机制趋同不是分野 → 真分野是**风险归谁**（矩阵事后列＋责任归属：厂商兜底 vs 你自担）＋由此逼出的**多诚实**（row2 剥密钥却否认是墙）。
**在场**只作"为什么是你自担"的上游成因出现一句，**不点名、不宣布交棒综合②**（守 campaign 铁律）。
**结构**（不套六拍·环境章自己的形状）：①问题（让渡行动权的下限）→ ②矩阵总览（趋同做弹簧·亮"事中隔离默认空/事后半格"两个反直觉）→ ③深潜A 两道地板两套判据（R2·王牌1训诫可并此）→ ④深潜B 外泄行的诚实反差（王牌2）→ ⑤两个共同盲区（外部后果/工具面）→ verdict 风险归属＋多诚实 → caveat 墙。
**DSN-04 开篇范式**：论断式 H1（呼应侧栏 label）＋ TL;DR 绿标 ＋ `00·问题` house 框。
