from flask import Flask, render_template, request, redirect, url_for , jsonify, session
from bs4 import BeautifulSoup
import requests
from duckduckgo_search import DDGS
from youtubesearchpython import VideosSearch
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.parse
from urllib.parse import quote_plus
import re
import time
import urllib.parse
import os
import json
from youtube_search import YoutubeSearch
import re
from duckduckgo_search import DDGS
from g4f.client import Client

client = Client()


app = Flask(__name__)
app.secret_key = 'exyser'



feedbacks_dir = os.path.join(os.getcwd(), 'feedbacks')

def scrape_google_results(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

    html = requests.get(url, headers=headers)

    soup = BeautifulSoup(html.text, 'html.parser')

    allData = soup.find_all("div", {"class": "g"})

    g = 0
    Data = []
    l = {}
    for i in range(0, len(allData)):
        link = allData[i].find('a').get('href')

        if (link is not None):
            if (link.find('https') != -1 and link.find('http') == 0 and link.find('aclk') == -1):
                g = g + 1
                l["link"] = link
                try:
                    l["title"] = allData[i].find('h3', {"class": "DKV0Md"}).text
                except:
                    l["title"] = None

                try:
                    l["description"] = allData[i].find("div", {"class": "VwiC3b"}).text
                except:
                    l["description"] = None

                l["position"] = g

                Data.append(l)

                l = {}

            else:
                continue

        else:
            continue

    return Data


def print_results(results):
    for result in results:
        print("Title: ", result.get("title", ""))
        print("Link: ", result.get("link", ""))
        print("Description: ", result.get("description", ""))
        print("Position: ", result.get("position", ""))
        print("\n")

def search_images(keyword, region="wt-wt", safesearch="moderate", max_results=30):
    results = DDGS().images(
        keywords=keyword,
        region=region,
        safesearch=safesearch,
        max_results=max_results
    )
    return results

def display_images(results):
    print("\nSearch Results:")
    for i, result in enumerate(results, start=1):
        print(f"{i}. {result['title']}: {result['image']}")



# def search_youtube_videos(query, max_results=10):
#     videos_search = VideosSearch(query, limit=max_results)
#     results = []
#     for video in videos_search.result()["result"]:
#         result = {
#             "title": video["title"],
#             "link": video["link"],
#             "id": video["id"],
#         }
#         results.append(result)
#     return results
def search_youtube_videos(query, max_results=10):
    videos_search = VideosSearch(query, limit=max_results)
    results = []
    for video in videos_search.result()["result"]:
        result = {
            "title": video["title"],
            "link": video["link"],
            "id": video["id"],
        }
        results.append(result)
    return results

def search_news(query, max_results=10):
    results = DDGS().news(
        keywords=query,
        max_results=max_results
    )
    return results

def is_math_query(query):
    math_keywords = re.compile(r'[\+\-\*/%^x\(\)\{\}\[\]|cube|square]')
    return bool(math_keywords.search(query))


# def extract_top_widget(query):
#     # Set up Chrome options
#     chrome_options = Options()
#     chrome_options.add_argument("--headless")  # Run in headless mode

#     # Specify the path to the ChromeDriver
#     # Update the path to where ChromeDriver is located on your machine
#     chrome_driver_path = 'D:\AKSHIT\Code\Company\search-engine\chromedriver.exe'  # Example: 'C:/path/to/chromedriver.exe' on Windows or '/usr/local/bin/chromedriver' on macOS/Linux

#     # Ensure the path is correct
#     if not os.path.exists(chrome_driver_path):
#         raise FileNotFoundError(f"ChromeDriver not found at path: {chrome_driver_path}")

#     # URL encode the query
#     encoded_query = urllib.parse.quote(query)

#     # Create a new instance of the Chrome driver
#     service = Service(chrome_driver_path)
#     driver = webdriver.Chrome(service=service, options=chrome_options)

#     # Define the URL with the user's query
#     google_url = f"https://www.google.com/search?q={encoded_query}"

#     # Navigate to the Google URL
#     driver.get(google_url)

#     # Allow time for the page to load
#     time.sleep(2)

#     top_widget_html = ""

#     try:
#         # Find the first element with the class name 'ULSxyf'
#         first_element = driver.find_element(By.CLASS_NAME, 'ULSxyf')
#         first_element_text = first_element.text

#         # Check if the result includes "Related searches", "People also ask", or "People also search for"
#         if "Related searches" in first_element_text or "People also ask" in first_element_text or "People also search for" in first_element_text:
#             # Use DuckDuckGo search instead
#             duckduckgo_url = f"https://duckduckgo.com/?q={encoded_query}&ia=web"
#             driver.get(duckduckgo_url)
            
#             # Allow time for the page to load
#             time.sleep(2)

#             try:
#                 # Scrape the first element with the class 'L6fj2A3X2mfJl5kE8caF'
#                 duckduckgo_result = driver.find_element(By.CLASS_NAME, 'L6fj2A3X2mfJl5kE8caF')
#                 top_widget_html = duckduckgo_result.get_attribute('outerHTML')
#             except Exception as e:
#                 print(f"An error occurred while scraping DuckDuckGo: {e}")
#         else:
#             top_widget_html = first_element.get_attribute('outerHTML')
#     except Exception as e:
#         print(f"An error occurred: {e}")

#     # Close the browser
#     driver.quit()
    
#     return top_widget_html




def is_math_query(query):
    math_keywords = re.compile(r'[\+\-\*/%^x\(\)\{\}\[\]|cube|square]')
    return bool(math_keywords.search(query))


def classify_query(query):
    translation_pattern = re.compile(r'(translate\s+.+\s+in\s+\w+|.+\s+in\s+\w+)', re.IGNORECASE)
    location_pattern = re.compile(r'(where\s+is\s+.+|.+\s+to\s+.+)', re.IGNORECASE)
    calculation_pattern = re.compile(r'(\d+\s*[\+\-\*/x]\s*\d+)', re.IGNORECASE)
    
    if translation_pattern.search(query):
        return "Translation"
    elif location_pattern.search(query):
        return "Location"
    elif calculation_pattern.search(query):
        return "Calculation"
    else:
        return "Other"

def evaluate_calculation(query):
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
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove specific elements as per the requirements

        # Remove elements with class "Gx5Zad xpd EtOod pkphOe", keeping the first two
        gx5_elements = soup.find_all(class_="Gx5Zad xpd EtOod pkphOe")
        for element in gx5_elements[2:]:  # Skip the first two elements
            element.decompose()  # Remove the element from the tree

        # Remove elements with class "EOlPnc"
        for element in soup.find_all(class_="EOlPnc"):
            element.decompose()  # Remove the element from the tree

        for element in soup.find_all(class_="uR9Zq"):
            element.decompose()  # Remove the element from the tree
        for element in soup.find_all(class_="q7fqqf"):
            element.decompose()  # Remove the element from the tree
        for element in soup.find_all(class_="J9hCCd"):
            element.decompose()  # Remove the element from the tree
        # Remove footer and header elements
        for element in soup.find_all(['footer', 'header']):
            element.decompose()  # Remove the element from the tree

        # Remove elements with class "KP7LCb"
        for element in soup.find_all(class_="KP7LCb"):
            element.decompose()  # Remove the element from the tree
        
        # Remove elements with class "oTWEpb"
        for element in soup.find_all(class_="oTWEpb"):
            element.decompose()  # Remove the element from the tree

        # Remove the first <style> tag in the HTML
        first_style_tag = soup.find('style')
        if first_style_tag:
            first_style_tag.decompose()  # Remove the first style tag from the tree

        # Remove unwanted text from the HTML content
        unwanted_text_1 = "/url?esrc=s&amp;q=&amp;rct=j&amp;sa=U&amp;url="
        unwanted_text_2 = "/url?esrc=s&q=&rct=j&sa=U&url="
        cleaned_html = str(soup).replace(unwanted_text_1, "").replace(unwanted_text_2, "")

        # Return the cleaned HTML content
        return cleaned_html
    else:
        return f"Please Sare Your Valuable Feedback Of Our Search Engine Here - https://forms.gle/1RFcZ2CgoS9E8ffy7"

def perform_translation(query):
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
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove specific elements as per the requirements

        # Remove elements with class "Gx5Zad xpd EtOod pkphOe", keeping the first two
        gx5_elements = soup.find_all(class_="Gx5Zad xpd EtOod pkphOe")
        for element in gx5_elements[2:]:  # Skip the first two elements
            element.decompose()  # Remove the element from the tree

        # Remove elements with class "EOlPnc"
        for element in soup.find_all(class_="EOlPnc"):
            element.decompose()  # Remove the element from the tree

        for element in soup.find_all(class_="uR9Zq"):
            element.decompose()  # Remove the element from the tree
        for element in soup.find_all(class_="q7fqqf"):
            element.decompose()  # Remove the element from the tree
        for element in soup.find_all(class_="J9hCCd"):
            element.decompose()  # Remove the element from the tree
        # Remove footer and header elements
        for element in soup.find_all(['footer', 'header']):
            element.decompose()  # Remove the element from the tree

        # Remove elements with class "KP7LCb"
        for element in soup.find_all(class_="KP7LCb"):
            element.decompose()  # Remove the element from the tree
        
        # Remove elements with class "oTWEpb"
        for element in soup.find_all(class_="oTWEpb"):
            element.decompose()  # Remove the element from the tree

        # Remove the first <style> tag in the HTML
        first_style_tag = soup.find('style')
        if first_style_tag:
            first_style_tag.decompose()  # Remove the first style tag from the tree

        # Remove unwanted text from the HTML content
        unwanted_text_1 = "/url?esrc=s&amp;q=&amp;rct=j&amp;sa=U&amp;url="
        unwanted_text_2 = "/url?esrc=s&q=&rct=j&sa=U&url="
        cleaned_html = str(soup).replace(unwanted_text_1, "").replace(unwanted_text_2, "")

        # Return the cleaned HTML content
        return cleaned_html
    else:
        return f"Please Sare Your Valuable Feedback Of Our Search Engine Here - https://forms.gle/1RFcZ2CgoS9E8ffy7"



def get_google_maps_link(query):
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
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove specific elements as per the requirements

        # Remove elements with class "Gx5Zad xpd EtOod pkphOe", keeping the first two
        gx5_elements = soup.find_all(class_="Gx5Zad xpd EtOod pkphOe")
        for element in gx5_elements[2:]:  # Skip the first two elements
            element.decompose()  # Remove the element from the tree

        # Remove elements with class "EOlPnc"
        for element in soup.find_all(class_="EOlPnc"):
            element.decompose()  # Remove the element from the tree

        for element in soup.find_all(class_="uR9Zq"):
            element.decompose()  # Remove the element from the tree
        for element in soup.find_all(class_="q7fqqf"):
            element.decompose()  # Remove the element from the tree
        for element in soup.find_all(class_="J9hCCd"):
            element.decompose()  # Remove the element from the tree
        # Remove footer and header elements
        for element in soup.find_all(['footer', 'header']):
            element.decompose()  # Remove the element from the tree

        # Remove elements with class "KP7LCb"
        for element in soup.find_all(class_="KP7LCb"):
            element.decompose()  # Remove the element from the tree
        
        # Remove elements with class "oTWEpb"
        for element in soup.find_all(class_="oTWEpb"):
            element.decompose()  # Remove the element from the tree

        # Remove the first <style> tag in the HTML
        first_style_tag = soup.find('style')
        if first_style_tag:
            first_style_tag.decompose()  # Remove the first style tag from the tree

        # Remove unwanted text from the HTML content
        unwanted_text_1 = "/url?esrc=s&amp;q=&amp;rct=j&amp;sa=U&amp;url="
        unwanted_text_2 = "/url?esrc=s&q=&rct=j&sa=U&url="
        cleaned_html = str(soup).replace(unwanted_text_1, "").replace(unwanted_text_2, "")

        # Return the cleaned HTML content
        return cleaned_html
    else:
        return f"Please Sare Your Valuable Feedback Of Our Search Engine Here - https://forms.gle/1RFcZ2CgoS9E8ffy7"

def get_duckduckgo_first_result(query):
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
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove specific elements as per the requirements

        # Remove elements with class "Gx5Zad xpd EtOod pkphOe", keeping the first two
        gx5_elements = soup.find_all(class_="Gx5Zad xpd EtOod pkphOe")
        for element in gx5_elements[2:]:  # Skip the first two elements
            element.decompose()  # Remove the element from the tree

        # Remove elements with class "EOlPnc"
        for element in soup.find_all(class_="EOlPnc"):
            element.decompose()  # Remove the element from the tree

        for element in soup.find_all(class_="uR9Zq"):
            element.decompose()  # Remove the element from the tree
        for element in soup.find_all(class_="q7fqqf"):
            element.decompose()  # Remove the element from the tree
        for element in soup.find_all(class_="J9hCCd"):
            element.decompose()  # Remove the element from the tree
        # Remove footer and header elements
        for element in soup.find_all(['footer', 'header']):
            element.decompose()  # Remove the element from the tree

        # Remove elements with class "KP7LCb"
        for element in soup.find_all(class_="KP7LCb"):
            element.decompose()  # Remove the element from the tree
        
        # Remove elements with class "oTWEpb"
        for element in soup.find_all(class_="oTWEpb"):
            element.decompose()  # Remove the element from the tree

        # Remove the first <style> tag in the HTML
        first_style_tag = soup.find('style')
        if first_style_tag:
            first_style_tag.decompose()  # Remove the first style tag from the tree

        # Remove unwanted text from the HTML content
        unwanted_text_1 = "/url?esrc=s&amp;q=&amp;rct=j&amp;sa=U&amp;url="
        unwanted_text_2 = "/url?esrc=s&q=&rct=j&sa=U&url="
        cleaned_html = str(soup).replace(unwanted_text_1, "").replace(unwanted_text_2, "")

        # Return the cleaned HTML content
        return cleaned_html
    else:
        return f"Please Sare Your Valuable Feedback Of Our Search Engine Here - https://forms.gle/1RFcZ2CgoS9E8ffy7"

def extract_top_widget(query):
    query_type = classify_query(query)
    top_widget_html = ""
    
    if query_type == "Calculation":
        top_widget_html = evaluate_calculation(query)
    elif query_type == "Translation":
        top_widget_html = perform_translation(query)
    elif query_type == "Location":
        top_widget_html = get_google_maps_link(query)
    elif query_type == "Other":
        top_widget_html = get_duckduckgo_first_result(query)
    
    return top_widget_html



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
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove specific elements as per the requirements

        # Remove elements with class "Gx5Zad xpd EtOod pkphOe", keeping the first two
        gx5_elements = soup.find_all(class_="Gx5Zad xpd EtOod pkphOe")
        for element in gx5_elements[2:]:  # Skip the first two elements
            element.decompose()  # Remove the element from the tree

        # Remove elements with class "EOlPnc"
        for element in soup.find_all(class_="EOlPnc"):
            element.decompose()  # Remove the element from the tree

        # Remove footer and header elements
        for element in soup.find_all(['footer', 'header']):
            element.decompose()  # Remove the element from the tree

        # Remove elements with class "KP7LCb"
        for element in soup.find_all(class_="KP7LCb"):
            element.decompose()  # Remove the element from the tree
        
        # Remove elements with class "oTWEpb"
        for element in soup.find_all(class_="oTWEpb"):
            element.decompose()  # Remove the element from the tree

        # Remove unwanted text from the HTML content
        unwanted_texts = [
            "/url?esrc=s&amp;q=&amp;rct=j&amp;sa=U&amp;url=",
            "&amp;ved=2ahUKEwj9r9z3hvqIAxWKrZUCHcz7G1MQFnoECAMQBQ&amp;usg=AOvVaw2GZ3mtY6X-VM_aTqT368LS"
        ]
        
        # Remove all unwanted texts
        cleaned_html = str(soup)
        for text in unwanted_texts:
            cleaned_html = cleaned_html.replace(text, "")

        # Remove text after "&amp;ved=" in href attributes of <a> tags
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            ved_index = href.find("&amp;ved=")
            if ved_index != -1:
                # Keep the portion before "&amp;ved="
                cleaned_href = href[:ved_index]
                a_tag['href'] = cleaned_href  # Update the href attribute

        # Process content from elements with class "BNeawe UPmit AP7Wnd UwRFLe"
        for element in soup.find_all(class_="BNeawe UPmit AP7Wnd UwRFLe"):
            # Remove spaces and replace › with /
            processed_content = element.get_text(strip=True).replace('›', '/').replace(' ', '')
            # Prepend with "https://"
            new_href = f"https://{processed_content}"

            # Find the parent <a> tag and update its href
            parent_a_tag = element.find_parent('a', href=True)
            if parent_a_tag:
                parent_a_tag['href'] = new_href  # Update the href attribute

        # Return the cleaned HTML content
        return str(soup)
    else:
        return f"Please Sare Your Valuable Feedback Of Our Search Engine Here - https://forms.gle/1RFcZ2CgoS9E8ffy7"

def preprocess_elements(elements):
    processed_elements = []
    for element in elements:
        processed_element = str(element)
        processed_element = processed_element.replace("copyToClipboard", "window.open")
        processed_element = processed_element.replace("Copy Link", "Open/Download Link")
        processed_element = processed_element.replace("1", "")
        processed_element = processed_element.replace("""Join FilePursuit on """, "")
        processed_element = processed_element.replace("""FilePursuit Discord Server""", "")
        processed_element = processed_element.replace("""/assets/images/Discord-Logo+Wordmark-White.png""", "")
        processed_element = processed_element.replace("""chat for discussions and more information.""", "")
        processed_elements.append(processed_element)
    return processed_elements

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_query = request.form['search_query']
        # session['toggle_ai'] = 'toggle_ai' in request.form
        return redirect(url_for('search_results', query=search_query, original_query=search_query))
    return render_template('index.html')

# @app.route('/search_q=<query>', methods=['GET', 'POST'])
# def search_results(query):
#     if request.method == 'POST' and 'results' in request.form:
#         return redirect(url_for('more_results', query=query))
#     toggle_ai = session.get('toggle_ai', False)
#     url = f"https://www.google.com/search?q={query}&ie=utf-8&oe=utf-8&num=11"
#     results = scrape_google_results(url)
#     top_widget_html = extract_top_widget(query)
#     return render_template('results.html', results=results, search_query=query, top_widget=top_widget_html, toggle_ai=toggle_ai)

# @app.route('/search_q=<query>&results=more', methods=['POST'])
# def more_results(query):
#     search_query = request.form['search_query']
#     num_results = int(request.form['num_results'])
#     toggle_ai = session.get('toggle_ai', False)
#     url = f"https://www.google.com/search?q={search_query}&ie=utf-8&oe=utf-8&num={num_results + 10}"
#     results = scrape_google_results(url)
#     return render_template('results.html', results=results, search_query=search_query, toggle_ai=toggle_ai)



@app.route('/search_q=<query>', methods=['GET', 'POST'])
def search_results(query):
    # original_query = request.args.get('original_query')
    if request.method == 'POST' and 'results' in request.form:
        return redirect(url_for('more_results', query=query))
    original_query = urllib.parse.unquote(query)  # Decode the query
    url = f"https://www.google.com/search?q={query}&ie=utf-8&oe=utf-8&num=11"
    results = scrape_google_results(url)
    # top_widget_html = extract_top_widget(query)

    return render_template('results.html', results=results, search_query=query, original_query=original_query)

@app.route('/search_q=<query>&results=more', methods=['POST'])
def more_results(query):
    original_query = urllib.parse.unquote(query)  # Decode the query
    search_query = request.form['search_query']
    num_results = int(request.form['num_results'])
    url = f"https://www.google.com/search?q={search_query}&ie=utf-8&oe=utf-8&num={num_results + 10}"
    results = scrape_google_results(url)
    return render_template('results.html', results=results, search_query=search_query, original_query=original_query)

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')

@app.route('/sitemap.xml', methods=['GET', 'POST'])
def sitemap():
    return render_template('sitemap.xml')

# @app.route('/search_q=<query>&toggle_ai=<toggle_ai>', methods=['GET', 'POST'])
# def search_results(query, toggle_ai):
#     if request.method == 'POST' and 'results' in request.form:
#         return redirect(url_for('more_results', query=query, toggle_ai=toggle_ai))
#     url = f"https://www.google.com/search?q={query}&ie=utf-8&oe=utf-8&num=11"
#     results = scrape_google_results(url)
#     top_widget_html = extract_top_widget(query)
#     return render_template('results.html', results=results, search_query=query, top_widget=top_widget_html, toggle_ai=toggle_ai)

# @app.route('/search_q=<query>&toggle_ai=<toggle_ai>&results=more', methods=['POST'])
# def more_results(query, toggle_ai):
#     search_query = request.form['search_query']
#     num_results = int(request.form['num_results'])
#     url = f"https://www.google.com/search?q={search_query}&ie=utf-8&oe=utf-8&num={num_results + 10}"
#     results = scrape_google_results(url)
#     return render_template('results.html', results=results, search_query=search_query, toggle_ai=toggle_ai)

# @app.route('/top_widget/<query>', methods=['GET'])
# def fetch_top_widget(query):
#     # top_widget_html = extract_top_widget(query)
#     # return jsonify({'top_widget': top_widget_html})
#     fquery = """Can you answer my query - """ + query + """. If my query is translation then do not give me source and just give the answer like - 
# Original query : {my original query}   {original query language}
# Answer: {translated query} {translated query language} . 
# Do not write anything else it.
# If my query is of claculation then do not give me source and just give the answer like - 
# {my question(which I asked from you)}

# Answer: {the result}. 
# Do not write anything else it.

# If my query is of asking for details belween 2 places like - {place 1} to {place 2} or something like that then then do not give me source and just give the answer like - 
#  Distance: {distance between the two places}
#  Time :
#    Walking: {time of waling between the 2 places}
#    Cycling: {time if I cycled that distance}
#    Driving: {time taken if I come from car}


# Google maps link: {google map link of the query}.(the google map link is liek - https://www.google.com/maps/dir/{place1}/{place2}/)

# . Do not write anything else it.





# If my query is not a translation,calculation or loaction , THEN RETURN THE ANSWER OF MY QUERY WIT ITS SOURCE(WITH IT URL).

#    """
#     resultswid = DDGS().chat(fquery , model='llama-3-70b')
#     top_widget_html = resultswid
#     return jsonify({'top_widget': top_widget_html})

@app.route('/ai_response/<query>', methods=['GET'])
def fetch_ai_response(query):

    fquery = "From now your name is ExyAI , an AI app for a search engine named Exyser. You have to help the uyser with their query. When ever user enter their query you have to repond them . If you have to bold a text enclose the text in <b> and </b> if you ahve to underline it enclose the text in <u> and </u>, if you ahve to italic it enclose the text in <i> and </i>. Now the user's query is - " + query
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": fquery}]
    )

    # # Debugging: Print the response object
    # print(response.choices[0].message.content)

    try:
        # Use the appropriate method or attribute to access content
        airesult = response.choices[0].message.content # Adjust this line based on the actual method
    except AttributeError as e:
        airesult = f"Error accessing attributes: {e}"
    except (IndexError, KeyError) as e:
        airesult = f"Error processing AI response: {e}"

    return jsonify({'ai_resp': airesult})

