from fastapi import APIRouter, Depends, HTTPException
from schemas import ProgramRequest
from auth.dependencies import get_current_user
from models import User
from ai.prompt import SYSTEM_PROMPT, validate_program
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/api/ai", tags=["ai"])

# ╔════════════════════════════════════════════════════════════════╗
# ║  CHANGE THIS TO SWITCH BETWEEN PROVIDERS                       ║
# ║                                                                 ║
# ║  Options: "openai" or "anthropic"                               ║
# ╚════════════════════════════════════════════════════════════════╝
AI_PROVIDER = os.getenv("AI_PROVIDER", "anthropic")  # Default to anthropic

MAX_RETRIES = 3


def generate_with_openai(user_text: str) -> dict:
    """Generate workout program using OpenAI."""
    from openai import OpenAI
    
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Budget-friendly model
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text}
        ],
        temperature=0.7,
        max_tokens=2000
    )
    
    return response.choices[0].message.content


def generate_with_anthropic(user_text: str) -> dict:
    """Generate workout program using Claude."""
    from anthropic import Anthropic
    
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",  # Can also use "claude-3-haiku-20240307" for cheaper
        max_tokens=2000,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": user_text}
        ]
    )
    
    return response.content[0].text


@router.post("/program")
def generate_program(
    request: ProgramRequest,
    current_user: User = Depends(get_current_user)
):
    """Generate a workout program using the configured AI provider."""
    
    for attempt in range(MAX_RETRIES):
        try:
            # Choose provider based on configuration
            if AI_PROVIDER == "openai":
                content = generate_with_openai(request.text)
            else:  # anthropic (default)
                content = generate_with_anthropic(request.text)
            
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


# Optional: Endpoint to check which provider is active
@router.get("/provider")
def get_provider(current_user: User = Depends(get_current_user)):
    """Check which AI provider is currently active."""
    return {"provider": AI_PROVIDER}