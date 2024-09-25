import streamlit as st
import json
import math
from serpapi import GoogleSearch

# site:aircraftspruce.ca OR site:texasairsalvage.com OR site:https://ww2.txtav.com/parts OR site:controller.com/parts
site_list = [
        "ebay.com/itm",
        "ebay.ca/itm",
        "aircraftspruce.ca",
        "texasairsalvage.com",
        "https://ww2.txtav.com/parts",
        "controller.com/parts",
        "trade-a-plane.com",
        "airpowerinc.com"
        ]
num = 20

def display_result(result):
    st.subheader(f"[{result['title']}]({result['link']})")
    # st.write(f"Position: {result['position']}")
    # st.write(f"Redirect Link: [Google Redirect]({result['redirect_link']})")
    # st.write(f"Displayed Link: {result['displayed_link']}")
    # Snippet
    st.write(f"{result['snippet']}")
    # st.write(f"Highlighted Words: {', '.join(result['snippet_highlighted_words'])}")
    st.write(f"Source: {result['source']}")
    st.image(result['favicon'])
    st.divider()

def handle_pagination(pagination, n_pages):
    col1, col2, col3 = st.columns(3)

    # current = pagination["current"]
    # assert(int(current) == st.session_state.page)
    # total_pages = len(pagination["other_pages"]) + 1 # note current page is not included
    # if n_pages != total_pages:
    #     print("Warning: calculated pages does not match api returned pages, using calculated page by default")
    # radio_label = [p+1 for p in range(n_pages)] 
    
    # # incase if the number of page is too large
    # if len(radio_label) > 8:
    #     radio_label = radio_label[max(0, st.session_state.page - 4):min(st.session_state.page + 4, len(radio_label) - 1)]
    
    if st.session_state.page > 1:
        col1.button("prev", on_click=lambda: setattr(st.session_state, 'page', st.session_state.page - 1))
    if st.session_state.page < n_pages:
        col3.button("next", on_click=lambda: setattr(st.session_state, 'page', st.session_state.page + 1))

    col2.write(f"{(st.session_state.page-1) * num + 1} -- {(st.session_state.page * num)}")

    # create options
    # col2.radio(
    #     "Page 👇",
    #     radio_label,
    #     key="page",
    #     label_visibility="collapsed",
    #     disabled= False,
    #     horizontal= True,
    # )


def display_response(response):
    # response = st.session_state.response
    if not response:
        return
    if not response["organic_results"]:
        return

    total_results = response["search_information"]["total_results"]
    st.write(f"Total results: {total_results}")

    # display results
    for result in response["organic_results"]:
        display_result(result)
    
    # handle pagination
    handle_pagination(response["serpapi_pagination"], n_pages=math.ceil(total_results / num))

    # DEBUG LOGGING
    # st.write(response)


def search(search_input, page):
    if not search_input:
        return

    site_str = " OR ".join(f"site:{site}" for site in site_list)
    query = f"\"{search_input}\" {site_str}"

    params = {
      "api_key": st.secrets["SERPAPI_API_KEY"],
      "engine": "google",
      "q": query,
      "location": "Austin, Texas, United States",
      "google_domain": "google.com",
      "gl": "us",
      "hl": "en",
      "num": num,
      "start": (page - 1) * num
    }

    search = GoogleSearch(params)
    response = search.get_dict()

    # with open('example_result.json', 'r') as file:
    #     response = json.load(file)
    
    # response["search_information"]["total_results"] = page - 1
    return response
    


st.title('Find Aviation Parts')
search_input = st.text_input(
        "Search Term / Part Number",
        placeholder="KX155A / 069-01032-0101",
        on_change=lambda: setattr(st.session_state, 'page', 1)
        )

if "page" not in st.session_state:
    st.session_state.page = 1

# if 'response' not in st.session_state:
#     st.session_state.response = {}
# response = search(search_input)
response = search(search_input, page=st.session_state.page)
display_response(response)