@app.route('/top_widget/<query>', methods=['GET'])
def fetch_top_widget(query):
    top_widget_html = extract_top_widget(query)
    return jsonify({'top_widget': top_widget_html})
    # Return the HTML content as a response


#     fquery = """Can you answer my query - """ + query + """. If my query is translation then do not give me source and just give the answer like - 

#     <style>
#         .translate-snippet {
#             background: #fff;
#             border: 1px solid #ccc;
#             border-radius: 8px;
#             box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
#             margin: 20px;
#             padding: 20px;
#             width: 300px;
#         }
#         h2 {
#             margin-top: 0;
#         }
#         .translate-container {
#             display: flex;
#             justify-content: space-between;
#         }
#         .translate-box {
#             width: 48%;
#             display: flex;
#             flex-direction: column;
#         }

#     </style>

#     <div class="translate-snippet">
#         <div class="translate-container">
#             <div class="translate-box">
#                 <label for="translateInput">{original query language}</label>
#                 <p>{my original query}</p>
#             </div>
#             <div class="translate-box">
#                 <label for="translateOutput">{translated query language}</label>
#                 <h4>{translated query}</h4>
#             </div>
#         </div>
#     </div>

# Do not write anything else it. And also do not provide source for these query.
# If my query is of claculation then do not give me source and just give the answer like - 

