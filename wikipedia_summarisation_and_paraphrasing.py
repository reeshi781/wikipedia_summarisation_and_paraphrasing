# Importing the module
import wikipediaapi
import openai

# Creating a Wikipedia api object
wiki = wikipediaapi.Wikipedia('en', extract_format=wikipediaapi.ExtractFormat.WIKI, headers={'User-Agent': 'Your-User-Agent'})

# Setting openai api key
api_key = "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"
openai.api_key = api_key


# Task 1
def Wikipedia_Page(page_name):
    page = wiki.page(page_name)  # Fetching the Wikipedia page
    if not page.exists(): # Checking page exists or not exists
        return "Page not found"
    # Printing the URL of the page if it exists
    return f'\nPage URL is: {page.fullurl}'

# Task 2
def Sections(page_name):
    return {section.title: section.text for section in wiki.page(page_name).sections}



# # task 4
def summary(text_content):

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": text_content},
            {"role": "assistant", "content": "Generate a summary of the provided text. Please give me a summary under 100 words."},
        ]
    )

    return response['choices'][0]['message']['content'].strip()

# print(summary(abc))


# Task 5
def Paraphrase(text_content):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": text_content},
            {"role": "assistant", "content": "Generate a paraphrase of the provided text.please give me paraphrase under 100 words"},
        ]
    )
    
    return response['choices'][0]['message']['content'].strip()
# print(Paraphrase())
