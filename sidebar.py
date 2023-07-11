import streamlit as st
from faq import faq


ss = st.session_state

def youtube_chunk():
    
    st.selectbox('Fragment size', [200,300,400,500,600,700,800,900,1000,1200], index=5, key='frag_size_yt',help="Maximum number of characters that a chunk can contain.")

def youtube_overlap():
    
    st.selectbox('Fragment overlap', [100,200,300,400,500,600,700], index=2, key='frag_overlap_yt',help = "Number of characters that overlap between two consecutive chunks")

def youtube_temp():
    
    st.slider('temperature', 0.0, 1.0, 0.2, 0.1, key='temperature_yt',format='%0.1f',help= "Randomness of the AI generated text. The closer to 0 the more deterministic")

def youtube_model():
	models = ['gpt-3.5-turbo','text-davinci-003','text-curie-001']
	st.selectbox('AI model', models, index= 0,key='model_yt',help="LLM models")
        
def pdf_chunk():
    
    st.selectbox('Fragment size', [200,300,400,500,600,700,800,900,1000], index=5, key='frag_size_pdf',help="Maximum number of characters that a chunk can contain.")

def pdf_overlap():
    
    st.selectbox('Fragment overlap', [100,200,300,400,500,600,700], index=2, key='frag_overlap_pdf',help = "Number of characters that overlap between two consecutive chunks")

def pdf_temp():
    st.slider('Temperature', 0.0, 1.0, 0.2, 0.1, key='temperature_pdf', format='%0.1f',help= "Randoness of the AI generated text. The closer to 0 the more deterministic")

def pdf_model():
    models = ['gpt-3.5-turbo','text-davinci-003','text-curie-001']
    st.selectbox('AI model', models,index=0, key='model_pdf',help="LLM models")

def pdf_summary():
    st.checkbox('Generate summary pdf', value=False, key='generate_summary_pdf',help=":red[This feature is expensive (0.35$ per 10 pdf pages)].")

def num_sample_questions_pdf():
    st.selectbox('Number of sample questions', [2,3,4,5,7], index=1, key='num_sample_questions_pdf',help="Number of sample questions about the contents of the file")


def csv_temp():
    st.slider('Temperature', 0.0, 1.0, 0.0, 0.1, key='temperature_csv', format='%0.1f',help= "How creative the AI model is allowed to be")

def csv_model():
    models = ['gpt-3.5-turbo','text-davinci-003','text-curie-001']
    st.selectbox('Model', models,index=0, key='model_csv')


if "reset_button_yt" not in ss:
    ss.reset_button_yt = False

if "reset_button_csv" not in ss:
    ss.reset_button_csv = False

if "reset_button_pdf" not in ss:
    ss.reset_button_pdf = False

def callback_reset_yt():
    ss.reset_button_yt = True

def callback_reset_csv():
    ss.reset_button_csv = True

def callback_reset_pdf():
    ss.reset_button_pdf = True


def sidebar():

    if "reset_button_yt" not in ss:
        ss.reset_button_yt = False

    if "reset_button_csv" not in ss:
        ss.reset_button_csv = False

    if "reset_button_pdf" not in ss:
        ss.reset_button_pdf = False

    def callback_reset_yt():
        ss.reset_button_yt = True

    def callback_reset_pdf():
        ss.reset_button_pdf = True

    if "OPENAI_API_KEY" not in ss:
        ss["OPENAI_API_KEY"] = ""

    with st.sidebar:

        st.title("AI KnowledgeBot")

        st.markdown('''
            This AI-powered tool is designed to help you obtain meaningful information of YouTube and PDF files. 
            
            Upload a Youtube video (*works only with single speaker videos*) and the AI will give you the transcript (using OpenAI's Whisper model) and its summary. Users can also do Q&A about the contents of the video.
            
            Upload a PDF file and and do Q&A about its contents. A summary of the file will also be generated.       
            
            ''')

        st.markdown(
            "## How to use\n"
            "1. Enter your OpenAI API key.\n"
            "2. If you don't have access to an OpenAI API key, you can get one [here](https://platform.openai.com/account/api-keys).\n"
        )

        api_key_input = st.text_input(
            "OpenAI API Key",
            type="password",
            placeholder="Paste your OpenAI API key here (sk-...)",
            help="You can get your API key from https://platform.openai.com/account/api-keys.",
            value=ss.get("OPENAI_API_KEY", ""),
        )
        
        submitted = st.button("Submit!")


        if api_key_input and submitted:
            if not api_key_input.startswith("sk-"):
                st.error(
                    "Please enter a correct API key. You can get your API key from https://platform.openai.com/account/api-keys."
                )

            else:
                ss["OPENAI_API_KEY"] = api_key_input
                
	    
        st.markdown("---")
        st.markdown("# Settings")
        st.markdown("""
            LLMs have parameters that can be tuned to generate different results, and you may want to adjust them to get better results.
        """)
        
        with st.expander("Youtube"):

            reset_button1 = st.empty()
            reset_button1.button("Reset values", on_click = callback_reset_yt,key='reset_button_yttt')
            if ss.reset_button_yt:      
                                      
                ss.temperature_yt = 0.2
                ss.frag_size_yt = 700
                ss.frag_overlap_yt = 300
                ss.model_yt = 'gpt-3.5-turbo'

                ss.reset_button_yt = False


            youtube_chunk()
            youtube_overlap()
            youtube_model()
            youtube_temp()

        with st.expander("PDF"):

            reset_button2 = st.empty()
            reset_button2.button("Reset values", on_click = callback_reset_pdf,key='reset_button_pdfff')
            if ss.reset_button_pdf:      

                ss.temperature_pdf = 0.2
                ss.frag_size_pdf = 700
                ss.frag_overlap_pdf = 300
                ss.model_pdf = 'gpt-3.5-turbo'
                ss.generate_summary_pdf = False
                ss.num_sample_questions_pdf = 3
                ss.reset_button_pdf = False   


            pdf_chunk()
            pdf_overlap()
            pdf_model()
            pdf_temp()
            pdf_summary()
            num_sample_questions_pdf()
        
       

        st.markdown("---")

        faq()
