import requests
import os
import hashlib
import mimetypes
from urllib.parse import urlparse
from typing import List, Optional
import time

class UbuntuImageFetcher:
    """
    Ubuntu Image Fetcher - A tool for mindfully collecting images from the web
    Embodying the Ubuntu philosophy: "I am because we are"
    """
    
    def __init__(self, directory: str = "Fetched_Images"):
        self.directory = directory
        self.downloaded_hashes = set()
        self.session = requests.Session()
        # Set a respectful user agent
        self.session.headers.update({
            'User-Agent': 'Ubuntu-Image-Fetcher/1.0 (Educational Tool; Respectful Community Member)'
        })
        
        # Create directory if it doesn't exist
        os.makedirs(self.directory, exist_ok=True)
        
        # Load existing image hashes to prevent duplicates
        self._load_existing_hashes()
    
    def _load_existing_hashes(self) -> None:
        """Load hashes of existing images to prevent duplicates"""
        try:
            for filename in os.listdir(self.directory):
                filepath = os.path.join(self.directory, filename)
                if os.path.isfile(filepath):
                    with open(filepath, 'rb') as f:
                        content = f.read()
                        file_hash = hashlib.md5(content).hexdigest()
                        self.downloaded_hashes.add(file_hash)
        except Exception as e:
            print(f"Note: Could not load existing hashes: {e}")
    
    def _get_content_info(self, response: requests.Response) -> tuple:
        """Extract content information from response headers"""
        content_type = response.headers.get('content-type', '').lower()
        content_length = response.headers.get('content-length')
        
        # Check if it's actually an image
        if not content_type.startswith('image/'):
            print(f"Warning: Content type is '{content_type}', not an image")
        
        # Check file size (be respectful of bandwidth)
        if content_length:
            size_mb = int(content_length) / (1024 * 1024)
            if size_mb > 10:  # 10MB limit
                raise ValueError(f"Image too large: {size_mb:.1f}MB (limit: 10MB)")
            print(f"Image size: {size_mb:.2f}MB")
        
        return content_type, content_length
    
    def _generate_filename(self, url: str, content_type: str) -> str:
        """Generate appropriate filename from URL or content type"""
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        
        # If no filename in URL, generate one
        if not filename or '.' not in filename:
            # Get extension from content type
            extension = mimetypes.guess_extension(content_type) or '.jpg'
            # Use domain name and timestamp for filename
            domain = parsed_url.netloc.replace('www.', '')
            timestamp = int(time.time())
            filename = f"{domain}_{timestamp}{extension}"
        
        # Sanitize filename
        filename = "".join(c for c in filename if c.isalnum() or c in '._-')
        return filename
    
    def _is_duplicate(self, content: bytes) -> bool:
        """Check if image content is a duplicate"""
        content_hash = hashlib.md5(content).hexdigest()
        if content_hash in self.downloaded_hashes:
            return True
        self.downloaded_hashes.add(content_hash)
        return False
    
    def fetch_image(self, url: str) -> bool:
        """
        Fetch a single image from URL with Ubuntu principles:
        - Community: Connect respectfully to web resources
        - Respect: Handle errors gracefully, check content appropriately
        - Sharing: Organize for community benefit
        """
        try:
            print(f"🌍 Connecting to: {url}")
            
            # Make request with timeout and error handling
            response = self.session.get(url, timeout=15, stream=True)
            response.raise_for_status()
            
            # Check content information
            content_type, content_length = self._get_content_info(response)
            
            # Get the actual content
            content = response.content
            
            # Check for duplicates
            if self._is_duplicate(content):
                print("⚠️  Image already exists (duplicate detected)")
                return False
            
            # Generate appropriate filename
            filename = self._generate_filename(url, content_type)
            filepath = os.path.join(self.directory, filename)
            
            # Ensure unique filename if file exists
            counter = 1
            original_filepath = filepath
            while os.path.exists(filepath):
                name, ext = os.path.splitext(original_filepath)
                filepath = f"{name}_{counter}{ext}"
                counter += 1
            
            # Save the image
            with open(filepath, 'wb') as f:
                f.write(content)
            
            print(f"✓ Successfully fetched: {os.path.basename(filepath)}")
            print(f"✓ Image saved to {filepath}")
            return True
            
        except requests.exceptions.Timeout:
            print("✗ Connection timeout - the server didn't respond in time")
            return False
        except requests.exceptions.ConnectionError:
            print("✗ Connection error - could not reach the server")
            return False
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print("✗ Image not found (404)")
            elif e.response.status_code == 403:
                print("✗ Access forbidden (403) - server declined our request")
            else:
                print(f"✗ HTTP error: {e.response.status_code}")
            return False
        except ValueError as e:
            print(f"✗ {e}")
            return False
        except Exception as e:
            print(f"✗ An unexpected error occurred: {e}")
            return False
    
    def fetch_multiple_images(self, urls: List[str]) -> dict:
        """Fetch multiple images with progress tracking"""
        results = {"successful": 0, "failed": 0, "duplicates": 0}
        
        print(f"🎯 Preparing to fetch {len(urls)} images...")
        print("=" * 50)
        
        for i, url in enumerate(urls, 1):
            print(f"\n[{i}/{len(urls)}] Processing:")
            success = self.fetch_image(url)
            
            if success:
                results["successful"] += 1
            else:
                results["failed"] += 1
            
            # Be respectful - small delay between requests
            if i < len(urls):
                time.sleep(1)
        
        return results
    
    def display_summary(self, results: dict) -> None:
        """Display summary in Ubuntu spirit"""
        print("\n" + "=" * 50)
        print("📊 UBUNTU IMAGE FETCHER SUMMARY")
        print("=" * 50)
        print(f"✅ Successfully fetched: {results['successful']}")
        print(f"❌ Failed attempts: {results['failed']}")
        print(f"📁 Images stored in: {self.directory}/")
        
        total_files = len([f for f in os.listdir(self.directory) 
                        if os.path.isfile(os.path.join(self.directory, f))])
        print(f"📚 Total images in collection: {total_files}")
        
        print("\n🌍 Connection strengthened. Community enriched.")
        print("💭 \"I am because we are\" - Ubuntu Philosophy")

