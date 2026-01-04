import e_Start from '../components/Nodes/e_Start.vue'
import e_Add from '../components/Nodes/e_Add.vue'
import e_Output from '../components/Nodes/e_Output.vue'
import { markRaw } from 'vue'
import type{ AddNodes,UpdateNodeData } from '@vue-flow/core'



/**
 * 节点类型定义
 */
export const nodeTypes = {
    Add: markRaw(e_Add),
    Start: markRaw(e_Start),
    Output: markRaw(e_Output),

}

const random_pos = () => ({ x: Math.random() * 400, y: Math.random() * 400 })

/**
 * 输入节点数据接口
 */
export interface InputNodeData {
    value: string | number,
}

export const addInputNode = (
  addNodes:AddNodes,
  data:InputNodeData
) => (    
  addNodes({
    id: `input`,
    type: 'Start',
    position: random_pos(),
    data: data,
  })
)

/**
 * 输出节点数据接口
 */

export const addOutputNode = (
  addNodes:AddNodes,
  updateNodeData:UpdateNodeData,
) => ( 
  addNodes({
    id: `output`,
    type: 'Output',
    position: random_pos(),
    data: {
      input_data:{   // 可以当作默认值，也可以当作检查数据类型的依据
       value: '',
      },
      value:'正在等待数据...',
      func:(data:any)=>{
        updateNodeData('output',{value:data.value})
        return data
      }
    },
  })
)