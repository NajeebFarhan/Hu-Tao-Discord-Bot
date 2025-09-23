from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, FewShotChatMessagePromptTemplate
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import json


model = ChatOllama(model="gemma2:latest", validate_model_on_init=True)


with open("dataset.json") as f:
    examples = json.loads(f.read())

    example_prompt = ChatPromptTemplate.from_messages([
        ("human", "{input}"),
        ("ai", "{output}")
    ])
    
    few_shot_examples = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=examples
    )
   
    
with open("prompt.txt") as f:
    prompt_template = ChatPromptTemplate.from_messages([
        SystemMessage(content=f.read()),
        few_shot_examples,
        MessagesPlaceholder("messages")
    ])
    

message_history = []

def llm_answer(message: str):
    message_history.append(HumanMessage(content=message))
        
    prompt = prompt_template.invoke({"messages": message_history})

    data = model.invoke(prompt)
    answer = data.content
    
    message_history.append(AIMessage(content=answer))
    
    return answer
