import streamlit as st
import json
import timeago, datetime
import asyncio
from llm import *
from newsapi import *

st.set_page_config(page_icon="📰", page_title="NewsGPT")
st.title('NewsGPT')

"""Hello 👋🏻 You can use NewsGPT to get the latest news about anything–any topic, category, entity or event."""

st.markdown("### Search the news")
user_query = st.text_input("Enter a topic, category, entity or event", placeholder="Enter your query in plain English")

st.markdown("""Examples:
- Show me articles that have Elon Musk in their title, but not SpaceX
- What happened in biotech 3 months ago in Germany?
- What are the latest car crashes?
- What's in the news about the president of China that has a negative sentiment?
- What's the latest news about ESG in banking?""")

async def search_news():
    query = await generate_query(user_query)
    return query

if st.button("Search"):
    query = asyncio.run(search_news())
    aql = query.split("\n")[1]
    params = json.loads(query.split("\n")[2])
    st.session_state['aql'] = aql
    st.session_state['params'] = params
    
    stories = retrieve_stories({
        "aql": aql,
        **params,
        "language": ["en"],
    }, n_pages=1, verbose=True)
    
    st.session_state['stories'] = stories

# Render the list of stories outside the "Search" button block
if 'stories' in st.session_state and len(st.session_state['stories']) > 0:
    st.markdown("**Generated query**")
    st.info(f"aql: {st.session_state['aql']}")
    st.info(f"params: {st.session_state['params']}")
    st.markdown("**Results**")
    results_md = ""
    for story in st.session_state['stories']:
        results_md += f"- [{story['title']}]({story['links']['permalink']}) - {story['source']['name']} ({timeago.format(convert_date_format(story['published_at']))})\n"
    st.markdown(results_md)

    st.markdown("### Summarise the news")

    num_sentences = st.slider(f"Number of sentences in the summary:", min_value=1, max_value=10, value=3)
    if st.button("Summarise"):
        headlines = [story['title'] for story in st.session_state['stories']]
        summary = summarise_news(headlines, num_sentences)
        st.markdown(summary)