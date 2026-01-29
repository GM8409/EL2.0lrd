<template>
  <div class="personal-home">
    <!-- 未注册状态 -->
    <div v-if="!isRegistered" class="unregistered-state">
      <div class="unregistered-card">
        <div class="unregistered-content">
          <div class="avatar-wrapper">
            <el-avatar :size="120" class="avatar-icon">
              <el-icon :size="60"><UserFilled /></el-icon>
            </el-avatar>
          </div>
          <h2 class="text-3xl font-bold mb-2 text-gray-800">欢迎来到 EarthLink</h2>
          <p class="text-gray-500 mb-2 text-sm">强大的遥感影像处理平台</p>
          <p class="text-gray-400 mb-8 text-xs">注册账号以解锁所有功能</p>
          <div class="button-group">
            <el-button type="primary" size="large" class="register-btn">立即注册</el-button>
            <el-button size="large" class="login-btn" @click="handleLogin">已有账号登录</el-button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 已注册状态 -->
    <div v-else class="registered-state">
      <!-- 顶部欢迎横幅 -->
      <div class="welcome-banner">
        <div class="banner-content">
          <h1 class="banner-title">👋 欢迎回来，{{ userName }}！</h1>
          <p class="banner-subtitle">在这里管理您的所有工作流和项目</p>
        </div>
        <el-button type="primary" size="large" class="create-btn">
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
          </svg>
          创建新工作流
        </el-button>
      </div>

      <!-- 个人资料卡 -->
      <div class="profile-card">
        <div class="profile-header">
          <div class="profile-avatar">
            <el-avatar :size="140" :src="userAvatar" class="avatar-image">
              <el-icon :size="70"><UserFilled /></el-icon>
            </el-avatar>
            <div class="avatar-status"></div>
          </div>
          
          <div class="profile-info">
            <div class="info-top">
              <div>
                <h2 class="text-3xl font-bold text-gray-800">{{ userName }}</h2>
                <p class="text-gray-500 text-sm mt-1">{{ userEmail }}</p>
              </div>
              <el-button type="primary" class="edit-profile-btn" plain>编辑资料</el-button>
            </div>
            
            <div class="profile-stats">
              <div class="stat-item">
                <div class="stat-icon workflow-icon">📊</div>
                <div class="stat-content">
                  <span class="stat-value">{{ workflowCount }}</span>
                  <span class="stat-label">工作流</span>
                </div>
              </div>
              <div class="stat-item">
                <div class="stat-icon project-icon">🎯</div>
                <div class="stat-content">
                  <span class="stat-value">{{ projectCount }}</span>
                  <span class="stat-label">项目</span>
                </div>
              </div>
              <div class="stat-item">
                <div class="stat-icon storage-icon">💾</div>
                <div class="stat-content">
                  <span class="stat-value">{{ storageUsed }}</span>
                  <span class="stat-label">已用存储</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 工作流存档 -->
      <div class="workflow-archive">
        <div class="archive-header">
          <div class="archive-title-group">
            <h3 class="text-2xl font-bold text-gray-800">📋 我的工作流</h3>
            <p class="text-gray-500 text-sm mt-1">{{ workflows.length }} 个工作流</p>
          </div>
          <el-button type="primary" size="large" class="new-workflow-btn">
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
            </svg>
            新建工作流
          </el-button>
        </div>
        
        <div class="workflow-list">
          <div v-for="workflow in workflows" :key="workflow.id" class="workflow-item">
            <div class="workflow-item-header">
              <div class="workflow-icon-badge">📁</div>
              <div class="workflow-info">
                <h4 class="workflow-name">{{ workflow.name }}</h4>
                <p class="workflow-description">{{ workflow.description }}</p>
              </div>
              <span class="workflow-status" :class="workflow.status">
                {{ workflow.statusText }}
              </span>
            </div>
            
            <div class="workflow-footer">
              <span class="workflow-date">
                <svg class="w-4 h-4 mr-1 inline" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v2h16V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clip-rule="evenodd"></path>
                </svg>
                {{ workflow.createdAt }}
              </span>
              <div class="workflow-actions">
                <el-button size="small" type="primary" link>编辑</el-button>
                <el-button size="small" type="success" link>运行</el-button>
                <el-button size="small" type="danger" link>删除</el-button>
              </div>
            </div>
          </div>
          
          <!-- 空状态 -->
          <div v-if="workflows.length === 0" class="empty-workflows">
            <div class="empty-icon">📭</div>
            <p class="empty-title">暂无工作流</p>
            <p class="empty-subtitle">点击下方按钮创建您的第一个工作流</p>
            <el-button type="primary" class="mt-6">开始创建</el-button>
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
  padding: 32px;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

/* ========== 未注册状态 ========== */
.unregistered-state {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
}

.unregistered-card {
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  padding: 60px 48px;
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.08);
  text-align: center;
  width: 100%;
  max-width: 500px;
  border: 1px solid rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  animation: slideUp 0.6s ease-out;
}

