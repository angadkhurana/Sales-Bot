import requests
import openai



def spell_check(text):
    # Define the prompt with the text and desired completion format
    prompt = f"""Given the text: '{text}', please correct any spelling or grammar mistakes. 
    The text will contain medical treatments like 'emsculpt' or 'hair loss'. So if someone types
    'haior loss' or something like that you will know that it is 'hair loss'. If someone types 
    'emsculpy' or something like that you will know it is the common non invasive muscle building 
    treatment called 'emsculpt'. Only fix the text the user gives, but the context of the text 
    will ALWAYS be medical treatments. Do not add any additional information. Your Output should ALWAYS
    be 'The corrected text is: 'corrected_text'"""

    # Request a completion from the model
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        temperature=0,
        max_tokens=100
    )

    # Extract corrected text from the response
    corrected_text = response.choices[0].text.strip()

    return corrected_text

def get_news_articles(api_key, cx, treatment, num_results):
    base_url = "https://www.googleapis.com/customsearch/v1"

    results_fetched = 0
    while results_fetched < num_results:
        params = {
            "q": f"{treatment}",
            "cx": cx,  # Custom Search Engine ID
            "key": api_key,
            "num": min(1, num_results - results_fetched),  # Adjust the number of results per request
            "start": results_fetched + 1,  # Start index of results for pagination
            "sort": "date:r:20150101:20231231",  # Date range (adjust as needed)
        }

        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            
            for item in data.get("items", []):
                title = item.get("title", "")
                link = item.get("link", "")
                snippet = item.get("snippet", "")

                print(f"{results_fetched+1}) Title: {title}\nLink: {link}\nSnippet: {snippet}\n")
                print("##################################################")
                results_fetched += 1

            if "queries" in data and "nextPage" in data["queries"]:
                next_page = data["queries"]["nextPage"][0]
                if "startIndex" in next_page:
                    results_fetched = int(next_page["startIndex"]) - 1
            else:
                break

        else:
            print(f"Failed to retrieve news articles. Status code: {response.status_code}")
            break

API_KEY = "AIzaSyBQuuWAPbpEhv0gXtoRv4TwaFeHHU6fmlc"
SEACH_ENGINE_ID = "33d3c2b2a85ff4505"
treatment = input("Treatment Name: ")
location = input("Enter the location of interest: ")

corrected_text = spell_check(treatment + " " + location)
semicolon_index = corrected_text.find(':')  # Find the index of the semicolon
processed_query = ''
if semicolon_index != -1:  # Check if semicolon is found
    processed_query = corrected_text[semicolon_index + 1:].strip().strip("'") # Extract substring after semicolon and strip leading/trailing whitespace
else:
    processed_query = corrected_text.strip("'")
num_results = int(input("Enter the number of results you want: "))
print("Showing results for: ", processed_query)
print("---------------------------------------------")
get_news_articles(API_KEY, SEACH_ENGINE_ID, processed_query, num_results)


# API_KEY = "AIzaSyCjOxGey7Xlb_kaNp67TvPxS-t78XymXNI"
# SEACH_ENGINE_ID = "33d3c2b2a85ff4505"