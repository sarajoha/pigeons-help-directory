import requests
from bs4 import BeautifulSoup
import pandas as pd
from unidecode import unidecode
import re

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
current_details = []
seen_centers = set()
current_center = None
invalid_names = {
    "¿Qué es un centro de recuperación?",
    "¿Cómo funcionan los centros de recuperación?",  # Add any other common invalid names here
}

# Regex pattern for extracting URLs
url_pattern = re.compile(r"(https?://[^\s|]+|www\.[a-zA-Z0-9-]+\.[a-zA-Z]{2,})")
email_pattern = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
phone_pattern = re.compile(r"\b(?:\d{2,3}[ -]?){2,4}\d{2,4}\b")

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

    # Skip invalid center names
    if center_name and center_name in invalid_names:
        continue  # Skip this iteration

    # Check if the extracted name contains "centro de " or "centre de"
    if center_name_lower and (
        "centro de " in center_name_lower
        or "centre de " in center_name_lower
        or "crea" in center_name_lower
        or "crema" in center_name_lower
    ):
        # Avoid duplicates
        if center_name_lower not in seen_centers:
            # If there's a previously stored center, save it before moving to the next
            if current_center:
                details_text = " | ".join(current_details)

                # Extract the first URL from details
                urls = url_pattern.findall(details_text)
                website = urls[0] if urls else None

                # Remove URL from details
                clean_details = re.sub(url_pattern, "", details_text).strip()

                # Extract the first email from details
                emails = email_pattern.findall(clean_details)
                email = emails[0] if emails else None

                # Remove email from details
                clean_details = re.sub(email_pattern, "", clean_details).strip()

                # Extract all phone numbers from details
                phones = phone_pattern.findall(clean_details)
                phone = (
                    " / ".join(phones) if phones else None
                )  # Join multiple numbers with a slash

                # Remove phone numbers from details
                clean_details = re.sub(phone_pattern, "", clean_details).strip()

                # Extract the first city from details
                words = clean_details.split()
                city = next(
                    (
                        word
                        for word in words
                        if unidecode(word.lower()) in spanish_cities
                    ),
                    None,
                )

                # Remove city from details
                if city:
                    clean_details = clean_details.replace(city, "").strip()

                rehab_centers.append(
                    {
                        "Center Name": current_center,
                        "Website": website,
                        "City": city,
                        "Email": email,
                        "Phone": phone,
                        "Details": " | ".join(current_details),
                    }
                )

            # Store the new center
            seen_centers.add(center_name_lower)  # Add to set to prevent duplicates
            current_center = center_name
            current_details = []

        print(current_center)
    else:
        # If we already have a center, collect details
        text = div.get_text(strip=True)
        if text:
            current_details.append(text)

# Save the last center
if current_center and current_center.lower() not in seen_centers:
    details_text = " | ".join(current_details)

    # Extract the first URL from details
    urls = url_pattern.findall(details_text)
    website = urls[0] if urls else None

    # Remove URL from details
    clean_details = re.sub(url_pattern, "", details_text).strip()

    # Extract the first email from details
    emails = email_pattern.findall(clean_details)
    email = emails[0] if emails else None

    # Remove email from details
    clean_details = re.sub(email_pattern, "", clean_details).strip()

    # Extract all phone numbers from details
    phones = phone_pattern.findall(clean_details)
    phone = " / ".join(phones) if phones else None  # Join multiple numbers with a slash

    # Remove phone numbers from details
    clean_details = re.sub(phone_pattern, "", clean_details).strip()

    # Extract the first city from details
    words = clean_details.split(" | ")
    city = next(
        (word for word in words if unidecode(word.lower()) in spanish_cities), None
    )

    # Remove city from details
    if city:
        clean_details = clean_details.replace(city, "").strip()

    rehab_centers.append(
        {
            "Center Name": current_center,
            "Website": website,
            "City": city,
            "Email": email,
            "Phone": phone,
            "Details": clean_details,
        }
    )

print(rehab_centers)
df = pd.DataFrame(rehab_centers)

df = df[["Center Name", "Website", "City", "Email", "Phone", "Details"]]

# Save to CSV (Optional)
df.to_csv("src/rehabilitation_centers.csv", index=False)

print("Data extracted and saved successfully!")
