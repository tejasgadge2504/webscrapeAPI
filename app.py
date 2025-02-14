from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_input_fields(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        
        soup = BeautifulSoup(response.text, 'html.parser')
        input_fields = soup.find_all('input')
        
        fields_data = []
        for field in input_fields:
            field_info = {
                'name': field.get('name', 'N/A'),
                'type': field.get('type', 'N/A'),
                'value': field.get('value', 'N/A'),
                'id': field.get('id', 'N/A'),
                'class': field.get('class', 'N/A')
            }
            fields_data.append(field_info)
        
        return fields_data
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json()
    url = data.get("url")
    if not url:
        return jsonify({"error": "URL is required"}), 400
    
    fields = get_input_fields(url)
    return jsonify(fields)

if __name__ == '__main__':
    app.run(debug=True)
