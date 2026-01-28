<template>
  <div class="step2-container">
    
    <el-tabs v-model="activeTab" class="mb-4">
      <!-- Landsat 标签页 -->
      <el-tab-pane label="Landsat" name="landsat">
        <el-form :model="landsatForm" :rules="landsatRules" ref="landsatFormRef">
          <el-form-item label="卫星类型" label-position="left" required>
            <el-select
              v-model="landsatForm.satellite"
              placeholder="请选择卫星类型"
              style="width: 100%"
            >
              <el-option value="LANDSAT/LM01/C02/">Landsat1-5MSS(1972-1999)</el-option>
              <el-option value="LANDSAT/LT04/C02/">Landsat4TM(1982-1993)</el-option>
              <el-option value="LANDSAT/LT05/C02/">Landsat5TM(1984-2012)</el-option>
              <el-option value="LANDSAT/LE07/C02/">Landsat7ETM+(1999-2021)</el-option>
              <el-option value="LANDSAT/LC08/C02/">Landsat8OLI/TIRS(2013至今)</el-option>
              <el-option value="LANDSAT/LC09/C02/">Landsat9OLI-2/TIRS-2(2021至今)</el-option>
            </el-select>
          </el-form-item>
          
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="数据类型" required>
                <el-select
                  v-model="landsatForm.category"
                  placeholder="Raw Images"
                  style="width: 100%"
                >
                  <el-option value="">Raw Images</el-option>
                  <el-option value="_TOA">Top of Atmosphere(表观反射率)</el-option>
                  <el-option value="_L2">Surface Reflectance(地表真实反射率)</el-option>
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="图像级别" required>
                <el-select
                  v-model="landsatForm.tier"
                  placeholder="请选择图像级别"
                  style="width: 100%"
                >
                  <el-option value="T1">Tier1</el-option>
                  <el-option value="T2">Tier2</el-option>
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>
          
    
            <el-button type="primary" @click="handleLandsatSubmit" style="width: 100%">
              <el-icon><Upload /></el-icon> 筛选该影像集
            </el-button>
          
        </el-form>
      </el-tab-pane>
      
      <!-- MODIS 标签页 -->
      <el-tab-pane label="MODIS" name="modis">
        <el-form :model="modisForm" :rules="modisRules" ref="modisFormRef" 
        label-width="auto" label-position="left">
          <el-form-item label="产品类型" required>
            <el-select
              v-model="modisForm.product"
              placeholder="请选择产品类型"
              style="width: 100%"
              @change="handleModisProductChange"
            >
              <el-option value="land">陆地产品 (植被/土地覆盖)</el-option>
              <el-option value="atmosphere">大气产品 (气溶胶/云)</el-option>
              <el-option value="ocean">海洋产品 (水色/海温)</el-option>
              <el-option value="ice">冰雪产品 (积雪/海冰)</el-option>
            </el-select>
          </el-form-item>
          
          <el-form-item label="推荐的数据集" required>
            <el-select
              v-model="modisForm.parameter"
              placeholder="请先选择产品类型"
              style="width: 100%"
            >
              <el-option
                v-for="option in modisParameters"
                :key="option.value"
                :label="option.label"
                :value="option.value"
              />
            </el-select>
          </el-form-item>
          
         
            <el-button type="primary" @click="handleModisSubmit" style="width: 100%">
              <el-icon><Upload /></el-icon> 筛选该影像集
            </el-button>
          
        </el-form>
      </el-tab-pane>
      
      <!-- Sentinel 标签页 -->
      <el-tab-pane label="Sentinel" name="sentinel">
        <el-form :model="sentinelForm" :rules="sentinelRules" ref="sentinelFormRef" label-width="auto">
          <el-form-item label="卫星类型" required>
            <el-select
              v-model="sentinelForm.satellite"
              placeholder="请选择卫星类型"
              style="width: 100%"
            >
              <el-option value="COPERNICUS/S2_SR_HARMONIZED">S2_SR_HARMONIZED(光学SR)</el-option>
              <el-option value="COPERNICUS/S2_HARMONIZED">S2_HARMONIZED(光学TOA)</el-option>
              <el-option value="COPERNICUS/S1_GRD">S1_GRD(合成孔径雷达)</el-option>
              <el-option value="COPERNICUS/S3/SLSTR">S3/SLSTR(海洋与陆地)</el-option>
            </el-select>
          </el-form-item>
          
          <el-form-item>
            <el-button type="primary" @click="handleSentinelSubmit" style="width: 100%">
              <el-icon><Upload /></el-icon> 筛选该影像集
            </el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>
    </el-tabs>

    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="12">
        <el-button @click="handlePrev" style="width: 100%">
          <el-icon><ArrowLeft /></el-icon> 上一步
        </el-button>
      </el-col>
      <el-col :span="12">
        <el-button type="primary" @click="handleNext" style="width: 100%">
          <el-icon><ArrowRight /></el-icon> 下一步
        </el-button>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch } from 'vue';
