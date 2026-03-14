<template>
  <div class="w-full pb-8">
     <!-- 影像信息 -->
    <div v-if="filterResult && filterResult.html" class="mb-4">
      <h3 class="text-lg font-semibold mb-2">影像信息</h3>
      <div class=" bg-white" v-html="filterResult.html"></div>
    </div>

    <h2 class="text-center mb-4">遥感影像可视化参数配置</h2>
    
    <el-tabs v-model="activeTab" class="mb-4">
      <!-- 基础设置标签页 -->
      <el-tab-pane label="基础设置" name="basic">
        <el-form :model="basicForm" :rules="basicRules" ref="basicFormRef" 
        label-position="left">
          <el-form-item label="波段组合" required>
            <el-select
              v-model="basicForm.bands"
              multiple
              placeholder="请选择波段组合"
              style="width: 100%"
            >
              <template v-if="bandOptions.length > 0">
                <el-option
                  v-for="option in bandOptions"
                  :key="option.value"
                  :value="option.value"
                  :label="option.label"
                />
              </template>
              <template v-else>
                <el-option value="" disabled>No bands available</el-option>
              </template>
            </el-select>
          </el-form-item>
          
          <el-form-item label="拉伸范围" required>
            <el-row :gutter="10">
              <el-col :span="12">
                <el-input-number
                  v-model="basicForm.min"
                  placeholder="最小值"
                  style="width: 100%"
                />
              </el-col>
            
              <el-col :span="12">
                <el-input-number
                  v-model="basicForm.max"
                  placeholder="最大值"
                  style="width: 100%"
                />
              </el-col>
            </el-row>
          </el-form-item>
          
          <el-form-item label="选择可视化影像" required label-position="top">
            <div class="border border-gray-200 rounded p-4 bg-white hide-scrollbar max-h-80 w-full overflow-y-auto">
              <template v-if="imageOptions.length > 0">
                <el-checkbox-group v-model="basicForm.selectedImages" style="width: 100%">
                  <div 
                    v-for="image in imageOptions" 
                    :key="image.value"
                    class="flex items-center p-2 border-b border-gray-100 hover:bg-gray-50"
                  >
                    <el-checkbox :label="image.value">
                      <div class="flex-1">
                        <div class="text-sm font-medium">{{ image.index }}. {{ image.prefix }}</div>
                        <div class="text-xs text-gray-500">{{ image.name }}</div>
                      </div>
                    </el-checkbox>
                  </div>
                </el-checkbox-group>
              </template>
              <template v-else>
                <div class="text-center text-gray-500 py-4">No images available</div>
              </template>
            </div>
          </el-form-item>
        </el-form>
      </el-tab-pane>
      
      <!-- 高级设置标签页 -->
      <el-tab-pane label="高级设置" name="advanced">
        <el-form :model="advancedForm" ref="advancedFormRef" label-width="auto" label-position="left">
          <el-form-item label="Gamma校正">
            <el-input-number
              v-model="advancedForm.gamma"
              :min="0.1"
              :max="3"
              :step="0.1"
              :default-value="1.0"
              style="width: 100%"
            />
          </el-form-item>
          
          <el-form-item label="透明度">
            <el-slider
              v-model="advancedForm.opacity"
              :min="0"
              :max="1"
              :step="0.1"
              style="width: 90%"
            />
          </el-form-item>
          
          <el-form-item label="波段计算">
            <el-input
              v-model="advancedForm.bandsMath"
              type="textarea"
              :rows="3"
              placeholder="示例: (b('B5') - b('B4')) / (b('B5') + b('B4'))"
              style="width: 100%"
            />
          </el-form-item>
          
          <el-form-item>
            <el-checkbox v-model="advancedForm.useNormalize">自动归一化到[0, 255]</el-checkbox>
          </el-form-item>
          
          <el-form-item>
            <el-checkbox v-model="advancedForm.medianComposite">中值合成</el-checkbox>
          </el-form-item>
          
          <el-form-item>
            <el-checkbox v-model="advancedForm.areaMask">按选定研究区掩膜提取</el-checkbox>
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
        <el-button type="primary" @click="handleSubmit" style="width: 100%">
          <el-icon><VideoPlay /></el-icon> 应用可视化参数
        </el-button>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue';
import { ArrowLeft, VideoPlay } from '@element-plus/icons-vue';
import { getMapUrlsFromStorage, getImageMapUrl } from '@/tools/apiService';
import { getFilterResult, getVisualParams, saveVisualParams } from '@/tools/storageManager';
import MapManager from '@/tools/mapManager';

const mapManager = MapManager.getInstance();

const emit = defineEmits(['prev-step']);
const activeTab = ref('basic');
const filterResult = ref(null);

// 基础设置表单
const basicFormRef = ref(null);
const basicForm = reactive({
  bands: [],
  min: 0,
  max: 10000,
  selectedImages: []
});

