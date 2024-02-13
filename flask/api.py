from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    rows = []
    query = request.args.get('query')  # Get the query paramete
    params = {
        'spider_name': 'test',
        'start_requests': True,
        'crawl_args': json.dumps({'cat': query}),  # Don't encode JSON
    }

    url = 'http://localhost:9080/crawl.json'

    if query:
        response = requests.get(url, params=params)
    
    # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Assuming the response contains JSON data
            data = response.json()
            rows = data.get('items', [])

        else:
            error_message = f"Request failed with status code {response.status_code}: {response.text}"
            return jsonify({"status": "error", "message": error_message}), response.status_code

    return render_template('form.html', rows=rows)


if __name__ == '__main__':
    app.run(debug=True)