#   <div class="calculation-snippet">
#         <h4>{the calculation query I asked from you}</h4>
#         <h2>{the result of my calculation}</h2>
#     </div>


# Do not write anything else it. And also do not provide source for these query.

# If my query is of asking for details belween 2 places like - {place 1} to {place 2} or something like that then then do not give me source and just give the answer like - 


#     <div class="location-snippet">
#         <p><iframe id="map-canvas" class="map_part" width="600"  height="450"  frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="https://maps.google.com/maps?width=100%&amp;height=100%&amp;hl=en&amp;q={place1} to {place2}&amp;t=&amp;z=14&amp;ie=UTF8&amp;iwloc=B&amp;output=embed">Powered by <a href="https://www.googlemapsgenerator.com">embed google maps html</a> and <a href="https://skipboregler.com/no/">skip bo regler</a></iframe></p>
#         <h2>{distance between the two places}</h2>
#         <h4>Driving : {time taken if I come from car}</h4>
#         <h4>Cycling: {time if I cycled that distance}</h4>
#         <h4>Walking: {time of waling between the 2 places}</h4>
#          <a href="{google map link of the query}">{google map link of the query}.(the google map link is liek - https://www.google.com/maps/dir/{place1}/{place2}/)</a>
#     </div>


# Google maps link: 

