"""Pydantic schemas for MCQ Solver API.

Defines request/response models for type validation and API documentation.
"""
from pydantic import BaseModel


class MCQRequest(BaseModel):
    """Request model for MCQ solving endpoint.

    Attributes:
        question (str): The multiple choice question text to be solved.
                       Should include the question and all answer options.

    Example:
        {
            "question": "What is the capital of France? A) London B) Paris C) Berlin D) Madrid"
        }
    """
    question: str