def main():
    """Main function demonstrating Ubuntu principles"""
    print("🌍 UBUNTU IMAGE FETCHER")
    print("A tool for mindfully collecting images from the web")
    print("Guided by Ubuntu: \"I am because we are\"")
    print("=" * 55)
    
    fetcher = UbuntuImageFetcher()
    
    # Get input from user
    print("\nChoose an option:")
    print("1. Fetch a single image")
    print("2. Fetch multiple images")
    
    try:
        choice = input("\nEnter your choice (1 or 2): ").strip()
        
        if choice == "1":
            url = input("\nPlease enter the image URL: ").strip()
            if url:
                success = fetcher.fetch_image(url)
                results = {"successful": 1 if success else 0, "failed": 0 if success else 1}
                fetcher.display_summary(results)
            else:
                print("✗ No URL provided")
                
        elif choice == "2":
            print("\nEnter image URLs (one per line, empty line to finish):")
            urls = []
            while True:
                url = input().strip()
                if not url:
                    break
                urls.append(url)
            
            if urls:
                results = fetcher.fetch_multiple_images(urls)
                fetcher.display_summary(results)
            else:
                print("✗ No URLs provided")
        else:
            print("✗ Invalid choice")
            
    except KeyboardInterrupt:
        print("\n\n🙏 Thank you for using Ubuntu Image Fetcher")
        print("Ubuntu reminds us: \"A person is a person through other persons\"")

# Security considerations and best practices
def security_recommendations():
    """
    Security considerations when downloading files:
    
    1. Validate URLs before processing
    2. Limit file sizes to prevent resource exhaustion
    3. Check content types to ensure they're actually images
    4. Use timeouts to prevent hanging connections
    5. Sanitize filenames to prevent directory traversal attacks
    6. Set appropriate User-Agent headers
    7. Consider virus scanning for production use
    8. Implement rate limiting to be respectful to servers
    9. Validate image content (not just headers) in production
    10. Use HTTPS when possible
    """
    pass

if __name__ == "__main__":
    main()