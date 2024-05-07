# Webpage-QA
### The Webpage-QA API provides a way to answer questions based on the content of a given webpage.

## Input Processing

### This code defines a function to extract answers to questions from a given URL's webpage context using a pre-trained question-answering model. It sets up a Gradio interface for users to input questions and URLs, and displays the extracted answers. The code also includes a background thread to process requests from a queue asynchronously.


## Input format:
### Question: Text
### URL: Text (URL format)
### Data validation: Minimal validation (e.g., URL format)
### Handling of missing or invalid input: Not specified
## Example input:
### json
## Sample request:
### json
```
{
  "question": "Where was Messi born?",
  "url": "https://en.wikipedia.org/wiki/Lionel_Messi"
}

{
  "answer": "Rosario, Santa Fe, Argentina"
}
```

## To execute : 
### install necessary modules
### cd to api folder
``` python app.py
