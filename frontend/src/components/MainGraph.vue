<!-- 父组件 -->
<template>
  <div class="h-screen flex flex-col">
    <!-- 工作流导航栏 -->
    <WorkflowNavbar 
      workflow-name="我的工作流" 
      workflow-version="v1.0" 
      :workflow-status="workflowStatus"
      @toggle-edit="toggleEditMode"
      @save="saveWorkflow"
      @run="runWorkflow"
      @stop="stopWorkflow"
      @reset="resetWorkflow"
      @export="exportWorkflow"
      @import="importWorkflow"
      @duplicate="duplicateWorkflow"
      @delete="deleteWorkflow"
    />
    
    <!-- 工作流画布区域 -->
    <div class="flex-1 flex flex-row-reverse h-full">
      <!-- Vue Flow 画布 -->
      <VueFlow
      class="flex-1"
        v-model:nodes="nodes"
        v-model:edges="edges"
        id="my-flow"
        @connect="nodeManager.addEdge($event)"
        :node-types="nodeTypes"
      >
        <Background :gap="15" />
      </VueFlow>
      <!-- 节点面板 -->
      <NodePanel 
    
        @toggleDebugPanel="isDebugPanelOpen = !isDebugPanelOpen"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { provide, ref } from 'vue'
import { VueFlow, useVueFlow, type Node, type Edge } from '@vue-flow/core'
import { Background } from '@vue-flow/background'
import NodePanel from './Workflow/NodePanel.vue'
import WorkflowNavbar from './Workflow/WorkflowNavbar.vue'
import { nodeTypes, NodeManager } from '../tools/nodeManager'

const isDebugPanelOpen = ref(false)
const workflowStatus = ref('idle') // idle, running, completed, error, editing
const isEditMode = ref(false)

// Vue Flow 实例
const flow = useVueFlow('my-flow')
const nodes = ref<Node[]>([])
const edges = ref<Edge[]>([])

const nodeManager = new NodeManager(flow)

provide('node_manager', nodeManager)

// 工作流导航栏方法
const toggleEditMode = (mode: boolean) => {
  isEditMode.value = mode
  workflowStatus.value = mode ? 'editing' : 'idle'
}

const saveWorkflow = () => {
  console.log('保存工作流')
  workflowStatus.value = 'idle'
  isEditMode.value = false
}

const runWorkflow = () => {
  console.log('运行工作流')
  workflowStatus.value = 'running'
  // 调用nodeManager的run方法
  nodeManager.run()
}

const stopWorkflow = () => {
  console.log('停止工作流')
  workflowStatus.value = 'idle'
}

const resetWorkflow = () => {
  console.log('重置工作流')
  workflowStatus.value = 'idle'
  // 调用nodeManager的reset方法
  nodeManager.reset()
}

const exportWorkflow = () => {
  console.log('导出工作流')
}

const importWorkflow = () => {
  console.log('导入工作流')
}

const duplicateWorkflow = () => {
  console.log('复制工作流')
}

const deleteWorkflow = () => {
  console.log('删除工作流')
}
</script>


