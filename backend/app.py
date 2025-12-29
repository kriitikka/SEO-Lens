import streamlit as st
from serp_scraper import scrape_serp
from llm_analyzer import analyze_serp_with_llm
from seo_recommender import generate_content_recommendations

st.set_page_config(page_title=" SEO Gemini", layout="wide")

# Sidebar for inputs
with st.sidebar:
    st.header("Settings")
    keyword = st.text_input("Keyword", placeholder="Ask Anything", key="keyword_input")
    num_results = st.slider("Number of SERP Results", 5, 20, 10)

#UI
st.title(f"SEO Analysis \n{keyword}")
if st.button("Analyze", type="primary"):
    with st.spinner("Scraping Google and analyzing with Gemini..."):
        #Scraping SERP
        serp_data = scrape_serp(keyword, num_results)
        
        #Analyzing with Gemini
        st.subheader(" Top Ranking Patterns")
        analysis = analyze_serp_with_llm(serp_data)
        st.markdown(analysis)
        
        #Generating Recommendations
        st.subheader(" Your SEO Blueprint")
        recommendations = generate_content_recommendations(keyword, serp_data)
        st.markdown(recommendations)
        st.divider()
        full_report = f"# SEO Report for: {keyword}\n\n## Analysis\n{analysis}\n\n## Recommendations\n{recommendations}"
        
        if hasattr(st, "copy_to_clipboard"):
            if st.button("Copy Full Report"):
                st.copy_to_clipboard(full_report)
                st.toast("Report copied!")

    st.success("Done! ")
