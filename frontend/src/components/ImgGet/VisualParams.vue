<template>
  <div class="w-full pb-8">
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
              <el-option value="B1">B1 (蓝)</el-option>
              <el-option value="B2">B2 (绿)</el-option>
              <el-option value="B3">B3 (红)</el-option>
              <el-option value="B4">B4 (近红外)</el-option>
              <el-option value="B5">B5 (短波红外1)</el-option>
              <el-option value="B6">B6 (短波红外2)</el-option>
              <el-option value="B7">B7 (短波红外3)</el-option>
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
          
          <el-form-item label="可视化影像张数" required>
            <el-input-number
              v-model="basicForm.imageCount"
              :min="1"
              :max="10"
              :step="1"
              :default-value="1"
              style="width: 100%"
            />
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
import { ref, reactive, onMounted } from 'vue';
import { ArrowLeft, VideoPlay } from '@element-plus/icons-vue';

const emit = defineEmits(['prev-step']);
const activeTab = ref('basic');

// 基础设置表单
const basicFormRef = ref(null);
const basicForm = reactive({
  bands: [],
  min: 0,
  max: 10000,
  imageCount: 1
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
  imageCount: [
    {
      required: true,
      message: '请输入可视化影像张数',
      trigger: 'blur'
    }
  ]
};

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
        localStorage.setItem('imgGetVisualParams', JSON.stringify(visualParams));
        console.log('可视化参数提交:', visualParams);
        
        // 这里可以添加API调用逻辑
        alert('可视化参数已应用');
      }
    });
  }
};
</script>

<style scoped>

.text-center {
  text-align: center;
}

.mb-4 {
  margin-bottom: 16px;
}
</style>