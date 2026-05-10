from flask import Flask, jsonify
from dotenv import load_dotenv
import boto3
import os
from datetime import datetime, timedelta

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

app = Flask(__name__)

def get_cost_data():
    client = boto3.client('ce')
    end = datetime.today().strftime('%Y-%m-%d')
    start = (datetime.today() - timedelta(days=30)).strftime('%Y-%m-%d')
    
    response = client.get_cost_and_usage(
        TimePeriod={'Start': start, 'End': end},
        Granularity='DAILY',
        Metrics=['UnblendedCost'],
        GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
    )
    return response['ResultsByTime']

@app.route('/api/costs')
def costs():
    data = get_cost_data()
    return jsonify(data)

@app.route('/')
def index():
    return 'RESIL Cloud Dashboard API is running'

if __name__ == '__main__':
    app.run(debug=True)
