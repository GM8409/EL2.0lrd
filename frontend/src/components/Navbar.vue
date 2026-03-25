<template>
  <!-- 外层容器：包裹菜单 + 适配页面布局 -->
  <div class="bg-white shadow-sm top-0 z-9999">
    <el-menu
      :default-active="activeIndex"
      class="el-menu-demo w-full mx-auto px-4"
      mode="horizontal"
      :ellipsis="false"
      @select="handleSelect"
      style="border-bottom: none; height: 70px; align-items: center;"
    >
      <!-- 左侧：🌏EarthLink 项目名称 -->
      <el-menu-item index="0" class="menu-logo transition-all duration-300 hover:text-blue-600">
        <span class="text-2xl font-bold flex items-center gap-2">
          <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#19888a" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-earth-icon lucide-earth">
            <path d="M21.54 15H17a2 2 0 0 0-2 2v4.54"/>
            <path d="M7 3.34V5a3 3 0 0 0 3 3a2 2 0 0 1 2 2c0 1.1.9 2 2 2a2 2 0 0 0 2-2c0-1.1.9-2 2-2h3.17"/>
            <path d="M11 21.95V18a2 2 0 0 0-2-2a2 2 0 0 1-2-2v-1a2 2 0 0 0-2-2H2.05"/>
            <circle cx="12" cy="12" r="10"/></svg>
          <span>EarthLink</span>
        </span>
      </el-menu-item>

      <!-- 中间：可选的导航菜单（按需添加） -->
      <el-menu-item index="1" class="transition-all duration-300 hover:text-blue-600">
        平台首页
      </el-menu-item>
      
      <el-menu-item index="2" class="transition-all duration-300 hover:text-blue-600">
        介绍文档
      </el-menu-item>

      <!-- 右侧：GetStart 按钮（推到最右侧） -->
      <el-menu-item index="3" class="ml-auto">
        快速开始
      </el-menu-item>
    </el-menu>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import router from '@/router/Router'

// 控制默认选中的菜单项
const activeIndex = ref('1')
// 菜单选中事件（可绑定路由跳转）
const handleSelect = (key: string, keyPath: string[]) => {
  console.log('选中的菜单key：', key, '路径：', keyPath)
  // 根据key跳转路由
  if (key === '1') router.push('/')
  if (key === '2') router.push('/about')
  if (key === '3') router.push('/home')
  if (key === '0') router.push('/')
}
</script>

<style scoped>
/* 核心：把第一个菜单项推到左侧，按钮推到右侧 */
.el-menu--horizontal > .el-menu-item:nth-child(1) {
  margin-right: auto;
}

/* 去除菜单默认的底部边框，优化视觉 */
.el-menu-demo {
  --el-menu-border-color: transparent;
}

/* 菜单文字大小/间距优化 */
.el-menu-item {
  font-size: 16px;
  padding: 0 20px !important;
}

/* logo菜单项去掉hover背景色（仅保留文字变色） */
.menu-logo {
  --el-menu-item-hover-bg-color: transparent;
  --el-menu-item-active-bg-color: transparent;
}


</style>