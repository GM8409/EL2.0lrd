<!-- 父组件 -->
<template>
  <div class="relative h-screen">
    <!-- Vue Flow 画布 -->
    <VueFlow
      v-model:nodes="nodes"
      v-model:edges="edges"
      @connect="addEdges($event)"
      :node-types="nodeTypes"
    >
      <Background :gap="15" />
    </VueFlow>
    
    <!-- 调试面板 -->
    <DebugPanel
      class="absolute top-4 right-4 w-96 z-50"
    />

    <button 
    class="btn top-4 left-4"
    @click="addInputNode(addNodes, {value:'你好'})">添加输入节点
  </button>
  <button 
    class="btn top-14 left-4"
    @click="addOutputNode(addNodes,updateNodeData)">添加输出节点
  </button>
  </div>
</template>

<script setup lang="ts">
import { provide, ref } from 'vue'
import { VueFlow, useVueFlow, type Node, type Edge } from '@vue-flow/core'
import { Background } from '@vue-flow/background'
import DebugPanel from './TestPanel.vue'
import { nodeTypes,addInputNode,addOutputNode } from '../tools/nodeManager'
import { StreamManager } from '../tools/streamManager'

// Vue Flow 实例
const { findNode,addNodes,addEdges,updateNodeData } = useVueFlow()
const nodes = ref<Node[]>([])
const edges = ref<Edge[]>([])

const streamManager = new StreamManager(
  nodes || [],
  edges || [],
  findNode || (() => undefined),
)

provide('stream_manager', streamManager)


</script>


<style scoped>
  @import 'tailwindcss';

  .btn {
  @apply absolute  z-50 bg-amber-400 cursor-pointer items-center justify-center w-28 h-8 rounded-lg
}
</style>