<!-- InputNode.vue -->
<script setup lang="ts">
import { Handle, Position, useNode,type NodeProps } from '@vue-flow/core'
import { ref, computed, watch } from 'vue'


const props = defineProps<NodeProps>()

const { node } = useNode()
const isEditing = ref(false)
const inputText = ref(props.data.label || '')
const inputRef = ref<HTMLInputElement>()

const nodeClasses = computed(() => ({
  'input-node': true,
  'input-node--selected': node.selected,
  'input-node--editing': isEditing.value,
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
    <div class="input-node__badge">
      输入
    </div>

    <!-- 内容区域 -->
    <div class="input-node__content">
      <!-- 左侧装饰线 -->
      <div class="input-node__decorator"></div>
      
      <!-- 可编辑区域 -->
      <div class="input-node__label">
        <!-- 编辑模式 -->
        <input
          v-if="isEditing"
          ref="inputRef"
          v-model="inputText"
          type="text"
          class="input-node__input"
          @blur="saveEditing"
          @keydown="handleKeydown"
          @mousedown.stop
          @click.stop
          placeholder="输入名称"
        />
        
        <!-- 查看模式 -->
        <div 
          v-else
          class="input-node__text"
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
      class="input-node__handle"
    />
    
    <!-- 可选输入连接点 -->
    <Handle 
      v-if="data.allowInput"
      type="target" 
      :position="Position.Top" 
      class="input-node__handle input-node__handle--target"
    />
  </div>
</template>

<style scoped>
.input-node {
  --primary-color: #3b82f6;
  --primary-light: #eff6ff;
  --edit-color: #3b82f6;
  --border-color: #e5e7eb;
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

.input-node:hover {
  border-color: var(--primary-color);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.12);
}

.input-node--selected {
  border-color: var(--primary-color);
  border-width: 2px;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.18);
}

.input-node--editing {
  border-color: var(--edit-color);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.25);
}

.input-node__badge {
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

.input-node__content {
  display: flex;
  align-items: center;
  gap: 8px;
}

.input-node__decorator {
  width: 4px;
  height: 24px;
  background: var(--primary-color);
  border-radius: 2px;
  opacity: 0.8;
}

.input-node__label {
  flex: 1;
  margin-top: 10px;
}

.input-node__text {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-color);
  cursor: pointer;
  transition: color 0.2s;
  min-height: 28px;
  line-height: 16px;
}

.input-node__text:hover {
  color: var(--primary-color);
}

.input-node__input {
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

.input-node__input:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
}

.input-node__handle {
  width: 10px;
  height: 10px;
  background: white;
  border: 2px solid var(--primary-color);
  transition: all 0.2s;
  right: -5px;
  top: 50%;
  transform: translateY(-50%);
  cursor: crosshair;
}

.input-node__handle:hover {
  background: var(--primary-color);
  transform: translateY(-50%) scale(1.2);
}

.input-node__handle--target {
  left: 50%;
  top: -5px;
  transform: translateX(-50%);
}

.input-node__handle--target:hover {
  background: var(--primary-color);
  transform: translateX(-50%) scale(1.2);
}

.input-node--editing .input-node__handle {
  opacity: 0.5;
  pointer-events: none;
}
</style>