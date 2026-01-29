# Element Plus Tooltip (文字提示) 使用经验

## 核心组件
- `el-tooltip`: 常用于展示按钮或图标的辅助文字。

## 常用属性
- `content`: 提示内容。
- `placement`: 提示出现位置（如 `top`, `bottom`, `left`, `right`）。
- `effect`: 主题，可选 `dark` (默认) 或 `light`。

## 参考代码
```vue
<template>
  <el-tooltip
    class="box-item"
    effect="dark"
    content="Right Center prompts info"
    placement="right"
  >
    <el-button>right-start</el-button>
  </el-tooltip>
</template>
```

## 注意事项
- 包裹的内容必须是单一根元素。
- 如果包裹的是自定义组件，确保该组件能转发原生事件。
