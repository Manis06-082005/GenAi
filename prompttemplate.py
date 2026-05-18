from langchain_mistralai import ChatMistralAI
from dotenv import load_dotenv
load_dotenv()
from langchain_core.prompts import ChatPromptTemplate
model=ChatMistralAI(
    model_name='mistral-small-latest',
    temperature=0.5,
    max_tokens=100
)
template_prompt=ChatPromptTemplate.from_messages(
    [
        ("system","""
You are an expert AI Interview Assistant for AI, Data Science, Machine Learning, SQL, Python, Power BI, Statistics, and Generative AI interviews.

Your responsibilities:
- Conduct realistic technical interviews
- Ask intelligent follow-up questions
- Evaluate answers honestly
- Give constructive feedback
- Explain mistakes clearly
- Adapt questions based on difficulty level
- Maintain a professional interview atmosphere

Rules:
- Ask one question at a time
- Do not immediately reveal answers
- Give hints if the candidate struggles
- Focus on practical and interview-oriented questions
- Keep responses concise and realistic
"""),
("human",
  """
Candidate Name: {name}
Role: {role}
Experience Level: {experience}
Skills: {skills}
Interview Type: {interview_type}
Difficulty Level: {difficulty}

Candidate Response:
{user_input}
""")
    ]
)
name=input("Enter candidate name: ")
role=input("Enter role: ")
experience=input("Enter experience level (e.g., Junior, Mid, Senior): ")
skills=input("Enter skills (comma-separated): ")
interview_type=input("Enter interview type (e.g., Technical, Behavioral): ")
difficulty=input("Enter difficulty level (e.g., Easy, Medium, Hard): ")



while True:
    user_input=input("Candidate': ")
    if user_input.lower()=='exit':
        break
    prompt=template_prompt.invoke(
        {
            "name":name,
            "role":role,
            "experience":experience,
            "skills":skills,
            "interview_type":interview_type,
            "difficulty":difficulty,
            "user_input":user_input
        }
    )
    response=model.invoke(prompt)
    print(response.content)