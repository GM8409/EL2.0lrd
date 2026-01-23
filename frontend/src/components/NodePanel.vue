<template>
<div class="panel">
    <!-- <button class="btn"
    @click="emit('toggleDebugPanel')"
    >
    切换调试面板
    </button> -->
    <button 
    class="btn"
    @click="()=>{
        nodeManager.addInput(input_data)
        nodeManager.addNode({
        id:'start',
        type:'Start',
        position: random_pos(),
        style_data:nodeManager.initial_data,
    })}"
    >添加输入节点
    </button>
    
    <button 
    class="btn"
    @click="nodeManager.addNode({
        id:'end',
        type:'Output',
        position: random_pos(),
        style_data:{value: output_result},
        func:(data)=>{nodeManager.flow.updateNodeData('end',{value: data})},
    })"
    >添加输出节点
    </button>

    <button 
    class="btn"
    @click="nodeManager.addNode({
        id:'add_'+Date.now(),
        type:'Add',
        position: random_pos(),
        style_data:{value: 2},
        func:(data)=>Number(data.value? data.value:data)+2,
        description:'加法节点',
    })"
    >添加加法节点
    </button>

    <button 
    class="btn"
    @click="nodeManager.step()"
    >单步调试
    </button>

    <button 
    class="btn"
    @click="nodeManager.run()"
    >运行到结束
    </button>

    <button 
    class="btn"
    @click="nodeManager.reset()"
    >重置运行起点
    </button>
</div>
</template>

<script setup>
import { inject,ref } from 'vue'
import { random_pos } from '../tools/nodeManager'

const nodeManager = inject('node_manager')

const emit = defineEmits(['toggleDebugPanel'])

// 响应式对象的属性被赋值不会丢失响应式
const input_data = ref({value:'默认输入'})
const output_result = ref('正在等待数据...')


</script>

<style scoped>
@import 'tailwindcss';

.panel {
    @apply fixed top-4 left-4 flex flex-col items-center justify-center w-32 min-h-32;
    @apply space-y-2
}

.btn {
    @apply w-28 h-8 rounded-lg bg-amber-400 text-black font-bold cursor-pointer;
}

</style>