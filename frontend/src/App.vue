<script setup lang="ts">
import Navbar from './components/Navbar.vue'
</script>

<template>
  <div class="app" >
    <!-- 导航栏保持在顶部，不随路由切换而变化 -->
    <Navbar />
    
    <!-- 路由内容区域，添加过渡动画 -->
    <div class="content">
        <router-view />
    </div>
  </div>
</template>

<style>

/* 确保内容区域占满剩余空间 */
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.content {
  flex: 1;
}

.no-scroll {
  overflow: hidden !important;
  height: 100vh !important;
}

/* 全局禁止滚动 */
body.no-scroll {
  overflow: hidden !important;
  height: 100vh !important;
}

</style>
