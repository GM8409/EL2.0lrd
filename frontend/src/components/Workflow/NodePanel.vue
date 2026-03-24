<template>
  <!-- 可收缩的节点库侧栏 -->
  <div :class="[
    'h-full bg-white border-r border-gray-200 shadow-sm transition-all duration-300 flex flex-col overflow-hidden',
    isExpanded ? 'w-64' : 'w-16'
  ]">
    <!-- 侧边栏头部 -->
    <div class="
      flex items-center justify-between px-4 py-3 border-b border-gray-100 bg-linear-to-r from-blue-50 to-cyan-50
    ">
      <!-- 标题区域：使用透明度和位移实现平滑过渡 -->
      <div :class="[
        'flex items-center gap-2 transition-all duration-300 transform origin-left',
        isExpanded ? 'opacity-100 scale-100 w-auto' : 'opacity-0 scale-95 w-0 pointer-events-none'
      ]">
        <el-icon class="text-blue-600">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="1"></circle>
            <path d="M12 2v6m0 4v6"></path>
            <circle cx="5" cy="5" r="1"></circle>
            <circle cx="19" cy="5" r="1"></circle>
            <circle cx="5" cy="19" r="1"></circle>
            <circle cx="19" cy="19" r="1"></circle>
          </svg>
        </el-icon>
        <span class="font-bold text-gray-800 text-sm whitespace-nowrap">节点库</span>
      </div>

      <!-- 收缩/展开按钮 -->
      <el-button 
        @click="isExpanded = !isExpanded"
        circle
        size="small"
        :title="isExpanded ? '收起侧栏' : '展开侧栏'"
        class="transition-all duration-300 shrink-0 z-10"
      >
        <el-icon :class="['transition-transform duration-300', isExpanded ? '' : 'rotate-180']">
          <ArrowLeft />
        </el-icon>
      </el-button>
    </div>

    <!-- 侧边栏内容区域：使用相对定位包裹两个交替显示的层 -->
    <div class="flex-1 relative">
      <!-- 展开状态的内容层 -->
      <div :class="[
        'absolute inset-0 p-2 overflow-y-auto overflow-x-hidden transition-all duration-300 delay-75 hide-scrollbar',
        isExpanded ? 'opacity-100 translate-x-0' : 'opacity-0 -translate-x-8 pointer-events-none'
      ]">
        <el-collapse v-model="activeNames" class="custom-collapse">
          <!-- I/O节点 -->
          <el-collapse-item name="io">
            <template #title>
              <div class="flex items-center gap-2 font-medium">
                <span><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-pen-icon lucide-pen">
                  <path d="M21.174 6.812a1 1 0 0 0-3.986-3.987L3.842 16.174a2 2 0 0 0-.5.83l-1.321 4.352a.5.5 0 0 0 .623.622l4.353-1.32a2 2 0 0 0 .83-.497z"/></svg></span>
                <span>I/O 节点</span>
              </div>
            </template>
            <div class="p-1 flex flex-col gap-2">
              <el-button type="success" size="small" class="w-full ml-0! justify-start" @click="addInputNode">
                <span class="mr-2"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-file-input-icon lucide-file-input">
                  <path d="M4 11V4a2 2 0 0 1 2-2h8a2.4 2.4 0 0 1 1.706.706l3.588 3.588A2.4 2.4 0 0 1 20 8v12a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2v-1"/>
                  <path d="M14 2v5a1 1 0 0 0 1 1h5"/>
                  <path d="M2 15h10"/><path d="m9 18 3-3-3-3"/></svg></span>输入节点
              </el-button>
              <el-button type="success" size="small" class="w-full ml-0! justify-start" @click="addOutputNode">
                <span class="mr-2"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-file-output-icon lucide-file-output">
                  <path d="M4.226 20.925A2 2 0 0 0 6 22h12a2 2 0 0 0 2-2V8a2.4 2.4 0 0 0-.706-1.706l-3.588-3.588A2.4 2.4 0 0 0 14 2H6a2 2 0 0 0-2 2v3.127"/>
                  <path d="M14 2v5a1 1 0 0 0 1 1h5"/><path d="m5 11-3 3"/><path d="m5 17-3-3h10"/></svg></span>输出节点
              </el-button>
            </div>
          </el-collapse-item>

          <!-- 计算节点 -->
          <el-collapse-item name="calc">
            <template #title>
              <div class="flex items-center gap-2 font-medium">
                <span><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-plus-icon lucide-plus">
                  <path d="M5 12h14"/><path d="M12 5v14"/></svg></span>
                <span>计算节点</span>
              </div>
            </template>
            <div class="p-1 flex flex-col gap-2">
              <el-button type="primary" size="small" class="w-full ml-0! justify-start" @click="addAddNode">
                <span class="mr-2"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-plus-icon lucide-plus"><path d="M5 12h14"/>
                  <path d="M12 5v14"/></svg></span>加法节点
              </el-button>
              <el-button type="primary" size="small" class="w-full ml-0! justify-start" @click="addSubNode">
                <span class="mr-2"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-minus-icon lucide-minus">
                  <path d="M5 12h14"/></svg></span>减法节点
              </el-button>
            </div>
          </el-collapse-item>

          <!-- AI 节点 -->
          <el-collapse-item name="ai">
            <template #title>
              <div class="flex items-center gap-2 font-medium">
                <span><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-bot-icon lucide-bot">
                  <path d="M12 8V4H8"/><rect width="16" height="12" x="4" y="8" rx="2"/>
                  <path d="M2 14h2"/><path d="M20 14h2"/>
                  <path d="M15 13v2"/><path d="M9 13v2"/></svg></span>
                <span>AI 节点</span>
              </div>
            </template>
            <div class="p-1 flex flex-col gap-2">
              <el-button type="info" size="small" class="w-full ml-0! justify-start" @click="addPredictNode">
                <span class="mr-2"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-bot-icon lucide-bot">
                  <path d="M12 8V4H8"/><rect width="16" height="12" x="4" y="8" rx="2"/>
                  <path d="M2 14h2"/><path d="M20 14h2"/>
                  <path d="M15 13v2"/><path d="M9 13v2"/></svg></span>预测节点
              </el-button>
            </div>
          </el-collapse-item>

          <!-- 展示节点 -->
          <el-collapse-item name="display">
            <template #title>
              <div class="flex items-center gap-2 font-medium">
                <span><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-spotlight-icon lucide-spotlight">
                  <path d="M15.295 19.562 16 22"/><path d="m17 16 3.758 2.098"/>
                  <path d="m19 12.5 3.026-.598"/>
                  <path d="M7.61 6.3a3 3 0 0 0-3.92 1.3l-1.38 2.79a3 3 0 0 0 1.3 3.91l6.89 3.597a1 1 0 0 0 1.342-.447l3.106-6.211a1 1 0 0 0-.447-1.341z"/>
                  <path d="M8 9V2"/></svg></span>
                <span>展示节点</span>
              </div>
            </template>
            <div class="p-1 flex flex-col gap-2">
              <el-button type="warning" size="small" class="w-full ml-0! justify-start" @click="addViewImgNode">
                <span class="mr-2"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-image-icon lucide-image">
                  <rect width="18" height="18" x="3" y="3" rx="2" ry="2"/>
                  <circle cx="8.5" cy="8.5" r=".5"/>
                  <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
                </svg></span>图片展示
              </el-button>
            </div>
          </el-collapse-item>

          <!-- 调试工具 -->
          <el-collapse-item name="debug">
            <template #title>
              <div class="flex items-center gap-2 font-medium text-red-600">
                <span><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-bug-icon lucide-bug">
                  <path d="M12 20v-9"/><path d="M14 7a4 4 0 0 1 4 4v3a6 6 0 0 1-12 0v-3a4 4 0 0 1 4-4z"/><path d="M14.12 3.88 16 2"/>
                  <path d="M21 21a4 4 0 0 0-3.81-4"/><path d="M21 5a4 4 0 0 1-3.55 3.97"/><path d="M22 13h-4"/>
                  <path d="M3 21a4 4 0 0 1 3.81-4"/><path d="M3 5a4 4 0 0 0 3.55 3.97"/>
                  <path d="M6 13H2"/><path d="m8 2 1.88 1.88"/><path d="M9 7.13V6a3 3 0 1 1 6 0v1.13"/></svg></span>
                <span>调试工具</span>
              </div>
            </template>
            <div class="p-1 flex flex-col gap-2">
              <el-button type="danger" size="small" class="w-full ml-0! justify-start" @click="nodeManager.step()">
                <span class="mr-2"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-check-icon lucide-check">
                  <path d="M20 6 9 17l-5-5"/></svg></span>单步调试
              </el-button>
              <el-button type="danger" size="small" class="w-full ml-0! justify-start" @click="nodeManager.run()">
                <span class="mr-2"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-check-check-icon lucide-check-check">
                  <path d="M18 6 7 17l-5-5"/>
                  <path d="m22 10-7.5 7.5L13 16"/></svg></span>运行到结束
              </el-button>
              <el-button type="danger" size="small" class="w-full ml-0! justify-start" @click="nodeManager.reset()">
                <span class="mr-2"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-loader-circle-icon lucide-loader-circle">
                  <path d="M21 12a9 9 0 1 1-6.219-8.56"/></svg></span>重置运行
              </el-button>
            </div>
          </el-collapse-item>
        </el-collapse>
      </div>

      <!-- 收缩状态的快捷图标层 -->
      <div :class="[
        'absolute inset-0 flex flex-col items-center  py-4 gap-4 transition-all duration-300',
        !isExpanded ? 'opacity-100 scale-100' : 'opacity-0 scale-75 pointer-events-none'
      ]">
      
        <el-tooltip content="I/O 节点" placement="right">
          <el-button circle type="success" @click="expandAndOpen('io')">📥</el-button>
        </el-tooltip>
        
        <el-tooltip content="计算节点" placement="right">
          <el-button class="ml-0!" circle type="primary" @click="expandAndOpen('calc')">➕</el-button>
        </el-tooltip>
        <el-tooltip content="AI 节点" placement="right">
          <el-button class="ml-0!" circle type="info" @click="expandAndOpen('ai')">🤖</el-button>
        </el-tooltip>
        <el-tooltip content="展示节点" placement="right">
          <el-button class="ml-0!" circle type="warning" @click="expandAndOpen('display')">🖼️</el-button>
        </el-tooltip>
        <el-tooltip content="调试工具" placement="right">
          <el-button class="ml-0!" circle type="danger" @click="expandAndOpen('debug')">🛠️</el-button>  
        </el-tooltip>
      </div>
    </div>
  </div>