import { Upload, ArrowLeft, ArrowRight } from '@element-plus/icons-vue';

const emit = defineEmits(['prev-step', 'next-step']);
const activeTab = ref('landsat');

// Landsat表单
const landsatFormRef = ref(null);
const landsatForm = reactive({
  satellite: '',
  category: '',
  tier: ''
});

const landsatRules = {
  satellite: [
    {
      required: true,
      message: '请选择卫星类型',
      trigger: 'change'
    }
  ],
  category: [
    {
      required: true,
      message: '请选择数据类型',
      trigger: 'change'
    }
  ],
  tier: [
    {
      required: true,
      message: '请选择图像级别',
      trigger: 'change'
    }
  ]
};

// MODIS表单
const modisFormRef = ref(null);
const modisForm = reactive({
  product: '',
  parameter: ''
});

const modisRules = {
  product: [
    {
      required: true,
      message: '请选择产品类型',
      trigger: 'change'
    }
  ],
  parameter: [
    {
      required: true,
      message: '请选择推荐的数据集',
      trigger: 'change'
    }
  ]
};

// MODIS参数选项
const modisParameters = computed(() => {
  const parameters = {
    land: [
      { value: 'MODIS/061/MOD13Q1', label: 'MOD13Q1 (植被指数, 16天, 250m)' },
      { value: 'MODIS/061/MOD13A1', label: 'MOD13A1 (植被指数, 16天, 500m)' },
      { value: 'MODIS/061/MCD12Q1', label: 'MCD12Q1 (土地覆盖类型, 年度, 500m)' }
    ],
    atmosphere: [
      { value: 'MODIS/061/MOD04_3K', label: 'MOD04_3K (气溶胶, 1天, 3km)' },
      { value: 'MODIS/061/MOD08_M3', label: 'MOD08_M3 (大气参数, 月度, 1度)' }
    ],
    ocean: [
      { value: 'MODIS/061/MODIS_Terra_Aqua_CorrectedReflectance_TrueColor', label: 'MODIS真彩色影像' },
      { value: 'MODIS/061/MY1DMM_CHLA', label: 'MY1DMM_CHLA (叶绿素a, 月度, 4km)' }
    ],
    ice: [
      { value: 'MODIS/061/MOD10A1', label: 'MOD10A1 (积雪覆盖, 1天, 500m)' },
      { value: 'MODIS/061/MOD29', label: 'MOD29 (海冰浓度, 1天, 25km)' }
    ]
  };
  return parameters[modisForm.product] || [];
});

const handleModisProductChange = () => {
  modisForm.parameter = '';
};

// Sentinel表单
const sentinelFormRef = ref(null);
const sentinelForm = reactive({
  satellite: ''
});

const sentinelRules = {
  satellite: [
    {
      required: true,
      message: '请选择卫星类型',
      trigger: 'change'
    }
  ]
};

// 提交函数
const handleLandsatSubmit = () => {
  if (landsatFormRef.value) {
    landsatFormRef.value.validate((valid) => {
      if (valid) {
        // 保存表单数据
        localStorage.setItem('imgGetStep2', JSON.stringify(landsatForm));
        console.log(localStorage.getItem('imgGetStep2'));
        // 这里可以添加API调用逻辑
      }
    });
  }
};

const handleModisSubmit = () => {
  if (modisFormRef.value) {
    modisFormRef.value.validate((valid) => {
      if (valid) {
        // 保存表单数据
        localStorage.setItem('imgGetStep2', JSON.stringify(modisForm));
        console.log(localStorage.getItem('imgGetStep2'));
        // 这里可以添加API调用逻辑
      }
    });
  }
};

const handleSentinelSubmit = () => {
  if (sentinelFormRef.value) {
    sentinelFormRef.value.validate((valid) => {
      if (valid) {
        // 保存表单数据
        localStorage.setItem('imgGetStep2', JSON.stringify(sentinelForm));
        console.log(localStorage.getItem('imgGetStep2'));
        // 这里可以添加API调用逻辑
      }
    });
  }
};


// 导航函数
const handlePrev = () => {
  emit('prev-step');
};

const handleNext = () => {
  emit('next-step');
};
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