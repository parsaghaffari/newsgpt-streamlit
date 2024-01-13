# NewsGPT

Hello 👋🏻 You can use NewsGPT to get the latest news about anything–any topic, category, entity or event. See it in action: [https://news-gpt-demo.streamlit.app/](https://news-gpt-demo.streamlit.app/)

NewsGPT is powered by GPT-3.5 and AYLIEN News API. The source code of NewsGPT can be accessed in this repository.

To run locally: 

1. Rename `.streamlit/secrets.example.toml` to `.streamlit/secrets.toml` and add your AYLIEN News API and OpenAI API keys to it
2. Install the dependencies by running `pip install -r requirements.txt`
3. Run `streamlit run app.py` in the root folder
