# 过程文档（findings）

每篇一个自包含 HTML，随调研累积。规则见根目录 `contract.md`。

**命名约定**（数字前缀 = 调研顺序，`inside`=轴一 Loop之内 / `outside`=轴二 Loop之外）：
- 轴一：`01-inside-control-loop.html`（✅）、`02-inside-input.html`、`03-inside-output.html`
- 轴一综合：`SYN-inside-story.html`（「一个 Loop 是怎么设计的」）
- 轴二：`04-outside-time-trigger.html`、`05-outside-user.html`（Loop 与用户，取代旧 `05-outside-programmability` + `05b-outside-user-adaptation`，已归档 `assets/`）、`06-outside-environment.html`、`07-outside-multiagent.html`
- 轴二综合：`SYN-outside-story.html`（「Loop 之外是怎么设计的」）
- 设计系统（勿动内容，仅复用其 style/script）：`_design-system.html`

**每篇 HTML 的骨架**（2026-07-04 起为**默认可偏离**：叙事顺序由该章视觉脚本决定，按论证逻辑排、不按槽位排——详见 `contract.md` 契约 3 + `docs/design-principles.md` §4；排版/可视化遵循 design-principles 三档重量与设计门）：
1. 结论摘要（先给判断）
2. 问题（用具体场景故事讲，产品语言）
3. 核心机制（纵向 `flowchart TD`；对比用 `.flow2` 两列等高）
4. 深潜 × 1–3（原"Hero"；名额随分歧密度、形式匹配机制形状、必须含真实制品——三条规则见契约 3）
5. 对比（`.compare` 双栏 / `.matrix` 矩阵 + `.verdict` 为何不同）
6. 悬而未决
7. 页脚 `file:line` 溯源（正文不出现代码；真实文案/数字是证据、不算代码，见契约 1 附注）
