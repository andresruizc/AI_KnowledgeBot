import streamlit as st
import numpy as np


def youtube_transcript_ui(youtube_transcript):
                                    
    if youtube_transcript != '':
        download_str_youtube_trasncript = []
        with st.expander("Video transcript"):
            down_button_trans = st.empty()
        
            st.success(youtube_transcript,icon="🎙️")
            download_str_youtube_trasncript.append("Transcript:" + youtube_transcript)

            if download_str_youtube_trasncript:
                download_str_youtube_trasncript = '\n'.join(download_str_youtube_trasncript)
                down_button_trans.download_button('Download',download_str_youtube_trasncript)                 
                                    

def youtube_summary_ui(youtube_summary):

    if youtube_summary != '':
        download_str_youtube_summary = []
        with st.expander("Video summary"):
            down_button = st.empty()
        
            st.success(youtube_summary,icon="📖")
            download_str_youtube_summary.append("Summary:" + youtube_summary)

            if download_str_youtube_summary:
                download_str_youtube_summary = '\n'.join(download_str_youtube_summary)
                down_button.download_button('Download',download_str_youtube_summary)
    
    
def youtube_cost_ui(youtube_qa_cost,youtube_summary_cost):

    with st.expander("Cost"):
                                            
        st.error("Q&A:   " + str(np.round(youtube_qa_cost,4)) + " $")
        st.error("Summary:  " + str(np.round(youtube_summary_cost,4)) + " $")

def pdf_cost_ui(pdf_qa_cost,sample_questions_cost,summary_cost, main_takeaways_cost):

    with st.expander("Cost"):
                                            
        st.error("Sample questions:  " + str(np.round(sample_questions_cost,4)) + " $")
        st.error("Summary:  " + str(np.round(summary_cost,4)) + " $")
        st.error("Takeaway ideas:  " + str(np.round(main_takeaways_cost,4)) + " $")
        st.error("Q&A:   " + str(np.round(pdf_qa_cost,4)) + " $")


def youtube_qa_ui(ss):

    download_str = []
    with st.expander("Q&A", expanded=True):

        down_button = st.empty()

        for i in range(len(ss['generated'])-1, -1, -1):
            st.info(ss["past"][i],icon="🧐")
            st.success(ss["generated"][i], icon="🤖")
            download_str.append("User: " + ss["past"][i])
            download_str.append("Chatbot: " + ss["generated"][i])

        if download_str:
            download_str = '\n'.join(download_str)
            down_button.download_button('Download chat',download_str)


def pdf_summary_ui(pdf_summary):

    download_str_pdf_summary = []
    with st.expander("PDF summary"):
        down_button = st.empty()

        st.success(pdf_summary,icon="📖")
        download_str_pdf_summary.append("Summary:" + pdf_summary)

        if download_str_pdf_summary:
            download_str_pdf_summary = '\n'.join(download_str_pdf_summary)
            down_button.download_button('Download',download_str_pdf_summary)

def pdf_takeaway_ui(pdf_takeaway):

    download_str_pdf_takeaway = []
    with st.expander("Main takeaways"):
        down_button = st.empty()

        st.success(pdf_takeaway,icon="📖")
        download_str_pdf_takeaway.append("Takeaway ideas:" + pdf_takeaway)

        if download_str_pdf_takeaway:
            download_str_pdf_takeaway = '\n'.join(download_str_pdf_takeaway)
            down_button.download_button('Download',download_str_pdf_takeaway)


def pdf_qa_ui(pdf_question,pdf_answer,callback_download):

    download_qa_pdf = []
    with st.expander("Q&A",expanded=True):

        down_button = st.empty()

        for i in range(len(pdf_question)-1, -1, -1):
            st.info(pdf_question[i],icon="🧐")
            st.success(pdf_answer[i], icon="🤖")
            download_qa_pdf.append("User: " + pdf_question[i])
            download_qa_pdf.append("Chatbot: " + pdf_answer[i])

        if download_qa_pdf:
            download_qa_pdf = '\n'.join(download_qa_pdf)
            down_button.download_button('Download chat',download_qa_pdf,on_click=callback_download)


def pdf_sample_questions(sample_questions,callback_download):
    download_str_pdf = []
    with st.expander("Sample questions"):

        down_button = st.empty()

        for i in range(len(sample_questions)):
            st.info(sample_questions[i]["question"],icon="🧐")
            st.success(sample_questions[i]["answer"], icon="🤖")
            download_str_pdf.append("Question: " + sample_questions[i]["question"])
            download_str_pdf.append("Answer: " + sample_questions[i]["answer"])

        if download_str_pdf:
            download_str_pdf = '\n'.join(download_str_pdf)
            down_button.download_button('Download',download_str_pdf,on_click=callback_download)

                                   
def get_text():
    st.info("Please enter a YouTube video URL press Enter ↵")
    input_text = st.text_input("", placeholder="Youtube Video URL", key="input")
    return input_text

def small_video(video_url):

    width = 60

    width = max(width, 0.01)
    side = max((100 - width) / 2, 0.01)

    _, container, _ = st.columns([side, width, side])
    return container.video(data=video_url)

