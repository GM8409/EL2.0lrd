<!-- DebugPanel.vue -->
<script setup lang="ts">
import {  computed,  inject} from 'vue'
import type { Node} from '@vue-flow/core'
import { StreamManager } from '../tools/streamManager'

// 从父组件注入流管理器
const streamManager = inject<StreamManager>('stream_manager')

// 确保流管理器已初始化
if (!streamManager) {
  throw new Error('TestPanel 组件必须在 Test 组件中使用，且必须提供 stream_manager 注入')
}



// 获取节点类型统计
const nodeTypeStats = computed(() => {
  const stats: Record<string, number> = {}
  streamManager.nodes.value.forEach((node:Node) => {
    const type = node.type || 'default'
    stats[type] = (stats[type] || 0) + 1
  })
  return stats
})

</script>

<template>
  <div class="debug-panel bg-white rounded-xl shadow-xl border border-gray-200">
    <!-- 面板头部 -->
    <div class="panel-header bg-linear-to-r bg-blue-500 px-6 py-4 rounded-t-xl">
      <div class="flex items-center justify-between">
        <div>
          <h2 class="text-xl font-bold text-white flex items-center gap-2">
            
            调试面板
          </h2>
        
        </div>
        
        <!-- 右上角控制按钮组 -->
        <div class="flex items-center gap-2">
          <button
            @click="streamManager.act(true)"
           
            class="px-4 py-2 bg-amber-500 hover:bg-amber-600 text-white text-sm rounded-lg transition-all hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
          >
            <span class="text-lg">⏭</span>
            <span>单步调试</span>
          </button>
          
          <button
            @click="streamManager.act()"
            
            class="px-4 py-2 bg-linear-to-r from-red-500 to-pink-600 hover:from-red-600 hover:to-pink-700 text-white text-sm rounded-lg transition-all hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
          >
            <span class="text-lg">🚀</span>
            <span>全部执行</span>
          </button>
        </div>
      </div>
    </div>
    
    <!-- 主要内容区域 -->
    <div class="p-6 space-y-6 max-h-[calc(100vh-200px)] overflow-y-auto">
      <!-- 系统状态卡片 -->
      <div class="bg-gray-50 rounded-lg p-4 border border-gray-200">
        <h3 class="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
          <span class="text-blue-500">📊</span>
          系统状态
        </h3>
        
        <div class="flex flex-wrap gap-3">
          <div class="flex-1 stat-card bg-white rounded-lg p-3 border border-gray-200">
            <div class="text-sm text-gray-500 mb-1">节点总数</div>
            <div class="text-2xl font-bold text-gray-800">{{ streamManager.nodes.value?.length || 0 }}</div>
          </div>
          
          <div class="flex-1 stat-card bg-white rounded-lg p-3 border border-gray-200">
            <div class="text-sm text-gray-500 mb-1">连线总数</div>
            <div class="text-2xl font-bold text-gray-800">{{ streamManager.edges.value?.length || 0 }}</div>
          </div>
          
        
          <div class="flex-1 stat-card bg-white rounded-lg p-3 border border-gray-200">
            <div class="text-sm text-gray-500 mb-1">执行状态</div>
            <div class="text-2xl font-bold" :class="streamManager.isFinished ? 'text-green-600' : 'text-amber-600'">
              {{ streamManager.isFinished ? '已完成' : '调试中' }}
            </div>
          </div>
        </div>
        
        <!-- 节点类型分布 -->
        <div class="mt-4">
          <h4 class="text-sm font-medium text-gray-700 mb-2">节点类型分布</h4>
          <div class="flex flex-wrap gap-2">
            <div 
              v-for="(count, type) in nodeTypeStats" 
              :key="type"
              class="px-3 py-1 bg-blue-50 text-blue-700 rounded-full text-xs font-medium"
            >
              {{ type }}: {{ count }}
            </div>
          </div>
        </div>
      </div>
      
      <!-- 跟踪参数卡片 -->
      <div class="bg-linear-to-br from-blue-50 to-indigo-50 rounded-lg p-4 border border-blue-200">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold text-gray-800 flex items-center gap-2">
            <span class="text-indigo-500">📍</span>
            跟踪参数
          </h3>
        </div>
        
        <div class="space-y-4">
          <!-- 当前边 -->
          <div class="param-card bg-white rounded-lg p-3 border border-blue-100">
            <div class="flex items-center justify-between mb-2">
              <div class="text-sm font-medium text-gray-700">当前连线</div>
              <div 
                v-if="streamManager.currentEdge.value"
                class="px-2 py-0.5 bg-blue-100 text-blue-800 text-xs rounded"
              >
                已连接
              </div>
              <div 
                v-else
                class="px-2 py-0.5 bg-gray-100 text-gray-600 text-xs rounded"
              >
                无
              </div>
            </div>
            <div 
              v-if="streamManager.currentEdge.value"
              class="text-sm text-gray-800 font-mono"
            >
              {{ streamManager.currentEdge.value.source }} → {{ streamManager.currentEdge.value.target }}
            </div>
            <div v-else class="text-sm text-gray-400 italic">暂无当前边</div>
          </div>
          
          <!-- 当前节点 -->
          <div class="param-card bg-white rounded-lg p-3 border border-blue-100">
            <div class="flex items-center justify-between mb-2">
              <div class="text-sm font-medium text-gray-700">当前节点</div>
              <div 
                v-if="streamManager.currentNode.value"
                :class="[
                  'px-2 py-0.5 text-xs rounded',
                  streamManager.currentNode.value.type === 'start' ? 'bg-green-100 text-green-800' :
                  streamManager.currentNode.value.type === 'output' ? 'bg-purple-100 text-purple-800' :
                  'bg-blue-100 text-blue-800'
                ]"
              >
                {{ streamManager.currentNode.value.type || 'default' }}
              </div>
              <div 
                v-else
                class="px-2 py-0.5 bg-gray-100 text-gray-600 text-xs rounded"
              >
                无
              </div>
            </div>
            <div 
              v-if="streamManager.currentNode.value"
              class="space-y-1"
            >
              <div class="text-sm text-gray-800">
                ID: <span class="font-mono">{{ streamManager.currentNode.value.id }}</span>
              </div>
              <div 
                v-if="streamManager.currentNode.value.data?.label"
                class="text-sm text-gray-600"
              >
                标签: {{ streamManager.currentNode.value.data.label }}
              </div>
            </div>
            <div v-else class="text-sm text-gray-400 italic">暂无当前节点</div>
          </div>
          
          <!-- 当前数据 -->
          <div class="param-card bg-white rounded-lg p-3 border border-blue-100">
            <div class="flex items-center justify-between mb-2">
              <div class="text-sm font-medium text-gray-700">当前数据</div>
              <div class="px-2 py-0.5 bg-indigo-100 text-indigo-800 text-xs rounded">
                {{ typeof streamManager.currentData.value }}
              </div>
            </div>
            <pre class="text-xs bg-gray-50 p-2 rounded border border-gray-200 overflow-x-auto font-mono">{{ 
              JSON.stringify(streamManager.currentData.value, null, 2) 
            }}</pre>
          </div>
        </div>
      </div>
      
      <!-- 控制按钮组 -->
      <div class="space-y-4">
        <div class="flex items-center gap-3">
          <button
            @click="streamManager.addTemplateData"
            class="flex-1 px-4 py-3 bg-linear-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white font-medium rounded-lg transition-all hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            <span class="text-lg">📋</span>
            <span>添加模板数据</span>
          </button>
        </div>
        
        <div class="flex items-center gap-3">
          <button
            @click="streamManager.initStream()"
            class="flex-1 px-4 py-3 bg-linear-to-r from-cyan-500 to-teal-600 hover:from-cyan-600 hover:to-teal-700 text-white font-medium rounded-lg transition-all hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            <span class="text-lg">🔄</span>
            <span>重置执行</span>
          </button>
        </div>
      </div>
    </div>
    
    <!-- 面板底部 -->
    <div class="panel-footer bg-gray-50 px-6 py-3 border-t border-gray-200 rounded-b-xl">
      <div class="flex items-center justify-between">
        <div class="text-sm text-gray-500">
          最后更新: {{ new Date().toLocaleTimeString() }}
        </div>
        
        <div class="flex items-center gap-3">
          <div 
            class="flex items-center gap-2"
          >
            <div 
            v-if="!streamManager.isFinished"
            class="animate-spin w-4 h-4 border-2 border-blue-500 border-t-transparent rounded-full"></div>
            <span class="text-sm text-blue-600">{{ streamManager.isFinished ? '完成' : '调试中' }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.debug-panel {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Segoe UI', Arial, sans-serif;
}

/* 自定义滚动条样式 */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* 动画效果 */
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.7;
  }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .debug-panel {
    margin: 0.5rem;
    max-height: calc(100vh - 100px);
  }
  
  .panel-header {
    padding: 1rem;
  }
  
  .grid-cols-2 {
    grid-template-columns: repeat(1, 1fr);
  }
  
  .grid-cols-4 {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>