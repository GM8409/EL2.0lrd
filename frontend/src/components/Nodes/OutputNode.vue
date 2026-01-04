<!-- OutputNode.vue -->
<script setup lang="ts">
import { Handle, Position, useNode,type NodeProps } from '@vue-flow/core'
import { ref, computed, watch } from 'vue'

const props = defineProps<NodeProps>()

const { node } = useNode()
const isEditing = ref(false)
const inputText = ref(props.data.label || '')
const inputRef = ref<HTMLInputElement>()

const nodeClasses = computed(() => ({
  'output-node': true,
  'output-node--selected': node.selected,
  'output-node--editing': isEditing.value,
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
    node.data.label = inputText.value.trim() || '输出'
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
    <div class="output-node__badge">
      输出
    </div>

    <!-- 内容区域 -->
    <div class="output-node__content">
      <!-- 可编辑区域 -->
      <div class="output-node__label">
        <!-- 编辑模式 -->
        <input
          v-if="isEditing"
          ref="inputRef"
          v-model="inputText"
          type="text"
          class="output-node__input"
          @blur="saveEditing"
          @keydown="handleKeydown"
          @mousedown.stop
          @click.stop
          placeholder="输出名称"
        />
        
        <!-- 查看模式 -->
        <div 
          v-else
          class="output-node__text"
          @click="startEditing"
          @dblclick="startEditing"
        >
          {{ inputText || '输出' }}
        </div>
      </div>
      
      <!-- 右侧装饰线 -->
      <div class="output-node__decorator"></div>
    </div>

    <!-- 输入连接点（左侧） -->
    <Handle 
      type="target" 
      :position="Position.Left" 
      class="output-node__handle"
    />
    
    <!-- 可选输出连接点 -->
    <Handle 
      v-if="data.allowOutput"
      type="source" 
      :position="Position.Bottom" 
      class="output-node__handle output-node__handle--source"
    />
  </div>
</template>

<style scoped>
.output-node {
  --primary-color: #10b981;
  --primary-light: #ecfdf5;
  --edit-color: #059669;
  --border-color: #d1fae5;
  --text-color: #374151;
  
  position: relative;
  min-width: 120px;
  max-width: 200px;
  background: white;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 16px 12px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
  transition: all 0.2s ease;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  cursor: grab;
  user-select: none;
}

.output-node:hover {
  border-color: var(--primary-color);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.12);
}

.output-node--selected {
  border-color: var(--primary-color);
  border-width: 2px;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.18);
}

.output-node--editing {
  border-color: var(--edit-color);
  box-shadow: 0 4px 12px rgba(5, 150, 105, 0.25);
}

.output-node__badge {
  position: absolute;
  top: -8px;
  left: 8px;
  background: var(--primary-color);
  color: white;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 10px;
  font-weight: 500;
  letter-spacing: 0.5px;
}

.output-node__content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.output-node__decorator {
  width: 4px;
  height: 24px;
  background: var(--primary-color);
  border-radius: 2px;
  opacity: 0.8;
}

.output-node__label {
  flex: 1;
}

.output-node__text {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-color);
  padding: 6px 0;
  cursor: pointer;
  transition: color 0.2s;
  min-height: 28px;
  line-height: 16px;
}

.output-node__text:hover {
  color: var(--primary-color);
}

.output-node__input {
  width: 100%;
  padding: 6px 8px;
  font-size: 14px;
  font-weight: 500;
  color: var(--text-color);
  background: white;
  border: 1px solid var(--primary-color);
  border-radius: 4px;
  outline: none;
  box-sizing: border-box;
  font-family: inherit;
}

.output-node__input:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.2);
}

.output-node__handle {
  width: 10px;
  height: 10px;
  background: white;
  border: 2px solid var(--primary-color);
  transition: all 0.2s;
  left: -5px;
  top: 50%;
  transform: translateY(-50%);
  cursor: crosshair;
}

.output-node__handle:hover {
  background: var(--primary-color);
  transform: translateY(-50%) scale(1.2);
}

.output-node__handle--source {
  left: 50%;
  top: auto;
  bottom: -5px;
  transform: translateX(-50%);
}

.output-node__handle--source:hover {
  background: var(--primary-color);
  transform: translateX(-50%) scale(1.2);
}

.output-node--editing .output-node__handle {
  opacity: 0.5;
  pointer-events: none;
}
</style>