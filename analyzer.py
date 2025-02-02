from langchain_ollama import ChatOllama
from langchain_community.document_loaders import PyPDFLoader
from pydantic import BaseModel,Field
from tkinter import filedialog
import re
class Result(BaseModel):
    amount:str = Field(description = "What is the amount")


llm = ChatOllama(
    model="llama3.1:latest",
    temperature=0
                 )

file_names:tuple = filedialog.askopenfilenames()
result = []
for file_name in file_names:
    loader = PyPDFLoader(file_path=file_name)
    docs =loader.load()
    message = [
        
        ("system","You are a transaction reader, type the amount transfered (it should be followed by 'SAR')"),
        ("human",docs[0].page_content)
        
    ]


    structured_llm = llm.with_structured_output(Result)
    ai_msg = str(structured_llm.invoke(message))
    result.append(ai_msg)
    
total:int = 0  
for response in result:
    search= re.findall(r"\d+ SAR",response)
    for money in search:
        print(money)
for response in result:
    search= re.findall(r"\d+",response)
    for money in search:
        total += int(money)
print(total)
