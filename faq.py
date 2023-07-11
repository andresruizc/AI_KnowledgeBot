import streamlit as st

def faq():
    st.title("FAQ")
    st.markdown("""

    
## What to I need to use AI KnowledgeBot?
You need an OpenAI API key. Creating one is free, but it requires a credit card so that you can be charged for the cost of the API calls.

## Is it free to use AI KnowledgeBot?
No, it is not free. You will be charged for the cost of the API calls. 

## Which is the cost of using AI KnowledgeBot?

The cost depends on the length of the video or pdf and the number of questions you ask. There is a section in both the Youtube and PDF pages that shows you the cost of any operations you perform.

Questions about the video or pdf will cost around \$0.001 each.
                
To avoid surprises, you can set a budget for the credit card you used to create the OpenAI API key. You can set a soft limit and a hard limit. The soft limit will trigger a warning when the budget is reached. The hard limit will stop making API calls when the budget is reached.

## How does AI KnowledgeBot work with Youtube URLs videos?
When you upload a Youtube URL and process it, the video will be transcribed using OpenAI Whisper model. Then, the transcript will be divided into smaller text chunks. 

These chunks will be used to create embeddings using OpenAIEmbeddings and then stored in a special type of database called a vector index that allows for later search and retrieval.

Using a combination of OpenAI LLMs and Langchain, a summary of the video will be generated. In addition, users can ask questions about the video and get an answer.

Any of these interactions can be downloaded as a text file for later use.

The cost associated with the summary and Q&A is also available to the user.  

## How does AI KnowledgeBot work with PDFs?
When you upload a pdf and process it, it will be divided into smaller text chunks. In a similar way than with Youtube videos, embeddings will be created and stored in a vector index.

Users can ask questions about the pdf and get an answer. A small set of sample questions about the pdf will be randomly generated so that users can get a sense of how to interact with the AI.

A summary of the pdf can be generated, but it is not created by default because it is expensive and time consuming. In case you want to generate a summary, go to the settings page and set the "Generate summary" option to "Yes".

Any of these interactions can be downloaded as a text file for later use.

The cost associated with the summary and Q&A is also available to the user.  

"""
    )