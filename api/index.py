from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

@app.route('/api')
def proxy_parse():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }
        response = requests.get(url, headers=headers, timeout=10)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        title = soup.title.string.strip() if soup.title else 'No title'

        price_match = re.search(r'"price":"(\\d+)"', html)
        price = int(price_match.group(1)) if price_match else None

        img_match = re.search(r'https://p\\d+\\.toutiaoimg\\.com/large/[\\w_]+\\.jpg', html)
        image_url = img_match.group(0) if img_match else None

        return jsonify({
            'title': title,
            'price_yuan': price,
            'image_url': image_url
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
