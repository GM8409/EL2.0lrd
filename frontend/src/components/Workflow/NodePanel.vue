<template>
<div>
    <!-- 面板卡片 -->
    <div class="panel-card">
        <!-- 标题 -->
        <div class="panel-header">
            <svg class="header-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="1"></circle>
                <path d="M12 2v6m0 4v6"></path>
                <circle cx="5" cy="5" r="1"></circle>
                <circle cx="19" cy="5" r="1"></circle>
                <circle cx="5" cy="19" r="1"></circle>
                <circle cx="19" cy="19" r="1"></circle>
            </svg>
            <span class="header-title">节点库</span>
        </div>

        <!-- 节点按钮分组 -->
        <div class="panel-content">
            <!-- 输入输出节点 -->
            <div class="node-group">
                <div class="group-label">I/O节点</div>
                <button 
                    class="node-btn io-btn"
                    @click="()=>{
                        nodeManager.addInput(input_data)
                        nodeManager.addNode({
                        id:'start',
                        type:'Start',
                        position: random_pos(),
                        style_data:nodeManager.initial_data,
                    })}"
                    title="添加输入节点"
                >
                    <span class="btn-icon">📥</span>
                    <span class="btn-text">输入</span>
                </button>
                
                <button 
                    class="node-btn io-btn"
                    @click="nodeManager.addNode({
                        id:'end',
                        type:'Output',
                        position: random_pos(),
                        style_data:{value: output_result},
                        func:(data)=>{nodeManager.flow.updateNodeData('end',{value: data})},
                    })"
                    title="添加输出节点"
                >
                    <span class="btn-icon">📤</span>
                    <span class="btn-text">输出</span>
                </button>
            </div>

            <!-- 计算节点 -->
            <div class="node-group">
                <div class="group-label">计算节点</div>
                <button 
                    class="node-btn calc-btn"
                    @click="nodeManager.addNode({
                        id:'add_'+Date.now(),
                        type:'Add',
                        position: random_pos(),
                        style_data:{value: 2},
                        func:(data)=>Number(data.value? data.value:data)+2,
                        description:'加法节点',
                    })"
                    title="添加加法节点"
                >
                    <span class="btn-icon">➕</span>
                    <span class="btn-text">加法</span>
                </button>

                <button 
                    class="node-btn calc-btn"
                    @click="nodeManager.addNode({
                        id:'sub_'+Date.now(),
                        type:'Subtract',
                        position: random_pos(),
                        style_data:{value: 2},
                        func:(data)=>Number(data.value? data.value:data)-2,
                        description:'减法节点',
                    })"
                    title="添加减法节点"
                >
                    <span class="btn-icon">➖</span>
                    <span class="btn-text">减法</span>
                </button>
            </div>

            <!-- AI节点 -->
            <div class="node-group">
                <div class="group-label">AI节点</div>
                <button 
                    class="node-btn ai-btn"
                    @click="()=>{
                        nodeManager.addNode({
                        id:'start',  
                        type:'Predict',
                        position: random_pos(),
                        style_data:{value: ''},
                        func:()=>{},
                        description:'预测节点',
                    })
                    watch(()=>nodeManager.flow.findNode('start').data.value,
                    (newVal)=>{
                        console.log('start节点数据更新',newVal)
                        nodeManager.addInput(newVal)
                    })
                    }"
                    title="添加预测节点"
                >
                    <span class="btn-icon">🤖</span>
                    <span class="btn-text">预测</span>
                </button>
            </div>

            <!-- 展示节点 -->
            <div class="node-group">
                <div class="group-label">展示节点</div>
                <button 
                    class="node-btn display-btn"
                    @click="nodeManager.addNode({
                        id:'viewimg',
                        type:'ViewImg',
                        position: random_pos(),
                        style_data:{imageUrl: ''},
                        func:(data)=>{
                            console.log('传来viewimg的节点数据',data)
                            nodeManager.flow.updateNodeData('viewimg',{
                                imageUrl: data.img_url,
                                status:data.status,
                            })
                            
                        },
                        description:'图片展示节点',
                    })"
                    title="添加图片展示"
                >
                    <span class="btn-icon">🖼️</span>
                    <span class="btn-text">图片</span>
                </button>
            </div>

            <!-- 调试控制 -->
            <div class="node-group">
                <div class="group-label">调试工具</div>
                <button 
                    class="node-btn debug-btn"
                    @click="nodeManager.step()"
                    title="单步调试"
                >
                    <span class="btn-icon">⏭️</span>
                    <span class="btn-text">单步</span>
                </button>

                <button 
                    class="node-btn debug-btn"
                    @click="nodeManager.run()"
                    title="运行到结束"
                >
                    <span class="btn-icon">▶️</span>
                    <span class="btn-text">运行</span>
                </button>

                <button 
                    class="node-btn debug-btn"
                    @click="nodeManager.reset()"
                    title="重置运行起点"
                >
                    <span class="btn-icon">🔄</span>
                    <span class="btn-text">重置</span>
                </button>
            </div>
        </div>
    </div>
