from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from typing import List,Optional
load_dotenv()
class CvScanner(BaseModel):
    name: str
    Job_title: str
    experience: Optional[str]
    skills: List[str]
    projects: Optional[List[str]]
    email: Optional[str]
    linkedin: Optional[str]
    github: Optional[str]
    summary: Optional[str]
    match_score: Optional[int]
parser=PydanticOutputParser(pydantic_object=CvScanner)


model=ChatMistralAI(
    model_name='mistral-small-latest')


prompt_template = ChatPromptTemplate.from_messages([
    
    ("system", """
You are a CV Scanner AI designed to extract structured information from unstructured CV text.

Your task is to analyze the provided CV content and extract key details such as:

- candidate name
- job title
- experience
- skills
- projects
- contact information
    - email
    - LinkedIn
    - GitHub
- brief summary
- match with job description
- give a score out of 10 based on the match with job description

The extracted information should follow the CvScanner schema.

{format_instructions}
"""),

    ("human", """
{CV_content},
{job_description}
""")

])
cv_content = input("Enter CV content: ")
job_description = input("Enter job description: ")

formatted_prompt=prompt_template.invoke(
    {
        "CV_content": cv_content,
        "job_description": job_description,
        "format_instructions": parser.get_format_instructions()
    }
)


response=model.invoke(formatted_prompt)
print(response.content)