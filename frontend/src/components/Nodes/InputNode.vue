<!-- InputNode.vue -->
<script setup lang="ts">
import { Handle, Position, useNode, type NodeProps } from '@vue-flow/core'
import { ref, computed, watch } from 'vue'

const props = defineProps<NodeProps>()

const { node } = useNode()
const isEditing = ref(false)
const inputText = ref(props.data.label || '')
const inputRef = ref<HTMLInputElement>()

const nodeClasses = computed(() => ({
  'min-w-[120px] max-w-[200px] bg-white border border-[#e5e7eb] rounded-lg p-4 shadow-[0_2px_6px_rgba(0,0,0,0.06)] transition-all duration-200 font-sans cursor-grab select-none relative': true,
  'border-[#3b82f6] border-2 shadow-[0_4px_12px_rgba(59,130,246,0.18)]': node.selected,
  'border-[#3b82f6] shadow-[0_4px_12px_rgba(59,130,246,0.25)]': isEditing.value,
  'hover:border-[#3b82f6] hover:shadow-[0_4px_12px_rgba(59,130,246,0.12)]': !isEditing.value && !node.selected,
}))

watch(() => props.data.label, (newLabel) => {
  if (!isEditing.value) {
    inputText.value = newLabel || ''
  }
})

function startEditing(event: Event) {
  event.stopPropagation()
  isEditing.value = true
  setTimeout(() => {
    inputRef.value?.focus()
    inputRef.value?.select()
  }, 10)
}

function saveEditing() {
  isEditing.value = false
  if (node.data) {
    node.data.label = inputText.value.trim() || '输入'
  }
}

function handleKeydown(event: KeyboardEvent) {
  if (event.key === 'Enter') {
    saveEditing()
  } else if (event.key === 'Escape') {
    isEditing.value = false
    inputText.value = props.data.label || ''
  }
}

function handleNodeClick(event: Event) {
  event.stopPropagation()
}
</script>

<template>
  <div 
    :class="nodeClasses" 
    @click="handleNodeClick"
  >
    <!-- 左上角标识 -->
    <div class="absolute top--2 left-2 bg-[#3b82f6] text-white px-2 py-0.5 rounded text-[10px] font-medium tracking-[0.5px]">
      输入
    </div>

    <!-- 内容区域 -->
    <div class="flex items-center gap-2">
      <!-- 左侧装饰线 -->
      <div class="w-1 h-6 bg-[#3b82f6] rounded-sm opacity-80"></div>
      
      <!-- 可编辑区域 -->
      <div class="flex-1 mt-2.5">
        <!-- 编辑模式 -->
        <input
          v-if="isEditing"
          ref="inputRef"
          v-model="inputText"
          type="text"
          class="w-full px-2 py-1.5 text-sm font-medium text-[#374151] bg-white border border-[#3b82f6] rounded outline-none box-border focus:shadow-[0_0_0_2px_rgba(59,130,246,0.2)]"
          @blur="saveEditing"
          @keydown="handleKeydown"
          @mousedown.stop
          @click.stop
          placeholder="输入名称"
        />
        
        <!-- 查看模式 -->
        <div 
          v-else
          class="text-sm font-medium text-[#374151] cursor-pointer transition-colors hover:text-[#3b82f6] min-h-7 leading-4"
          @click="startEditing"
          @dblclick="startEditing"
        >
          {{ inputText || '输入' }}
        </div>
      </div>
    </div>

    <!-- 输出连接点（右侧） -->
    <Handle 
      type="source" 
      :position="Position.Right" 
      class="w-2.5 h-2.5 bg-white border-2 border-[#3b82f6] transition-all duration-200 right--1.25 top-1/2 -translate-y-1/2 cursor-crosshair hover:bg-[#3b82f6] hover:scale-120"
      :style="{ opacity: isEditing ? 0.5 : 1, pointerEvents: isEditing ? 'none' : 'auto' }"
    />
    
    <!-- 可选输入连接点 -->
    <Handle 
      v-if="data.allowInput"
      type="target" 
      :position="Position.Top" 
      class="w-2.5 h-2.5 bg-white border-2 border-[#3b82f6] transition-all duration-200 left-1/2 top--1.25 -translate-x-1/2 cursor-crosshair hover:bg-[#3b82f6] hover:scale-120"
      :style="{ opacity: isEditing ? 0.5 : 1, pointerEvents: isEditing ? 'none' : 'auto' }"
    />
  </div>
</template>

<style scoped>
/* 仅保留Tailwind难以直接实现的定位样式（scoped下对Handle组件的定位） */
/* 其余样式已全部迁移到template和computed的class中 */
:deep(.vue-flow__handle) {
  position: absolute;
}
</style>