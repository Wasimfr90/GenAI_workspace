import openai
import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv

# from secrect_key import openapi_key


# Loads environment variables from .env
load_dotenv()

# Set your OpenAI API key (you can also use environment variable)
openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("Excel Query Assistant with OpenAI")

uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file:
    # Read the Excel file
    df = pd.read_excel(uploaded_file)
    st.write("Preview of Excel Data:")
    st.dataframe(df)

    # Convert DataFrame to a string for prompt
    table_string = df.to_csv(index=False)

    # User query input
    user_query = st.text_input("Enter your question about the data:")

    if user_query:
        with st.spinner("Querying OpenAI..."):
            # Build the prompt
            prompt = f"""
You are a data analyst assistant. The user has provided a dataset in CSV format below:

{table_string}

Now, answer the following question based on the data:
{user_query}
"""

            # Send to OpenAI
            response = openai.chat.completions.create(
                model="gpt-4.1-nano",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that answers questions based on CSV data."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2
            )

            # answer = response['choices'][0]['message']['content']
            answer = response.choices[0].message.content
            st.markdown("### Answer:")
            st.write(answer)
