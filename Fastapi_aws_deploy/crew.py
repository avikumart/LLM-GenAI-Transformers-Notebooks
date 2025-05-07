from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from crewai import Agent, Task, Crew
import os
from typing import List, Dict, Any
from dotenv import load_dotenv

# load the env variables
load_dotenv()
OpenAI_API = os.getenv("OPENAI_API")
os.environ["OPENAI_API_KEY"] = OpenAI_API

# Define the email drafter class
class EmailDrafter:
    def __init__(self):
        self.agent = Agent(
            role="Email Drafter",
            goal="Draft an email to a specific recipient with clear, concise, and to the point response",
            backstory="You are an email drafter. You will be given a task to draft an email to a specific recipient. You will be given the context of the email and the recipient's name. You will also be given the subject of the email. You will draft the email in a clear, concise, and to the point manner.",
            llm="gpt-3.5-turbo"
        )

    def run(self, input_email):
        description=f"""Draft a profressional email to the given input email
        that is effective and proper.
        input email: {input_email}"""
        task = Task(
            description=description,
            agent=self.agent
        )
        crew = Crew(
            agents=[self.agent],
            tasks = [task]
        )
        result = crew.kickoff()
        return result

# instatiate the emaildrafter
email_drafter = EmailDrafter()

# Define the FastAPI app
app = FastAPI()

# Define the request and response models
class EmailRequest(BaseModel):
    input_email: str

@app.get("/")
async def read_root():
    return {"message":"Welcome to the Email Drafter API"}

@app.post("/Email-draft/", response_model=Dict[str, Any])  
async def draft_email(request: str):
    try:
        resp = email_drafter.run(request.strip())  # Added strip() to clean input
        return {"drafter_email": resp}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# example email
"""
Subject: Concerns Regarding Recent Project Collaboration

Dear John,

I hope you're well. I wanted to reach out to discuss some concerns regarding our recent project at ABC Tech Solutions. While we've made progress, I've noticed a few challenges that have affected the overall flow and efficiency of the work.

Specifically, there have been delays in communication and missed deadlines that have impacted the timelines we had set. I believe that with more timely responses and a clearer understanding of expectations, we could have avoided some of these setbacks.

I value the work you've done, but I think it's important for us to address these issues moving forward. I would appreciate an opportunity to discuss how we can improve our collaboration to ensure we're on the same page and working towards the same goals.

Please let me know when you would be available for a conversation.

Best regards,
Alex
Senior Project Manager
ABC Tech Solutions
alex@abctech.com
"""