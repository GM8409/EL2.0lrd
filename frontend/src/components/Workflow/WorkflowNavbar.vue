<template>
  <!-- 工作流导航栏容器 -->
  <div
    @wheel="(e: any) => e.preventDefault()"
    class="sticky top-0 z-50 flex items-center justify-between w-full px-4 py-3 backdrop-blur-md bg-white/95 border-b border-gray-200 transition-all duration-300"
  >
    <!-- 左侧：工作流信息 -->
    <div class="flex items-center space-x-4">
      <!-- 工作流图标 -->
      <div class="flex items-center justify-center p-2 rounded-lg bg-blue-600 text-white transition-all duration-300 hover:scale-105 hover:shadow-md hover:shadow-blue-600/30">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
        </svg>
      </div>
        
      <!-- 工作流名称和状态 -->
      <div class="workflow-info">
        <div class="flex items-center space-x-2">
          <h2 class="text-lg font-semibold text-gray-800 transition-all duration-300">{{ workflowName }}</h2>
          <span class="text-xs text-gray-500">{{ workflowVersion }}</span>
        </div>
        <div class="flex items-center space-x-2 mt-1">
          <span 
            :class="[
              'px-2 py-0.5 rounded-full text-xs font-medium transition-all duration-300',
              workflowStatus === 'idle' ? 'bg-sky-50 text-sky-700 border border-sky-200' : '',
              workflowStatus === 'running' ? 'bg-amber-50 text-amber-700 border border-amber-200' : '',
              workflowStatus === 'completed' ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : '',
              workflowStatus === 'error' ? 'bg-red-50 text-red-700 border border-red-200' : '',
              workflowStatus === 'editing' ? 'bg-pink-50 text-pink-700 border border-pink-200' : ''
            ]"
          >
            {{ workflowStatusText }}
          </span>
          <span v-if="workflowStatus === 'running'" class="w-2 h-2 rounded-full bg-amber-600 animate-pulse"></span>
        </div>
      </div>
    </div>
      
    <!-- 右侧：操作按钮 -->
    <div class="flex items-center space-x-3">
      <!-- 编辑模式按钮 -->
      <el-button 
        size="small" 
        :type="isEditMode ? 'primary' : 'default'"
        @click="toggleEditMode"
        class="transition-all duration-300"
      >
        {{ isEditMode ? '退出编辑' : '编辑工作流' }}
      </el-button>
        
      <!-- 保存按钮 -->
      <el-button 
        size="small" 
        type="success" 
        @click="saveWorkflow"
        :disabled="!isEditMode"
        class="transition-all duration-300"
      >
        保存
      </el-button>
        
      <!-- 运行按钮 -->
      <el-button 
        size="small" 
        type="primary" 
        @click="runWorkflow"
        :disabled="isEditMode || workflowStatus === 'running'"
        class="transition-all duration-300"
      >
        运行
      </el-button>
        
      <!-- 停止按钮 -->
      <el-button 
        size="small" 
        type="danger" 
        @click="stopWorkflow"
        :disabled="workflowStatus !== 'running'"
        class="transition-all duration-300"
      >
        停止
      </el-button>
        
      <!-- 重置按钮 -->
      <el-button 
        size="small" 
        @click="resetWorkflow"
        :disabled="workflowStatus === 'running'"
        class="transition-all duration-300"
      >
        重置
      </el-button>
        
      <!-- 更多操作下拉菜单 -->
      <el-dropdown>
        <el-button size="small" class="transition-all duration-300">
          更多 <el-icon class="el-icon--right"><arrow-down /></el-icon>
        </el-button>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item @click="exportWorkflow">导出工作流</el-dropdown-item>
            <el-dropdown-item @click="importWorkflow">导入工作流</el-dropdown-item>
            <el-dropdown-item @click="duplicateWorkflow">复制工作流</el-dropdown-item>
            <el-dropdown-item divided @click="deleteWorkflow" class="text-danger">删除工作流</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, computed } from 'vue'
import { ArrowDown } from '@element-plus/icons-vue'

// Props
const props = defineProps({
  workflowName: {
    type: String,
    default: '未命名工作流'
  },
  workflowVersion: {
    type: String,
    default: 'v1.0'
  },
  workflowStatus: {
    type: String,
    default: 'idle', // idle, running, completed, error, editing
    validator: (value: string) => ['idle', 'running', 'completed', 'error', 'editing'].includes(value)
  }
})

// Emits
const emit = defineEmits([
  'toggle-edit',
  'save',
  'run',
  'stop',
  'reset',
  'export',
  'import',
  'duplicate',
  'delete'
])

// State
const isEditMode = ref(false)

// Computed
const workflowStatusText = computed(() => {
  const statusMap: Record<string, string> = {
    idle: '就绪',
    running: '运行中',
    completed: '已完成',
    error: '错误',
    editing: '编辑中'
  }
  return statusMap[props.workflowStatus] || '未知状态'
})

// Methods
const toggleEditMode = () => {
  isEditMode.value = !isEditMode.value
  emit('toggle-edit', isEditMode.value)
}

const saveWorkflow = () => {
  emit('save')
}

const runWorkflow = () => {
  emit('run')
}

const stopWorkflow = () => {
  emit('stop')
}

const resetWorkflow = () => {
  emit('reset')
}

const exportWorkflow = () => {
  emit('export')
}

const importWorkflow = () => {
  emit('import')
}

const duplicateWorkflow = () => {
  emit('duplicate')
}

const deleteWorkflow = () => {
  emit('delete')
}
</script>

<style scoped>
/* 响应式设计 */
@media (max-width: 768px) {
  .workflow-info h2 {
    font-size: 14px;
  }
  
  .workflow-info span {
    display: none;
  }
  
  .flex.items-center.space-x-3 {
    flex-wrap: wrap;
    gap: 8px;
  }
  
  .el-button {
    font-size: 12px;
    padding: 4px 8px;
  }
}

@media (max-width: 480px) {
  .flex.items-center.justify-between {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .flex.items-center.space-x-4 {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .workflow-info {
    width: 100%;
  }
  
  .flex.items-center.space-x-3 {
    width: 100%;
    justify-content: space-between;
  }
}
</style>