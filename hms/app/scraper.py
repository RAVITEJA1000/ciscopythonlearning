import requests
from bs4 import BeautifulSoup
import json
import os

# URL of the WHO health topics page
url = 'https://www.who.int/health-topics/'

# Function to extract disease information from the page
def extract_diseases(soup):
    diseases_list = []
    # Find the main content area with health topics
    content = soup.find('div', class_='list-view--item')
    if not content:
        print("Disease content not found.")
        return diseases_list

    # Find all disease entries (links to health topics)
    disease_entries = content.find_all('a', class_='link-container')
    for entry in disease_entries[:10]:  # Limit to first 10 entries to avoid excessive data
        disease_name = entry.get_text(strip=True)
        # Check if the entry has a valid href to a disease-specific page
        disease_url = entry.get('href')
        if disease_name and disease_url:
            # Basic validation to ensure it's a valid disease link
            if disease_name and not disease_name.startswith(('See all', 'More', 'View all')):
                try:
                    # Fetch a brief description from the disease-specific page
                    full_url = disease_url if disease_url.startswith('http') else f'https://www.who.int{disease_url}'
                    response = requests.get(full_url, timeout=10)
                    response.raise_for_status()
                    disease_soup = BeautifulSoup(response.content, 'html.parser')
                    # Look for a description paragraph (adjust selector as needed)
                    description_elem = disease_soup.find('div', class_='sf-content-block')
                    description = description_elem.get_text(strip=True)[:200] + '...' if description_elem else 'No description available.'
                    disease_data = {
                        'disease': disease_name,
                        'description': description,
                        'source': 'WHO Health Topics',
                        'url': full_url
                    }
                    diseases_list.append(disease_data)
                except (requests.RequestException, ValueError) as e:
                    print(f"Error fetching details for {disease_name}: {e}")
                    # Add entry with minimal data if detailed fetch fails
                    diseases_list.append({
                        'disease': disease_name,
                        'description': 'No description available.',
                        'source': 'WHO Health Topics',
                        'url': full_url
                    })
    return diseases_list

# Function to scrape disease information and save to JSON
def scrape():
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        diseases_list = extract_diseases(soup)
        
        # Ensure directory exists
        os.makedirs('./patient_app', exist_ok=True)
        
        # Save the data to a JSON file
        file_path = "./patient_app/scraped_diseases.json"
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(diseases_list, json_file, ensure_ascii=False, indent=4)
        
        print(f"Data saved to {file_path}")
        print(f"Extracted {len(diseases_list)} disease entries.")
    
    except requests.RequestException as e:
        print(f"Error fetching page: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    scrape()