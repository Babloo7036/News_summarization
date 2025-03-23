from flask import Flask, request, jsonify, send_from_directory
from utils import *

app = Flask(__name__)

kw_model = KeyBERT()

@app.route('/')
def home():
    return 'Welcome this is to the News summarization API'

@app.route('/analyze-news', methods=['POST'])
def analyze_news():
    try:
        data = request.json
        company_name = data.get('company_name')
        
        if not company_name:
            return jsonify({"error": "Company name is required"}), 400
        
        articles = fetch_news_articles(company_name)
        
        if not articles:
            return jsonify({"error": "No articles found"}), 404
        
        for article in articles:
            article["Sentiment"] = analyze_sentiment(article["Summary"])
            article["key_words"] = extract_keywords(article["Summary"])
            article["Hindi_Audio"] = generate_hindi_audio(article["Summary"])
        
        sentiment_counts = comparative_analysis(articles)
        comparative_insights = generate_comparative_insights(articles)
        
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
        }
        
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/tts/<filename>')
def serve_tts(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=False)