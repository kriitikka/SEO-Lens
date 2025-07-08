import google.generativeai as genai
import streamlit as st
import os
from typing import List, Dict

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('models/gemini-1.5-flash-latest')

def analyze_serp_with_llm(serp_data: List[Dict]) -> str:
    #preparing prompt for gemini
    snippets = [result.get("snippet", "") for result in serp_data]
    prompt = f"""
    Analyze these top Google search snippets for SEO patterns:
    {snippets}

    Identify:
    1. Common keywords (besides the main query).
    2. Content structure (e.g., lists, comparisons).
    3. Sentiment tone (positive/neutral/authoritative).
    4. 3 actionable recommendations to rank higher.

    Return in Markdown format with headings.
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error analyzing with Gemini: {e}"

#test
if __name__ == "__main__":
    test_data = [
        {"title": "Best Running Shoes 2024", "snippet": "Top 10 running shoes for marathon training"},
        {"title": "Buying Guide: Running Shoes", "snippet": "Compare Nike, Adidas, and Hoka for comfort"}
    ]
    print(analyze_serp_with_llm(test_data))
