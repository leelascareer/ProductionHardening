from langchain.messages import SystemMessage, HumanMessage
from models import ErrorCode, InvocationResult
from langchain_openai import ChatOpenAI
from trackers.CircuitBreaker import CircuitBreaker
from utils import load_system_prompt
from security import detect_injection
from typing import Final
import time

breaker = CircuitBreaker()

#Layer3: Response Generation with LLM
def production_invoke(user_input: str, max_retires: int = 3) -> InvocationResult:
    if not breaker.allow_request():
          return InvocationResult(success=False,error_message="Circuit breaker open",
                                  error_code=ErrorCode.UNKNOWN,
                                  attempts=0
                                  )
    
    llm = ChatOpenAI(model="gpt-4", temperature=0.2)
    system_prompt = load_system_prompt("system")
    messages = [SystemMessage(content=system_prompt),HumanMessage(content=user_input)]

    if detect_injection(user_input):
            return InvocationResult(success=False, error_message="Harmful content detected.",error_code=ErrorCode.UNKNOWN )
    
    for attempt in range(max_retires):        
        try:
            raw_response = llm.invoke(messages)
            content = raw_response.content 

            #Layer 4: Output Filtering
            dangerous_keywords: Final[list[str]] = ["hack", "fraud", "system prompt", "jailbreak", "ignore instructions"]
            for keyword in dangerous_keywords:
                if keyword in content.lower():
                    content = "I can only provide support related to our products and services."
                    break
            return InvocationResult(success=True, content=content, attempts=attempt+1)
            
        except Exception as e:
            error_message = str(e).lower()
            if "rate limit" in error_message:
                delay = 2 ** attempt 
                time.sleep(delay)  # Exponential backoff
                continue
            elif "context length" in error_message or "maximum context length" in error_message:
                return InvocationResult(success=False,error_code=ErrorCode.CONTEXT_OVERFLOW,
                                        error_message="Context length exceeded.",attempts=attempt+1)
            elif "authentication" in error_message:
                return InvocationResult(success=False, error_code=ErrorCode.AUTH_ERROR,
                                        error_message="Authentication failed.")
            else:
                return InvocationResult(success=False,error_code=ErrorCode.MODEL_ERROR,error_message=str(e))
    
    return InvocationResult(success=False,error_code=ErrorCode.UNKNOWN,
                            error_message="Failed to generate response after maximum attempts.")
