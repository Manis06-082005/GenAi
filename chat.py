
#Chat INIT METHOD

from dotenv import load_dotenv

from langchain.chat_models import init_chat_model
load_dotenv()
model=init_chat_model('google_genai:gemini-2.5-flash-lite'
                      ,temperature=0.5,
                      max_tokens=100)
response=model.invoke('why do we fall in philosophical terms?')
print(response.content)

#Class MODEL METHOD MISTALAI
from langchain_mistralai import ChatMistralAI
model2=ChatMistralAI(temperature=0.5,max_tokens=100)
response2=model2.invoke('why do we fall in philosophical terms?')
print(response2.content)
load_dotenv()


#Class MODEL METHOD GOOGLE GENAI
from langchain_google_genai import ChatGoogleGenerativeAI
model=ChatGoogleGenerativeAI(model='gemini-2.5-flash-lite',
    temperature=0.5,max_tokens=100)
response=model.invoke('why do we fall in philosophical terms?')
print(response.content)
