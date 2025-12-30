import streamlit as st
from serp_scraper import scrape_serp
from llm_analyzer import analyze_serp_with_llm, generate_content_recommendations, analyze_aeo_with_llm

st.set_page_config(page_title=" SEO & AEO", layout="wide")

# Sidebar for inputs
with st.sidebar:
    st.header("Settings")
    keyword = st.text_input("Keyword",  placeholder="Ask Anything", key="keyword_input")
    num_results = st.slider("Number of SERP Results to Analyze", 5, 20, 10)

#UI
st.title(f"Dual Engine Analysis: SEO + AEO \n{keyword}")
if st.button("Analyze", type="primary"):
    with st.spinner("Mining Google SERP data and running AI audits..."):
        
        
        #Generating Recommendations
        st.subheader(" Your SEO Blueprint")
        full_data = scrape_serp(keyword, num_results)
            
        seo_analysis = analyze_serp_with_llm(full_data["organic"])
        seo_blueprint = generate_content_recommendations(keyword, full_data["organic"])
            
            # AEO Path
        aeo_analysis = analyze_aeo_with_llm(keyword, full_data)

            # 3. Display Results in Tabs or Columns
        tab1, tab2 = st.tabs(["SEO Analysis", "AEO Strategy"])
            
        with tab1:
                st.subheader("SEO Ranking Patterns")
                st.markdown(seo_analysis)
                st.subheader("Content Blueprint")
                st.markdown(seo_blueprint)
                
        with tab2:
                st.subheader("Answer Engine Strategy")
                st.markdown(aeo_analysis)
                if full_data["paa"]:
                    st.info(f"Analyzed {len(full_data['paa'])} 'People Also Ask' questions for this report.")

            # 4. Global Copy/Download Section
        st.divider()
        full_master_report = f"""# Master Report: {keyword}
---
## SEO AUDIT
{seo_analysis}
{seo_blueprint}

---
## AEO STRATEGY
{aeo_analysis}
"""
