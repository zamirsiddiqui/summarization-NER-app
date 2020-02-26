# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import streamlit as st
#Summary Package
from gensim.summarization import summarize
#from sumy.parsers.plaintext import PlaintextParser
#from sumy.nlp.tokenizers import Tokenizer
#from sumy.summarizers.lex_rank import LexRankSummarizer
import spacy
import en_core_web_sm
nlp = en_core_web_sm.load()
#nlp = spacy.load("en_core_web_sm")
from spacy import displacy
#HTML_WRAPPER == """<div style = "overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem">{}</div>"""


#NLP
#@st.cache(allow_output_mutation=True)
def analyze_text(text):
    return nlp(text)
# Function for Sumy Summarization
def sumy_summarization(text):
    parser = PlaintextParser.from_string(text, Tokenizer("English"))
    lex_summarizer = LexRankSummarizer()
    summary = lex_summarizer(parser.document,3)
    summary_list = [str(sentence) for sentence in summary]
    result = ' '.join(summary_list)
    return result


# Web Scraping
from bs4 import BeautifulSoup
from urllib.request import urlopen

@st.cache
def get_text(url):
    page = urlopen(url)
    soup = BeautifulSoup(page, features="lxml")
    fetched_text = ' '.join(map(lambda p:p.text, soup.find_all('p')))
    return fetched_text



def main():
    st.title("Summary and Entity Checker") 
    activities = ["Summarize", "NER Checker", "NER for URL", "Summarize from URL"]
    choice = st.sidebar.selectbox("Select Activity" , activities)    
    if choice == 'Summarize':
        st.subheader("Summary with NLP")
        raw_text = st.text_area("Enter Text Here","Type Here...")
        summary_choice = st.selectbox("Summary Choice", ["Gensim", "Sumy Lex Rank"])
        if st.button('Summarize'):
            if summary_choice == 'Gensim':
                summary_result = summarize(raw_text)
            elif summary_choice == 'Sumy Lex Rank':
                summary_result = summarize(raw_text)            
            st.write(summary_result)
    if choice == 'NER Checker':
        st.subheader("Entity Recognition")
        raw_text = st.text_area("Enter Text Here","Type Here...")
        if st.button("Analyze"):
            nlpText = analyze_text(raw_text)
            html = displacy.render(nlpText, style = 'ent')
            html = html.replace("n\n","n")
            st.markdown(html,unsafe_allow_html=True)
        
    if choice == 'NER for URL':
        st.subheader('Analyze text from URL')
        url = st.text_input("Enter URL", "Type Here ...")
        if st.button("Check NER"):
            if url != "Type Here ...":
                result = get_text(url)
                nlpText = analyze_text(result)
                html = displacy.render(nlpText, style = 'ent')
                html = html.replace("n\n","n")
                st.markdown(html,unsafe_allow_html=True)
               # st.write(result)
    if choice == 'Summarize from URL':
        st.subheader('Analyze text from URL')
        url = st.text_input("Enter URL", "Type Here ...")
        if st.button("Summarize"):
            if url != "Type Here ...":
                result = get_text(url)
                summary_result = summarize(result)
                st.write(summary_result)
    
    

if __name__ == '__main__':
    main()
