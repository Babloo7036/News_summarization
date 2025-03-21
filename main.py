from flask import Flask, request, jsonify,render_template
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
from gtts import gTTS
import pandas as pd
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

# News Extraction Function
def fetch_news_articles(company_name):
    url = f"https://news.google.com/search?q={company_name}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    articles = []
    for item in soup.find_all('article')[:10]:  # Limit to 10 articles
        title = item.find('a', class_='DY5T1d').text
        link = "https://news.google.com" + item.find('a', class_='DY5T1d')['href'][1:]
        summary = item.find('div', class_='Da10Tb').text if item.find('div', class_='Da10Tb') else ""
        
        articles.append({
            "title": title,
            "link": link,
            "summary": summary
        })
    return articles

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
    df = pd.DataFrame(articles)
    sentiment_counts = df['sentiment'].value_counts()
    return sentiment_counts

# Text-to-Speech (TTS) Function
def generate_tts(text, output_file="output.mp3"):
    tts = gTTS(text=text, lang='hi')
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
        article['sentiment'] = analyze_sentiment(article['summary'])
    
    sentiment_counts = comparative_analysis(articles)
    tts_file = generate_tts(f"कंपनी {company_name} के बारे में समाचार विश्लेषण।")
    
    return jsonify({
        "articles": articles,
        "sentiment_counts": sentiment_counts.to_dict(),
        "tts_file": tts_file
    })

# Run the Flask App
if __name__ == '__main__':
    app.run(debug=True)