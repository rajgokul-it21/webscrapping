import requests
from bs4 import BeautifulSoup


url = "https://www.agroinfomedia.com/"


response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")


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
    print(link)
