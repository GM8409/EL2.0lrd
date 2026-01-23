<!-- Nodes/StartNode.vue -->
<script setup lang="ts">
import { Handle, Position,type NodeProps } from '@vue-flow/core'

const props = defineProps<NodeProps>()

</script>

<template>
  <div class="start-node">
    <div class="node-header">
      <span class="node-type">开始</span>
      <span class="node-id">{{ id.slice(0, 8) }}</span>
    </div>
    
    <div class="node-content">
      <div class="input-container">
        <label>输入数据:</label>
        <input
          v-model="props.data.value"
          type="text"
          class="value-input"
          placeholder="请输入..."
        />
      </div>
      <div class="current-value" v-if="data.value">
        当前值: <strong>{{ props.data }}</strong>
      </div>
    </div>
    
    <!-- 输出连接点（右侧） -->
    <Handle 
      type="source" 
      :position="Position.Right" 
      class="node-handle"
    />
  </div>
</template>

<style scoped>
.start-node {
  min-width: 160px;
  background: white;
  border: 2px solid #4CAF50;
  border-radius: 8px;
  padding: 12px;
  box-shadow: 0 3px 10px rgba(76, 175, 80, 0.1);
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
  background: #4CAF50;
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
  gap: 10px;
}

.input-container {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.input-container label {
  font-size: 12px;
  color: #424242;
  font-weight: 500;
}

.value-input {
  padding: 6px 10px;
  border: 1px solid #BDBDBD;
  border-radius: 4px;
  font-size: 13px;
  outline: none;
}

.value-input:focus {
  border-color: #4CAF50;
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
}

.current-value {
  font-size: 12px;
  color: #616161;
  padding: 6px 10px;
  background: #F5F5F5;
  border-radius: 4px;
}

.node-handle {
  width: 10px;
  height: 10px;
  background: white;
  border: 2px solid #4CAF50;
  right: -5px;
  top: 50%;
}
</style>