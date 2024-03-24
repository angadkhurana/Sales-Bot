import requests
from bs4 import BeautifulSoup

def search_searx(query, num_results=5):
    # Define the Searx URL
    url = "https://github.com/searxng/searxng"  # Replace "searx.example.com" with your Searx instance URL

    # Define the search parameters
    params = {
        "q": query,
        "num": num_results
    }

    # Send GET request to Searx and get the response
    response = requests.get(url, params=params)

    # Check if request was successful
    if response.status_code == 200:
        # Parse the HTML content of the response
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract search results
        results = []
        for result in soup.find_all('div', class_='result'):
            title = result.find('a', class_='result-title').text.strip()
            link = result.find('a', class_='result-title')['href']
            results.append({"title": title, "link": link})

        return results
    else:
        print("Error: Failed to fetch search results.")
        return []

# Example usage:
query = "Python programming"
num_results = 5
search_results = search_searx(query, num_results)
print(search_results)
# Print the search results
for idx, result in enumerate(search_results, start=1):
    print(f"{idx}. {result['title']} - {result['link']}")
