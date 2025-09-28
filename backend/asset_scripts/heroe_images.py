import requests
import os


links = ["https://assets-bucket.deadlock-api.com/assets-api-res/images/heroes/astro_sm.png", 
         "https://assets-bucket.deadlock-api.com/assets-api-res/images/heroes/bull_sm.png",
         "https://assets-bucket.deadlock-api.com/assets-api-res/images/heroes/inferno/icon_sm.png",
         "https://assets-bucket.deadlock-api.com/assets-api-res/images/heroes/victor/icon_sm.png",
         "https://assets-bucket.deadlock-api.com/assets-api-res/images/heroes/bookworm_sm.png",
         "https://assets-bucket.deadlock-api.com/assets-api-res/images/heroes/tengu_sm.png",
         "https://assets-bucket.deadlock-api.com/assets-api-res/images/heroes/doorman_sm.png",
         "https://assets-bucket.deadlock-api.com/assets-api-res/images/heroes/vampirebat_sm.png",
         "https://assets-bucket.deadlock-api.com/assets-api-res/images/heroes/gigawatt_sm.png",
         "https://assets-bucket.deadlock-api.com/assets-api-res/images/heroes/magician_sm.png",
         "https://assets-bucket.deadlock-api.com/assets-api-res/images/heroes/archer_sm.png",
         "https://assets-bucket.deadlock-api.com/assets-api-res/images/heroes/synth_sm.png",
         "https://assets-bucket.deadlock-api.com/assets-api-res/images/heroes/engineer_sm.png",
         "https://assets-bucket.deadlock-api.com/assets-api-res/images/heroes/digger_sm.png",
         "https://assets-bucket.deadlock-api.com/assets-api-res/images/heroes/spectre_sm.png",
         "https://assets-bucket.deadlock-api.com/assets-api-res/images/heroes/nano_sm.png",
         "https://assets-bucket.deadlock-api.com/assets-api-res/images/heroes/chrono_sm.png"
        ]



# --- Configuration ---
# The API endpoint to get the list of all heroes
HERO_API_URL = "https://assets.deadlock-api.com/v2/heroes"

# The folder where images will be saved, relative to the backend directory
OUTPUT_FOLDER = "assets_hero_images"

# --- Script ---

def download_hero_images():

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    for link in links:
        try:
            # Extract the filename from the end of the URL
            # e.g., "astro.png" from ".../astro.png"
            filename = link.split('/')[-1]
            
            # Construct the full path to save the file
            output_path = os.path.join(OUTPUT_FOLDER, filename)
            # Get the image data
            image_response = requests.get(link)
            image_response.raise_for_status()

            # Save the image to the file in binary write mode
            with open(output_path, 'wb') as f:
                f.write(image_response.content)
            
            print(f"  - Successfully downloaded sm.png")

        except requests.exceptions.RequestException as e:
            print(f"  - Failed to download image. Error: {e}")

    print("\nDownload process finished.")

if __name__ == "__main__":
    download_hero_images()