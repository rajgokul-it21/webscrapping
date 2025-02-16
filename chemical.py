import requests
import json
from bs4 import BeautifulSoup

# Base URL
base_url = "https://www.chemicalbook.in/"
headers = {"User-Agent": "Mozilla/5.0"}

# Step 1: Extract Category Links
response = requests.get(base_url, headers=headers)

category_links = []
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    catalogue_div = soup.find("div", class_="catalogue")

    if catalogue_div:
        for li in catalogue_div.find_all("li"):
            a_tag = li.find("a")
            if a_tag and "href" in a_tag.attrs:
                category_name = a_tag.get_text(strip=True)
                if category_name.lower() != "all categories":
                    category_links.append({
                        "name": category_name,
                        "link": base_url + a_tag["href"].lstrip("/")
                    })

# Step 2: Visit Each Category Page & Extract Supplier Links
supplier_links = []
for category in category_links:
    category_url = category["link"]
    category_response = requests.get(category_url, headers=headers)

    if category_response.status_code == 200:
        category_soup = BeautifulSoup(category_response.text, "html.parser")
        supplier_divs = category_soup.find_all("div", class_="prosuppname")

        for div in supplier_divs:
            a_tag = div.find("a")
            if a_tag and "href" in a_tag.attrs and "/company-details/" in a_tag["href"]:
                supplier_name = a_tag.get_text(strip=True)
                supplier_links.append({
                    "name": supplier_name,
                    "link": base_url + a_tag["href"].lstrip("/")
                })

# Step 3: Visit Each Supplier Page & Extract Details
suppliers_data = []
for supplier in supplier_links:
    supplier_url = supplier["link"]
    supplier_response = requests.get(supplier_url, headers=headers)

    if supplier_response.status_code == 200:
        supplier_soup = BeautifulSoup(supplier_response.text, "html.parser")
        contact_div = supplier_soup.find("div", id="Content_SupplierContact")

        if contact_div:
            company_details = {
                "name": supplier["name"],
                "link": supplier_url,
                "website": "",
                "phone": "",
                "email": "",
                "nationality": "",
                "description": ""
            }

            # Extracting Contact Information
            rows = contact_div.find_all("tr")
            for row in rows:
                tds = row.find_all("td")
                if len(tds) == 2:
                    key = tds[0].get_text(strip=True)
                    value = tds[1].get_text(strip=True)

                    if "WebSite" in key:
                        company_details["website"] = value
                    elif "Tel" in key:
                        company_details["phone"] = value
                    elif "Email" in key:
                        company_details["email"] = value
                    elif "Product Total" in key:
                        company_details["product_count"] = value
                    elif "Nationality" in key:
                        company_details["nationality"] = value

            # Extracting Company Description
            intro_div = contact_div.find("div", id="liCompanyintro")
            if intro_div:
                company_details["description"] = intro_div.get_text(strip=True)

            # Extracting Product Names
            product_table = supplier_soup.find("tbody")
            if product_table:
                for tr in product_table.find_all("tr"):
                    td = tr.find("td", width="46%")  # Product name column
                    if td and td.find("a"):
                        product_name = td.find("a").get_text(strip=True)
                        company_details["products"].append(product_name)

            suppliers_data.append(company_details)

# Step 4: Save to JSON File
with open("suppliers_data.json", "w", encoding="utf-8") as file:
    json.dump(suppliers_data, file, indent=4, ensure_ascii=False)

print("Data extraction completed! Saved to 'suppliers_data.json'.")
