import os
from dotenv import load_dotenv
import google.generativeai as genai
import streamlit as st
from langchain.sql_database import SQLDatabase 
from langchain.chains import create_sql_query_chain
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()

API_KEY = os.getenv('Google_API_KEY')

genai.configure(api_key=API_KEY)

# db details 
# username = 'avnadmin'
# password = 'AVNS_JGYSlUE8_DMQFL0Y4ml'
# host = 'pg-gemini-server-gem-postgre.a.aivencloud.com'
# port = '22752'  
# database_name = 'pg-gemini-server'


db = SQLDatabase.from_uri("postgres://avnadmin:AVNS_Nq9wk_bgSlbqY2FncEY@pg-gemini-gem-postgre.a.aivencloud.com:22752/geminitestdata?sslmode=require")


def get_gemini_response(prompt):
    # model = genai.GenerativeModel('gemini-pro')
    model = ChatGoogleGenerativeAI(model="gemini-pro" , google_api_key=API_KEY)
    chain = create_sql_query_chain(model, db)
    response = chain.invoke(prompt)
    # response = model.generate_content(prompt)
    return response


st.set_page_config(page_title="Text to SQL Query Generator")
st.header("Gemini App to Get SQL Query")

question = st.text_input("Input: ",key="input")
submit = st.button("Submit")

if submit:
    response = get_gemini_response({"question":question})
    print(response)
    query = "Query : " + response
    output = "Output : " + db.run(response)
    print(query)
    print(output)
    st.header(query)
    st.header(output)