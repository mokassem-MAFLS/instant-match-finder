import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def get_source_site(url):
    if "crateandbarrel.me" in url:
        return "Crate & Barrel UAE"
    elif "cb2.ae" in url:
        return "CB2 UAE"
    else:
        return "Unknown"

def scrape_product_details(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return {"error": "Failed to retrieve product page."}

    soup = BeautifulSoup(response.content, "html.parser")

    product_name = soup.find("h1")
    product_name = product_name.text.strip() if product_name else "N/A"

    sku_tag = soup.find("span", class_="product-sku")
    sku = sku_tag.text.strip() if sku_tag else "N/A"

    price_tag = soup.find("span", class_="price-sales")
    price = price_tag.text.strip() if price_tag else "N/A"

    color_tag = soup.find("span", class_="product-variation")
    color = color_tag.text.strip() if color_tag else "N/A"

    dimensions = []
    dimension_tags = soup.find_all("li", class_="product-dimension")
    for tag in dimension_tags:
        dimensions.append(tag.text.strip())

    return {
        "Product Name": product_name,
        "SKU": sku,
        "Price": price,
        "Color": color,
        "Dimensions": dimensions,
        "Source Site": get_source_site(url),
        "Product Link": url
    }

st.title("🪑 Instant Match Finder")
st.write("Enter a product link from Crate & Barrel UAE or CB2 UAE to view product details.")

product_url = st.text_input("🔗 Product Link")

if product_url:
    with st.spinner("Fetching product details..."):
        details = scrape_product_details(product_url)

    if "error" in details:
        st.error(details["error"])
    else:
        st.subheader("📦 Product Details")
        st.write(f"**Product Name:** {details['Product Name']}")
        st.write(f"**SKU:** {details['SKU']}")
        st.write(f"**Price:** {details['Price']}")
        st.write(f"**Color:** {details['Color']}")
        st.write(f"**Source Site:** {details['Source Site']}")
        st.write(f"**Product Link:** [View Product]({details['Product Link']})")

        if details["Dimensions"]:
            st.write("**Dimensions:**")
            for dim in details["Dimensions"]:
                st.write(f"- {dim}")

        st.markdown("---")
        st.subheader("🧠 Matching Logic (Coming Soon)")
        st.info("This section will suggest similar items based on color, dimensions, and design.")
