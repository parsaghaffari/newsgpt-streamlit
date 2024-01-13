from copy import deepcopy
import requests
import json
from datetime import datetime
import streamlit as st

HEADERS = {
    'X-AYLIEN-NewsAPI-Application-ID': st.secrets['NEWSAPI_APP_ID'],
    'X-AYLIEN-NewsAPI-Application-Key': st.secrets['NEWSAPI_APP_KEY']
}
STORIES_ENDPOINT = 'https://api.aylien.com/news/stories'

def make_newsapi_request(
        endpoint,
        params,
        headers,
        trials=10,
        wait_seconds=30,
):
    for i in range(trials):
        try:
            response = requests.get(
                endpoint,
                params,
                headers=headers
            )
            return response.json()
        except Exception as e:
            print("uncaught exception validating request")
            raise e

def retrieve_stories(params,
                     n_pages=1,
                     headers=HEADERS,
                     endpoint=STORIES_ENDPOINT,
                     verbose=False):
    params = deepcopy(params)
    stories = []
    cursor = '*'
    for i in range(n_pages):
        if verbose:
            print(f'page: {i}, stories: {len(stories)}')
        params['cursor'] = cursor
        data = make_newsapi_request(endpoint, params, headers)
        stories += data["stories"]
        if data.get('next_page_cursor', '*') != cursor:
            cursor = data['next_page_cursor']
        else:
            break
    return stories

def convert_date_format(date_str):
    # Parse the input date string
    date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")

    # Format the date to the desired output format
    formatted_date = date_obj.strftime("%Y-%m-%d %H:%M:%S")

    return formatted_date