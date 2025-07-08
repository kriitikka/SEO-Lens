import requests
import os
import json
from pathlib import Path
import streamlit as st

serp_key = st.secrets["SERPAPI_KEY"]
gemini_key = st.secrets["GEMINI_API_KEY"]
print(serp_key)
print(gemini_key)

def scrape_serp(keyword: str, num_results: int = 10) -> list[dict]:
    """
    Fetches top Google search results for a keyword using SerpAPI.
    Returns a list of dictionaries with 'title', 'link', and 'snippet'.
    """
    api_key = st.secrets["SERPAPI_KEY"]
    if not api_key:
        raise ValueError("SERPAPI_KEY not found in .env")

    params = {
        "q": keyword,
        "api_key": api_key,
        "num": num_results,
        "engine": "google"  # Use 'google_images' or 'google_news' for other types
    }

    try:
        response = requests.get("https://serpapi.com/search", params=params)
        response.raise_for_status()  # Raises HTTPError for bad responses
        return response.json().get("organic_results", [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching SERP data: {e}")
        return []

# Example usage (test in isolation):
if __name__ == "__main__":
    results = scrape_serp("best running shoes 2024")
    for idx, result in enumerate(results, 1):
        print(f"{idx}. {result['title']}\n   {result['link']}\n")
