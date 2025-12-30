import google.generativeai as genai
from dotenv import load_dotenv
import os
from typing import List, Dict

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
# Using the standard flash model for reliability, though your lite version works too
model = genai.GenerativeModel('models/gemini-2.5-flash-lite')

def analyze_serp_with_llm(serp_data: List[Dict]) -> str:
    """
    Performs a deep competitive analysis of the SERP landscape.
    """
    # Combining title and snippet gives the LLM better context on CTR patterns
    context = [f"Title: {r.get('title')}\nSnippet: {r.get('snippet')}" for r in serp_data]
    
    prompt = f"""
    You are a Senior SEO Strategist. Analyze the following Google SERP data to reverse-engineer the ranking requirements:
    
    DATA:
    {context}

    Please provide an Advanced SEO Audit in Markdown:
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

def analyze_aeo_with_llm(keyword: str, serp_data: Dict) -> str:
    # Extracting PAA and Answer Box for context
    paa_questions = [q.get("question") for q in serp_data.get("paa", [])]
    answer_box = serp_data.get("answer_box", {}).get("answer", "No direct answer found.")
    organic_snippets = [r.get("snippet", "") for r in serp_data.get("organic", [])[:5]]

    prompt = f"""
    You are an AEO (Answer Engine Optimization) Specialist. 
    Analyze the following search landscape for the query: "{keyword}" to determine how to become the 'definitive answer' for AI agents like Gemini, Perplexity, and SearchGPT.

    CONTEXT:
    - Current Google Answer Box: {answer_box}
    - People Also Ask (PAA): {paa_questions}
    - Top Snippets: {organic_snippets}

    Provide an AEO Strategic Report:
    1. **The 'Zero-Click' Target**: Write a perfect 40-60 word 'Answer Box' snippet that is more factual and concise than the current one.
    2. **Entity Knowledge Graph**: List the key entities (brands, technical terms, people) an AI expects to see to trust this content.
    3. **Q&A Roadmap**: List 3 specific questions (from PAA or inferred) that this content must answer in H2 tags.
    4. **Factual Density**: Suggest 2 data points or statistics that would make an AI cite this page as a source.
    5. **Structuring for LLMs**: Recommendation on using specific Schema (FAQ, HowTo, or Dataset).
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error analyzing AEO: {e}"
    

def generate_content_recommendations(keyword: str, serp_data: List[Dict]) -> str:
    """
    Generates high-CTR meta tags and content outlines based on SERP patterns.
    """
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

if __name__ == "__main__":
    test_data = [
        {"title": "Best Running Shoes 2024", "snippet": "We tested the top 10 running shoes for marathon training including Nike and Hoka."},
        {"title": "Running Shoe Buying Guide", "snippet": "Learn how to choose the right running shoes based on arch support and cushioning."}
    ]
    print(analyze_serp_with_llm(test_data))
