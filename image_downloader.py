import requests
import os
import hashlib
from urllib.parse import urlparse

VALID_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"]

def get_extension_from_content_type(content_type):
    """Map Content-Type header to a file extension."""
    mapping = {
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "image/gif": ".gif",
        "image/bmp": ".bmp",
        "image/webp": ".webp",
    }
    return mapping.get(content_type.lower(), ".jpg")  # Default to .jpg

def get_filename(url, content_type):
    """Extract filename or generate one with proper extension."""
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)

    # If filename is empty, generate one
    if not filename:
        filename = "downloaded_image.jpg"

    # Check if it already has a valid extension
        if not any(filename.lower().endswith(ext) for ext in VALID_EXTENSIONS):
            filename += get_extension_from_content_type(content_type)

    return filename

def file_already_exists(filepath, content):
    """Check if a file with the same content already exists."""
    if not os.path.exists(filepath):
        return False
    with open(filepath, "rb") as f:
        existing_content = f.read()
    return hashlib.sha256(existing_content).hexdigest() == hashlib.sha256(content).hexdigest()

def fetch_image(url):
    # Fetch and save an image from a URL, handling errors respectfully.
    try:
        # Fetch the image with a timeout
        headers = {"User-Agent": "UbuntuImageFetcher/1.0 (respectful bot)"}
        response = requests.get(url, timeout=10, headers=headers)
        response.raise_for_status()  # Raise exception for bad HTTP status

        # Verify it's an image
        content_type = response.headers.get("Content-Type", "")
        if "image" not in content_type.lower():
            print(f"✗ Skipped: {url} (Not an image)")
            return

        # Get proper filename with extension
        filename = get_filename(url, content_type)
        filepath = os.path.join("Fetched_Images", filename)

        # Prevent duplicates
        if file_already_exists(filepath, response.content):
            print(f"⚠ Duplicate skipped: {filename}")
            return

        # Save file
        with open(filepath, "wb") as f:
            f.write(response.content)

        print(f"✓ Successfully fetched: {filename}")
        print(f"✓ Image saved to {filepath}")

    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error: {e}")
    except Exception as e:
        print(f"✗ An error occurred: {e}")

def main():
    print("---ℹ️😁😁Welcome to the Ubuntu Image Fetcher---\n")
    print("A tool for mindfully🤔 collecting images from the web\n")

    # Create directory for images
    os.makedirs("Fetched_Images", exist_ok=True)

    # Get multiple URLs from user
    urls = input("Please enter image URLs (separated by spaces): ").split()

    for url in urls:
        fetch_image(url)

    print("\nConnection strengthened. Community enriched.")

if __name__ == "__main__":
    main()
