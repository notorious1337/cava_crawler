# cava_crawler
This is a personalised and customized crawling tool for the brand cava athleisure.
# Activewear Product Crawler with Fabric Details Extraction

A comprehensive Python-based web crawler designed to extract product information from Kica Active, BlissClub, SilverTraq, and Terra-active e-commerce websites, with a **critical focus on Fabric Details**.

## 🎯 Features

- **Multi-Brand Support**: Crawls all four major Indian activewear brands
- **Fabric Details Priority**: Specifically designed to extract fabric composition and details
- **All Categories**: Automatically crawls all product categories on each site
- **Comprehensive Data**: Extracts product name, price, fabric details, description, and URL
- **Export Options**: Saves data to both CSV and JSON formats
- **Error Handling**: Robust error handling to continue crawling even if individual products fail
- **Headless Mode**: Runs in background without opening browser windows

## 📋 Prerequisites

Before running the crawler, ensure you have:

1. **Python 3.7+** installed
2. **Google Chrome** browser installed
3. **ChromeDriver** matching your Chrome version

## 🔧 Installation

### Step 1: Install Required Libraries

Open your terminal/command prompt and run:

```bash
pip install requests
pip install beautifulsoup4
pip install selenium
pip install lxml
```

### Step 2: Download ChromeDriver

1. Check your Chrome version: Go to `chrome://settings/help` in Chrome
2. Download matching ChromeDriver from: https://chromedriver.chromium.org/downloads
3. Extract and place `chromedriver.exe` in your project folder OR add to system PATH

**For Windows:**
- Place `chromedriver.exe` in `C:\Windows\System32\` or your project folder

**For Mac/Linux:**
```bash
# Mac (using Homebrew)
brew install chromedriver

# Linux
sudo apt-get install chromium-chromedriver
```

### Step 3: Download the Crawler

Save the `activewear_crawler.py` file to your preferred directory.

## 🚀 Usage

### Basic Usage - Full Crawl (All Brands, All Categories)

```python
from activewear_crawler import ActivewearCrawler

# Initialize crawler
crawler = ActivewearCrawler(headless=True)

# Run complete crawl
crawler.run_full_crawl()
```

### Run in VS Code

1. Open VS Code
2. Open the folder containing `activewear_crawler.py`
3. Create a new file `run_crawler.py`:

```python
from activewear_crawler import ActivewearCrawler

# Initialize the crawler
crawler = ActivewearCrawler(headless=True)

# Run full crawl for all brands
crawler.run_full_crawl()

print("\nCrawling complete! Check activewear_products.csv for results.")
```

4. Press `F5` or click "Run Python File" in VS Code

### Individual Brand Crawls

```python
from activewear_crawler import ActivewearCrawler

crawler = ActivewearCrawler(headless=True)

# Crawl individual brands
crawler.crawl_kica()
crawler.crawl_blissclub()
crawler.crawl_silvertraq()
crawler.crawl_terractive()

# Export results
crawler.export_to_csv("my_products.csv")
crawler.export_to_json("my_products.json")
```

### Custom Configuration

```python
# Run with visible browser (for debugging)
crawler = ActivewearCrawler(headless=False)

# Customize crawl
crawler.crawl_kica()  # Only Kica
crawler.export_to_csv("kica_products.csv")
```

## 📊 Output Format

### CSV Output (`activewear_products.csv`)

| Brand | Product Name | Price | Fabric Details | Description | URL | Crawled At |
|-------|-------------|-------|----------------|-------------|-----|------------|
| Kica Active | High Impact Sports Bra | Rs. 1,299 | 79% Nylon, 21% Spandex | High support for... | https://... | 2025-10-22 18:50:00 |
| BlissClub | FreeDame AirUndie | Rs. 499 | Shell: 79% Nylon, 21% Spandex | Seamless comfort... | https://... | 2025-10-22 18:51:00 |

### JSON Output (`activewear_products.json`)

```json
[
  {
    "Brand": "Kica Active",
    "Product Name": "High Impact Sports Bra",
    "Price": "Rs. 1,299",
    "Fabric Details": "79% Nylon, 21% Spandex | Moisture-wicking | Quick-dry",
    "Description": "High support sports bra designed for intense workouts...",
    "URL": "https://kicaactive.com/products/...",
    "Crawled At": "2025-10-22 18:50:00"
  }
]
```

## 🗂️ Crawled Categories

### Kica Active
- All Products
- Sports Bras
- Leggings
- Tops
- Flare Pants
- Shorts
- Tracks
- Co-ord Sets

### BlissClub
- All Products
- Sports Bras
- Leggings
- Tops
- Shorts
- Undies

### SilverTraq
- All Products
- Sports Bras
- Leggings
- Tops
- Jackets
- Shorts

### Terra-active
- All Products
- Tees
- Bottoms
- Women's Collection
- Men's Collection

## ⚙️ Configuration Options

### Modify Product Limit (For Testing)

In the crawler code, find these lines in each `crawl_[brand]` method:

```python
for product_url in product_links[:5]:  # Limit for testing
```

Change `[:5]` to crawl more products:
- `[:10]` - First 10 products
- `[:50]` - First 50 products
- Remove `[:5]` completely to crawl ALL products

### Adjust Crawl Speed

Modify sleep times to speed up or slow down:

```python
time.sleep(2)  # Change to time.sleep(1) for faster crawling
```

**Note**: Too fast may trigger anti-bot protections!

## 🛠️ Troubleshooting

### Issue: "ChromeDriver not found"

**Solution:**
```python
# Specify ChromeDriver path directly
from selenium import webdriver