# . Do not write anything else it. And also do not provide source for these query.





# If my query is not a translation,calculation or loaction , THEN RETURN THE ANSWER OF MY QUERY should be ike this - 

#     <div class="other-snippet">
#         <h4>{ansewr of my query}</h4>
#         <a href="{answer's source}">{answer's source}</a>
#     </div>
#  IF YOU CAN NOT DETRMINE WHAT USER IS ASKING THEN JUST RETURN WHATEVERY YOU THINK WHAT'S USER QUERY IS AND THEN RETURN THE RESPONCE LIKE THIS - <div class="other-snippet">
#         <h4>{ansewr of my query}</h4>
#         <a href="{answer's source}">{answer's source}</a>
#     </div>



#     Do not forget to give me the source of querys which are not rasnaltio,location or calculation. DO NOT BEHAVE LIKE AN AI, BEHAVE LIKE THE SNIPEET OF GOOGLE. 
#    """
#     try:
#         resultswid = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[{"role": "user", "content": fquery}]
#     )
#         resultswidd = resultswid.choices[0].message.content
#         top_widget_html = resultswidd
#     except Exception as e:
#         top_widget_html = str(e)
#     return jsonify({'top_widget': top_widget_html})


def get_suggestions(query):
    ddgs = DDGS()
    suggestions = ddgs.suggestions(query)
    return [suggestion['phrase'] for suggestion in suggestions]

