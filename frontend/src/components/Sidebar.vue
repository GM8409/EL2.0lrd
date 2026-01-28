<template>
  <el-menu
    default-active="2"
    class="el-menu-vertical-demo"
    :collapse="isCollapse"
    @open="handleOpen"
    @close="handleClose"
    @mousedown="preventDefault"
    @mouseup="preventDefault"
    @click="preventDefault"
    @wheel="preventDefault"
  >
    <!-- 控制侧栏开闭的按钮 -->
    <el-menu-item index="1" class="collapse-btn" @click="toggleCollapse">
      <el-icon v-if="isCollapse"><Expand /></el-icon>
      <el-icon v-else><Fold /></el-icon>
      <template #title v-if="!isCollapse"><span @wheel="preventDefault">收起菜单</span></template>
      <template #title v-else><span @wheel="preventDefault">展开菜单</span></template> 
    </el-menu-item>

    <el-menu-item index="2" @click="navigateTo('')">
      <el-icon><User /></el-icon>
      <template #title><span @wheel="preventDefault">个人主页</span></template>
    </el-menu-item>

    <el-menu-item index="3" @click="navigateTo('imgGet')">
      <el-icon><DataBoard /></el-icon>
      <template #title><span @wheel="preventDefault">获取和查看图片</span></template>
    </el-menu-item>
    
    <el-menu-item index="4" @click="navigateTo('workflow')">
      <el-icon><Tools /></el-icon>
      <template #title ><span @wheel="preventDefault">影像处理工作流</span></template>
    </el-menu-item>
    
    <el-menu-item index="5" @click="navigateTo('dataAnalyse')">
      <el-icon><PieChart /></el-icon>
      <template #title><span @wheel="preventDefault">数据分析中心</span></template>
    </el-menu-item>
    
    <el-menu-item index="6" @click="navigateTo('chat')">
      <el-icon><Service /></el-icon>
      <template #title><span @wheel="preventDefault">与AI聊天</span></template>
    </el-menu-item>
    
    <el-menu-item index="7" @click="navigateTo('setting')">
      <el-icon><Setting /></el-icon>
      <template #title><span @wheel="preventDefault">设置</span></template>
    </el-menu-item>
    
  </el-menu>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import {
  Setting,
  DataBoard,
  Tools,
  User,
  Fold,
  Expand,
  PieChart,
  Service
} from '@element-plus/icons-vue'

const router = useRouter()
const isCollapse = ref(true)

const handleOpen = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
}

const handleClose = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
}

const toggleCollapse = () => {
  isCollapse.value = !isCollapse.value
}

const navigateTo = (path: string) => {
  router.push(`/home/${path}`)
}

// 阻止默认行为
const preventDefault = (event: Event) => {
  event.preventDefault()
}
</script>

<style scoped>
.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 200px;
}

.el-menu--collapse {
  width: 64px;
}
</style>