<template>
  <div class="personal-home">
    <!-- 未注册状态 -->
    <div v-if="!isRegistered" class="unregistered-state">
      <div class="unregistered-card">
        <el-avatar :size="100">
            <el-icon :size="50"><UserFilled /></el-icon>
        </el-avatar>
        <h2 class="text-2xl font-bold mb-4">您尚未注册</h2>
        <p class="text-slate-600 mb-6">注册账号以使用更多功能</p>
        <el-button type="primary" size="large">立即注册</el-button>
        <el-button size="large" class="ml-4" @click="handleLogin">登录</el-button>
      </div>
    </div>
    
    <!-- 已注册状态 -->
    <div v-else class="registered-state">
      <!-- 个人资料卡 -->
      <div class="profile-card">
        <div class="profile-header">
          <el-avatar :size="120" :src="userAvatar" />
          <div class="profile-info">
            <h2 class="text-2xl font-bold">{{ userName }}</h2>
            <p class="text-slate-600">{{ userEmail }}</p>
            <div class="profile-stats">
              <div class="stat-item">
                <span class="stat-value">{{ workflowCount }}</span>
                <span class="stat-label">工作流</span>
              </div>
              <div class="stat-item">
                <span class="stat-value">{{ projectCount }}</span>
                <span class="stat-label">项目</span>
              </div>
              <div class="stat-item">
                <span class="stat-value">{{ storageUsed }}</span>
                <span class="stat-label">已用存储</span>
              </div>
            </div>
          </div>
          <el-button type="primary" class="edit-profile-btn">编辑资料</el-button>
        </div>
      </div>
      
      <!-- 工作流存档 -->
      <div class="workflow-archive">
        <div class="workflow-header">
          <h3 class="text-xl font-bold">工作流存档</h3>
          <el-button type="primary">创建新工作流</el-button>
        </div>
        
        <div class="workflow-list">
          <div v-for="workflow in workflows" :key="workflow.id" class="workflow-item">
            <div class="workflow-info">
              <h4 class="workflow-name">{{ workflow.name }}</h4>
              <p class="workflow-description">{{ workflow.description }}</p>
              <div class="workflow-meta">
                <span class="workflow-date">{{ workflow.createdAt }}</span>
                <span class="workflow-status" :class="workflow.status">{{ workflow.statusText }}</span>
              </div>
            </div>
            <div class="workflow-actions">
              <el-button size="small">编辑</el-button>
              <el-button size="small">运行</el-button>
              <el-button size="small" type="danger">删除</el-button>
            </div>
          </div>
          
          <!-- 空状态 -->
          <div v-if="workflows.length === 0" class="empty-workflows">
            <el-empty description="暂无工作流" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { UserFilled } from '@element-plus/icons-vue'


const isRegistered = ref(false) // 模拟未注册状态，可根据实际情况修改

// 模拟用户数据
const userAvatar = ref('')
const userName = ref('用户名')
const userEmail = ref('user@example.com')
const workflowCount = ref(5)
const projectCount = ref(3)
const storageUsed = ref('1.2GB')

// 登录处理函数
const handleLogin = () => {
  isRegistered.value = true
}

// 模拟工作流数据
const workflows = ref([
  {
    id: 1,
    name: '遥感影像分类工作流',
    description: '使用机器学习算法对遥感影像进行分类',
    createdAt: '2024-01-20',
    status: 'completed',
    statusText: '已完成'
  },
  {
    id: 2,
    name: '变化检测工作流',
    description: '检测不同时期遥感影像的变化',
    createdAt: '2024-01-18',
    status: 'pending',
    statusText: '待处理'
  }
])
</script>

<style scoped>
.personal-home {
  padding: 24px;
  min-height: 100vh;
  background-color: #f5f7fa;
}

/* 未注册状态 */
.unregistered-state {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
}

.unregistered-card {
  background-color: #fff;
  padding: 48px;
  border-radius: 12px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  text-align: center;
  width: 100%;
  max-width: 480px;
}

/* 已注册状态 */
.registered-state {
  width: 100%;
}

/* 个人资料卡 */
.profile-card {
  background-color: #fff;
  padding: 32px;
  border-radius: 12px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  margin-bottom: 24px;
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 24px;
}

.profile-info {
  flex: 1;
}

.profile-stats {
  display: flex;
  gap: 48px;
  margin-top: 16px;
}

.stat-item {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: bold;
  color: #1890ff;
}

.stat-label {
  font-size: 0.875rem;
  color: #666;
}

/* 工作流存档 */
.workflow-archive {
  background-color: #fff;
  padding: 32px;
  border-radius: 12px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.workflow-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.workflow-list {
  width: 100%;
}

.workflow-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  margin-bottom: 16px;
  transition: all 0.3s;
}

.workflow-item:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.workflow-info {
  flex: 1;
}

.workflow-name {
  font-size: 1.125rem;
  font-weight: bold;
  margin-bottom: 8px;
}

.workflow-description {
  color: #666;
  margin-bottom: 12px;
}

.workflow-meta {
  display: flex;
  align-items: center;
  gap: 16px;
  font-size: 0.875rem;
  color: #999;
}

.workflow-status {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.75rem;
}

.workflow-status.completed {
  background-color: #f6ffed;
  color: #52c41a;
  border: 1px solid #b7eb8f;
}

.workflow-status.pending {
  background-color: #e6f7ff;
  color: #1890ff;
  border: 1px solid #91d5ff;
}

.workflow-actions {
  display: flex;
  gap: 8px;
}

.empty-workflows {
  padding: 48px 0;
  text-align: center;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .profile-header {
    flex-direction: column;
    text-align: center;
  }
  
  .profile-stats {
    justify-content: center;
  }
  
  .workflow-item {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .workflow-actions {
    margin-top: 16px;
    align-self: flex-end;
  }
}
</style>