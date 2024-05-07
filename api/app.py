from urllib.parse import urlparse  # Importing necessary libraries
import gradio as gr
import requests
from bs4 import BeautifulSoup
from transformers import pipeline
import queue
import threading

# Load the trained model
qa_model = pipeline("question-answering", model="distilbert-base-cased-distilled-squad", revision="50ba811")

# Queue for incoming requests
request_queue = queue.Queue()

def extract_answer(question, url):
    """Get context from URL and use it to answer the question"""
    try:
        # Check if the URL is missing the scheme and add 'https://' if needed
        if not urlparse(url).scheme:
            url = 'https://' + url

        # Retrieve actual page content
        html = requests.get(url).content
    except requests.exceptions.RequestException as e:
        return f"I don’t know the answer"
    
    # Create BS4 object to handle HTML data
    soup = BeautifulSoup(html, 'html.parser')

    for data in soup(['style', 'script', 'meta', 'link', 'noscript']):
        # Remove tags
        data.decompose()

    # Get and clean up plain text
    context = soup.get_text()
    while "\n\n" in context:
        context = context.replace("\n\n", "\n")
    
    answer_dict = qa_model(question=question, context=context)
    
    if 'answer' not in answer_dict or not answer_dict['answer']:
        return "I don't know the answer"
    
    return answer_dict['answer']

def process_requests():
    """Process requests from the queue"""
    while True:
        request = request_queue.get()
        if request is None:
            break
        question, url = request
        answer = extract_answer(question, url)
        print(answer)

# Start a thread to process requests from the queue
request_processor = threading.Thread(target=process_requests)
request_processor.start()

# Interface setup
title = "Webpage-Based Question Answering"
description = "Using a webpage as context for extractive question answering."
examples=[
    ["Where was Messi born?", "https://en.wikipedia.org/wiki/Lionel_Messi"],
    ["When was Cristiano Ronaldo born?", "https://en.wikipedia.org/wiki/Cristiano_Ronaldo"]
]

iface = gr.Interface(
    fn=lambda question, url: extract_answer(question, url),
    inputs=["text", "text"],
    outputs="text",
    title=title,  # Set title of the interface
    description=description,  # Set description of the interface
    examples=examples  # Set example inputs for the interface
)

iface.launch()  # Launch the interface
