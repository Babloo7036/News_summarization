import streamlit as st
import requests

# Flask API URL
FLASK_API_URL = "http://127.0.0.1:5000/analyze-news"

# Streamlit App
st.title("News Sentiment Analyzer")
st.write("Enter a company name to analyze news sentiment and get insights.")

# Input for company name
company_name = st.text_input("Company Name")

if st.button("Analyze"):
    if company_name:
        with st.spinner("Analyzing news sentiment..."):
            try:
                response = requests.post(FLASK_API_URL, json={"company_name": company_name})
                response.raise_for_status()
                data = response.json()
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to the API. Error: {e}")
                st.stop()
            except ValueError:
                st.error("Invalid response from the API.")
                st.stop()
    else:
        st.error("Please enter a company name.")
        st.stop()

    # Display results
    if not data["Articles"]:
        st.warning("No articles found for the given company name.")
        st.stop()

    st.header(f"Analysis for {data['Company']}")

    # Articles
    st.subheader("Articles")
    for article in data["Articles"]:
        st.write(f"**Title:** {article['Title']}")
        st.write(f"**Summary:** {article['Summary']}")
        st.write(f"**Sentiment:** {article['Sentiment']}")
        st.write(f"**Topics:** {', '.join(article['key_words'])}")
        if article["Hindi_Audio"]:
            st.audio(article["Hindi_Audio"], format="audio/mp3")
        else:
            st.write("Audio not available.")
        st.write("---")

    # Comparative Sentiment Score
    st.subheader("Comparative Sentiment Score")
    st.write(f"**Sentiment Distribution:** {data['Comparative Sentiment Score']['Sentiment Distribution']}")

    with st.expander("Coverage Differences"):
        for insight in data["Comparative Sentiment Score"]["Coverage Differences"]:
            st.write(f"- **Comparison:** {insight['Comparison']}")
            st.write(f"- **Impact:** {insight['Impact']}")

    # Final Sentiment Analysis
    st.subheader("Final Sentiment Analysis")
    st.write(data["Final Sentiment Analysis"])

if st.button("Reset"):
    st.experimental_rerun()