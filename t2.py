# import requests
# from bs4 import BeautifulSoup

# def get_google_search_results(query):
#     # Define the URL for the Google search
#     url = "https://www.google.com/search"
    
#     # Parameters for the search query
#     params = {"q": query}

#     # Send a request to Google with the query
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
#     }

#     # Make the request
#     response = requests.get(url, params=params, headers=headers)

#     # Check if the request was successful
#     if response.status_code == 200:
#         # Parse the HTML content using BeautifulSoup
#         soup = BeautifulSoup(response.text, 'html.parser')

#         # Remove specific elements as per the requirements

#         # Remove elements with class "Gx5Zad xpd EtOod pkphOe", keeping the first two
#         gx5_elements = soup.find_all(class_="Gx5Zad xpd EtOod pkphOe")
#         for element in gx5_elements[2:]:  # Skip the first two elements
#             element.decompose()  # Remove the element from the tree

#         # Remove elements with class "EOlPnc"
#         for element in soup.find_all(class_="EOlPnc"):
#             element.decompose()  # Remove the element from the tree

#         # Remove footer and header elements
#         for element in soup.find_all(['footer', 'header']):
#             element.decompose()  # Remove the element from the tree

#         # Remove elements with class "KP7LCb"
#         for element in soup.find_all(class_="KP7LCb"):
#             element.decompose()  # Remove the element from the tree
        
#         # Remove elements with class "oTWEpb"
#         for element in soup.find_all(class_="oTWEpb"):
#             element.decompose()  # Remove the element from the tree

#         # Remove unwanted text from the HTML content
#         unwanted_texts = [
#             "/url?esrc=s&amp;q=&amp;rct=j&amp;sa=U&amp;url=",
#             "&amp;ved=2ahUKEwj9r9z3hvqIAxWKrZUCHcz7G1MQFnoECAMQBQ&amp;usg=AOvVaw2GZ3mtY6X-VM_aTqT368LS"
#         ]
        
#         # Remove all unwanted texts
#         cleaned_html = str(soup)
#         for text in unwanted_texts:
#             cleaned_html = cleaned_html.replace(text, "")

#         # Remove text after "&amp;ved=" in href attributes of <a> tags
#         for a_tag in soup.find_all('a', href=True):
#             href = a_tag['href']
#             ved_index = href.find("&amp;ved=")
#             if ved_index != -1:
#                 # Keep the portion before "&amp;ved="
#                 cleaned_href = href[:ved_index]
#                 a_tag['href'] = cleaned_href  # Update the href attribute

#         # Process content from elements with class "BNeawe UPmit AP7Wnd UwRFLe"
#         for element in soup.find_all(class_="BNeawe UPmit AP7Wnd UwRFLe"):
#             # Remove spaces and replace › with /
#             processed_content = element.get_text(strip=True).replace('›', '/').replace(' ', '')
#             # Prepend with "https://"
#             new_href = f"https://{processed_content}"

#             # Find the parent <a> tag and update its href
#             parent_a_tag = element.find_parent('a', href=True)
#             if parent_a_tag:
#                 parent_a_tag['href'] = new_href  # Update the href attribute

#         # Return the cleaned HTML content
#         return str(soup)
#     else:
#         return f"Error: Unable to fetch page (Status Code: {response.status_code})"

# if __name__ == "__main__":
#     query = input("Enter your search query: ")
#     html_content = get_google_search_results(query)
#     print(html_content)
#     # # Save the cleaned HTML content to a file
#     # with open("cleaned_google_search_results.html", "w", encoding="utf-8") as file:
#     #     file.write(html_content)
    
from gi_scraper import Scraper


# Pass a Cache instance with a custom directory path and timeout
# Set cache timeout to -1 for caching indefinitely

"""
from gi_scraper import Cache

cache = Cache(dir_path="gi_cache", timeout=-1)
sc = Scraper(workers=8, headless=False, cache=cache)
"""

# The object creation has an overhead time
# The same object can be reused to fire multiple queries
sc = Scraper(headless=False)

for query, count in {"Naruto": 20, "Gintoki": 30}.items():
    print("Scraping...", query, ":", count)

    # scrape method returns a stream object
    stream = sc.scrape(query, count)

    # stream.get method yields Response object with following attributes
    # - query (str): The query associated with the response.
    # - name (str): The name attribute of the response.
    # - src_name (str): The source name attribute of the response.
    # - src_page (str): The source page attribute of the response.
    # - thumbnail (str): The thumbnail attribute of the response.
    # - image (str): The image attribute of the response.
    # - width (int): The width attribute of the response.
    # - height (int): The height attribute of the response.

    for index, response in enumerate(stream.get()):
        if index == 10:
            sc.terminate_query()  # Terminate current query midway
            break
        # response.to_dict returns python representable dictionary
        print(response.width, "x", response.height, ":", response.image)


# call this to terminate scraping (auto-called by destructor)
sc.terminate()