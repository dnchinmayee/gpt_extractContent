import openai
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel


load_dotenv()

os.environ["MAKE_SOMETHING_UP"] = "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"

openai.api_key = os.getenv('MAKE_SOMETHING_UP')

app = FastAPI()

function_descriptions = [
    {
        "name": "extract_info_from_email",
        "description": "categorise & extract key info from an email, such as use case, company name, contact details, etc.",
        "parameters": {
            "type": "object",
            "properties": {
                "companyName": {
                    "type": "string",
                    "description": "the name of the company that sent the email"
                },                                        
                "product": {
                    "type": "string",
                    "description": "Try to identify which product the client is interested in, if any"
                },
                "amount":{
                    "type": "string",
                    "description": "Try to identify the amount of products the client wants to purchase, if any"
                },
                "category": {
                    "type": "string",
                    "description": "Try to categorise this email into categories like those: 1. Sales 2. customer support; 3. consulting; 4. partnership; etc."
                },
                "nextStep":{
                    "type": "string",
                    "description": "What is the suggested next step to move this forward?"
                },
                "priority": {
                    "type": "string",
                    "description": "Try to give a priority score to this email based on how likely this email will leads to a good business opportunity, from 0 to 10; 10 most important"
                },
            },
            "required": ["companyName", "amount", "product", "priority", "category", "nextStep"]
        }
    }
]

email = """
Dear Jason 
I hope this message finds you well. I'm Shirley from Gucci;

I'm looking to purchase some company T-shirt for my team, we are a team of 10 people, and we want to get 2 t-shirt per personl

Please let me know the price and timeline you can work with; Looking forward Shirley Lou
"""

prompt = f"Please extract key information from this email: {email} "
message = [{"role": "user", "content": prompt}]

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=message,
    functions = function_descriptions,
    function_call="auto"
)

print(response)



class Email(BaseModel):
    from_email:str
    content:str

@app.get("/LoL")
def read_root():
    return {"Hello": "World"}


@app.post("/")

def analyze_email(email:Email):
    content = email.content
    query = f"please extract key information from this email:{content}"
    messages = [{"role":"user", "content":query}]

    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=message,
    functions = function_descriptions,
    function_call="auto"
    )

    arguments = response.choices[0]["message"]["function_call"]["arguments"]
    companyName = eval(arguments).get("companyName")
    priority = eval(arguments).get("priority")
    product = eval(arguments).get("product")
    amount = eval(arguments).get("amount")
    category = eval(arguments).get("category")
    nextStep = eval(arguments).get("nextStep")

    return {
        "companyName": companyName,
        "product": product,
        "amount": amount,
        "priority": priority,
        "category": category,
        "nextStep": nextStep
    }
    
    
