<script setup lang="ts">
import { Handle, Position, type NodeProps } from '@vue-flow/core'

const props = defineProps<NodeProps>()

// 解构props中的data和id，避免模板中上下文报错
const { data, id } = props
</script>

<template>
  <div class="min-w-40 bg-white border-2 border-[#4CAF50] rounded-lg p-3 shadow-[0_3px_10px_rgba(76,175,80,0.1)] font-['-apple-system','BlinkMacSystemFont','Segoe UI',Roboto,sans-serif] select-none relative">
    <div class="flex justify-between items-center mb-3 pb-2 border-b border-[#e0e0e0]">
      <span class="bg-[#4CAF50] text-white px-2.5 py-1 rounded text-xs font-semibold">开始</span>
      <span class="text-[10px] text-[#757575]">{{ id.slice(0, 8) }}</span>
    </div>
    
    <div class="flex flex-col gap-2.5">
      <div class="flex flex-col gap-1.5">
        <label class="text-[12px] text-[#424242] font-medium">输入数据:</label>
        <input
          v-model="props.data.value"
          type="text"
          class="px-2.5 py-1.5 border border-[#BDBDBD] rounded text-[13px] outline-none focus:border-[#4CAF50] focus:shadow-[0_0_0_2px_rgba(76,175,80,0.2)]"
          placeholder="请输入..."
        />
      </div>
      <div v-if="data.value" class="text-[12px] text-[#616161] px-2.5 py-1.5 bg-[#F5F5F5] rounded">
        当前值: <strong>{{ props.data.value }}</strong>
      </div>
    </div>
    
    <!-- 输出连接点（右侧） -->
    <Handle 
      type="source" 
      :position="Position.Right" 
      class="w-2.5 h-2.5 bg-white border-2 border-[#4CAF50] absolute right--2.5 top-1/2 -translate-y-1/2"
    />
  </div>
</template>

<!-- 移除所有scoped样式和类选择器 -->