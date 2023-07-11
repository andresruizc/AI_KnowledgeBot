import streamlit as st
from streamlit_option_menu import option_menu

import streamlit as st
from youtube_chat import create_db_from_youtube_video_url, get_response_from_query,load_docs,generate_random_questions,create_db_from_pdf,new_process_pdf,youtube_whisper
from helpers import small_video, youtube_transcript_ui,youtube_summary_ui,youtube_cost_ui,youtube_qa_ui,pdf_summary_ui,pdf_qa_ui,pdf_sample_questions,pdf_cost_ui,pdf_takeaway_ui
from youtube_initializer import youtube_initialize,callback_process,callback_process_new_video,callback_chat,callback_reset, callback_new_video
from pdf_initializer import callback_chat_pdf,callback_download_pdf,pdf_initialize
import numpy as np
from sidebar import sidebar
from langchain.callbacks import get_openai_callback
import os


ss = st.session_state

sidebar()

os.environ["OPENAI_API_KEY"] = ss.get("OPENAI_API_KEY")


st.subheader(" ")
selected = option_menu(menu_title=None,
        options=["Youtube", "PDF"],
        icons=["none", "none"],
        default_index=0,
        menu_icon="menu-up", 
        orientation="horizontal")



if selected == "Youtube":
        
        st.subheader("Enter a YouTube video")

        youtube_initialize()

        input_container = st.container()

        with input_container:
                
                chunk_size_yt = ss.get("frag_size_yt")
                frag_overlap_yt = ss.get("frag_overlap_yt")
                temperature_yt = ss.get("temperature_yt")
                model_yt = ss.get("model_yt")

                print("chunk_size_yt",chunk_size_yt)
                print("frag_overlap_yt",frag_overlap_yt)
                print("temperature_yt",temperature_yt)
                print("model_yt",model_yt)

                

                text_form = st.empty()
                user_input = text_form.text_input("", placeholder="Enter a YouTube video URL press Enter ↵",key="user_input2")

                if ss["OPENAI_API_KEY"].startswith("sk-"):

                    if user_input:
                                try:
                                    small_video(user_input)
                                except:
                                    st.error("Please make sure that you only enter a valid YouTube video URL")
                                    st.stop()
       
                                placeholder_process = st.empty()
                                if not ss.process_clicked_video and ss.user_question == "":
                                    placeholder_process.button("Process video!", on_click = callback_process)
                                
                                if ss.process_clicked:

                                    new_video = st.empty()
                                    
                                    if not ss.new_video:

                                        info_1 = st.empty()
                                        info_1.info("`Transcribing the video ...`")
                                        placeholder_process.empty() 
                                        with get_openai_callback() as cb:
                                            response,transcription = create_db_from_youtube_video_url(user_input,chunk_size_yt,frag_overlap_yt)
                                            ss.youtube_transcript = transcription
                                            ss.response = response

                                            print(cb)
                                        info_1.empty()
                                        

                                        if not ss.youtube_summary_created:
                                            with get_openai_callback() as cb:

                                                info_2 = st.empty()
                                                info_2.info("`Generating the summary ...`")

                                                prompt_summary = "Generate a summary of the youtube video uploaded."
                 
                                                ss.youtube_summary, docs = get_response_from_query(ss.response,prompt_summary,model_yt,temperature_yt,True)
                                                print(cb)
                                                ss.youtube_summary_cost += np.round(cb.total_cost,4)
        
                                            ss.youtube_summary_created = True
                                            info_2.empty()
                                        
                                        
                                        info_1.empty()

                                        ss.new_video = True

                                    new_video.button("New video!", on_click = callback_process_new_video)
                                    youtube_transcript_ui(ss.youtube_transcript)
                                    youtube_summary_ui(ss.youtube_summary)
                                    youtube_cost_ui(ss.youtube_qa_cost,ss.youtube_summary_cost)
                                    
                                    ss.user_question = st.chat_input("Ask a question and hit Enter",on_submit=callback_chat)

                                    if ss.user_question != "":

                                        if ss.process_chat:
                                            ss.process_chat = False
                                            info_ = st.empty()
                                            info_.info("`Generating Q&A question ...`")
                                            with get_openai_callback() as cb:
                                                response_, docs = get_response_from_query(ss.response, ss.user_question,model_yt,temperature_yt)
                                                print(cb)
                                                ss.youtube_qa_cost += np.round(cb.total_cost,4)
                                            info_.empty()
                                            
                                            ss.past.append(ss.user_question)
                                            ss.generated.append(response_)  

                                        if len(ss.past) > 0 and not ss.reset: youtube_qa_ui(ss)                      
                                            
                                else:
                                    ss.new_video = False
                                    
                                    ss.process_clicked,ss.process_chat,ss.youtube_summary_created,ss.process_clicked_video = False,False,False,False
                                    ss.youtube_qa_cost,ss.youtube_summary_cost = 0,0
                                    ss.past,ss.generated = [],[]
                                    ss.youtube_summary = ''
                                    ss.youtube_transcript = ''
                                    ss.response = ''
                                    ss.user_question = ""

                else:
                    st.error("Please enter a valid OpenAI API key in the sidebar.")

