import axios from 'axios';

// RAG服务响应接口
interface RagResponse {
  status: string;
  answer?: string;
  context?: string;
  message?: string;
}

// RAG服务类
export class RagService {
  private static instance: RagService;
  private baseUrl: string;

  private constructor() {
    // 设置后端API基础URL
    this.baseUrl = 'http://localhost:5000/api';
  }

  // 单例模式
  public static getInstance(): RagService {
    if (!RagService.instance) {
      RagService.instance = new RagService();
    }
    return RagService.instance;
  }

  /**
   * 发送RAG查询请求
   * @param question 用户问题
   * @returns AI回答和上下文
   */
  public async query(question: string): Promise<{ answer: string; context: string }> {
    try {
      const response = await axios.post<RagResponse>(`${this.baseUrl}/rag`, {
        question
      });

      if (response.data.status === 'success' && response.data.answer) {
        return {
          answer: response.data.answer,
          context: response.data.context || ''
        };
      } else {
        throw new Error(response.data.message || 'Failed to get answer');
      }
    } catch (error) {
      console.error('RAG query error:', error);
      throw error;
    }
  }

  /**
   * 发送RAG查询请求（流式响应）
   * @param question 用户问题
   * @param callback 回调函数，用于处理流式数据
   */
  public async streamQuery(question: string, callback: (chunk: string, context: string) => void): Promise<void> {
    try {
      const response = await fetch(`${this.baseUrl}/rag/stream`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ question })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const reader = response.body?.getReader();
      if (!reader) {
        throw new Error('No response body');
      }

      const decoder = new TextDecoder();
      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) {
          // 处理最后剩余的缓冲区数据
          if (buffer.trim()) {
            try {
              const data = JSON.parse(buffer.trim());
              callback(data.chunk || '', data.context || '');
            } catch (e) {
              console.error('Error parsing final stream data:', e);
              console.error('Invalid buffer:', buffer);
            }
          }
          break;
        }

        buffer += decoder.decode(value, { stream: true });
        
        // 处理每一行数据
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';

        for (const line of lines) {
          const trimmedLine = line.trim();
          if (trimmedLine) {
            try {
              const data = JSON.parse(trimmedLine);
              callback(data.chunk || '', data.context || '');
            } catch (e) {
              // 尝试修复常见的JSON格式问题
              try {
                // 移除可能的多余字符
                const cleanedLine = trimmedLine.replace(/[^{]*{/, '{').replace(/}[^}]*$/, '}');
                const data = JSON.parse(cleanedLine);
                callback(data.chunk || '', data.context || '');
              } catch (e2) {
                console.error('Error parsing stream data:', e);
                console.error('Invalid line:', trimmedLine);
              }
            }
          }
        }
      }
    } catch (error) {
      console.error('RAG stream query error:', error);
      throw error;
    }
  }
}

// 导出默认实例
export default RagService.getInstance();
