from flask import Flask, jsonify
import json
import requests
import urllib.parse

app = Flask(__name__)

@app.route("/test")
def hello_world():
    return "<p>Hello Africa.</p>"


@app.route("/scrape")
def scrape_route():
    return "Test"


@app.route('/scrapyrt')
def scrape():
    params = {
        'spider_name': 'test',
        'start_requests': True,
        'crawl_args': urllib.parse.quote(json.dumps({'cat': 'lenovo laptops'})),
    }

    # Construct the full URL with query parameters
    url = 'http://localhost:9080/crawl.json'
    
    # Make a GET request to the URL with params
    response = requests.get(url, params=params)
    

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Assuming the response contains JSON data
        data = response.json()
        return jsonify({"status": "success", "data": data})
    else:
        error_message = f"Request failed with status code {response.status_code}: {response.text}"
        return jsonify({"status": "error", "message": error_message}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)