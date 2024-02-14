# Importing the module
import wikipediaapi
import openai
import mysql.connector

# Creating a Wikipedia api object
wiki = wikipediaapi.Wikipedia('en', extract_format=wikipediaapi.ExtractFormat.WIKI, headers={'User-Agent': 'Your-User-Agent'})

# Setting openai api key
api_key = "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"
openai.api_key = api_key

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="quantacus"
)

mycursor = db.cursor()



# Task 1
def Wikipedia_Page(page_name):
    # Fetching the Wikipedia page
    page = wiki.page(page_name)

    # Checking page exists or not exists
    if not page.exists():
        return "Page not found"

    # Printing the URL of the page if it exists
    return f'\nPage URL is: {page.fullurl}'


# Task 2
def Sections(page_name):
    return {section.title: section.text for section in wiki.page(page_name).sections}

# Task 3
def Get_section_text(page_name, section_name):
    page = wiki.page(page_name)
    sections = {section.title: section for section in page.sections}
    
    if section_name in sections:
        section_text = sections[section_name].text
        return f'page name is {page_name} and text of {section_name} is {section_text}'
    else:
        return f"Section {section_name} not found in the page."




# # task 4
def summary():
    # Fetching section_text from the 'texts' table
    mycursor.execute("SELECT section_text FROM texts")
    results = mycursor.fetchall()
    
    # Convert the fetched text to a string
    text_content = " ".join(result[0] for result in results)

    # Generating a summary using OpenAI GPT-3.5-turbo
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": text_content},
            {"role": "assistant", "content": "Generate a summary of the provided text. Please give me a summary under 100 words."},
        ]
    )

    summary_text = response['choices'][0]['message']['content'].strip()
    mycursor.execute("CREATE TABLE IF NOT EXISTS Summary (text TEXT)")
    mycursor.execute("TRUNCATE TABLE Summary")
    mycursor.execute("INSERT INTO Summary (text) VALUES (%s)", (summary_text,))
    db.commit()

    # Return the generated summary
    return summary_text

# print(summary())


# Task 5
def Paraphrase():
    # Fetching section_text from the 'texts' table
    mycursor.execute("SELECT text FROM Summary")
    results = mycursor.fetchall()
    
    # Convert the fetched text to a string
    text_content = " ".join(result[0] for result in results)

    # Generating a summary using OpenAI GPT-3.5-turbo
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": text_content},
            {"role": "assistant", "content": "Generate a paraphrase of the provided text.please give me paraphrase under 100 words"},
        ]
    )

    paraphrased_text = response['choices'][0]['message']['content'].strip()
    mycursor.execute("CREATE TABLE IF NOT EXISTS Paraphrase (text TEXT)")
    mycursor.execute("TRUNCATE TABLE Paraphrase")
    mycursor.execute("INSERT INTO Summary (text) VALUES (%s)", (paraphrased_text,))
    db.commit()

    # Return the generated summary
    return paraphrased_text
# print(Paraphrase())
