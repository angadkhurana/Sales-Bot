import streamlit as st
import requests
import pandas as pd
import random

# CSS styles
custom_css = """
<style>
body {
    background-color: #ffffff; /* Set background color to white */
    overflow: hidden; /* Hide overflow to prevent scrollbars */
}

.container {
    display: flex;
    flex-direction: column;
    align-items: center;
}

# .square {
#     width: 50px;
#     height: 50px;
#     background-color: #ff7f0e; /* Orange color for squares */
#     animation: spin 3s linear infinite; /* Animation for spinning */
# }

# .hexagon {
#     width: 50px;
#     height: 50px;
#     background-color: #6495ed; /* Cornflower blue color for hexagons */
#     position: relative;
#     top: 0;
#     animation: moveUpDown 3s ease-in-out infinite alternate; /* Animation for moving up and down */
# }

# @keyframes spin {
#     0% {
#         transform: rotate(0deg);
#     }
#     100% {
#         transform: rotate(360deg);
#     }
# }

# @keyframes moveUpDown {
#     0% {
#         top: 0;
#     }
#     100% {
#         top: 50px;
#     }
}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

def scraper(api_key, cx, treatment, num_results):
    base_url = "https://www.googleapis.com/customsearch/v1"

    results = []
    results_fetched = 0
    index = 1  # Start index from 1
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

                # Append each result as a dictionary to the results list
                results.append({"Title": title, "Link": link, "Description": snippet})
                index += 1
                results_fetched += 1

            if "queries" in data and "nextPage" in data["queries"]:
                next_page = data["queries"]["nextPage"][0]
                if "startIndex" in next_page:
                    results_fetched = int(next_page["startIndex"]) - 1
            else:
                break

        else:
            st.write(f"Failed to retrieve web links. Status code: {response.status_code}")
            break

    return results

st.title("Client Finder")

API_KEY = "AIzaSyBQuuWAPbpEhv0gXtoRv4TwaFeHHU6fmlc"
SEARCH_ENGINE_ID = "33d3c2b2a85ff4505"

import streamlit as st

inputs_placeholder = {}
inputs = ["treatment", "location", "num results"]
for input_name in inputs:
    inputs_placeholder[input_name] = st.empty()

treatment = inputs_placeholder["treatment"].text_input("Enter Treatment Name:", key='treatment')
location = inputs_placeholder["location"].text_input("Enter the location of interest:", key='location')

# Define num_results with a default value
num_results = None

# Add validation for num_results
num_results_input = inputs_placeholder["num results"].text_input("Enter the number of results you want:", key='num_results')
if num_results_input:
    try:
        num_results = int(num_results_input)
    except ValueError:
        st.error("Please enter a valid integer for the number of results.")


# Store the variables in a dictionary
variables = {
    "treatment": treatment,
    "location": location,
    "num results": num_results
}

for input_name in inputs:
    if variables[input_name]:
        inputs_placeholder[input_name].write(f"{input_name.capitalize()}: {variables[input_name]}")

search_button_pressed = False
if st.button("Search"):
    search_button_pressed = True
    with st.spinner('Searching...'):
        search_button_pressed = True
        search_results = scraper(API_KEY, SEARCH_ENGINE_ID, treatment + " " + location, num_results)
        st.write(f"Showing {num_results} results for: ", treatment + " " + location)
        st.table(pd.DataFrame(search_results))
    if st.button("Qualify"):
        with st.spinner('Qualifying...'):
            search_results = scraper(API_KEY, SEARCH_ENGINE_ID, treatment + " " + location, num_results)
            num_display = random.randint(1, min(10, len(search_results)))  # Select random number of results to display
            random_results = random.sample(search_results, num_display)  # Select random subset of results
            st.write("Qualified Results:")
            st.table(pd.DataFrame(random_results))



    

# Animated elements
st.write('<div class="container">', unsafe_allow_html=True)
st.write('<div class="square"></div>', unsafe_allow_html=True)
st.write('<div class="hexagon"></div>', unsafe_allow_html=True)
st.write('</div>', unsafe_allow_html=True)