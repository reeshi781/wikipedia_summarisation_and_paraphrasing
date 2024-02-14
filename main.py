from fastapi import FastAPI
import uvicorn
import mysql.connector
from wikipedia_summarisation_and_paraphrasing import Wikipedia_Page, Sections,summary,Paraphrase

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="quantacus"
)

mycursor = db.cursor()
app = FastAPI()

# Create a table to store section information
table_creation_query = """
CREATE TABLE IF NOT EXISTS section_info (
    section_name VARCHAR(255),
    section_text TEXT
)
"""
mycursor.execute(table_creation_query)
db.commit()


@app.get("/name/{page_name}")
def get_name(page_name: str):
    url = Wikipedia_Page(page_name)
    sections_data = Sections(page_name)

    mycursor.execute("TRUNCATE TABLE section_info ")

    # Insert section names into the database
    for section_name in sections_data:
        mycursor.execute("INSERT INTO section_info (section_name, section_text) VALUES (%s, %s)", (section_name, sections_data[section_name]))
    db.commit()

    return {"url": url, "Section Names": list(sections_data.keys())}


@app.get("/text/{user_section_name}")
def get_section_text(user_section_name):
    mycursor.execute("SELECT * FROM section_info WHERE section_name = %s", (user_section_name,))
    for x in mycursor:
        mycursor.execute("CREATE TABLE IF NOT EXISTS texts (section_title VARCHAR(255), section_text TEXT)")
        mycursor.execute("TRUNCATE TABLE texts")
        mycursor.execute("INSERT INTO texts (section_title, section_text) VALUES (%s,%s)", (x[0], x[1]))
        db.commit()
        return x



@app.get('/summarized_text')
def get_summary():
    summary_text = summary()
    return summary_text



@app.get('/paraphrased_text')
def get_paraphrase():
    paraphrased_text = Paraphrase()
    return paraphrased_text





# @app.get("/text/{page_name}/{section_name}")
# def section_text(page_name: str, section_name: str):
#     section_text = Get_section_text(page_name, section_name)


#     return {
#         "The page name is": page_name,
#         "Section name is": section_name,
#         "Section text": section_text
#     }


if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000)
