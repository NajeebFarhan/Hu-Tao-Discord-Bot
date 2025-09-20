from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage


model = ChatOllama(model="gemma2:latest", validate_model_on_init=True)

with open("prompt.txt") as f:
    prompt_template = ChatPromptTemplate([
        ("system", f.read()),
        MessagesPlaceholder("messages")
    ])
    

message_history = []

def llm_answer(message: str):
    message_history.append(HumanMessage(message))
        
    prompt = prompt_template.invoke({"messages": message_history})

    data = model.invoke(prompt)
    answer = data.content
    
    message_history.append(AIMessage(answer))
    
    return answer
