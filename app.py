import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Set up the Streamlit page
st.set_page_config(page_title="CNB/CB2 Replacement Tool", layout="centered")
st.title("🔄 CNB/CB2 Replacement Suggestion Tool")
st.markdown("Welcome to the CNB/CB2 Replacement Tool! - **Mohammed Kassem**")
st.markdown("Enter a SKU or product URL to get replacement suggestions based on color, dimensions, and design.")

# Input field for SKU or product URL
user_input = st.text_input("Enter SKU or Product URL")

# Function to fetch and parse product data using ScrapingBee API or fallback
def fetch_product_data(url):
    try:
        # Use ScrapingBee API to fetch the page
        api_key = "YOUR_SCRAPINGBEE_API_KEY"  # Replace with your actual API key
        api_url = f"https://app.scrapingbee.com/api/v1/?api_key={api_key}&url={url}&render_js=False"
        response = requests.get(api_url, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
    except Exception:
        # Fallback to direct request for CB2.ae
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
    return soup

# Function to find replacement products
def find_replacements(user_input):
    try:
        # Determine the URL to fetch
        if "http" in user_input:
            url = user_input
        else:
            url = f"https://www.crateandbarrel.me/en-ae/search?q={user_input}"

        soup = fetch_product_data(url)

        # Extract product attributes from <ul><li>...</li></ul>
        attributes = soup.find_all("li")
        attr_texts = [li.get_text(strip=True) for li in attributes]

        # Try to extract color, dimensions, and design from the list
        color = next((text for text in attr_texts if "marble" in text.lower() or "color" in text.lower()), "Unknown")
        dimensions = next((text for text in attr_texts if "cm" in text.lower() or "dia" in text.lower() or "dimensions" in text.lower()), "Unknown")
        design = next((text for text in attr_texts if "design" in text.lower() or "legs" in text.lower()), "Unknown")

        # Mocked replacement suggestions
        replacements = [
            {
                "Name": "Alternative Product A",
                "Color": color,
                "Dimensions": dimensions,
                "Design": design,
                "Link": "https://www.cnb.com/productA"
            },
            {
                "Name": "Alternative Product B",
                "Color": color,
                "Dimensions": dimensions,
                "Design": design,
                "Link": "https://www.cnb.com/productB"
            }
        ]
        return pd.DataFrame(replacements)

    except Exception as e:
        return pd.DataFrame([{"Error": str(e)}])

# Display results if input is provided
if user_input:
    st.info(f"Searching for replacements for: {user_input}")
    results_df = find_replacements(user_input)
    st.dataframe(results_df)
