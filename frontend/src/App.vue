<script setup lang="ts">
import Navbar from './components/Navbar.vue'
</script>

<template>
  <div class="flex flex-col h-screen" >
    <!-- 导航栏保持在顶部，不随路由切换而变化 -->
    <Navbar />
    
    <!-- 路由内容区域，添加过渡动画 -->
    <div class="content overflow-y-auto hide-scrollbar">
        <router-view />
    </div>
  </div>
</template>

