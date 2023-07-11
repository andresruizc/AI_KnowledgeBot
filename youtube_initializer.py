import streamlit as st

ss = st.session_state

def youtube_initialize():
        if 'generated' not in ss:
            ss['generated'] = []

        if 'past' not in ss:
            ss['past'] = []

        if "process_clicked" not in ss:
            ss.process_clicked = False
    
        if "user_question"not in ss:
            ss.user_question = ""

        if "process_chat" not in ss:
            ss.process_chat = False

        if "reset" not in ss:
            ss.reset = False

        if "new_video" not in ss:
            ss.new_video = False

        if "youtube_summary" not in ss:
            ss.youtube_summary = ''
        
        if "response" not in ss:
            ss.response = ''

        if "youtube_transcript" not in ss:
            ss.youtube_transcript = ''

        if "youtube_summary_created" not in ss:
            ss.youtube_summary_created = False

        if "youtube_qa_cost" not in ss:
            ss.youtube_qa_cost = 0

        if "youtube_summary_cost" not in ss:
            ss.youtube_summary_cost = 0

        if "process_clicked_video" not in ss:
            ss.process_clicked_video = False

def callback_process():
    ss.process_clicked = True

def callback_process_new_video():
    ss.process_clicked = False
    ss.process_clicked_video = True

def callback_chat():
    ss.process_chat = True

def callback_reset():
    ss.reset = True

def callback_new_video():
    ss.new_video = True
