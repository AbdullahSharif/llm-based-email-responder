import os
from dotenv import load_dotenv
from openai import OpenAI
from fastapi import APIRouter, Depends, HTTPException
from ..schemas import EmailRequest, EmailResponse, EmailLogCreate
from ..database import get_session
from ..crud import crud_email_log



load_dotenv()

DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key = DEEPSEEK_API_KEY
)


email_router = APIRouter()

@email_router.post("/", response_model=EmailResponse)
async def generate_email(
    request: EmailRequest,
    db = Depends(get_session)
):
    try:
        system_prompt = f"""
            You are a helpful email assistant. 
            You get a prompt to write an email, 
            you reply with the email and nothing else.
        """

        prompt = f"""
            Write an email based on the following input:
            - User Input: {request.user_input}
            - Reply to: {request.reply_to if request.reply_to else 'N/A'}
            - Context: {request.context if request.context else 'N/A'}
            - Length: {request.length if request.length else 'N/A'} characters (don't exceed the length of the email more than this.) 
            - Tone: {request.tone if request.tone else 'formal'}
        """

        response = client.chat.completions.create(
            model="qwen/qwen-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            max_tokens=request.length
        )

        generated_email = response.choices[0].message.content.strip()
        email_log = EmailLogCreate(
            user_id = request.user_id,
            user_input=request.user_input,
            reply_to=request.reply_to,
            context=request.context,
            length=request.length,
            tone=request.tone,
            generated_email=generated_email,
        )

        # store the email log in the db.
        await crud_email_log.create(db, email_log)

        

        return EmailResponse(generated_email=generated_email)



    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
