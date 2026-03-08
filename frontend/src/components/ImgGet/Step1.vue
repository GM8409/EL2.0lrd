<template>
  <div class="">
    <hr class="mb-4 border border-gray-300">
    
    <!-- 搜索框 -->
    <div class="mb-4">
      <el-input
        v-model="searchKeyword"
        placeholder="搜索数据集（如 Sentinel、Landsat 等）"
        style="width: 100%"
        prefix-icon="el-icon-search"
        @keyup.enter="handleSearch"
      >
        <template #append>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
        </template>
      </el-input>
    </div>
    
    <!-- 搜索结果列表 -->
    <div class="mb-4 max-h-[200px] overflow-auto hide-scrollbar">
      <el-table
        v-loading="loading"
        :data="datasets"
        style="width: 100%;"
        @row-click="handleDatasetSelect"
        :row-class-name="tableRowClassName"
      >
        <el-table-column label="数据集" min-width="200">
          <template #default="scope">
            <div class="dataset-item">
              <div class="dataset-title">{{ scope.row.name }}</div>
              <div class="dataset-time">{{ scope.row.数据集可用时间 }}</div>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="频率" label="频率" width="100" />
      </el-table>
    </div>
    
    <!-- 选中的数据集信息 -->
    <SelectedDatasetPanel :selectedDataset="selectedDataset" />
    
    <el-button 
      class="float-right" 
      type="primary" 
      @click="handleNext" 
      style="width: 30%"
      :disabled="!selectedDataset"
    >
      <el-icon><ArrowRight /></el-icon> 下一步
    </el-button>
  
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { ArrowRight } from '@element-plus/icons-vue';
import { searchDatasets, getSelectedDataset, saveStep1FormData } from '@/tools/apiService';
import config from '@/config';
import SelectedDatasetPanel from './SelectedDatasetPanel.vue';

const emit = defineEmits(['next-step']);

// 搜索相关
const searchKeyword = ref('');
const loading = ref(false);
const datasets = ref([]);
const selectedDataset = ref(null);

// 处理搜索
const handleSearch = async () => {
  try {
    loading.value = true;
    const result = await searchDatasets({
      keyword: searchKeyword.value
    });
    if (result.status === 'success') {
      datasets.value = result.datasets;
    }
  } catch (error) {
    console.error('Failed to search datasets:', error);
  } finally {
    loading.value = false;
  }
};

// 处理数据集选择
const handleDatasetSelect = (row) => {
  selectedDataset.value = row;
};

// 表格行样式
const tableRowClassName = ({ row }) => {
  return selectedDataset.value && row.id === selectedDataset.value.id ? 'el-table__row--highlight' : '';
};

// 处理下一步
const handleNext = async () => {
  if (selectedDataset.value) {
    // 保存选中的数据集到本地存储
    localStorage.setItem(config.SELECTED_DATASET_KEY, JSON.stringify(selectedDataset.value));
    
    // 保存Step1表单数据
    saveStep1FormData({
      searchKeyword: searchKeyword.value,
      selectedDatasetId: selectedDataset.value.id
    });
    
    console.log('Selected dataset saved:', selectedDataset.value);
    emit('next-step');
  }
};

// 生命周期钩子
onMounted(async () => {
  // 从localStorage加载数据
  const savedDataset = getSelectedDataset();
  if (savedDataset) {
    selectedDataset.value = savedDataset;
  }
  
  // 初始加载一些数据集
  await handleSearch();
});
</script>

<style scoped>
.el-table__row--highlight {
  background-color: #ecf5ff !important;
}

.dataset-item {
  padding: 4px 0;
}

.dataset-title {
  font-weight: 500;
  margin-bottom: 2px;
}

.dataset-time {
  font-size: 12px;
  color: #909399;
}
</style>
