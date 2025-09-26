from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, FewShotChatMessagePromptTemplate
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from db import SessionLocal, Chat
import json


model = ChatOllama(model="gemma2:latest", validate_model_on_init=True)


# with open("dataset.json") as f:
#     examples = json.loads(f.read())

#     example_prompt = ChatPromptTemplate.from_messages([
#         ("human", "{input}"),
#         ("ai", "{output}")
#     ])
    
#     few_shot_examples = FewShotChatMessagePromptTemplate(
#         example_prompt=example_prompt,
#         examples=examples
#     )
   
# TODO: optimization of training. FewShotChatMessagePromptTemplate seems slow
  
with open("prompt.txt") as f:
    prompt_template = ChatPromptTemplate.from_messages([
        SystemMessage(content=f.read()),
        # few_shot_examples,            
        MessagesPlaceholder("messages")
    ])
    

message_history = []

with SessionLocal() as session:
    message_data = session.query(Chat).all()
    message_history = [(m.role, m.message) for m in message_data]

def llm_answer(message: str):
    message_history.append(("human", message))
        
    prompt = prompt_template.invoke({"messages": message_history})

    data = model.invoke(prompt)
    answer: str = data.content  # type: ignore
    
    message_history.append(("ai", answer))
    
    return answer
