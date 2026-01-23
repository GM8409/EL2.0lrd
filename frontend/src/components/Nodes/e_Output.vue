<!-- Nodes/OutputNode.vue -->
<script setup lang="ts">
import { Handle, Position,type NodeProps } from '@vue-flow/core'

const props = defineProps<NodeProps>()

</script>

<template>
  <div class="output-node">
    <div class="node-header">
      <span class="node-type">输出</span>
      <span class="node-id">{{ id.slice(0, 8) }}</span>
    </div>
    
    <div class="node-content">
      <div class="output-display">
        <div class="output-label">输出结果:</div>
        <div class="output-value" :class="{ 'empty': props.data.value == '正在等待数据...' }">
          {{ props.data.value }}
        </div>
      </div>
      
      
    </div>
    
    <!-- 输入连接点（左侧） -->
    <Handle 
      type="target" 
      :position="Position.Left" 
      class="node-handle"
    />
  </div>
</template>

<style scoped>
.output-node {
  min-width: 160px;
  background: white;
  border: 2px solid #9C27B0;
  border-radius: 8px;
  padding: 12px;
  box-shadow: 0 3px 10px rgba(156, 39, 176, 0.1);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  user-select: none;
}

.node-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid #e0e0e0;
}

.node-type {
  background: #9C27B0;
  color: white;
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
}

.node-id {
  font-size: 10px;
  color: #757575;
}

.node-content {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.output-display {
  padding: 12px;
  background: #F3E5F5;
  border-radius: 6px;
  border: 1px dashed #BA68C8;
}

.output-label {
  font-size: 12px;
  color: #7B1FA2;
  margin-bottom: 6px;
  font-weight: 600;
}

.output-value {
  font-size: 14px;
  font-weight: 600;
  color: #424242;
  min-height: 20px;
  word-break: break-all;
}

.output-value.empty {
  color: #9E9E9E;
  font-style: italic;
  font-weight: normal;
}

.node-info {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  font-size: 11px;
  padding: 4px 8px;
  background: #F5F5F5;
  border-radius: 4px;
}

.info-label {
  color: #616161;
}

.info-value {
  color: #424242;
  font-weight: 500;
}

.node-handle {
  width: 10px;
  height: 10px;
  background: white;
  border: 2px solid #9C27B0;
  left: -5px;
  top: 50%;
}
</style>