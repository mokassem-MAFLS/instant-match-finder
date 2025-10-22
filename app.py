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

# Function to find replacement products
def find_replacements(user_input):
    try:
        # Determine the URL to fetch
        if "http" in user_input:
            url = user_input
        else:
            url = f"https://www.cnb.com/search?q={user_input}"

        # Fetch the page content
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract product attributes (adjust selectors as needed)
        color = soup.find("div", class_="color")
        dimensions = soup.find("div", class_="dimensions")
        design = soup.find("div", class_="design")

        color_text = color.text.strip() if color else "Unknown"
        dimensions_text = dimensions.text.strip() if dimensions else "Unknown"
        design_text = design.text.strip() if design else "Unknown"

        # Mocked replacement suggestions
        replacements = [
            {
                "Name": "Alternative Product A",
                "Color": color_text,
                "Dimensions": dimensions_text,
                "Design": design_text,
                "Link": "https://www.cnb.com/productA"
            },
            {
                "Name": "Alternative Product B",
                "Color": color_text,
                "Dimensions": dimensions_text,
                "Design": design_text,
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
