import type { Node, Edge,FindNode } from "@vue-flow/core";
import { watch } from 'vue'
import { ref ,type Ref } from 'vue'

/**
 * ## 流管理类.
 * 用于管理流中的节点和边.
 * 适用于已经写好和连好线的单线程流.可以执行和单步调试
 * 
 * ## 前置知识：
 * edge对象提供source和target属性，分别表示边的起始节点和目标节点的id
 * edge提供了node 的id 但是edge不知道从哪找
 * 对于一条连线来说一定有两个对应的端点，分别是source和target 
 * 对于一个节点来说，它可能有多个入边和多个出边.
 * useVueFlow提供的方法不能在ts里面使用，他依赖Vue组件上下文，只能把要用的工具当参数传递
 * useVueFlow提供findNode方法，用于根据id获取node对象.
 * useVueFlow提供findEdge方法，用于根据id获取edge对象.
 * useVueFlow提供getEdges方法，用于获取当前状态下的所有连线.
 * useVueFlow提供updateNodeData方法，用于更新节点数据.
 * 
 * ### 考虑：
 * - 连线方式：目前先通过find next_edge.source === current_edge.target 来获取下一条连线实现单线串连.后续考虑优化为映射表.
 * - filter可以实现多线，但是先不考虑
 * - 图表结构改变---也就是节点或边发生变化时，需要重新初始化流.不然不知道起点或者终点.
 * - 当前的起点判断是约定查找类型为start的节点
 * - 考虑把流控制器中的三个中间状态参数改成响应式，方便在外部监听和使用，渲染到页面上.
 * - 结束保护：当执行到输出节点时，停止执行，避免不停重复最后节点的执行和无限循环.
 * - 数据传递：连线中途需要携带数据包，数据包需要在节点之间传递，每个节点需要根据数据包进行处理，处理结果作为下一个节点的输入.
 * - 类型判断：如果节点携带的数据类型不一致，应该执行失败，而不是返回空
 */

export class StreamManager {
    nodes: Ref<Node[]>;
    edges:  Ref<Edge[]>;
    currentEdge: Ref<Edge | undefined> = ref(undefined);
    currentNode: Ref<Node | undefined> = ref(undefined);  // 认为当前节点是当前边的source节点
    currentData: Ref<any> = ref({});
    isFinished: boolean = false;  // 流是否执行完毕
    private findNode: FindNode;
  
    constructor(
        nodes: Ref<Node[]>, 
        edges: Ref<Edge[]>,
        findNode: FindNode,
    ) {
        this.findNode = findNode;
        this.nodes = nodes;
        this.edges = edges;
        this.initStream();  // 初始化开始节点和开始连线
        this._watchGraphChange()
    }

    /**
     * ## 初始化流
     * 初始流的初始数据，初始节点，和初始边
     * 也可以理解为重置状态，回到最开始的节点和连线
     */
    initStream(): void {
        this.isFinished = false
        this.currentNode = ref(this.nodes.value.find((node) => node.type === "Start"));
        this.currentData = ref(this.currentNode.value?.data || {}); // 初始化输入数据 如果当前节点没有数据 则为空
        this.currentEdge = ref(this.edges.value.find((edge) => edge.source === this.currentNode.value?.id));
        console.log(
            '初始化完毕，当前工作流的状态为：\n',
            '节点：', this.currentNode.value,'\n',
            '数据：', this.currentData.value,'\n',
            '连线：', this.currentEdge.value,
        )
    }

    addTemplateData(){
        this.nodes.value = templateNodes
        this.edges.value = templateEdges
        console.log('📋 模板数据已添加')
    }

