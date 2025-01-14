import requests
from bs4 import BeautifulSoup
import csv

# List of product URLs
urls = [
    "https://www.fashionandfriends.com/al/tommy-hilfiger-kepuce-me-take-per-femra-thfw0fw08156-0hs/",
    "https://www.fashionandfriends.com/al/replay-hallie-xhinse-per-femra-rwa526h-808-779-009/",
    "https://www.fashionandfriends.com/al/calvin-klein-kepuce-te-zeza-me-take-per-femra-ckhw0hw02171-beh/",
    "https://www.fashionandfriends.com/al/tommy-hilfiger-canta-per-femra-bordeaux-thaw0aw16511-vlp/",
]

# Function to extract product data
def extract_product_data(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract the title
            title_element = soup.find('h1')
            title = title_element.text.strip() if title_element else "Not Found"

            # Extract the price
            price_element = soup.find('span', class_='price')
            price = price_element.text.strip() if price_element else "Not Found"

            # Extract the meta description
            meta_description = soup.find('meta', attrs={'name': 'description'})
            description = meta_description['content'].strip() if meta_description else "Not Found"

            return [title, price, description]
        else:
            print(f"Error fetching {url}. Status code: {response.status_code}")
            return ["Error", "Error", "Error"]
    except Exception as e:
        print(f"An error occurred while processing {url}: {e}")
        return ["Error", "Error", "Error"]

# Open a CSV file to save the data
csv_filename = "products_with_description.csv"
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    # Write the header row
    writer.writerow(['Title', 'Price', 'Description'])

    # Loop through each URL and extract data
    for url in urls:
        print(f"Processing {url}...")
        product_data = extract_product_data(url)
        writer.writerow(product_data)

print(f"All data extracted and saved to {csv_filename}!")