if selected == "PDF":
        
        st.subheader("Enter a PDF")

        pdf_initialize()

        uploaded_files = st.file_uploader("", type=["pdf"], accept_multiple_files=True)


        chunk_size_pdf = ss.get("frag_size_pdf")
        frag_overlap_pdf = ss.get("frag_overlap_pdf")
        temperature_pdf = ss.get("temperature_pdf")
        model_pdf  = ss.get("model_pdf")
        generate_summary_pdf = ss.get("generate_summary_pdf")
        num_sample_questions_pdf = ss.get("num_sample_questions_pdf")


        if ss["OPENAI_API_KEY"].startswith("sk-"):
            if uploaded_files:
                
                if ss.button_down:
                    ss.counter_down += 1

                if 'last_uploaded_files' not in ss or ss.last_uploaded_files != uploaded_files:
                    ss.last_uploaded_files = uploaded_files
                    ss.db_pdf = False

                    if 'eval_set' in ss:
                        del ss['eval_set']
                    if "pdf_question" in ss:
                        ss['pdf_question'] = []
                    if "pdf_answer" in ss:
                        ss['pdf_answer'] = []
                    
                    if "pdf_qa_cost" in ss:
                        ss.pdf_qa_cost = 0
        
                    if "pdf_sample_qa_cost" in ss:
                        ss.pdf_sample_qa_cost = 0  

                    ss.db = None
                    ss.pdf_docs_summary = None

                info_statusss = st.empty()
                if not ss.button_down and not ss.db_pdf:

                    info_statusss.info("`Processing pdf file ...`")
                    
                    loaded_docs = load_docs(uploaded_files)

                    print(loaded_docs)

                    ss.db,ss.pdf_docs_summary = create_db_from_pdf(loaded_docs,chunk_size_pdf,frag_overlap_pdf)

                    ss.db_pdf = True

                    info_statusss.empty()
                        
                    
                if 'eval_set' not in ss:
                
                    num_eval_questions = num_sample_questions_pdf
                    
                    info_statusss = st.empty()
                    
                    with get_openai_callback() as cb_sample:
                        info_statusss.info("`Generating sample questions ...`")
                        ss.eval_set = generate_random_questions(
                            loaded_docs, num_eval_questions,model_pdf,temperature_pdf, 2000)
                        
                        info_statusss.empty()
                        if ss.pdf_sample_qa_cost == 0:
                            ss.pdf_sample_qa_cost += np.round(cb_sample.total_cost,4)
                    
            
                    for i, qa_pair in enumerate(ss.eval_set):

                        answer_template =  f'{qa_pair["question"]}:\n{qa_pair["answer"]}'
            
                    with get_openai_callback() as cb:
                        
                        info_statusss_2 = st.empty()
                        info_statusss_2.info("`Generating summary ...`")

                        prompt_summary = "Generate a summary of the pdf file. Be as clear and detailed as possible."
                        ss.pdf_summary = new_process_pdf(ss.db,prompt_summary,model_pdf, temperature_pdf,True)
                        ss.summary_pdf_created = True

                        if ss.pdf_summary_cost == 0:
                                ss.pdf_summary_cost += np.round(cb.total_cost,4)
                        
                        info_statusss_2.empty()
                    

                    with get_openai_callback() as cb:
                        
                        info_statusss_3 = st.empty()
                        info_statusss_3.info("`Generating main takeaways ...`")
                        prompt_main_takeaway = "Enumerate the three main takeaways of the pdf file uploaded. Be clear and concise."
                        ss.pdf_main_takeaways = new_process_pdf(ss.db,prompt_main_takeaway,model_pdf, temperature_pdf,True)
                        ss.main_takeaway_pdf_created = True
                        
                        if ss.pdf_takeaways_cost == 0:
                                ss.pdf_takeaways_cost += np.round(cb.total_cost,4)
                
                        info_statusss_3.empty()

                pdf_sample_questions(ss.eval_set,callback_download_pdf)

                pdf_summary_ui(ss.pdf_summary)

                pdf_takeaway_ui(ss.pdf_main_takeaways)
                
                pdf_cost_ui(ss.pdf_qa_cost,ss.pdf_sample_qa_cost,ss.pdf_summary_cost,ss.pdf_takeaways_cost)

                user_question_pdf = st.chat_input("Ask a question and hit Enter",on_submit=callback_chat_pdf)
                
                if user_question_pdf != "" and ss.process_chat_pdf and not ss.button_down:
                    with get_openai_callback() as cb:
                        info_ = st.empty()
                        info_.info("`Generating Q&A  question ...`")
                        response_pdf = new_process_pdf(ss.db,user_question_pdf,model_pdf, temperature_pdf)
                        info_.empty()
                        print("Response:",cb)
                        ss.pdf_qa_cost += np.round(cb.total_cost,4)

                    ss['pdf_question'].append(user_question_pdf)
                    ss['pdf_answer'].append(response_pdf)
                    ss.process_chat_pdf = False


                if len(ss['pdf_question']) > 0:
                    pdf_qa_ui(ss["pdf_question"],ss["pdf_answer"],callback_download_pdf)
                
                if ss.counter_down > 0 and ss.button_down:
                    ss.button_down = False
      
        else:
            st.error("Please enter a valid OpenAI API key in the sidebar.")



