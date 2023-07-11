import streamlit as st

ss = st.session_state

def pdf_initialize():
        if "counter_down" not in ss:
            ss.counter_down = 0

        if "process_chat_pdf" not in ss:
            ss.process_chat_pdf = False

        if "button_down" not in ss:
            ss.button_down = False

        if "pdf_question" not in ss:
            ss['pdf_question'] = []
            
        if "pdf_answer" not in ss:
            ss['pdf_answer'] = []

        if 'pdf_summary' not in ss:
            ss.pdf_summary = ''
        
        if "pdf_main_takeaways" not in ss:
            ss.pdf_main_takeaways = ''

        if 'summary_pdf_created' not in ss:
            ss.summary_pdf_created = False
        
        if "main_takeaway_pdf_created" not in ss:
            ss.main_takeaway_pdf_created = False

        if 'new_file' not in ss:
            ss.new_file = False 

        if "db_pdf" not in ss:
            ss.db_pdf = False

        if "db" not in ss:
            ss.db = None

        if "pdf_docs_summary" not in ss:
            ss.pdf_docs_summary = None

        if "pdf_qa_cost" not in ss:
            ss.pdf_qa_cost = 0
        
        if "pdf_summary_cost" not in ss:
            ss.pdf_summary_cost = 0
        
        if "pdf_takeaways_cost" not in ss:
            ss.pdf_takeaways_cost = 0

        if "pdf_sample_qa_cost" not in ss:
            ss.pdf_sample_qa_cost = 0                               

def callback_chat_pdf():
    ss.process_chat_pdf = True

def callback_download_pdf():
    ss.button_down = True