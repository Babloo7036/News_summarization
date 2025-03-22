from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
from gtts import gTTS
import pandas as pd
import os
import uuid

app = Flask(__name__)

@app.route('/')
def home():
    return 'Welcome this is to the News summarization API'

# News Extraction Function
def fetch_news_articles(company_name):
    urls = [
        f"https://www.bbc.com/search?q={company_name}&page=0",
        f"https://www.bbc.com/search?q={company_name}&page=1",
        f"https://www.bbc.com/search?q={company_name}&page=2",
        f"https://www.bbc.com/search?q={company_name}&page=3",
        f"https://www.bbc.com/search?q={company_name}&page=4",
        f"https://www.bbc.com/search?q={company_name}&page=5"
    ]
    articles = []
    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            for item in soup.find_all('div', class_='sc-c6f6255e-0 eGcloy'):
                title = item.find('h2').text
                summary = item.find('div', class_='sc-4ea10043-3 kMizuB').text
                articles.append({
                    "Title": title,
                    "Summary": summary,
                    "Sentiment": "",
                    "Topics": []  # Placeholder for topic extraction
                })
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            continue

    return articles[:15]

# Sentiment Analysis Function
def analyze_sentiment(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return "Positive"
    elif analysis.sentiment.polarity < 0:
        return "Negative"
    else:
        return "Neutral"

# Comparative Analysis Function
def comparative_analysis(articles):
    sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}
    for article in articles:
        sentiment_counts[article["Sentiment"]] += 1
    return sentiment_counts

# Generate Comparative Insights
def generate_comparative_insights(articles):
    insights = []
    for i in range(len(articles) - 1):
        comparison = f"Article {i + 1} highlights {articles[i]['Title']}, while Article {i + 2} discusses {articles[i + 1]['Title']}."
        impact = f"The first article focuses on {articles[i]['Sentiment']} aspects, while the second highlights {articles[i + 1]['Sentiment']} aspects."
        insights.append({"Comparison": comparison, "Impact": impact})
    return insights

# Topic Extraction (Placeholder - Replace with actual topic extraction logic)
def extract_topics(text):
    # Placeholder logic for topic extraction
    topics = ["Electric Vehicles", "Stock Market", "Innovation", "Regulations", "Autonomous Vehicles"]
    return topics[:2]  # Return 2 random topics for demonstration

# Text-to-Speech (TTS) Function
def generate_tts(text, lang='hi'):
    unique_id = str(uuid.uuid4())
    output_file = f"output_{unique_id}.mp3"
    tts = gTTS(text=text, lang=lang)
    tts.save(output_file)
    return output_file

# API Endpoint
@app.route('/analyze-news', methods=['POST'])
def analyze_news():
    data = request.json
    company_name = data.get('company_name')
    
    if not company_name:
        return jsonify({"error": "Company name is required"}), 400
    
    articles = fetch_news_articles(company_name)
    
    for article in articles:
        article["Sentiment"] = analyze_sentiment(article["Summary"])
        article["Topics"] = extract_topics(article["Summary"])
    
    sentiment_counts = comparative_analysis(articles)
    comparative_insights = generate_comparative_insights(articles)
    tts_file = generate_tts(f"कंपनी {company_name} के बारे में समाचार विश्लेषण।")
    
    response = {
        "Company": company_name,
        "Articles": articles,
        "Comparative Sentiment Score": {
            "Sentiment Distribution": sentiment_counts,
            "Coverage Differences": comparative_insights,
            "Topic Overlap": {
                "Common Topics": list(set(articles[0]["Topics"]).intersection(articles[1]["Topics"])),
                "Unique Topics in Article 1": list(set(articles[0]["Topics"]).difference(articles[1]["Topics"])),
                "Unique Topics in Article 2": list(set(articles[1]["Topics"]).difference(articles[0]["Topics"]))
            }
        },
        "Final Sentiment Analysis": f"{company_name}'s latest news coverage is mostly {max(sentiment_counts, key=sentiment_counts.get)}.",
        "Audio": f"/tts/{tts_file}"
    }
    
    return jsonify(response)

# Serve TTS files
@app.route('/tts/<filename>')
def serve_tts(filename):
    return send_from_directory(os.getcwd(), filename)

# Run the Flask App
if __name__ == '__main__':
    app.run(debug=True)