@app.route('/suggestions', methods=['GET'])
def suggestions():
    query = request.args.get('query', '')
    if query:
        suggestion_list = get_suggestions(query)
        return jsonify(suggestion_list)
    return jsonify([])

@app.route('/clear_history', methods=['POST'])
def clear_history():
    session.pop('selected_suggestions', None)
    return jsonify({'success': True})




@app.route('/toggle_suggestions', methods=['POST'])
def toggle_suggestions():
    data = request.get_json()
    enabled = data.get('enabled', True)
    session['suggestions_enabled'] = enabled
    return jsonify({'success': True})

@app.route('/search_q=<search_query>&type=images', methods=['POST'])
def display_images_route(search_query):
    original_query = urllib.parse.unquote(search_query)  # Decode the query
    search_query = request.form['search_query']
    results = search_images(search_query)
    return render_template('images.html', results=results, search_query=search_query, original_query=original_query)

@app.route('/search_q=<search_query>&type=images&results=more', methods=['POST'])
def more_images(search_query):
    original_query = urllib.parse.unquote(search_query)  # Decode the query
    search_query = request.form['search_query']
    num_results = int(request.form['num_results'])
    updated_results = search_images(search_query, max_results=num_results + 10)
    return render_template('images.html', results=updated_results, search_query=search_query, original_query=original_query)