// 高级设置表单
const advancedFormRef = ref(null);
const advancedForm = reactive({
  gamma: 1.0,
  opacity: 1,
  bandsMath: '',
  useNormalize: false,
  medianComposite: false,
  areaMask: false
});

// 计算属性：获取波段列表
const bandOptions = computed(() => {
  // 新的API暂时不返回详细的波段信息，这里使用空数组作为占位
  return [];
});

// 计算属性：获取影像列表
const imageOptions = computed(() => {
  if (!filterResult.value || !filterResult.value.images || filterResult.value.images.length === 0) {
    return [];
  }
  
  return filterResult.value.images.map((image, index) => {
    const id = image.id;
    const parts = id.split('/');
    const name = parts.pop() || id;
    const prefix = parts.join('/');
    return {
      value: id,
      index: index + 1,
      prefix: prefix,
      name: name
    };
  });
});

const basicRules = {
  bands: [
    {
      required: true,
      message: '请选择波段组合',
      trigger: 'change'
    }
  ],
  min: [
    {
      required: true,
      message: '请输入最小值',
      trigger: 'blur'
    }
  ],
  max: [
    {
      required: true,
      message: '请输入最大值',
      trigger: 'blur'
    }
  ],
  selectedImages: [
    {
      required: true,
      message: '请选择至少一张影像',
      trigger: 'change'
    }
  ]
};

// 导航函数
const handlePrev = () => {
  emit('prev-step');
};

// 提交函数
const handleSubmit = () => {
  if (basicFormRef.value) {
    basicFormRef.value.validate((valid) => {
      if (valid) {
        // 保存表单数据
        const visualParams = {
          basic: basicForm,
          advanced: advancedForm
        };
        saveVisualParams(visualParams);
        console.log('可视化参数提交:', visualParams);
        
        // 新的API调用逻辑（待完善，因为新API是针对单个影像的）
        console.log('使用新的API方法获取地图URL');
        
        // 老方法（已注释）
        // 调用API获取地图URL
        // getMapUrlsFromStorage().then((response) => {
        //   console.log('获取地图URL成功:', response);
        //   
        //   // 清理之前的影像图层
        //   mapManager.clearImageLayers();
        //   
        //   // 从本地存储中获取选中的影像ID
        //   const visParams = getVisualParams();
        //   const { selectedImages } = visParams.basic;
        //   
        //   // 获取地图URL列表
        //   const mapUrls = response.result;
        //   
        //   // 遍历地图URL列表，添加到地图上
        //   if (Array.isArray(mapUrls) && mapUrls.length > 0) {
        //     mapUrls.forEach((mapUrl, index) => {
        //       if (mapUrl && selectedImages[index]) {
        //         // 从影像ID中截取最后一个斜杠的后半部分作为图层名称
        //         const imageId = selectedImages[index];
        //         const layerName = imageId.split('/').pop() || imageId;
        //         
        //         // 创建Leaflet图层
        //         const layer = L.tileLayer(mapUrl, {
        //           attribution: 'Google Earth Engine'
        //         });
        //         
        //         // 添加图层到地图
        //         mapManager.addImageLayer(layer, layerName, true);
        //       }
        //     });
        //   }
        // }).catch((error) => {
        //   console.error('获取地图URL失败:', error);
        // });
      }
    });
  }
};

// 生命周期钩子
onMounted(() => {
  // 加载筛选结果
  filterResult.value = getFilterResult();
  
  // 加载可视化参数
  const savedVisualParams = getVisualParams();
  if (savedVisualParams) {
    if (savedVisualParams.basic) {
      basicForm.bands = savedVisualParams.basic.bands || [];
      basicForm.min = savedVisualParams.basic.min || 0;
      basicForm.max = savedVisualParams.basic.max || 10000;
      basicForm.selectedImages = savedVisualParams.basic.selectedImages || [];
    }
    if (savedVisualParams.advanced) {
      advancedForm.gamma = savedVisualParams.advanced.gamma || 1.0;
      advancedForm.opacity = savedVisualParams.advanced.opacity || 1;
      advancedForm.bandsMath = savedVisualParams.advanced.bandsMath || '';
      advancedForm.useNormalize = savedVisualParams.advanced.useNormalize || false;
      advancedForm.medianComposite = savedVisualParams.advanced.medianComposite || false;
      advancedForm.areaMask = savedVisualParams.advanced.areaMask || false;
    }
  }
  
  // 新的API暂时不返回详细的波段信息，使用默认值
  if (!savedVisualParams || !savedVisualParams.basic) {
    basicForm.min = 0;
    basicForm.max = 10000;
  }
});
</script>

<style scoped>

.text-center {
  text-align: center;
}

.mb-4 {
  margin-bottom: 16px;
}
</style>