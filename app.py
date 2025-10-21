import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
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
        # Set up headless Chrome browser
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)

        # Navigate to the product page or search page
        if "http" in user_input:
            driver.get(user_input)
        else:
            driver.get(f"https://www.cnb.com/search?q={user_input}")

        # Parse the page content
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Extract product attributes
        color = soup.find("div", class_="color").text if soup.find("div", class_="color") else "Unknown"
        dimensions = soup.find("div", class_="dimensions").text if soup.find("div", class_="dimensions") else "Unknown"
        design = soup.find("div", class_="design").text if soup.find("div", class_="design") else "Unknown"

        driver.quit()

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
