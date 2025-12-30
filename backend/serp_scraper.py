import requests
import os
from dotenv import load_dotenv
import json
from pathlib import Path

load_dotenv()

serp_key = os.getenv("SERPAPI_KEY")  # Returns the key
gemini_key = os.getenv("GEMINI_API_KEY")
print(serp_key)
print(gemini_key)

def scrape_serp(keyword: str, num_results: int = 10) -> list[dict]:
    
    api_key = os.getenv("SERPAPI_KEY")
    if not api_key:
        raise ValueError("SERPAPI_KEY not found in .env")

    params = {
        "q": keyword,
        "api_key": api_key,
        "num": num_results,
        "engine": "google", 
        "hl" : "en",
        "gl": "us"
    }

    try:
        response = requests.get("https://serpapi.com/search", params=params)
        response.raise_for_status()  
        data = response.json()
        
        return {
            "organic": data.get("organic_results", []),
            "answer_box": data.get("answer_box", {}),
            "paa": data.get("related_questions", [])  # People Also Ask
        }
    except requests.exceptions.RequestException as e:
        print(f"Error fetching SERP data: {e}")
        return []

# Example usage (test in isolation):
if __name__ == "__main__":
    results = scrape_serp("best running shoes 2024")
    for idx, result in enumerate(results, 1):
        print(f"{idx}. {result['title']}\n   {result['link']}\n")
