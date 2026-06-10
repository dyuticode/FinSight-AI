import os
from google import genai
from google.genai import types
from pydantic import BaseModel

class CategorizedTransaction(BaseModel):
    category: str  # e.g., Housing, Food, Entertainment, Income, Utilities, Shopping, Miscellaneous

def categorize_transactions_llm(descriptions):
    """
    Uses Gemini 2.5 to batch categorize transaction descriptions.
    """
    # Check if key is in environment or Streamlit session state
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        # Fallback if no API key is provided yet
        print("No API Key found. Using basic keyword fallback fallback.")
        return ["Shopping" if "walmart" in desc.lower() else "Food" for desc in descriptions]

    # Initialize client dynamically only when we have a key
    client = genai.Client(api_key=api_key)
    
    unique_descriptions = list(set(descriptions))
    categories_mapping = {}

    prompt = f"""
    You are a financial AI. Categorize the following bank transaction descriptions into exactly one of these categories:
    [Housing, Food, Entertainment, Income, Utilities, Shopping, Transportation, Miscellaneous].
    
    Transactions: {unique_descriptions}
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=list[CategorizedTransaction],
                temperature=0.1
            ),
        )
        
        import json
        results = json.loads(response.text)
        for desc, res in zip(unique_descriptions, results):
            categories_mapping[desc] = res.get('category', 'Miscellaneous')
            
    except Exception as e:
        print(f"LLM Error: {e}")
        for desc in unique_descriptions:
            categories_mapping[desc] = "Miscellaneous"

    return [categories_mapping.get(d, "Miscellaneous") for d in descriptions]