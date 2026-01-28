<template>
  <div class="results-list">
    <div class="results-header">
      <h3>影像筛选结果</h3>
      <el-button type="primary" size="small" @click="$emit('show-download')">
        下载设置
      </el-button>
    </div>
    
    <div class="params-summary">
      <h4>采集参数</h4>
      <div class="param-item">
        <span class="param-label">研究区:</span>
        <span class="param-value">{{ selectedProvince || '未选择' }}</span>
      </div>
      <div class="param-item">
        <span class="param-label">日期范围:</span>
        <span class="param-value">{{ dateRange || '未选择' }}</span>
      </div>
      <div class="param-item">
        <span class="param-label">云量限制:</span>
        <span class="param-value">{{ cloudLimit || '未设置' }}%</span>
      </div>
      <div class="param-item">
        <span class="param-label">采集ID:</span>
        <span class="param-value">{{ collectionId || '未生成' }}</span>
      </div>
    </div>
    
    <div class="download-section">
      <el-button type="success" @click="$emit('show-download')">
        <el-icon><Download /></el-icon> 下载影像
      </el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, defineEmits } from 'vue';
import { Download } from '@element-plus/icons-vue';

const emit = defineEmits(['show-download']);

// 参数信息
const selectedProvince = ref('陕西省');
const dateRange = ref('2023-01-01 至 2023-02-01');
const cloudLimit = ref(20);
const collectionId = ref('CID_20230101_123456');

// 从本地存储获取参数
onMounted(() => {
  try {
    const step1Data = JSON.parse(localStorage.getItem('imgGetStep1') || '{}');
    if (step1Data.province) {
      selectedProvince.value = step1Data.province;
    }
    if (step1Data.dateRange) {
      dateRange.value = `${step1Data.dateRange[0]} 至 ${step1Data.dateRange[1]}`;
    }
    if (step1Data.cloud) {
      cloudLimit.value = step1Data.cloud;
    }
  } catch (error) {
    console.error('Error loading data from localStorage:', error);
  }
});
</script>

<style scoped>
.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.results-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: bold;
}

.params-summary {
  background-color: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.params-summary h4 {
  margin-top: 0;
  margin-bottom: 15px;
  font-size: 16px;
}

.param-item {
  margin-bottom: 10px;
  display: flex;
  justify-content: space-between;
}

.param-label {
  font-weight: 500;
  color: #666;
}

.param-value {
  color: #333;
}

.download-section {
  margin-bottom: 20px;
}
</style>