# @app.route('/videos/<query>', methods=['GET'])
# def video_results(query):
#     results = YoutubeSearch(query, max_results=10).to_json()
#     results_dict = json.loads(results)
#     return render_template('videos.html', results=results_dict['videos'], search_query=query)

# @app.route('/videos/<query>/more', methods=['GET'])
# def more_videos(query):
#     results = YoutubeSearch(query, max_results=30).to_json()
#     results_dict = json.loads(results)
#     more_results = results_dict['videos'][10:]  # Get more results after the first 10
#     return render_template('videos.html', results=more_results, search_query=query)
@app.route('/search_q=<query>&type=videos', methods=['GET'])
def video_results(query):
    original_query = urllib.parse.unquote(query)  # Decode the query
    results = YoutubeSearch(query, max_results=10).to_json()
    results_dict = json.loads(results)
    videos = [{'title': video['title'], 'link': f"https://www.youtube.com{video['url_suffix']}", 'id': video['id'], 'channel': video['channel'], 'publish_time': video['publish_time']} for video in results_dict['videos']]
    return render_template('videos.html', results=videos, search_query=query, original_query=original_query)

@app.route('/search_q=<query>&type=videos&results=more', methods=['GET'])
def more_videos(query):
    original_query = urllib.parse.unquote(query)  # Decode the query
    results = YoutubeSearch(query, max_results=30).to_json()
    results_dict = json.loads(results)
    more_results = results_dict['videos'][10:]  # Get more results after the first 10
    videos = [{'title': video['title'], 'link': f"https://www.youtube.com{video['url_suffix']}", 'id': video['id'], 'channel': video['channel'], 'publish_time': video['publish_time']} for video in more_results]
    return render_template('videos.html', results=videos, search_query=query, original_query=original_query)


