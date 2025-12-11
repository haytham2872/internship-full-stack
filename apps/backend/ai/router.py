from fastapi import APIRouter, Depends, HTTPException
from schemas import ProgramRequest
from auth.dependencies import get_current_user
from models import User
from ai.prompt import SYSTEM_PROMPT, validate_program
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

router = APIRouter(prefix="/api/ai", tags=["ai"])

MAX_RETRIES = 3


def generate_with_openai(user_text: str) -> str:
    """Generate workout program using OpenAI gpt-4o-mini."""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text}
        ],
        temperature=1
    )

    return response.choices[0].message.content


@router.post("/program")
def generate_program(
    request: ProgramRequest,
    current_user: User = Depends(get_current_user)
):
    """Generate a workout program using OpenAI gpt-4o-mini."""

    for attempt in range(MAX_RETRIES):
        try:
            content = generate_with_openai(request.text)

            # Validate and parse the JSON response
            program = validate_program(content)
            return program.model_dump()

        except Exception as e:
            if attempt == MAX_RETRIES - 1:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to generate valid program: {str(e)}"
                )

    raise HTTPException(status_code=500, detail="Generation failed")