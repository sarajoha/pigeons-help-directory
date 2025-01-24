import requests
from bs4 import BeautifulSoup
import pandas as pd
from unidecode import unidecode

# URL of the page to scrape
url = "https://www.misamigaslaspalomas.com/2011/07/6-listado-de-centros-de-rehabilitacion.html"

# Fetch the webpage content
response = requests.get(url)
if response.status_code != 200:
    print(f"Failed to fetch page: {response.status_code}")
    exit()

# Parse the HTML content
soup = BeautifulSoup(response.text, "html.parser")

# Find all divs containing the centers
divs = soup.find_all("div")

# Predefined list of Spanish cities (converted to lowercase and accent-free)
spanish_cities = {
    unidecode(city.lower())
    for city in [
        "Madrid",
        "Barcelona",
        "Valencia",
        "Sevilla",
        "Zaragoza",
        "Málaga",
        "Murcia",
        "Palma",
        "Las Palmas",
        "Bilbao",
        "Alicante",
        "Córdoba",
        "Valladolid",
        "Vigo",
        "Gijón",
        "Eibar",
        "Granada",
        "Santander",
        "Pamplona",
        "Almería",
        "San Sebastián",
        "Salamanca",
        "Burgos",
        "Albacete",
        "Oviedo",
        "Cádiz",
        "Huelva",
        "Lleida",
        "León",
    ]
}

# Initialize a list to store extracted data
rehab_centers = []
seen_centers = set()
current_center = None
city_name = None

for div in divs:
    # Check if the div contains a <b> or <span> tag (Center Name)
    bold_tag = div.find("b")
    span_tag = div.find("span")

    center_text_bold = bold_tag.get_text(strip=True) if bold_tag else None
    center_text_span = span_tag.get_text(strip=True) if span_tag else None

    # Choose the first available name (bold preferred over span)
    center_name = center_text_bold or center_text_span

    # Convert to lowercase for case-insensitive comparison
    if center_name:
        center_name_lower = center_name.lower()
    else:
        center_name_lower = None

    # Check if the extracted name contains "centro de " or "centre de"
    if center_name_lower and (
        "centro de " in center_name_lower or "centre de " in center_name_lower
    ):
        # Avoid duplicates
        if center_name_lower not in seen_centers:
            # If there's a previously stored center, save it before moving to the next
            if current_center:
                rehab_centers.append({"Center Name": current_center, "City": city_name})

            # Store the new center
            seen_centers.add(center_name_lower)  # Add to set to prevent duplicates
            current_center = center_name
            city_name = None  # Reset city for the new center

        print(current_center)
    # If we already have a center, look for the first meaningful city-like text
    elif current_center and not city_name:
        bold_tag = div.find("b")
        text = bold_tag.get_text(strip=True) if bold_tag else ""
        text_clean = unidecode(text.lower())  # Normalize text for comparison

        # Validate if the extracted text is a known city
        if text_clean in spanish_cities:
            city_name = text  # Save original text version (not lowercased)
        elif text and len(text.split()) < 5:  # Heuristic: city names are usually short
            city_name = text

# Save the last center
if current_center and current_center.lower() not in seen_centers:
    rehab_centers.append({"Center Name": current_center, "City": city_name})

print(rehab_centers)
df = pd.DataFrame(rehab_centers)

# Save to CSV (Optional)
df.to_csv("rehabilitation_centers.csv", index=False)

print("Data extracted and saved successfully!")