@app.route('/search_q=<search_query>&type=maps', methods=['POST'])
def maps(search_query):
    original_query = urllib.parse.unquote(search_query)  # Decode the query
    search_query = request.form['search_query']
    results = search_images(search_query)
    return render_template('maps.html', results=results, search_query=search_query, original_query=original_query)

@app.route('/search_q=<search_query>&type=maps&results=more', methods=['POST'])
def more_maps(search_query):
    original_query = urllib.parse.unquote(search_query)  # Decode the query
    search_query = request.form['search_query']
    num_results = int(request.form['num_results'])
    updated_results = search_images(search_query, max_results=num_results + 10)
    return render_template('maps.html', results=updated_results, search_query=search_query, original_query=original_query)


# @app.route('/search_q=<search_query>&type=videos', methods=['POST'])
# def videos(search_query):
#     search_query = request.form['search_query']
#     video_results = search_youtube_videos(search_query)
#     return render_template('videos.html', search_query=search_query, video_results=video_results)

# @app.route('/search_q=<search_query>&type=videos&results=more', methods=['POST'])
# def more_videos(search_query):
#     search_query = request.form['search_query']
#     current_results = int(request.form['num_results'])
#     additional_results = search_youtube_videos(search_query, max_results=current_results + 10)
#     return render_template('videos.html', search_query=search_query, video_results=additional_results)
    

