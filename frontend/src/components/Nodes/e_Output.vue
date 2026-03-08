<!-- Nodes/OutputNode.vue -->
<script setup lang="ts">
import { Handle, Position, type NodeProps } from '@vue-flow/core'

const props = defineProps<NodeProps>()
</script>

<template>
  <div class="output-node min-w-40 bg-white border-2 border-[#9C27B0] rounded-lg p-3 shadow-[0_3px_10px_rgba(156,39,176,0.1)] font-sans select-none relative">
    <div class="node-header flex justify-between items-center mb-3 pb-2 border-b border-[#e0e0e0]">
      <span class="node-type bg-[#9C27B0] text-white px-2.5 py-1 rounded text-xs font-semibold">输出</span>
      <span class="node-id text-[10px] text-[#757575]">{{ id.slice(0, 8) }}</span>
    </div>
    
    <div class="node-content flex flex-col gap-3">
      <div class="output-display p-3 bg-[#F3E5F5] rounded-md border border-dashed border-[#BA68C8]">
        <div class="output-label text-xs text-[#7B1FA2] mb-1.5 font-semibold">输出结果:</div>
        <div 
          class="output-value text-sm font-semibold text-[#424242] min-h-5 break-all"
          :class="{ 'text-[#9E9E9E] italic font-normal': props.data.value == '正在等待数据...' }"
        >
          {{ props.data.value }}
        </div>
      </div>
    </div>
    
    <!-- 输入连接点（左侧） -->
    <Handle 
      type="target" 
      :position="Position.Left" 
      class="node-handle w-2.5 h-2.5 bg-white border-2 border-[#9C27B0] left--1.25 top-1/2"
    />
  </div>
</template>

<style scoped>
/* 仅保留Tailwind难以直接实现的定位样式（scoped下对Handle组件的定位） */
:deep(.vue-flow__handle) {
  position: absolute;
}
</style>