<!-- Nodes/HTTPNode.vue -->
<script setup lang="ts">
import { Handle, Position, type NodeProps } from '@vue-flow/core'
import { ref,  onMounted } from 'vue'

// 继承NodeProps并扩展data类型，定义HTTP节点需要的字段
interface HTTPNodeData {
  imageUrl: string // 图片请求URL
  status: 'idle' | 'loading' | 'success' | 'error' // 请求状态
  errorMsg?: string // 错误信息
  imgWidth?: number // 图片宽度
  imgHeight?: number // 图片高度
}

// 定义Props，指定data的类型为HTTPNodeData
const props = defineProps<NodeProps<HTTPNodeData>>()

// 响应式状态：控制图片加载（基于props.data，保留响应式）
const imgLoading = ref(props.data.status === 'loading')
const imgError = ref(false)

// 核心方法：请求图片（处理加载/成功/失败状态）
const fetchImage = () => {
  if (!props.data.imageUrl) {
    props.data.status = 'error'
    props.data.errorMsg = '图片URL不能为空'
    return
  }

  // 更新状态为加载中
  props.data.status = 'loading'
  imgLoading.value = true
  imgError.value = false

  // 创建图片对象请求资源
  const img = new Image()
  img.onload = () => {
    // 成功：记录图片尺寸，更新状态
    props.data.status = 'success'
    props.data.imgWidth = img.width
    props.data.imgHeight = img.height
    imgLoading.value = false
  }
  img.onerror = (err) => {
    // 失败：记录错误信息
    props.data.status = 'error'
    props.data.errorMsg = '图片加载失败：URL无效或网络错误'
    imgLoading.value = false
    imgError.value = true
    console.error('图片加载失败：', err)
  }
  img.src = props.data.imageUrl
}

// 组件挂载时：如果已有URL且状态为idle，自动请求（可选）
onMounted(() => {
  if (props.data.imageUrl && props.data.status === 'idle') {
    fetchImage()
  }
})
</script>

<template>
  <div class="http-node min-w-55 max-h-110 max-w-75 bg-white border-2 border-[#2196F3] rounded-lg p-3 shadow-[0_3px_10px_rgba(33,150,243,0.1)] font-sans select-none relative">
    <!-- 节点头部：和加法节点结构一致 -->
    <div class="node-header flex justify-between items-center mb-3 pb-2 border-b border-[#e0e0e0]">
      <span class="node-type bg-[#2196F3] text-white px-2.5 py-1 rounded text-xs font-semibold">HTTP图片请求节点</span>
      <span class="node-id text-[10px] text-[#757575]">{{ props.id }}</span>
    </div>

    <!-- 节点内容区：适配图片请求逻辑 -->
    <div class="node-content flex flex-col gap-2.5">
      <!-- URL展示+请求按钮区域（替代加法节点的运算区） -->
      <div class="request-area flex flex-col gap-2 p-2.5 bg-[#E3F2FD] rounded-md">
        <div class="url-display flex flex-wrap gap-1 text-xs">
          <span class="url-label text-[#1976D2] font-medium">图片URL：</span>
          <span class="url-value text-[#424242] flex-1 break-all">{{ props.data.imageUrl || '未设置URL' }}</span>
        </div>
        <button 
          class="request-btn bg-[#2196F3] text-white border-0 rounded px-2.5 py-1 text-xs font-semibold cursor-pointer transition-colors duration-200 disabled:bg-[#90CAF9] disabled:cursor-not-allowed"
          @click="fetchImage"
          :disabled="props.data.status === 'loading'"
        >
          {{ props.data.status === 'loading' ? '加载中...' : '请求图片' }}
        </button>
      </div>

      <!-- 状态提示区域 -->
      <div class="status-area flex flex-col gap-1 text-[11px]" v-if="props.data.status !== 'idle'">
        <span 
          class="status-tag inline-block px-1.5 py-0.5 rounded text-[11px]"
          :class="{
            'bg-[#FFF3E0] text-[#FF9800]': props.data.status === 'loading',
            'bg-[#E8F5E9] text-[#4CAF50]': props.data.status === 'success',
            'bg-[#FFEBEE] text-[#F44336]': props.data.status === 'error'
          }"
        >
          {{ 
             props.data.status === 'loading' ? '加载中' : 
             props.data.status === 'success' ? '加载成功' : '加载失败' 
          }}
        </span>
        <span class="error-msg text-[#F44336] text-[10px]" v-if="props.data.status === 'error'">
          {{ props.data.errorMsg || '图片加载失败' }}
        </span>
      </div>

      <!-- 图片展示区域（核心） -->
      <div class="image-preview p-2 border border-[#e0e0e0] rounded-md min-h-25 flex flex-col items-center justify-center">
        <div v-if="props.data.status === 'loading'" class="loading-placeholder flex flex-col items-center justify-center gap-1.5 text-[#757575] text-xs">
          <span class="loading-text">图片加载中...</span>
        </div>
        <div v-else-if="props.data.status === 'success'" class="image-container w-full">
          <img 
            :src="props.data.imageUrl" 
            alt="请求的图片"
            class="preview-img max-w-full max-h-30"
          >
          <div class="img-info mt-1.5 text-[10px] text-[#757575] text-center">
            尺寸：{{ props.data.imgWidth }} × {{ props.data.imgHeight }}
          </div>
        </div>
        <div v-else-if="props.data.status === 'error'" class="error-placeholder flex flex-col items-center justify-center gap-1.5 text-[#757575] text-xs">
          <span class="error-icon text-[20px]">⚠️</span>
          <span class="error-text">{{ props.data.errorMsg || '图片加载失败' }}</span>
        </div>
        <div v-else class="empty-placeholder flex flex-col items-center justify-center gap-1.5 text-[#757575] text-xs">
          <span class="empty-text">点击「请求图片」加载URL</span>
        </div>
      </div>
    </div>

    <!-- 输入连接点（左侧）：和加法节点一致 -->
    <Handle 
      type="target" 
      :position="Position.Left" 
      class="node-handle node-handle-target w-2.5 h-2.5 bg-white border-2 border-[#2196F3] left--1.25 top-1/2"
    />
    
    <!-- 输出连接点（右侧）：和加法节点一致 -->
    <Handle 
      type="source" 
      :position="Position.Right" 
      class="node-handle node-handle-source w-2.5 h-2.5 bg-white border-2 border-[#2196F3] right--1.25 top-1/2"
    />
  </div>
</template>

<style scoped>
/* 仅保留无法用Tailwind实现的样式（如scoped下的定位） */
/* 其余样式已全部迁移到template的class中 */
.node-handle-target {
  left: -5px;
  top: 50%;
}

.node-handle-source {
  right: -5px;
  top: 50%;
}
</style>