@app.route('/search_q=<query>&type=maps', methods=['GET'])
def maps_results(query):
    original_query = urllib.parse.unquote(query)  # Decode the query
    google_maps = f"https://www.google.com/maps/search/{query}"
    bing_maps = f"https://www.bing.com/maps?q={query}"
    duckduckgo_maps = f"https://duckduckgo.com/?q={query}&ia=maps"
    open_street_maps = f"https://www.openstreetmap.org/search?query={query}"
    return render_template('maps.html', search_query=query, google_maps=google_maps, bing_maps=bing_maps, duckduckgo_maps=duckduckgo_maps, open_street_maps=open_street_maps, original_query=original_query)


@app.route('/search_q=<search_query>&type=news', methods=['POST'])
def news(search_query):
    original_query = urllib.parse.unquote(search_query)  # Decode the query
    search_query = request.form['search_query']
    news_results = search_news(search_query)
    return render_template('news.html', search_query=search_query, news_results=news_results, original_query=original_query)

@app.route('/search_q=<search_query>&type=news&results=more', methods=['POST'])
def more_news(search_query):
    original_query = urllib.parse.unquote(search_query)  # Decode the query
    search_query = request.form['search_query']
    current_results = int(request.form['num_results'])
    additional_results = search_news(search_query, max_results=current_results + 10)
    return render_template('news.html', search_query=search_query, news_results=additional_results, original_query=original_query)


@app.route('/search_files', methods=['POST'])
def search_files():
    search_query = request.form['search_query']
    # Redirect to the file search route and pass the query
    return redirect(url_for('file_search', query=search_query))


@app.route('/search_q=<query>&type=file', methods=['GET'])
def file_search(query):
    encoded_query = quote_plus(query)
    url = "https://filepursuit.com/pursuit?q=" + encoded_query + "&type=all"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        col_md_12_elements = soup.find_all(class_="col-md-12")
        processed_elements = preprocess_elements(col_md_12_elements)
        return render_template('files.html', elements=processed_elements, search_query=query)
    else:
        return "Failed to retrieve webpage."


if __name__ == "__main__":
    app.run(host="0.0.0.0" , port="5000",debug=True)
