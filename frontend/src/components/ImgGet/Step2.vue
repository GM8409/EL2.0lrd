<template>
  <div class="step2-container">
    <!-- 选中的数据集信息 -->
    <SelectedDatasetPanel :selectedDataset="selectedDataset" />
    
    <!-- 筛选条件表单 -->
    <el-form :model="filterForm" :rules="filterRules" ref="filterFormRef" label-width="100px" class="mb-4">
      <el-form-item 
        label="研究区"
        label-position="left"
        required>
        <div class="flex gap-4">
          <el-radio-group v-model="areaType" @change="handleAreaTypeChange" style="margin-right: 20px">
            <el-radio value="region">行政区划</el-radio>
            <el-radio value="custom">自定义研究区</el-radio>
          </el-radio-group>
        </div>
        
        <div v-if="areaType === 'region'" style="margin-top: 12px;width: 100%">
          <el-cascader
            v-model="regionData"
            :options="regionOptions"
            :props="cascaderProps"
            placeholder="请选择省/市"
            style="width: 100%"
            :loading="loading"
          />
        </div>
        <div v-else-if="areaType === 'custom'" style="margin-top: 12px;width: 100%">
          <el-input
            v-model="filterForm.bounds"
            placeholder="自定义研究区"
            style="width: 100%"
            readonly
            value="roi"
          />
        </div>
      </el-form-item>
       
      <el-form-item
        label="日期范围"
        label-position="left"
        required>
        <el-date-picker
          v-model="filterForm.dateRange"
          type="daterange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          style="width: 100%"
          required
        />
      </el-form-item>

      <el-form-item 
        label="最大云量(%)"
        label-position="left">
        <el-input-number
          v-model="filterForm.cloud"
          :min="0"
          :max="100"
          :step="5"
          :default-value="20"
          style="width: 100%"
        />
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="handleFilterSubmit" style="width: 100%">
          <el-icon><Search /></el-icon> 筛选影像
        </el-button>
      </el-form-item>
    </el-form>
    
    <!-- 筛选结果 -->
    <div v-if="filterResult" class="mb-4 p-4 border border-green-200 rounded bg-green-50">
      <h3 class="text-lg font-semibold mb-2">筛选结果</h3>
      <p><strong>筛选到的影像数量:</strong> {{ filterResult.ids ? filterResult.ids.length : 0 }}</p>
      <p><strong>边界筛选状态:</strong> {{ filterResult.bounds_filtered ? '已筛选' : '未筛选' }}</p>
    </div>
    
    <!-- 影像信息 -->
    <div v-if="filterResult && filterResult.html" class="mb-4">
      <h3 class="text-lg font-semibold mb-2">影像信息</h3>
      <div class=" bg-white small-scrollbar" v-html="filterResult.html"></div>
    </div>

    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="12">
        <el-button @click="handlePrev" style="width: 100%">
          <el-icon><ArrowLeft /></el-icon> 上一步
        </el-button>
      </el-col>
      <el-col :span="12">
        <el-button 
          type="primary" 
          @click="handleNext" 
          style="width: 100%"
          :disabled="!filterResult"
        >
          <el-icon><ArrowRight /></el-icon> 下一步
        </el-button>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue';
import { Search, ArrowLeft, ArrowRight } from '@element-plus/icons-vue';
import { filterImages, getSelectedDataset, getStep2FormData, saveStep2FormData, getFilterResult } from '@/tools/apiService';
import MapManager from '@/tools/mapManager';
import geoDataService from '@/services/GeoDataService';
import config from '@/config';
import SelectedDatasetPanel from './SelectedDatasetPanel.vue';

const emit = defineEmits(['prev-step', 'next-step']);

// 选中的数据集
const selectedDataset = ref(null);

// 筛选表单数据
const filterForm = reactive({
  dateRange: null,
  cloud: 20,
  bounds: '',
  bounds_type: ''
});

// 区域选择类型
const areaType = ref('region');

// 级联选择器数据
const regionData = ref([]);
const regionOptions = ref([]);
const loading = ref(false);

// 筛选结果
const filterResult = ref(null);

// 级联选择器配置
const cascaderProps = {
  value: 'value',
  label: 'label',
  children: 'children',
  checkStrictly: true
};

// 验证规则
const filterRules = {
  dateRange: [
    {
      required: true,
      message: '请选择日期范围',
      trigger: 'change'
    }
  ],
  bounds: [
    {
      required: true,
      message: '请选择研究区',
      trigger: 'change'
    }
  ]
};

// 处理区域类型切换
const handleAreaTypeChange = () => {
  if (areaType.value === 'custom') {
    filterForm.bounds = 'roi';
    filterForm.bounds_type = '';
    regionData.value = [];
  } else {
    filterForm.bounds = '';
    filterForm.bounds_type = '';
  }
  
  // 保存Step2表单数据
  saveStep2FormData({
    areaType: areaType.value,
    bounds: filterForm.bounds,
    bounds_type: filterForm.bounds_type,
    cloud: filterForm.cloud,
    dateRange: filterForm.dateRange,
    regionData: regionData.value
  });
};