.unregistered-content {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.avatar-wrapper {
  margin-bottom: 24px;
}

.avatar-icon {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
  box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
}

.button-group {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.register-btn {
  flex: 1;
  max-width: 200px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
}

.login-btn {
  flex: 1;
  max-width: 200px;
  border: 2px solid #667eea;
  color: #667eea;
}

/* ========== 已注册状态 ========== */
.registered-state {
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
}

/* ========== 欢迎横幅 ========== */
.welcome-banner {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 40px 48px;
  border-radius: 16px;
  margin-bottom: 32px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 15px 40px rgba(102, 126, 234, 0.3);
  backdrop-filter: blur(10px);
  animation: slideDown 0.6s ease-out;
}

.banner-content {
  flex: 1;
}

.banner-title {
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 8px;
}

.banner-subtitle {
  font-size: 14px;
  opacity: 0.9;
}

.create-btn {
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
  display: flex;
  align-items: center;
}

.create-btn:hover {
  background: rgba(255, 255, 255, 0.3) !important;
}

/* ========== 个人资料卡 ========== */
.profile-card {
  background: white;
  padding: 40px;
  border-radius: 16px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
  margin-bottom: 32px;
  border: 1px solid rgba(0, 0, 0, 0.05);
  animation: fadeIn 0.6s ease-out 0.2s both;
}

.profile-header {
  display: flex;
  align-items: flex-start;
  gap: 32px;
}

.profile-avatar {
  position: relative;
  flex-shrink: 0;
}

.avatar-image {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
  box-shadow: 0 15px 40px rgba(102, 126, 234, 0.25);
}

.avatar-status {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 18px;
  height: 18px;
  background: #52c41a;
  border: 3px solid white;
  border-radius: 50%;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.profile-info {
  flex: 1;
}

.info-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 28px;
}

.edit-profile-btn {
  border-color: #667eea;
  color: #667eea;
}

.edit-profile-btn:hover {
  background-color: rgba(102, 126, 234, 0.05);
}

.profile-stats {
  display: flex;
  gap: 40px;
  flex-wrap: wrap;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.stat-icon {
  font-size: 32px;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
}

.workflow-icon {
  background: rgba(102, 126, 234, 0.1);
}

.project-icon {
  background: rgba(76, 175, 80, 0.1);
}

.storage-icon {
  background: rgba(255, 152, 0, 0.1);
}

.stat-content {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 20px;
  font-weight: bold;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.stat-label {
  font-size: 12px;
  color: #999;
  margin-top: 4px;
}

/* ========== 工作流存档 ========== */
.workflow-archive {
  background: white;
  padding: 40px;
  border-radius: 16px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(0, 0, 0, 0.05);
  animation: fadeIn 0.6s ease-out 0.4s both;
}

.archive-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 2px solid #f5f7fa;
}

.archive-title-group {
  flex: 1;
}

.new-workflow-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  display: flex;
  align-items: center;
}

.workflow-list {
  width: 100%;
  display: grid;
  gap: 16px;
}

.workflow-item {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 12px;
  border: 1px solid #e8e8e8;
  transition: all 0.3s ease;
  animation: slideIn 0.4s ease-out;
}

.workflow-item:hover {
  background: white;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  border-color: #667eea;
  transform: translateY(-2px);
}

.workflow-item-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 16px;
}

.workflow-icon-badge {
  font-size: 24px;
  min-width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  background: rgba(102, 126, 234, 0.1);
  border-radius: 8px;
}

.workflow-info {
  flex: 1;
}

.workflow-name {
  font-size: 16px;
  font-weight: bold;
  color: #333;
  margin-bottom: 6px;
}

.workflow-description {
  color: #999;
  font-size: 13px;
  margin: 0;
}

.workflow-status {
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  white-space: nowrap;
}

.workflow-status.completed {
  background: linear-gradient(135deg, rgba(82, 196, 26, 0.1) 0%, rgba(82, 196, 26, 0.05) 100%);
  color: #52c41a;
  border: 1px solid rgba(82, 196, 26, 0.2);
}

.workflow-status.pending {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(102, 126, 234, 0.05) 100%);
  color: #667eea;
  border: 1px solid rgba(102, 126, 234, 0.2);
}

.workflow-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 12px;
  border-top: 1px solid #e8e8e8;
}

.workflow-date {
  font-size: 12px;
  color: #999;
}

.workflow-actions {
  display: flex;
  gap: 4px;
}

.workflow-actions :deep(.el-button) {
  font-size: 12px;
}

/* 空状态 */
.empty-workflows {
  padding: 60px 40px;
  text-align: center;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.empty-title {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin-bottom: 8px;
}

.empty-subtitle {
  font-size: 14px;
  color: #999;
  margin-bottom: 0;
}

/* ========== 动画 ========== */
@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* ========== 响应式设计 ========== */
@media (max-width: 1024px) {
  .personal-home {
    padding: 24px;
  }

  .profile-header {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .info-top {
    flex-direction: column;
    align-items: center;
  }

  .profile-stats {
    justify-content: center;
    gap: 32px;
  }

  .welcome-banner {
    flex-direction: column;
    text-align: center;
    gap: 20px;
  }

  .workflow-item-header {
    flex-direction: column;
    align-items: flex-start;
  }
}

@media (max-width: 768px) {
  .personal-home {
    padding: 16px;
  }

  .unregistered-card {
    padding: 40px 24px;
  }

  .profile-card,
  .workflow-archive {
    padding: 24px;
  }

  .welcome-banner {
    padding: 24px;
  }

  .profile-stats {
    gap: 20px;
  }

  .stat-item {
    gap: 8px;
  }

  .stat-icon {
    width: 40px;
    height: 40px;
    font-size: 24px;
  }

  .workflow-footer {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .workflow-actions {
    width: 100%;
    justify-content: flex-end;
  }

  .button-group {
    flex-direction: column;
  }

  .register-btn,
  .login-btn {
    max-width: 100%;
  }
}

@media (max-width: 480px) {
  .personal-home {
    padding: 12px;
  }

  .unregistered-card {
    padding: 32px 16px;
  }

  .profile-card,
  .workflow-archive {
    padding: 16px;
  }

  .archive-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .new-workflow-btn {
    width: 100%;
  }

  .banner-title {
    font-size: 20px;
  }

  .banner-subtitle {
    font-size: 12px;
  }

  .profile-avatar :deep(.el-avatar) {
    width: 100px !important;
    height: 100px !important;
  }

  .stat-value {
    font-size: 16px;
  }
}
</style>