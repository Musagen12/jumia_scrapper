from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from io import BytesIO
from datetime import datetime
import requests
import json
import psycopg2

app = Flask(__name__)

#########################################################################################



CORS(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:kali@localhost/scrapper'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///database.db'

db = SQLAlchemy(app)

class TrackedProducts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tracked_product_url = db.Column(db.String(1000))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, tracked_product_url):
        self.tracked_product_url = tracked_product_url


##########################################################################################

def db_conn():
     conn = psycopg2.connect(database="scrapper", host="localhost", user="postgres", password="kali")
     return conn

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


@app.route('/logs', methods=['GET', 'POST'])
def logs():
    if request.method == 'POST':
        conn = db_conn()
        cur = conn.cursor()
        cur.execute('''SELECT * FROM jumia''')
        data = cur.fetchall()
        cur.close()
        conn.close()

        return render_template('logs.html', data=data)
    else:
        return "GET request received, but this endpoint only accepts POST requests"

@app.route("/download")
def convert_to_csv():
    conn = db_conn()
    cur = conn.cursor()
    cur.execute('''SELECT * FROM jumia''')
    rows = cur.fetchall()
    cur.close()
    conn.close()

    if not rows:
        return "No data found"

    column_names = [desc[0] for desc in cur.description]
    df = pd.DataFrame(rows, columns=column_names)
    csv_data = bytes(df.to_csv(index=False).encode())
    return send_file(BytesIO(csv_data), download_name="Text.csv", as_attachment=True)


###############################################################################################

@app.route('/add_tracked_item', methods=['POST'])
def adding_tracked():
    if request.method == "POST":
        item_url = request.form.get('url')  # Use request.form to get form data
        print(item_url)
        if item_url:
            new_tracked_item_url = TrackedProducts(tracked_product_url=item_url)
            db.session.add(new_tracked_item_url)
            db.session.commit()
            return "Tracked item added successfully"
        else:
            return "Error: Tracked item URL is missing"
    return render_template("t.html")

# @app.route('/price_tracking', methods=['GET', 'POST'])
# def price_tracking():
#     rows = []
#     url = 'http://localhost:9080/crawl.json'
#     # tracked = TrackedProducts.query.all()  
#     tracked_products = TrackedProducts.query.all()
    
#     serialized_data = [{
#         'tracked_product_url': tracked.tracked_product_url
#     } for tracked in tracked_products]

#     for query in serialized_data:  
#         params = {
#             'spider_name': 'spec',
#             'start_requests': True,
#             'crawl_args': json.dumps({'cat': query}), 
#         }


#         if tracked_products:
#             response = requests.get(url, params=params)
        
#         # Check if the request was successful (status code 200)
#             if response.status_code == 200:
#                 # Assuming the response contains JSON data
#                 data = response.json()
#                 rows = data.get('items', [])

#             else:
#                 error_message = f"Request failed with status code {response.status_code}: {response.text}"
#                 return jsonify({"status": "error", "message": error_message}), response.status_code

#     return render_template('new.html', rows=rows)

@app.route('/price_tracking', methods=['GET', 'POST'])
def price_tracking():
    rows = []
    url = 'http://localhost:9080/crawl.json'
    tracked_products = TrackedProducts.query.all()
    
    for tracked in tracked_products:
        params = {
            'spider_name': 'spec',
            'start_requests': True,
            'crawl_args': json.dumps({'cat': tracked.tracked_product_url}), 
        }

        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            rows.extend(data.get('items', []))
        else:
            error_message = f"Request failed with status code {response.status_code}: {response.text}"
            return jsonify({"status": "error", "message": error_message}), response.status_code

    return render_template('new.html', rows=rows)




#######################################################################################################

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)