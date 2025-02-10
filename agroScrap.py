import requests
from bs4 import BeautifulSoup
import json

url = "https://www.agroinfomedia.com/"
agro_list = []
agro_data = []

print(f"Scraping page")
data = requests.get(url)
soup = BeautifulSoup(data.text, "html.parser")
div_tag = soup.find("div")  


table_tag = div_tag.find("table") if div_tag else None


filtered_links = set()
if table_tag:
    for a_tag in table_tag.find_all("a", href=True):  
        links = a_tag["href"]
        if "category.php?id=" in links:  
            filtered_links.add(links)

filtered_links = list(filtered_links)

for link in filtered_links:
    full_url = url + link  
    agro_list.append(full_url)




for agro in agro_list:
    try:
        print(f"Scraping: {agro}")
        try:
            agro_data = requests.get(agro)
            agro_data.raise_for_status()
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

with open("agri.json", "w") as file:
    json.dump(books_data, file, indent=4)