</div>
</template>

<script setup>
import { inject,ref,watch } from 'vue'
import { random_pos } from '../../tools/nodeManager'


const nodeManager = inject('node_manager')

const emit = defineEmits(['toggleDebugPanel'])

// 响应式对象的属性被赋值不会丢失响应式
const input_data = ref({value:'默认输入'})
const output_result = ref('正在等待数据...')


</script>

<style scoped>
@import 'tailwindcss';


.panel-card {
    @apply bg-white rounded-xl shadow-lg border border-gray-100;
    @apply max-h-full overflow-y-auto;
    width: 180px;
    backdrop-filter: blur(10px);
    background-color: rgba(255, 255, 255, 0.95);
}


.panel-header {
    @apply flex items-center gap-2 px-4 py-3 border-b border-gray-100 bg-gradient-to-r from-blue-50 to-cyan-50;
    @apply sticky top-0 z-20;
}

.header-icon {
    @apply w-5 h-5 text-blue-600;
}

.header-title {
    @apply font-bold text-gray-800 text-sm;
}

.panel-content {
    @apply p-3 space-y-3;
}

.node-group {
    @apply space-y-2;
}

.group-label {
    @apply text-xs font-semibold text-gray-500 uppercase tracking-wide px-1 mt-2 first:mt-0;
}

.node-btn {
    @apply w-full h-9 rounded-lg font-medium text-sm cursor-pointer transition-all duration-200;
    @apply flex items-center justify-center gap-2 px-3;
    @apply border border-transparent;
    @apply hover:shadow-md active:scale-95;
}

/* I/O节点按钮 */
.io-btn {
    @apply bg-gradient-to-r from-green-400 to-emerald-500 text-white;
    @apply hover:from-green-500 hover:to-emerald-600 hover:shadow-green-300/50;
}

/* 计算节点按钮 */
.calc-btn {
    @apply bg-gradient-to-r from-blue-400 to-cyan-500 text-white;
    @apply hover:from-blue-500 hover:to-cyan-600 hover:shadow-blue-300/50;
}

/* AI节点按钮 */
.ai-btn {
    @apply bg-gradient-to-r from-purple-400 to-pink-500 text-white;
    @apply hover:from-purple-500 hover:to-pink-600 hover:shadow-purple-300/50;
}

/* 展示节点按钮 */
.display-btn {
    @apply bg-gradient-to-r from-amber-400 to-orange-500 text-white;
    @apply hover:from-amber-500 hover:to-orange-600 hover:shadow-amber-300/50;
}

/* 调试工具按钮 */
.debug-btn {
    @apply bg-gradient-to-r from-red-400 to-rose-500 text-white;
    @apply hover:from-red-500 hover:to-rose-600 hover:shadow-red-300/50;
}

.btn-icon {
    @apply text-lg;
}

.btn-text {
    @apply text-xs font-semibold;
}

/* 响应式设计 */
@media (max-width: 768px) {
    .node-panel-container {
        @apply left-2 top-20;
    }
    
    .panel-card {
        width: 160px;
    }
    
    .node-btn {
        @apply h-8 text-xs;
    }
}
</style>