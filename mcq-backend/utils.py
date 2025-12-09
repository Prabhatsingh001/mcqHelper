"""Utility functions for MCQ Solver backend.

Provides helper functions for prompt construction and other common operations.
"""


def build_prompt(question: str) -> str:
    """Build a prompt for the Gemini API to solve an MCQ.

    Constructs a formatted prompt that instructs the Gemini model to solve
    the MCQ and return only the correct answer option letter.

    Args:
        question (str): The MCQ question text including all options.

    Returns:
        str: A formatted prompt ready to be sent to the Gemini API.

    Example:
        >>> prompt = build_prompt("What is 2+2? A)3 B)4 C)5 D)6")
        >>> print(prompt)
        Solve this MCQ.
        Return ONLY the correct option letter (A, B, C, or D).
        ...
    """
    return f"""
Solve this MCQ.

Return ONLY the correct option letter (A, B, C, or D).
No explanation.

Question:
{question}
"""