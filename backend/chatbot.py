from fastapi import APIRouter, HTTPException
import os
from demo.text_2_text import generate_answer
import warnings
warnings.filterwarnings("ignore")
from pydantic import BaseModel

# Initialize the router
router = APIRouter()

class QuestionInput(BaseModel):
    question: str

@router.post("/ask")
async def ask_question(data: QuestionInput):
    """
    Endpoint to ask a question and get an answer from the chatbot.
    Args:
        data (QuestionInput): The input data containing the question.
    Returns:
        dict: A dictionary with the question and the generated answer.
    """
    question = data.question
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    
    try:
        answer = generate_answer(question)
        return {"question": question, "answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
