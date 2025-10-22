import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import csv
import json
from datetime import datetime

class ActivewearCrawler:
    """
    Comprehensive crawler for Kica, BlissClub, SilverTraq, and Terra-active
    Extracts product details with focus on Fabric Details
    """

    def __init__(self, headless=True):
        """Initialize the crawler with Selenium WebDriver"""
        self.chrome_options = Options()
        if headless:
            self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

        self.results = []

    def init_driver(self):
        """Initialize Chrome WebDriver"""
        return webdriver.Chrome(options=self.chrome_options)

    # ==================== KICA ACTIVE ====================
    def crawl_kica(self):
        """Crawl all products from Kica Active"""
        print("\n=== Starting Kica Active Crawl ===")

        categories = [
            "https://kicaactive.com/collections/all",
            "https://kicaactive.com/collections/sports-bras",
            "https://kicaactive.com/collections/leggings",
            "https://kicaactive.com/collections/tops",
            "https://kicaactive.com/collections/flare-pants",
            "https://kicaactive.com/collections/shorts",
            "https://kicaactive.com/collections/tracks",
            "https://kicaactive.com/collections/co-ord-sets"
        ]

        driver = self.init_driver()

        try:
            for category_url in categories:
                print(f"\nCrawling category: {category_url}")
                driver.get(category_url)
                time.sleep(3)

                # Scroll to load all products
                for _ in range(3):
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)

                soup = BeautifulSoup(driver.page_source, 'html.parser')

                # Find all product links
                product_links = []
                product_cards = soup.find_all('a', class_='product-card')
                if not product_cards:
                    product_cards = soup.find_all('a', href=lambda x: x and '/products/' in str(x))

                for card in product_cards:
                    href = card.get('href', '')
                    if href and '/products/' in href:
                        full_url = f"https://kicaactive.com{href}" if not href.startswith('http') else href
                        if full_url not in product_links:
                            product_links.append(full_url)

                print(f"Found {len(product_links)} products in this category")

                # Crawl each product
                for product_url in product_links[:5]:  # Limit for testing, remove [:5] for full crawl
                    self.crawl_kica_product(driver, product_url)
                    time.sleep(1)

        finally:
            driver.quit()

    def crawl_kica_product(self, driver, url):
        """Extract product details from Kica product page"""
        try:
            driver.get(url)
            time.sleep(2)

            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Extract product name
            product_name = soup.find('h1', class_='product-title')
            if not product_name:
                product_name = soup.find('h1')
            product_name = product_name.text.strip() if product_name else "N/A"

            # Extract price
            price = soup.find('span', class_='price')
            if not price:
                price = soup.find('span', class_='money')
            price_text = price.text.strip() if price else "N/A"

            # Extract fabric details - CRITICAL SECTION
            fabric_details = "N/A"

            # Method 1: Look for "Fabric" or "Material" headings
            fabric_section = soup.find(text=lambda x: x and ('fabric' in x.lower() or 'material' in x.lower()))
            if fabric_section:
                parent = fabric_section.find_parent()
                if parent:
                    # Get next siblings or children
                    details_list = parent.find_next('ul') or parent.find_next('div')
                    if details_list:
                        fabric_details = details_list.get_text(separator=" | ", strip=True)

            # Method 2: Check product description for fabric info
            if fabric_details == "N/A":
                description = soup.find('div', class_='product-description')
                if description:
                    desc_text = description.get_text()
                    # Look for fabric percentages
                    import re
                    fabric_match = re.search(r'(\d+%.*?(?:cotton|polyester|nylon|spandex|elastane).*?)(?:\.|\n)', desc_text, re.IGNORECASE)
                    if fabric_match:
                        fabric_details = fabric_match.group(1).strip()

            # Extract other details
            description = soup.find('div', class_='product-description')
            description_text = description.get_text(strip=True) if description else "N/A"

            # Store result
            product_data = {
                "Brand": "Kica Active",
                "Product Name": product_name,
                "Price": price_text,
                "Fabric Details": fabric_details,
                "Description": description_text[:200],  # First 200 chars
                "URL": url,
                "Crawled At": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            self.results.append(product_data)
            print(f"✓ Extracted: {product_name}")

        except Exception as e:
            print(f"✗ Error crawling {url}: {str(e)}")

    # ==================== BLISSCLUB ====================
    def crawl_blissclub(self):
        """Crawl all products from BlissClub"""
        print("\n=== Starting BlissClub Crawl ===")

        categories = [
            "https://blissclub.com/collections/all",
            "https://blissclub.com/collections/sports-bras",
            "https://blissclub.com/collections/leggings",
            "https://blissclub.com/collections/tops",
            "https://blissclub.com/collections/shorts",
            "https://blissclub.com/collections/undies"
        ]

        driver = self.init_driver()

        try:
            for category_url in categories:
                print(f"\nCrawling category: {category_url}")
                driver.get(category_url)
                time.sleep(3)

                # Scroll to load products
                for _ in range(3):
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)

                soup = BeautifulSoup(driver.page_source, 'html.parser')

                # Find product links
                product_links = []
                product_cards = soup.find_all('a', href=lambda x: x and '/products/' in str(x))

                for card in product_cards:
                    href = card.get('href', '')
                    if href and '/products/' in href:
                        full_url = f"https://blissclub.com{href}" if not href.startswith('http') else href
                        if full_url not in product_links:
                            product_links.append(full_url)

                print(f"Found {len(product_links)} products in this category")

                # Crawl each product
                for product_url in product_links[:5]:  # Limit for testing
                    self.crawl_blissclub_product(driver, product_url)
                    time.sleep(1)

        finally:
            driver.quit()

    def crawl_blissclub_product(self, driver, url):
        """Extract product details from BlissClub product page"""
        try:
            driver.get(url)
            time.sleep(2)

            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Extract product name
            product_name = soup.find('h1')
            product_name = product_name.text.strip() if product_name else "N/A"

            # Extract price
            price = soup.find('span', class_='price') or soup.find('span', class_='money')
            price_text = price.text.strip() if price else "N/A"

            # Extract fabric details - CRITICAL SECTION
            fabric_details = "N/A"

            # BlissClub typically has "FABRIC DETAILS" section
            fabric_heading = soup.find(text=lambda x: x and 'fabric details' in x.lower())
            if fabric_heading:
                parent = fabric_heading.find_parent()
                # Look for list or div containing fabric info
                fabric_list = parent.find_next('ul') or parent.find_next_sibling()
                if fabric_list:
                    fabric_items = fabric_list.find_all('li') if fabric_list.name == 'ul' else [fabric_list]
                    fabric_details = " | ".join([item.get_text(strip=True) for item in fabric_items])

            # Alternative: Check for accordion or tab content
            if fabric_details == "N/A":
                accordion_items = soup.find_all('div', class_=lambda x: x and ('accordion' in str(x).lower() or 'tab' in str(x).lower()))
                for item in accordion_items:
                    text = item.get_text()
                    if 'fabric' in text.lower():
                        fabric_details = item.get_text(separator=" | ", strip=True)
                        break

            description = soup.find('div', class_=lambda x: x and 'description' in str(x).lower())
            description_text = description.get_text(strip=True) if description else "N/A"

            product_data = {
                "Brand": "BlissClub",
                "Product Name": product_name,
                "Price": price_text,
                "Fabric Details": fabric_details,
                "Description": description_text[:200],
                "URL": url,
                "Crawled At": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            self.results.append(product_data)
            print(f"✓ Extracted: {product_name}")

        except Exception as e:
            print(f"✗ Error crawling {url}: {str(e)}")

    # ==================== SILVERTRAQ ====================
    def crawl_silvertraq(self):
        """Crawl all products from SilverTraq"""
        print("\n=== Starting SilverTraq Crawl ===")

        categories = [
            "https://www.silvertraq.com/collections/all",
            "https://www.silvertraq.com/collections/sports-bras",
            "https://www.silvertraq.com/collections/leggings",
            "https://www.silvertraq.com/collections/tops",
            "https://www.silvertraq.com/collections/jackets",
            "https://www.silvertraq.com/collections/shorts"
        ]

        driver = self.init_driver()

        try:
            for category_url in categories:
                print(f"\nCrawling category: {category_url}")
                driver.get(category_url)
                time.sleep(3)

                # Scroll to load products
                for _ in range(3):
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)

                soup = BeautifulSoup(driver.page_source, 'html.parser')

                # Find product links
                product_links = []
                product_cards = soup.find_all('a', href=lambda x: x and '/products/' in str(x))

                for card in product_cards:
                    href = card.get('href', '')
                    if href and '/products/' in href:
                        full_url = f"https://www.silvertraq.com{href}" if not href.startswith('http') else href
                        if full_url not in product_links:
                            product_links.append(full_url)

                print(f"Found {len(product_links)} products in this category")

                # Crawl each product
                for product_url in product_links[:5]:  # Limit for testing
                    self.crawl_silvertraq_product(driver, product_url)
                    time.sleep(1)

        finally:
            driver.quit()

    def crawl_silvertraq_product(self, driver, url):
        """Extract product details from SilverTraq product page"""
        try:
            driver.get(url)
            time.sleep(2)

            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Extract product name
            product_name = soup.find('h1')
            product_name = product_name.text.strip() if product_name else "N/A"

            # Extract price
            price = soup.find('span', class_='price') or soup.find('span', class_='money')
            price_text = price.text.strip() if price else "N/A"

            # Extract fabric details
            fabric_details = "N/A"

            # Look for fabric/material section
            fabric_section = soup.find(text=lambda x: x and ('fabric' in x.lower() or 'material' in x.lower() or 'composition' in x.lower()))
            if fabric_section:
                parent = fabric_section.find_parent()
                details = parent.find_next('ul') or parent.find_next('div')
                if details:
                    fabric_details = details.get_text(separator=" | ", strip=True)

            description = soup.find('div', class_=lambda x: x and 'description' in str(x).lower())
            description_text = description.get_text(strip=True) if description else "N/A"

            product_data = {
                "Brand": "SilverTraq",
                "Product Name": product_name,
                "Price": price_text,
                "Fabric Details": fabric_details,
                "Description": description_text[:200],
                "URL": url,
                "Crawled At": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            self.results.append(product_data)
            print(f"✓ Extracted: {product_name}")

        except Exception as e:
            print(f"✗ Error crawling {url}: {str(e)}")

    # ==================== TERRA-ACTIVE ====================
    def crawl_terractive(self):
        """Crawl all products from Terra-active"""
        print("\n=== Starting Terra-active Crawl ===")

        categories = [
            "https://terractive.in/collections/all",
            "https://terractive.in/collections/tees",
            "https://terractive.in/collections/bottoms",
            "https://terractive.in/collections/women",
            "https://terractive.in/collections/men"
        ]

        driver = self.init_driver()

        try:
            for category_url in categories:
                print(f"\nCrawling category: {category_url}")
                driver.get(category_url)
                time.sleep(3)

                # Scroll to load products
                for _ in range(3):
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)

                soup = BeautifulSoup(driver.page_source, 'html.parser')

                # Find product links
                product_links = []
                product_cards = soup.find_all('a', href=lambda x: x and '/products/' in str(x))

                for card in product_cards:
                    href = card.get('href', '')
                    if href and '/products/' in href:
                        full_url = f"https://terractive.in{href}" if not href.startswith('http') else href
                        if full_url not in product_links:
                            product_links.append(full_url)

                print(f"Found {len(product_links)} products in this category")

                # Crawl each product
                for product_url in product_links[:5]:  # Limit for testing
                    self.crawl_terractive_product(driver, product_url)
                    time.sleep(1)

        finally:
            driver.quit()

    def crawl_terractive_product(self, driver, url):
        """Extract product details from Terra-active product page"""
        try:
            driver.get(url)
            time.sleep(2)

            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Extract product name
            product_name = soup.find('h1')
            product_name = product_name.text.strip() if product_name else "N/A"

            # Extract price
            price = soup.find('span', class_='price') or soup.find('span', class_='money')
            price_text = price.text.strip() if price else "N/A"

            # Extract fabric details - Terra-active emphasizes their TerraSoft fabric
            fabric_details = "N/A"

            # Look for fabric section
            fabric_section = soup.find(text=lambda x: x and ('fabric' in x.lower() or 'terrasoft' in x.lower() or 'material' in x.lower()))
            if fabric_section:
                parent = fabric_section.find_parent()
                details = parent.find_next('ul') or parent.find_next('div')
                if details:
                    fabric_details = details.get_text(separator=" | ", strip=True)

            description = soup.find('div', class_=lambda x: x and 'description' in str(x).lower())
            description_text = description.get_text(strip=True) if description else "N/A"

            product_data = {
                "Brand": "Terra-active",
                "Product Name": product_name,
                "Price": price_text,
                "Fabric Details": fabric_details,
                "Description": description_text[:200],
                "URL": url,
                "Crawled At": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            self.results.append(product_data)
            print(f"✓ Extracted: {product_name}")

        except Exception as e:
            print(f"✗ Error crawling {url}: {str(e)}")

    # ==================== EXPORT METHODS ====================
    def export_to_csv(self, filename="activewear_products.csv"):
        """Export results to CSV"""
        if not self.results:
            print("No results to export")
            return

        keys = self.results[0].keys()
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(self.results)

        print(f"\n✓ Exported {len(self.results)} products to {filename}")

    def export_to_json(self, filename="activewear_products.json"):
        """Export results to JSON"""
        if not self.results:
            print("No results to export")
            return

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)

        print(f"✓ Exported {len(self.results)} products to {filename}")

    def run_full_crawl(self):
        """Run complete crawl for all brands"""
        print("="*60)
        print("ACTIVEWEAR CRAWLER - FABRIC DETAILS EXTRACTOR")
        print("="*60)

        # Crawl all brands
        self.crawl_kica()
        self.crawl_blissclub()
        self.crawl_silvertraq()
        self.crawl_terractive()

        # Export results
        self.export_to_csv()
        self.export_to_json()

        print(f"\n{'='*60}")
        print(f"CRAWL COMPLETE - Total Products: {len(self.results)}")
        print(f"{'='*60}")


# ==================== MAIN EXECUTION ====================
if __name__ == "__main__":
    # Initialize crawler
    crawler = ActivewearCrawler(headless=True)

    # Run full crawl
    crawler.run_full_crawl()

    # Optional: Run individual brand crawls
    # crawler.crawl_kica()
    # crawler.crawl_blissclub()
    # crawler.crawl_silvertraq()
    # crawler.crawl_terractive()
    # crawler.export_to_csv()