</template>

<script setup>
import { inject, ref, watch } from 'vue'
import { random_pos } from '../../tools/nodeManager'
import { ArrowLeft, ArrowRight } from '@element-plus/icons-vue'

const nodeManager = inject('node_manager')

// 响应式状态
const isExpanded = ref(true)
const activeNames = ref(['io'])

// 节点操作逻辑
const addInputNode = () => {
  nodeManager.addInput({value:'默认输入'})
  nodeManager.addNode({
    id:'start',
    type:'Start',
    position: random_pos(),
    style_data:nodeManager.initial_data,
  })
}

const addOutputNode = () => {
  nodeManager.addNode({
    id:'end',
    type:'Output',
    position: random_pos(),
    style_data:{value: '正在等待数据...'},
    func:(data)=>{nodeManager.flow.updateNodeData('end',{value: data})},
  })
}

const addAddNode = () => {
  nodeManager.addNode({
    id:'add_'+Date.now(),
    type:'Add',
    position: random_pos(),
    style_data:{value: 2},
    func:(data)=>Number(data.value? data.value:data)+2,
    description:'加法节点',
  })
}

const addSubNode = () => {
  nodeManager.addNode({
    id:'sub_'+Date.now(),
    type:'Subtract',
    position: random_pos(),
    style_data:{value: 2},
    func:(data)=>Number(data.value? data.value:data)-2,
    description:'减法节点',
  })
}

