from langchain_mistralai import ChatMistralAI
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage


load_dotenv()

model = ChatMistralAI(
    model_name="mistral-small-latest",
    temperature=0.5,
    max_tokens=100
)

message = [
    SystemMessage(content="""you are a helpful assistant . who is helping a user who overthinks
    a lot even in  small topic you have to make it happpy if he/she asks or without asking you have to make 
    him/her happy and give him/her a good answer """)
]

while True:

    user_input = input("Manish: ")
    # Store user message
    message.append(HumanMessage(content=user_input))

    if user_input.lower() == "exit":
        break
    # Send full conversation
    response = model.invoke(message)

    # Store assistant response
    message.append(AIMessage(content=response.content))

    print( response.content)
    
#MANUAL MESSAGES
''''
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

messages = [
    SystemMessage(content="You are a poetry expert"),
    HumanMessage(content="Write a haiku about spring"),
    AIMessage(content="Cherry blossoms bloom..."),
    HumanMessage(content="Write a haiku about winter")
]
response = model.invoke(messages)
print(response.content) '''