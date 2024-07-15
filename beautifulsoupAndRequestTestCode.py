import requests
from bs4 import BeautifulSoup

def test_beautifulsoup_installation():
    # Test URL
    url = "http://example.com"
    
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the title tag and print its content
        title_tag = soup.title
        if title_tag:
            print(f"Title of the page: {title_tag.string}")
        else:
            print("Title tag not found.")
        
        print("BeautifulSoup and requests are installed and working correctly.")
        
    except Exception as e:
        print(f"An error occurred: {e}")

# Run the test
test_beautifulsoup_installation()
