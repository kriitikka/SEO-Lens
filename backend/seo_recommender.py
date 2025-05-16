# backend/seo_recommender.py
from typing import Dict, List
from llm_analyzer import model  # Reuse Gemini model

def generate_content_recommendations(keyword: str, serp_data: List[Dict]) -> str:
    """
    Uses Gemini to suggest optimized content based on SERP data.
    Returns: Markdown-formatted recommendations.
    """
    prompt = f"""
    You are an SEO expert. For the keyword '{keyword}', suggest:
    1. A compelling meta title (60 chars max).
    2. A meta description (160 chars max).
    3. 3 header (H2) ideas.
    4. 3 semantic keywords to include.

    Base this on top-ranking results:
    {[r.get('snippet', '')[:200] for r in serp_data]}
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating recommendations: {e}"

# Test
if __name__ == "__main__":
    test_data = [{"snippet": "Top 10 running shoes for 2024..."}]
    print(generate_content_recommendations("best running shoes", test_data))