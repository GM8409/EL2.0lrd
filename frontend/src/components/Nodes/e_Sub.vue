<!-- Nodes/AddNode.vue -->
<script setup lang="ts">
import { Handle, Position, type NodeProps } from '@vue-flow/core'

const props = defineProps<NodeProps>()

// 解构props中的data，方便模板使用（原代码中直接用data会报错，这里补充）
const { data, id } = props
</script>

<template>
  <div class="min-w-40 bg-white border-2 border-[#2196F3] rounded-lg p-3 shadow-[0_3px_10px_rgba(33,150,243,0.1)] font-['-apple-system','BlinkMacSystemFont','Segoe UI',Roboto,sans-serif] select-none relative">
    <div class="flex justify-between items-center mb-3 pb-2 border-b border-[#e0e0e0]">
      <span class="bg-[#2196F3] text-white px-2.5 py-1 rounded text-xs font-semibold">减法</span>
      <span class="text-[10px] text-[#757575]">{{ 'sub_'+id.slice(12, 16) }}</span>
    </div>
    
    <div class="flex flex-col gap-3">
      <div class="flex items-center gap-2.5 p-2.5 bg-[#E3F2FD] rounded-md">
        <div class="text-[20px] font-bold text-[#1976D2] w-9 h-9 flex items-center justify-center bg-white rounded-full">-{{ props.data.value }}</div>
        <div class="text-[13px] text-[#424242] flex-1">输入值减{{ props.data.value }}</div>
      </div>
      
      <div class="flex flex-col gap-1.5">
        <div v-if="data.input" class="flex justify-between text-[12px] px-2 py-1 bg-[#F5F5F5] rounded">
          <span class="text-[#616161] font-medium">输入:</span>
          <span class="text-[#424242] font-semibold">{{ data.input }}</span>
        </div>
        <div v-if="data.output" class="flex justify-between text-[12px] px-2 py-1 bg-[#F5F5F5] rounded">
          <span class="text-[#616161] font-medium">输出:</span>
          <span class="text-[#424242] font-semibold">{{ data.output }}</span>
        </div>
      </div>
    </div>
    
    <!-- 输入连接点（左侧） -->
    <Handle 
      type="target" 
      :position="Position.Left" 
      class="w-2.5 h-2.5 bg-white border-2 border-[#2196F3] left-1.25 top-1/2"
    />
    
    <!-- 输出连接点（右侧） -->
    <Handle 
      type="source" 
      :position="Position.Right" 
      class="w-2.5 h-2.5 bg-white border-2 border-[#2196F3] right-1.25 top-1/2"
    />
  </div>
</template>
