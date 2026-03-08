<template>
  <div v-if="selectedDataset" class="mb-4 p-4 border border-blue-200 rounded bg-blue-50">
    <div class="flex justify-between items-center mb-2">
      <h3 class="text-lg font-semibold">选中的数据集</h3>
      <el-button 
        type="text" 
        @click="toggleDatasetInfo"
        size="small"
      >
        <el-icon v-if="isDatasetInfoExpanded"><ArrowUp /></el-icon>
        <el-icon v-else><ArrowDown /></el-icon>
      </el-button>
    </div>
    <transition name="fade">
      <div v-if="isDatasetInfoExpanded">
        <p><strong>ID:</strong> {{ selectedDataset.id }}</p>
        <p><strong>名称:</strong> {{ selectedDataset.name }}</p>
        <p><strong>频率:</strong> {{ selectedDataset.频率 }}</p>
        <p><strong>可用时间:</strong> {{ selectedDataset.数据集可用时间 }}</p>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { ArrowUp, ArrowDown } from '@element-plus/icons-vue';

interface Dataset {
  id: string;
  name: string;
  频率: string;
  数据集可用时间: string;
}

const props = defineProps<{
  selectedDataset: Dataset | null;
}>();

const isDatasetInfoExpanded = ref(true);

const toggleDatasetInfo = () => {
  isDatasetInfoExpanded.value = !isDatasetInfoExpanded.value;
};
</script>

<style scoped>
/* 展开/收起动画 */
.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
  max-height: 200px;
  overflow: hidden;
}

.fade-enter-from,
.fade-leave-to {
  max-height: 0;
  opacity: 0;
  overflow: hidden;
}
</style>