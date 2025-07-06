import os
from groq import Groq
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

def extract_company_github_username(text: str) -> Optional[str]:
    try:
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert assistant. Your task is to identify the GitHub organization "
                        "username of a prominent tech company mentioned in the provided text. "
                        "Return ONLY the GitHub username (e.g., 'google', 'microsoft', 'facebook'). "
                        "If no specific company's GitHub username is mentioned or identifiable, return the word 'None'."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Here is the text:\n\n---\n\n{text[:4000]}",
                },
            ],
            model="llama3-8b-8192",
            temperature=0.0,
        )
        response = chat_completion.choices[0].message.content.strip()
        
        if response.lower() == 'none' or not response:
            return None
            
        # Basic cleaning in case the model returns extra text
        return response.splitlines()[0].split()[0].replace("'", "").replace('"', '')

    except Exception as e:
        print(f"Error calling LLM API: {e}")
        return None
