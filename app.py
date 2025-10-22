def find_replacements(user_input):
    try:
        # Use CNB product URL directly
        url = user_input

        # Fetch the page content
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract all text from the page
        page_text = soup.get_text(separator=' ', strip=True).lower()

        # Keyword-based extraction
        color = "White" if "white" in page_text else "Unknown"
        dimensions = "54\" dia. x 30\"H" if "54" in page_text and "30" in page_text else "Unknown"
        design = "Hourglass pedestal silhouette" if "hourglass" in page_text else "Unknown"

        # Mocked replacement suggestions
        replacements = [
            {
                "Name": "Alternative Product A",
                "Color": color,
                "Dimensions": dimensions,
                "Design": design,
                "Link": "https://www.crateandbarrel.me/en-ae/product/alternative-product-a"
            },
            {
                "Name": "Alternative Product B",
                "Color": color,
                "Dimensions": dimensions,
                "Design": design,
                "Link": "https://www.crateandbarrel.me/en-ae/product/alternative-product-b"
            }
        ]
        return pd.DataFrame(replacements)

    except Exception as e:
        return pd.DataFrame([{"Error": str(e)}])
