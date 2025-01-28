import requests
from bs4 import BeautifulSoup
import pandas as pd
from unidecode import unidecode
import re

URL = "https://www.misamigaslaspalomas.com/2011/07/6-listado-de-centros-de-rehabilitacion.html"


def extract_divs(url):
    # Fetch the webpage content
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch page: {response.status_code}")
        return None

    # Parse the HTML content
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all divs containing the centers
    return soup.find_all("div")


def get_spanish_cities():
    # Predefined list of Spanish cities (converted to lowercase and accent-free)
    return {
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


def get_details(current_details):
    url_pattern = re.compile(r"(https?://[^\s|]+|www\.[a-zA-Z0-9-]+\.[a-zA-Z]{2,})")
    email_pattern = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
    phone_pattern = re.compile(r"\b(?:\d{2,3}[ -]?){2,4}\d{2,4}\b")

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
    words = clean_details.split()
    city = next(
        (word for word in words if unidecode(word.lower()) in get_spanish_cities()),
        None,
    )

    # Remove city from details
    if city:
        clean_details = clean_details.replace(city, "").strip()

    return {
        "Website": website,
        "City": city,
        "Email": email,
        "Phone": phone,
        "Details": " | ".join(current_details),
    }


def extract_data():
    rehab_centers = []
    current_details = []
    seen_centers = set()
    current_center = None
    invalid_names = {
        "¿Qué es un centro de recuperación?",
        "¿Cómo funcionan los centros de recuperación?",
    }

    divs = extract_divs(URL)
    for div in divs:
        # Check if the div contains a <b> or <span> tag (Center Name)
        bold_tag = div.find("b")
        span_tag = div.find("span")

        center_text_bold = bold_tag.get_text(strip=True) if bold_tag else None
        center_text_span = span_tag.get_text(" ", strip=True) if span_tag else None

        # Choose the first available name (span preferred over bold)
        center_name = center_text_span or center_text_bold

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
                    details = get_details(current_details)
                    details["Center Name"] = current_center
                    rehab_centers.append(details)

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
        details = get_details(current_details)
        details["Center Name"] = current_center
        rehab_centers.append(details)

    print(rehab_centers)
    df = pd.DataFrame(rehab_centers)

    df = df[["Center Name", "Website", "City", "Email", "Phone", "Details"]]

    # Save to CSV
    df.to_csv("rehabilitation_centers.csv", index=False)

    print("Data extracted and saved successfully!")


extract_data()
