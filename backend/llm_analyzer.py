import google.generativeai as genai
import streamlit as st
import os
from typing import List, Dict

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('models/gemini-2.5-flash-lite')

def analyze_serp_with_llm(serp_data: List[Dict]) -> str:
    #preparing prompt for gemini
    snippets = [result.get("snippet", "") for result in serp_data]
     prompt = f"""
    You are a Senior SEO Strategist. Analyze the following Google SERP data to reverse-engineer the ranking requirements:
    DATA:{snippets}

    IdentifyAdvanced SEO Audit in Markdown:
    1. **Search Intent Analysis**: Identify if the intent is Informational, Commercial, or Transactional. Why is Google rewarding these specific pages?
    2. **Semantic Keyword Map**: Extract secondary LSI keywords and "Entities" (topics, brands, or technical terms) that appear across multiple top results.
    3. **Content Structure Patterns**: Identify the winning format (e.g., "The ultimate guide", "Top X listicle", "Calculator/Tool"). 
    4. **The 'Content Gap' Opportunity**: What is one thing none of these competitors are explaining well that we can capitalize on?
    5. **3 High-Impact Recommendations**: Specific, technical steps to outperform these results.
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
