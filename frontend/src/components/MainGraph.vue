<!-- 父组件 -->
<template>
  <div class="relative h-screen">
    <!-- Vue Flow 画布 -->
    <VueFlow
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
    <!-- 调试面板 暂时不要了
    <DebugPanel
      v-show="isDebugPanelOpen"  
      class="absolute top-4 right-4 w-96 z-50"
    /> -->

  </div>
</template>

<script setup lang="ts">
import { provide, ref } from 'vue'
import { VueFlow, useVueFlow, type Node, type Edge } from '@vue-flow/core'
import { Background } from '@vue-flow/background'
import DebugPanel from './TestPanel.vue'
import NodePanel from './NodePanel.vue'
import { nodeTypes,NodeManager } from '../tools/nodeManager'
import { StreamManager } from '../tools/streamManager'

const isDebugPanelOpen = ref(false)

// Vue Flow 实例
const flow = useVueFlow('my-flow')
const nodes = ref<Node[]>([])
const edges = ref<Edge[]>([])

const nodeManager = new NodeManager(flow)
// const streamManager = new StreamManager(
//   nodes || [],
//   edges || [],
//   flow.findNode || (() => undefined),
// )

// provide('stream_manager', streamManager)
provide('node_manager', nodeManager)

</script>


