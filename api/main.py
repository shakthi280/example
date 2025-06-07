from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from typing import Optional
from api.model_utils import generate_answer
from api.image_utils import extract_text_from_base64
import traceback
import os

app = FastAPI()

class QuestionInput(BaseModel):
    question: Optional[str] = None
    image: Optional[str] = None  # base64 encoded image string or None

@app.post("/api/")
async def get_answer(input: QuestionInput):
    try:
        user_question = input.question or ""

        # If image is provided, try to extract text and append to question
        if input.image:
            extracted_text = extract_text_from_base64(input.image)
            if extracted_text.startswith("Error decoding image:"):
                # Could optionally return an error here or ignore OCR failure
                raise HTTPException(status_code=400, detail=extracted_text)
            user_question += f"\n\nExtracted from image:\n{extracted_text}"

        if not user_question.strip():
            raise HTTPException(status_code=400, detail="No question or image text provided.")

        answer, links = generate_answer(user_question)
        return {
            "answer": answer,
            "links": links
        }

    except HTTPException as he:
        # Pass through HTTP errors cleanly
        raise he
    except Exception as e:
        # Print full traceback to server logs for debugging
        traceback.print_exc()
        return {"error": f"Internal Server Error: {str(e)}"}
