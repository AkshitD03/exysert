import requests
from bs4 import BeautifulSoup

def get_google_search_results(query):
    # Define the URL for the Google search
    url = "https://www.google.com/search"
    
    # Parameters for the search query
    params = {"q": query}

    # Send a request to Google with the query
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    # Make the request
    response = requests.get(url, params=params, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        return response.text
    else:
        return f"Error: Unable to fetch page (Status Code: {response.status_code})"

def clean_html(html_content):
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # 1. Keep the first two divs with class "Gx5Zad xpd EtOod pkphOe", remove the rest
    divs_to_keep = soup.find_all("div", class_="Gx5Zad xpd EtOod pkphOe")
    for i, div in enumerate(divs_to_keep):
        if i >= 2:
            div.decompose()

    # 2. Remove all elements with class "EOlPnc"
    for element in soup.find_all(class_="EOlPnc"):
        element.decompose()

    # 3. Remove <footer> elements
    for footer in soup.find_all("footer"):
        footer.decompose()

    # 4. Remove <header> elements
    for header in soup.find_all("header"):
        header.decompose()

    # 5. Remove divs with class "KP7LCb"
    for div in soup.find_all("div", class_="KP7LCb"):
        div.decompose()

    # Return the cleaned HTML content
    return soup.prettify()

if __name__ == "__main__":
    query = input("Enter your search query: ")
    html_content = get_google_search_results(query)

    # Clean the HTML content by removing the specified elements
    cleaned_html = clean_html(html_content)
    
    # Save the cleaned HTML content to a file
    with open("cleaned_google_search_results.html", "w", encoding="utf-8") as file:
        file.write(cleaned_html)

    print("Cleaned search results saved to 'cleaned_google_search_results.html'.")
