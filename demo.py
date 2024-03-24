#### TEST 1 ####
# Treatment Name: emsculpt 
# Enter the location of interest: london
# Enter the number of results you want: 100

#### TEST 2 ####
# Treatment Name: emscukpy
# Enter the location of interest: londpm
# Enter the number of results you want: 2

import requests

def scraper(api_key, cx, treatment, num_results):
    base_url = "https://www.googleapis.com/customsearch/v1"

    results_fetched = 0
    while results_fetched < num_results:
        params = {
            "q": f"{treatment}",
            "cx": cx,  # Custom Search Engine ID
            "key": api_key,
            "num": min(10, num_results - results_fetched),  # Adjust the number of results per request
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
            print(f"Failed to retrieve web links. Status code: {response.status_code}")
            break


SEACH_ENGINE_ID = "33d3c2b2a85ff4505"
treatment = input("Treatment Name: ")
location = input("Enter the location of interest: ")
num_results = int(input("Enter the number of results you want: "))

print("---------------------------------------------")
scraper(API_KEY, SEACH_ENGINE_ID, treatment + " " + location, num_results)


# API_KEY = "AIzaSyCjOxGey7Xlb_kaNp67TvPxS-t78XymXNI"
# SEACH_ENGINE_ID = "33d3c2b2a85ff4505"