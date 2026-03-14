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
        <p><strong>CID:</strong> {{ selectedDataset.cid }}</p>
        <p><strong>名称:</strong> {{ selectedDataset.name }}</p>
        <p><strong>分辨率:</strong> {{ formatPixelSize(selectedDataset.pixel_size_num) }}</p>
        <p><strong>可用时间:</strong> {{ getDatasetTimeRange(selectedDataset) }}</p>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { ArrowUp, ArrowDown } from '@element-plus/icons-vue';
import { type SearchData } from '@/config';

const props = defineProps<{
  selectedDataset: SearchData | null;
}>();

const isDatasetInfoExpanded = ref(true);

const toggleDatasetInfo = () => {
  isDatasetInfoExpanded.value = !isDatasetInfoExpanded.value;
};

// 格式化日期显示
const formatDateDisplay = (dateStr: string) => {
  if (dateStr === '至今') {
    return dateStr;
  }
  try {
    const date = new Date(dateStr);
    return date.getFullYear().toString();
  } catch {
    return dateStr;
  }
};

// 格式化数据集时间覆盖范围
const getDatasetTimeRange = (dataset: SearchData) => {
  const startYear = formatDateDisplay(dataset.date_start);
  const endYear = formatDateDisplay(dataset.date_end);
  return `${startYear} - ${endYear}`;
};

// 格式化像素分辨率显示
const formatPixelSize = (pixelSizeNum: number | null) => {
  if (pixelSizeNum === null) {
    return '未知';
  }
  return `${pixelSizeNum} 米`;
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