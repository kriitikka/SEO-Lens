# backend/seo_recommender.py
from typing import Dict, List
from llm_analyzer import model  # Reuse Gemini model

def generate_content_recommendations(keyword: str, serp_data: List[Dict]) -> str:
    context = [f"Title: {r.get('title')}\nSnippet: {r.get('snippet')}" for r in serp_data]
    
    prompt = f"""
    Act as a Content Optimizer. For the target keyword '{keyword}', generate a content plan that is '10x better' than the current top results.
    
    COMPETITOR DATA:
    {context}

    OUTPUT THE FOLLOWING:
    1. **High-CTR Meta Title**: Create a title that uses a 'Power Word' and stays under 60 chars.
    2. **Persuasive Meta Description**: A 155-character description with a clear Call to Action (CTA).
    3. **Optimized H1 & H2 Outline**: Provide a logical heading structure that covers the user's journey.
    4. **Semantic Cloud**: 5-7 NLP keywords that must be included to satisfy the search algorithm's topical relevance.
    5. **EEAT Signal**: One suggestion on how to prove "First-hand Experience" for this specific topic.
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
