# 创建 Vue Element Plus 使用指南 Skill

## 1. 调研与数据收集
*   通过搜索和分析官网（`https://element-plus.org/en-US/component/overview`）获取所有组件的分类（如 Basic, Form, Data 等）。
*   提取每个组件对应的 URL Slug（如 `button`, `input-number`, `date-picker` 等）。
*   建立完整的组件分类映射表，包含组件名、分类和对应的文档 URL。

## 2. Skill 开发
*   创建目录 `.trae/skills/vue-element-plus/`。
*   编写 `SKILL.md`：
    *   **Frontmatter**: 定义 Skill 名称和触发场景（用户询问 Element Plus 组件使用时）。
    *   **组件索引**: 提供按分类排列的组件列表及文档链接。
    *   **使用规范**: 结合项目已有的 Tailwind 规范，指导如何在 Element Plus 组件上应用 Tailwind 类（如通过 `class` 或 `style` 覆盖样式）。
    *   **交互逻辑**: 规定在回答组件问题时，应优先参考映射表中的官方文档路径。

## 3. 验证与优化
*   验证生成的 Slug 是否准确（特别是多词组件）。
*   确保 Skill 能与现有的 `vue-tailwind-css` Skill 协同工作，保持风格统一。

确认后我将开始执行第一步：收集并整理组件列表。