driver = webdriver.Chrome(executable_path="C:/path/to/chromedriver.exe")
```

### Issue: "Selenium WebDriver not loading"

**Solution:**
1. Update Selenium: `pip install --upgrade selenium`
2. Ensure ChromeDriver version matches Chrome browser version

### Issue: "No fabric details extracted"

**Solution:**
- Some products may not have fabric details listed
- Check the product page manually to verify
- Modify the fabric extraction logic in the respective `crawl_[brand]_product` method

### Issue: "Getting blocked by website"

**Solution:**
1. Increase sleep time between requests
2. Add random delays
3. Rotate user agents
4. Respect robots.txt

## 📝 Code Structure

```
activewear_crawler.py
│
├── ActivewearCrawler Class
│   ├── __init__() - Initialize crawler
│   ├── init_driver() - Setup Selenium driver
│   │
│   ├── Kica Methods
│   │   ├── crawl_kica() - Crawl all Kica categories
│   │   └── crawl_kica_product() - Extract individual product
│   │
│   ├── BlissClub Methods
│   │   ├── crawl_blissclub()
│   │   └── crawl_blissclub_product()
│   │
│   ├── SilverTraq Methods
│   │   ├── crawl_silvertraq()
│   │   └── crawl_silvertraq_product()
│   │
│   ├── Terra-active Methods
│   │   ├── crawl_terractive()
│   │   └── crawl_terractive_product()
│   │
│   └── Export Methods
│       ├── export_to_csv()
│       ├── export_to_json()
│       └── run_full_crawl()
```

## 🔍 Fabric Details Extraction Strategy

The crawler uses multiple strategies to extract fabric details:

1. **Direct Section Search**: Looks for headings containing "Fabric", "Material", or "Composition"
2. **List Extraction**: Extracts fabric info from `<ul>` or `<div>` elements
3. **Pattern Matching**: Uses regex to find fabric percentages (e.g., "79% Nylon")
4. **Accordion/Tab Search**: Checks collapsible sections and tabs
5. **Description Parsing**: Falls back to product description if dedicated section not found

## 📈 Performance

- **Average Speed**: ~3-5 seconds per product
- **Estimated Time**: 
  - 100 products: ~5-8 minutes
  - 500 products: ~25-40 minutes
  - 1000+ products: ~60-90 minutes

## 🚨 Important Notes

1. **Ethical Crawling**: 
   - Respect website terms of service
   - Implement rate limiting
   - Don't overload servers

2. **Legal Compliance**: 
   - Check robots.txt for each site
   - Use data responsibly
   - Don't use for commercial purposes without permission

3. **Maintenance**: 
   - Websites change their structure regularly
   - Update selectors if extraction fails
   - Test regularly to ensure functionality

## 🎓 Customization Examples

### Add More Categories

```python
def crawl_kica(self):
    categories = [
        # Add your custom category URLs
        "https://kicaactive.com/collections/new-arrivals",
        "https://kicaactive.com/collections/sale"
    ]
```

### Extract Additional Fields

```python
# In crawl_[brand]_product method, add:
size_options = soup.find_all('select', {'name': 'size'})
colors = soup.find_all('div', class_='color-swatch')

product_data['Sizes'] = [size.text for size in size_options]
product_data['Colors'] = [color.text for color in colors]
```

### Filter by Price Range

```python
# After extracting price
price_value = float(price_text.replace('Rs.', '').replace(',', '').strip())
if 500 <= price_value <= 2000:
    self.results.append(product_data)
```

## 📞 Support

If you encounter issues:
1. Check ChromeDriver compatibility
2. Verify Python package versions
3. Inspect website HTML structure (may have changed)
4. Check console errors for specific issues

## 📜 License

This crawler is for educational purposes only. Ensure you comply with each website's terms of service before use.

---

**Happy Crawling! 🕷️**
