#Sample Request
import requests
from bs4 import BeautifulSoup
import json

url = "https://books.toscrape.com/catalogue/"
books_list = []
books_data = []
for num in range(1,3):
    print(f"Scraping page {num}")
    store_url = url + f"page-{num}.html"
    data = requests.get(store_url)
    soup = BeautifulSoup(data.text, "html.parser")
    product_box = soup.find_all("article", {"class": "product_pod"})
    for i in product_box:
        book_url = i.find("a").get("href")
        product_url = url + book_url
        books_list.append(product_url)

for book in books_list:
    try:
        print(f"Scraping: {book}")
        try:
            book_data = requests.get(book)
            book_data.raise_for_status()
        except Exception as e:
            print(f"Error: {e}")
            continue
        soup= BeautifulSoup(book_data.text, "html.parser")
        try:
            title = soup.find("h1").get_text()
        except Exception as e:
            title = "No title found"
        try:
            price = soup.find("p", {"class": "price_color"}).get_text()
        except Exception as e:
            price = "No price found"
        try:
            desc = soup.find_all("p")[3].get_text()
        except Exception as e:
            desc = "No description found"

        book_data = {
            "title": title,
            "price": price,
            "desc": desc,
        }
        try:
            info = soup.find("table", {"class": "table table-striped"})
            details = info.find_all("tr")
            for i in details:
                key = i.find("th").get_text()
                value = i.find("td").get_text()
                book_data[key] = value
        except Exception as e:
            print(f"Error: {e}")

        books_data.append(book_data)

    except Exception as e:
        print(f"Error: {e}")
        continue

with open("books.json", "w") as file:
    json.dump(books_data, file, indent=4)