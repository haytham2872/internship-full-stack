from pydantic import BaseModel, ValidationError
from typing import List
import json

class Exercise(BaseModel):
    name: str
    sets: int
    reps: str  
    rest: str

class WorkoutDay(BaseModel):
    day: int
    focus: str
    duration_minutes: int
    equipment: List[str]
    warmup: str
    exercises: List[Exercise]
    cooldown: str
    estimated_calories: int

class WorkoutProgram(BaseModel):
    program: List[WorkoutDay]

SYSTEM_PROMPT = """You are a fitness program generator. Generate a structured workout program based on user requirements.

IMPORTANT: Respond ONLY with valid JSON matching this exact structure:
{
  "program": [
    {
      "day": 1,
      "focus": "Upper Body",
      "duration_minutes": 45,
      "equipment": ["barbell", "bench"],
      "warmup": "5 min light cardio + dynamic stretches",
      "exercises": [
        {"name": "Bench Press", "sets": 4, "reps": "10", "rest": "90 sec"},
        {"name": "Rows", "sets": 3, "reps": "12", "rest": "60 sec"}
      ],
      "cooldown": "5 min stretching",
      "estimated_calories": 300
    }
  ]
}

Rules:
- Respect user's equipment constraints
- Match the requested number of sessions/week
- Adjust intensity to fitness level
- Keep within time constraints
- NO text outside the JSON"""

def validate_program(response_text: str) -> WorkoutProgram:
    """Parse and validate LLM response."""
    # Clean potential markdown
    cleaned = response_text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("```")[1]
        if cleaned.startswith("json"):
            cleaned = cleaned[4:]
    
    data = json.loads(cleaned)
    return WorkoutProgram(**data)