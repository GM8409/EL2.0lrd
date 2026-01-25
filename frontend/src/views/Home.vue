<template>
  <div class="home-container flex">
    <!-- 侧边栏 -->
    <div class="sticky top-[70px] h-[calc(100vh-70px)]">
      <Sidebar />
    </div>
    <!-- 主内容区 -->
    <div id="main-content" 
    class=" flex-1 overflow-y-auto h-screen hide-scrollbar bg-[#f5f7fa] transition-margin-left">
      <router-view />
    </div>
  </div>
</template>

<script lang="ts" setup>
import Sidebar from '@/components/Sidebar.vue'

</script>