    /**
     * ## 监听图结构变化
     * 当节点或边发生变化时，重新初始化流.
     */
    _watchGraphChange(){
        watch(()=>[this.nodes.value,this.edges.value],
        ([nodes,edges])=>{
            this.nodes.value = nodes as Node[]   // 类型断言 确保 nodes 是 Node[] 类型
            this.edges.value = edges as Edge[]   // 空的，没定义也不要紧，影响不大，因为本来就接收
            console.log('🔄检测到图结构发生改变，正在重新初始化..')
            this.initStream()
        })
    }
    /**
     * ## 获取当前节点的下一条连线.
     * 用currentEdge的target作为source，通过 find 单线串连，返回下一条连线.只找符合条件的第一条连线.
     * 当找到最后一条边的时候，再找，就会返回undefined.
     */
    getNextEdge(): void {
        this.currentEdge.value = this.edges.value.find((edge) => edge.source === this.currentEdge.value?.target)
        if (!this.currentEdge.value){
            this.isFinished = true
        }
        return 
    }
    /**
     * ## 检查数据类型
     * 检查输入数据是否符合节点要求的类型.
     * 支持基本类型和对象类型的递归检查.
     */
    checkDataType(input_data:any,input_data_type:any):boolean{
        const in_type = typeof input_data
        const need_type = typeof input_data_type
        if (in_type !== need_type){
            return false
        }else if (in_type === 'object' && need_type === 'object'){
            // 递归检查对象的每个属性
            for (const key in input_data_type){
                if (!this.checkDataType(input_data[key],input_data_type[key])){
                    return false
                }
            }
        }
        return true
    }
    
    /**
     * ## 执行单步调试
     * 执行当前节点的函数，更新当前数据和当前边.
     * 当执行到输出节点时，停止执行.
     */
    async step(): Promise<void> {
        if (this.isFinished) {
            console.log('✅当前节点没有下一条连线,工作流执行完毕') 
            return
        }   // 如果运行完毕请不要运行
        try{
            this.currentNode.value = this.findNode(this.currentEdge.value?.target!);      // 先更新当前节点
            const input_data = this.currentData.value
            const input_data_type = this.currentNode.value?.data.input_data
            if (!this.checkDataType(input_data,input_data_type)){
                console.warn('输入数据类型错误，请检查输入数据是否符合节点要求')   // 宽松警告，之后考虑触发
            }
            const output_data = await this.currentNode.value?.data.func(input_data); // 再更新当前数据
            this.currentData.value = output_data;
            this.getNextEdge();}
        
        catch (error){
            this.isFinished = true
            this.initStream()    // 报错时重新初始化
            throw new Error('执行节点出错,调试器已停止运行：' + error)
        }
       
    }
   
    
    async act(debug: boolean = false) {
        if (debug){
            console.log('开始执行\n=====================================')
            await this.step();
            console.log('当前节点为：', this.currentNode.value)
            console.log('当前数据为：', this.currentData.value)
            console.log('当前连线为：', this.currentEdge.value)
        }
        else{      // 不是调试模式 则一直执行到最后
        while (this.currentEdge !== undefined){
           await this.step()
            if (this.isFinished) break
        }
    }
    
}}



// 模板数据

const templateNodes: Node[] = [
{
    id: 'start_1',
    type: 'Start',
    position: { x: 200, y: 100 },
    data: {
        label: '开始节点',
        value: 100,
        originalName: '开始节点',
        nodeType: 'start'
    }
},
{
    id: 'add_1',
    type: 'add',
    position: { x: 400, y: 100 },
    data: {
        label:'加法节点1',
        input_data:{
            label:'',
        },
        func: (data: any) => {
            const num = Number(data.value) || 0
            return num + 1
        }
    }
},
{
    id: 'add_2',
    type: 'add',
    position: { x: 600, y: 100 },
    data: {
    label: '加法节点2',
    originalName: '加法节点2',
    nodeType: 'add',
    func: (data: any) => {
        const num = Number(data) || 0
        return num * 2
    }
    }
},
{
    id: 'output_1',
    type: 'Output',
    position: { x: 800, y: 100 },
    data: {
    input_data:{   // 可以当作默认值，也可以当作检查数据类型的依据
       value: '',
      },
      value:'正在等待数据...',
      func:(data:any)=>{
        return data
    }}
}
]

const templateEdges: Edge[] = [
{
    id: 'edge_start_add1',
    source: 'start_1',
    target: 'add_1',
    label: '数据流',
    animated: true
},
{
    id: 'edge_add1_add2',
    source: 'add_1',
    target: 'add_2',
    label: '数据流',
    animated: true
},
{
    id: 'edge_add2_output',
    source: 'add_2',
    target: 'output_1',
    label: '数据流',
    animated: true
}
]
