<template>
  <!-- 工作流导航栏容器 -->
  <div
  @wheel="(e: any) => e.preventDefault()"
   class="workflow-navbar bg-white shadow-md border-b border-gray-200">
    <div class="container mx-auto px-4 py-0 flex items-center justify-between">
      <!-- 左侧：工作流信息 -->
      <div class="flex items-center space-x-4">
        <!-- 工作流图标 -->
        <div class="workflow-icon bg-blue-600 text-white rounded-lg p-2 flex items-center justify-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
        </div>
        
        <!-- 工作流名称和状态 -->
        <div class="workflow-info">
          <div class="flex items-center space-x-2">
            <h2 class="workflow-name text-lg font-semibold text-gray-800">{{ workflowName }}</h2>
            <span class="workflow-version text-xs text-gray-500">{{ workflowVersion }}</span>
          </div>
          <div class="flex items-center space-x-2 mt-1">
            <span class="workflow-status" :class="`status-${workflowStatus}`">
              {{ workflowStatusText }}
            </span>
            <span v-if="workflowStatus === 'running'" class="status-indicator animate-pulse"></span>
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
.workflow-navbar {
  position: sticky;
  z-index: 9998;
  backdrop-filter: blur(8px);
  background-color: rgba(255, 255, 255, 0.95);
  transition: all 0.3s ease;
}

.workflow-icon {
  transition: all 0.3s ease;
}

.workflow-icon:hover {
  transform: scale(1.05);
  box-shadow: 0 2px 8px rgba(37, 99, 235, 0.3);
}

.workflow-name {
  transition: all 0.3s ease;
}

.workflow-status {
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.status-idle {
  background-color: #f0f9ff;
  color: #0284c7;
  border: 1px solid #bae6fd;
}

.status-running {
  background-color: #fef3c7;
  color: #d97706;
  border: 1px solid #fde68a;
}

.status-completed {
  background-color: #f0fdf4;
  color: #15803d;
  border: 1px solid #bbf7d0;
}

.status-error {
  background-color: #fef2f2;
  color: #dc2626;
  border: 1px solid #fecaca;
}

.status-editing {
  background-color: #fdf2f8;
  color: #be185d;
  border: 1px solid #fbcfe8;
}

.status-indicator {
  width: 8px;
  height: 8px;
  background-color: #d97706;
  border-radius: 50%;
  display: inline-block;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .workflow-navbar {
    top: 60px;
  }
  
  .container {
    padding-left: 12px;
    padding-right: 12px;
  }
  
  .workflow-name {
    font-size: 14px;
  }
  
  .workflow-version {
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
  .workflow-navbar {
    padding: 8px 0;
  }
  
  .flex.items-center.space-x-4 {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .workflow-info {
    width: 100%;
  }
  
  .flex.items-center.justify-between {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .flex.items-center.space-x-3 {
    width: 100%;
    justify-content: space-between;
  }
}
</style>