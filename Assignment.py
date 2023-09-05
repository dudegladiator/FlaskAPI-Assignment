from flask import Flask, request, jsonify
from datetime import datetime
import pandas as pd
import requests

app = Flask(__name__)

url = 'https://app.ylytic.com/ylytic/test'


try:
    response = requests.get(url)

    # Checking if the request was successful (status code 200)
    if response.status_code == 200:
        # Loading the JSON data into a Python dictionary
        json_data = response.json()
        
        # Extracting the "comments" part of the JSON data
        comments_data = json_data.get("comments", [])
        
        # Converting the "comments" data into a Pandas DataFrame
        df = pd.DataFrame(comments_data)
        df['at'] = pd.to_datetime(df['at'])

        print('Loaded Successfully')
    else:
        
        print(f"Failed to retrieve data. Status code: {response.status_code}")
except Exception as e:
    print(f"An error occurred: {str(e)}")

@app.route('/')
def home():
    return 'Welcome to the Ylytic Assignment Solution!'


@app.route('/search')
def search():
    # Extract query parameters from the URL
    
    search_author = request.args.get('search_author')
    at_from = request.args.get('at_from')
    at_to = request.args.get('at_to')
    like_from = request.args.get('like_from')
    like_to = request.args.get('like_to')
    reply_from = request.args.get('reply_from')
    reply_to = request.args.get('reply_to')
    search_text = request.args.get('search_text')

    if response.status_code != 200:
        return jsonify({'error': 'Failed to retrieve data.'})
    
    
    query = df.copy()  # Created a copy of the DataFrame

    
    #Applying filters to the DataFrame
    if at_from:
        at_from_date = datetime.strptime(at_from, '%d-%m-%Y')
        at_from_date = at_from_date.strftime('%Y-%m-%d')
        query = query[query['at'] >= at_from_date]

    if at_to:
        at_to_date = datetime.strptime(at_to, '%d-%m-%Y')
        at_to_date = at_to_date.strftime('%Y-%m-%d')
        query = query[query['at'] <= at_to_date]

    if like_from:
        query = query[query['like'] >= int(like_from)]

    if like_to:
        query = query[query['like'] <= int(like_to)]

    if reply_from:
        query = query[query['reply'] >= int(reply_from)]

    if reply_to:
        query = query[query['reply'] <= int(reply_to)]
        
    if search_author:
        query = query[query['author'] == search_author]
        
    if search_text:
        #search_text = fr'\b{search_text}\b'
        query = query[query['text'].str.contains(search_text, case=False)]

    # Serializing the results to JSON
    serialized_results = query.to_dict(orient='records')


    return jsonify(serialized_results)


if __name__ == '__main__':
    app.run(debug=True)
    
 
    
    
