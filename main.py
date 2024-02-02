import mysql.connector
from fastapi import FastAPI
import uvicorn


db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="quantacus"
)

mycursor =  db.cursor()


app =  FastAPI()

@app.get('/summary')
def get_summary():
    mycursor.execute("SELECT * FROM summary")
    for x in mycursor:
        return x


@app.get('/paraphrase')
def get_paraphrase():
    mycursor.execute("SELECT * FROM paraphrase")
    for x in mycursor:
        return x
    

if __name__ == "__main__":
    uvicorn.run(app,  host = '127.0.0.1', port=8000)