// 加载地理数据
const loadGeoData = async () => {
  try {
    loading.value = true;
    
    // 初始化地理数据服务
    await geoDataService.initialize();
    
    // 获取省份数据
    const provinces = geoDataService.getProvinces();
    
    // 构建级联选择器选项
    const options = provinces.map(province => {
      // 获取该省份的城市
      const cities = geoDataService.getCitiesByProvince(province.name);
      
      return {
        value: province.name,
        label: province.name,
        children: cities.map(city => ({
          value: city.name,
          label: city.name
        }))
      };
    });
    
    regionOptions.value = options;
  } catch (error) {
    console.error('Failed to load geo data:', error);
  } finally {
    loading.value = false;
  }
};

// 监听区域数据变化
const updateProvinceData = () => {
  if (regionData.value && regionData.value.length > 0) {
    // 如果选择了城市，使用"省+市"格式；否则使用省份名称
    filterForm.bounds = regionData.value;
    // 设置bounds_type：长度为1表示省份，长度为2表示城市
    filterForm.bounds_type = regionData.value.length === 1 ? 'province' : 'city';
  } else {
    filterForm.bounds = '';
    filterForm.bounds_type = '';
  }
  
  // 保存Step2表单数据
  saveStep2FormData({
    areaType: areaType.value,
    bounds: filterForm.bounds,
    bounds_type: filterForm.bounds_type,
    cloud: filterForm.cloud,
    dateRange: filterForm.dateRange,
    regionData: regionData.value
  });
};

// 监听区域数据变化
watch(regionData, () => {
  updateProvinceData();
}, { deep: true });

// 监听表单数据变化
watch(filterForm, () => {
  // 保存Step2表单数据
  saveStep2FormData({
    areaType: areaType.value,
    bounds: filterForm.bounds,
    bounds_type: filterForm.bounds_type,
    cloud: filterForm.cloud,
    dateRange: filterForm.dateRange,
    regionData: regionData.value
  });
}, { deep: true });

// 处理筛选提交
const handleFilterSubmit = async () => {
  if (!selectedDataset.value) {
    return;
  }
  
  if (filterForm.dateRange) {
    const start_date = filterForm.dateRange[0].toISOString().split('T')[0];
    const end_date = filterForm.dateRange[1].toISOString().split('T')[0];
    
    try {
      loading.value = true;
      const result = await filterImages(selectedDataset.value.id, {
        start_date,
        end_date,
        bounds: filterForm.bounds,
        cloud: filterForm.cloud
      });
      
      if (result.status === 'success') {
        filterResult.value = result;
        // 保存筛选结果到本地存储
        localStorage.setItem(config.FILTER_RESULT_KEY, JSON.stringify(result));
        
        // 如果有筛选地区，缩放到该地区
        if (filterForm.bounds && filterForm.bounds !== 'roi') {
          const mapManager = MapManager.getInstance();
          if (Array.isArray(filterForm.bounds)) {
            // 处理行政区划选择
            const regionName = filterForm.bounds[filterForm.bounds.length - 1];
            const geoDataItem = geoDataService.getGeoDataItemByName(regionName);
            if (geoDataItem) {
              await mapManager.handleRegionSelected(geoDataItem, false);
            }
          }
        }
      }
    } catch (error) {
      console.error('Failed to filter images:', error);
    } finally {
      loading.value = false;
    }
  }
};

// 导航函数
const handlePrev = () => {
  emit('prev-step');
};

const handleNext = () => {
  if (filterResult.value) {
    emit('next-step');
  }
};

// 生命周期钩子
onMounted(async () => {
  // 加载选中的数据集
  const savedDataset = getSelectedDataset();
  if (savedDataset) {
    selectedDataset.value = savedDataset;
  }
  
  // 加载Step2表单数据
  const savedStep2Data = getStep2FormData();
  if (savedStep2Data) {
    if (savedStep2Data.areaType) {
      areaType.value = savedStep2Data.areaType;
    }
    if (savedStep2Data.bounds) {
      filterForm.bounds = savedStep2Data.bounds;
    }
    if (savedStep2Data.bounds_type) {
      filterForm.bounds_type = savedStep2Data.bounds_type;
    }
    if (savedStep2Data.cloud) {
      filterForm.cloud = savedStep2Data.cloud;
    }
    if (savedStep2Data.dateRange) {
      // 转换日期字符串为Date对象
      if (Array.isArray(savedStep2Data.dateRange)) {
        filterForm.dateRange = savedStep2Data.dateRange.map(dateStr => new Date(dateStr));
      }
    }
    if (savedStep2Data.regionData) {
      regionData.value = savedStep2Data.regionData;
    }
  }
  
  // 加载筛选结果
  const savedFilterResult = getFilterResult();
  if (savedFilterResult) {
    filterResult.value = savedFilterResult;
  }
  
  // 加载地理数据
  await loadGeoData();
});
</script>

<style scoped>
.step2-container {
  width: 100%;
}

.text-center {
  text-align: center;
}

.mb-4 {
  margin-bottom: 16px;
}


</style>