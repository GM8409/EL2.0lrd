# Element Plus Collapse (折叠面板) 使用经验

## 核心组件
- `el-collapse`: 容器，通过 `v-model` 控制展开的面板。
- `el-collapse-item`: 子项，`title` 属性定义标题，`name` 定义唯一标识。

## 常用属性
- `accordion`: 是否手风琴模式（每次只展开一个面板）。
- `v-model`: 绑定当前展开面板的 `name`（数组或字符串，取决于是否为手风琴模式）。

## 参考代码
```vue
<template>
  <el-collapse v-model="activeNames" accordion @change="handleChange">
    <el-collapse-item title="一致性 Consistency" name="1">
      <div>与现实生活一致：与现实生活的流程、逻辑保持一致，遵循用户习惯的语言和概念。</div>
    </el-collapse-item>
    <el-collapse-item title="反馈 Feedback" name="2">
      <div>控制反馈：通过界面样式和交互效果让用户清晰的感知自己的操作。</div>
    </el-collapse-item>
  </el-collapse>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
const activeNames = ref(['1'])
const handleChange = (val: string[]) => {
  console.log(val)
}
</script>
```

## 注意事项
- 内容区域默认有内边距，可以通过覆盖 CSS 或在内部嵌套容器调整。
- 如果需要自定义标题，可以使用 `title` 具名插槽。
