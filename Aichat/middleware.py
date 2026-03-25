from langchain.agents import wrap_tool_call
from langchain_core.messages import ToolMessage
import time

@wrap_tool_call
def retry_tool_errors(request, handler):
    """带重试的工具错误处理（可自定义重试次数、退避时间）"""
    max_retries = 3  # 最大重试次数
    retry_delay = 1  # 重试间隔（秒）
    
    for attempt in range(max_retries):
        try:
            return handler(request)  # 尝试执行工具
        except Exception as e:
            if attempt < max_retries - 1:
                # 未达最大重试次数：等待后重试
                time.sleep(retry_delay)
                retry_delay *= 2  # 指数退避（可选）
            else:
                # 达最大重试次数：返回自定义错误
                return ToolMessage(
                    content=f"Tool failed after {max_retries} retries. Error: {str(e)}",
                    tool_call_id=request.tool_call["id"]
                )
                