const addPredictNode = () => {
  nodeManager.addNode({
    id:'start',  
    type:'Predict',
    position: random_pos(),
    style_data:{value: ''},
    func:()=>{},
    description:'预测节点',
  })
  watch(()=>nodeManager.flow.findNode('start')?.data?.value, (newVal)=>{
    if(newVal) nodeManager.addInput(newVal)
  })
}

const addViewImgNode = () => {
  nodeManager.addNode({
    id:'viewimg',
    type:'ViewImg',
    position: random_pos(),
    style_data:{imageUrl: ''},
    func:(data)=>{
      nodeManager.flow.updateNodeData('viewimg',{
        imageUrl: data.img_url,
        status:data.status,
      })
    },
    description:'图片展示节点',
  })
}

const expandAndOpen = (name) => {
  isExpanded.value = true
  activeNames.value = [name]
}
</script>

<style scoped>
@reference 'tailwindcss';

.custom-collapse {
  @apply border-none bg-transparent;
}
:deep(.el-collapse-item__header) {
  @apply px-2 border-b-0 h-10 transition-colors hover:bg-gray-50;
}
:deep(.el-collapse-item__wrap) {
  @apply border-b-0 bg-transparent;
}
:deep(.el-collapse-item__content) {
  @apply pb-2;
}
</style>
