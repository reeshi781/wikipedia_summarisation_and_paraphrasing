from fastapi import FastAPI
import uvicorn
from wikipedia_summarisation_and_paraphrasing import Wikipedia_Page, Sections,summary,Paraphrase

app = FastAPI()

page_names = ""
section_info = {}
section_text =  ''

summarize_text = ''



@app.get("/name/{page_name}")
def get_name(page_name: str):

    global page_names
    page_names =  page_name
    global section_info

    url = Wikipedia_Page(page_name )
    sections_data = Sections(page_name)

    section_info =  sections_data

    return {"url": url, "Section Names": list(sections_data.keys())}



@app.get('/page_name/{user_input}')
def get_page_name(user_input):
    global  section_text
    for key, value in section_info.items():
        if key == user_input:
            section_text =  str(value)
            return key, value
        


@app.get('/summarized_text')
def get_summary():
    global summarize_text
    summarize_text = summary(section_text)
    return summarize_text


@app.get('/Paraphrase_text')
def get_paraphrase():
    paraphrase_text =  Paraphrase(summarize_text)
    return paraphrase_text
        

if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000)
