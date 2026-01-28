<template>
  <div class="w-full">
   
    <hr class="mb-4 border border-gray-300">
    <el-form :model="formData" :rules="rules" ref="formRef" label-width="100px">
      <el-form-item 
      label="研究区"
      label-position="left"
      required>
        <el-select
          v-model="formData.province"
          placeholder="请选择研究区"
          style="width: 100%"
          required
        >
          <el-option value="roi">自定义研究区</el-option>
          <el-option value="北京市">北京市</el-option>
          <el-option value="天津市">天津市</el-option>
          <el-option value="河北省">河北省</el-option>
          <el-option value="河南省">河南省</el-option>
          <el-option value="安徽省">安徽省</el-option>
          <el-option value="江苏省">江苏省</el-option>
          <el-option value="浙江省">浙江省</el-option>
          <el-option value="上海市">上海市</el-option>
          <el-option value="江西省">江西省</el-option>
          <el-option value="湖北省">湖北省</el-option>
          <el-option value="湖南省">湖南省</el-option>
          <el-option value="福建省">福建省</el-option>
          <el-option value="广东省">广东省</el-option>
          <el-option value="广西壮族自治区">广西壮族自治区</el-option>
          <el-option value="贵州省">贵州省</el-option>
          <el-option value="云南省">云南省</el-option>
          <el-option value="四川省">四川省</el-option>
          <el-option value="重庆市">重庆市</el-option>
          <el-option value="陕西省">陕西省</el-option>
          <el-option value="甘肃省">甘肃省</el-option>
          <el-option value="新疆维吾尔自治区">新疆维吾尔自治区</el-option>
          <el-option value="青海省">青海省</el-option>
          <el-option value="西藏自治区">西藏自治区</el-option>
          <el-option value="内蒙古自治区">内蒙古自治区</el-option>
          <el-option value="宁夏回族自治区">宁夏回族自治区</el-option>
          <el-option value="山西省">山西省</el-option>
          <el-option value="山东省">山东省</el-option>
          <el-option value="辽宁省">辽宁省</el-option>
          <el-option value="吉林省">吉林省</el-option>
          <el-option value="黑龙江省">黑龙江省</el-option>
          <el-option value="海南省">海南省</el-option>
          <el-option value="香港特别行政区">香港特别行政区</el-option>
          <el-option value="澳门特别行政区">澳门特别行政区</el-option>
          <el-option value="台湾省">台湾省</el-option>
        </el-select>
      </el-form-item>
       
        <el-form-item
      label="日期范围"
       label-position="left"
       required>
        <el-date-picker
          v-model="formData.dateRange"
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
          v-model="formData.cloud"
          :min="0"
          :max="100"
          :step="5"
          :default-value="20"
          style="width: 100%"
        />
      </el-form-item>

      

    </el-form>
     <el-button class="float-right" type="primary" @click="handleNext" style="width: 30%">
          <el-icon><ArrowRight /></el-icon> 下一步
     </el-button>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { Download , ArrowRight } from '@element-plus/icons-vue';

const emit = defineEmits(['next-step']);
const formRef = ref(null);

const formData = reactive({
  dateRange: null,
  cloud: 20,
  province: ''
});

const rules = {
  dateRange: [
    {
      required: true,
      message: '请选择日期范围',
      trigger: 'change'
    }
  ],
  province: [
    {
      required: true,
      message: '请选择研究区',
      trigger: 'change'
    }
  ]
};

const handleNext = () => {
  if (formRef.value) {
    formRef.value.validate((valid) => {
      if (valid) {
        // 保存表单数据到全局状态或本地存储
        localStorage.setItem('imgGetStep1', JSON.stringify(formData));
        console.log(localStorage.getItem('imgGetStep1'));
        emit('next-step');
      } else {
        console.log('表单验证失败');
      }
    });
  }
};
</script>
