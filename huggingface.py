from dotenv import load_dotenv
from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
load_dotenv()
llm=HuggingFaceEndpoint(
    repo_id="deepseek-ai/DeepSeek-V4-Pro",
    temperature=0.5
)
model=ChatHuggingFace(llm=llm)
response=model.invoke('famous dialogue from the movie Batman')
print(response.content)