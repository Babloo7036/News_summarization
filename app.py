import streamlit as st
import requests

# Flask API URL
FLASK_API_URL = "http://127.0.0.1:5000/analyze-news"

# Streamlit App
st.title("News Sentiment Analyzer")
st.write("Enter a company name to analyze news sentiment and get insights.")

# Input for company name
company_name = st.text_input("Company Name",)

if st.button("Analyze"):
    if company_name:
        # Call Flask API
        response = requests.post(FLASK_API_URL, json={"company_name": company_name})
        
        if response.status_code == 200:
            data = response.json()
            
            # Display results
            st.header(f"Analysis for {data['Company']}")
            
            # Articles
            st.subheader("Articles")
            for article in data["Articles"]:
                st.write(f"**Title:** {article['Title']}")
                st.write(f"**Summary:** {article['Summary']}")
                st.write(f"**Sentiment:** {article['Sentiment']}")
                st.write(f"**Topics:** {article['key_words']}")
                st.audio(article["Hindi_Audio"], format="audio/mp3")
                st.write("---")
            
            # Comparative Sentiment Score
            st.subheader("Comparative Sentiment Score")
            st.write(f"**Sentiment Distribution:** {data['Comparative Sentiment Score']['Sentiment Distribution']}")
            
            st.write("**Coverage Differences:**")
            for insight in data["Comparative Sentiment Score"]["Coverage Differences"]:
                st.write(f"- **Comparison:** {insight['Comparison']}")
                st.write(f"- **Impact:** {insight['Impact']}")
            
            # Final Sentiment Analysis
            st.subheader("Final Sentiment Analysis")
            st.write(data["Final Sentiment Analysis"])
            
            # Audio
            # st.subheader("Audio Summary")
            # st.audio(data["Audio"], format="audio/mp3")
        else:
            st.error(f"Error: {response.json().get('error', 'Unknown error')}")
    else:
        st.error("Please enter a company name.")