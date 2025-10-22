"""
Advanced Configuration for Activewear Crawler
Fast, full-site crawling for all products; CSV output enabled
"""

# ==================== CRAWL SETTINGS ====================
CRAWL_CONFIG = {
    'page_load_delay': 0.5,      # Minimal wait for page loads (adjust if you get rate-limited)
    'between_products_delay': 0.05,   # As fast as practical between products
    'scroll_delay': 0.15,        # Minimal delay between scrolls
    'scroll_iterations': 1,      # Only 1 scroll to speed up crawling
    'max_products_per_category': None, # No product limit, crawl all!
    'headless': True,            # Headless browser for best performance
    'window_size': '1920,1080',
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
}

# ==================== BRAND CONFIGURATIONS ====================
KICA_CONFIG = {
    'base_url': 'https://kicaactive.com',
    'categories': [
        '/collections/all',
        '/collections/sports-bras',
        '/collections/leggings',
        '/collections/tops',
        '/collections/flare-pants',
        '/collections/shorts',
        '/collections/tracks',
        '/collections/co-ord-sets',
        '/collections/sports-tanks',
    ],
    'product_selectors': {
        'product_link': 'a[href*="/products/"]',
        'product_name': 'h1.product-title, h1',
        'price': 'span.price, span.money',
        'description': 'div.product-description',
        'fabric_keywords': ['fabric', 'material', 'composition', 'blend'],
    }
}

BLISSCLUB_CONFIG = {
    'base_url': 'https://blissclub.com',
    'categories': [
        '/collections/all',
        '/collections/sports-bras',
        '/collections/leggings',
        '/collections/tops',
        '/collections/shorts',
        '/collections/undies',
        '/collections/joggers',
        '/collections/jackets',
    ],
    'product_selectors': {
        'product_link': 'a[href*="/products/"]',
        'product_name': 'h1',
        'price': 'span.price, span.money',
        'description': 'div[class*="description"]',
        'fabric_keywords': ['fabric details', 'material', 'composition'],
    }
}

SILVERTRAQ_CONFIG = {
    'base_url': 'https://www.silvertraq.com',
    'categories': [
        '/collections/all',
        '/collections/sports-bras',
        '/collections/leggings',
        '/collections/tops',
        '/collections/jackets',
        '/collections/shorts',
        '/collections/co-ord-sets',
    ],
    'product_selectors': {
        'product_link': 'a[href*="/products/"]',
        'product_name': 'h1',
        'price': 'span.price, span.money',
        'description': 'div[class*="description"]',
        'fabric_keywords': ['fabric', 'material', 'traqtech', 'composition'],
    }
}

TERRACTIVE_CONFIG = {
    'base_url': 'https://terractive.in',
    'categories': [
        '/collections/all',
        '/collections/tees',
        '/collections/bottoms',
        '/collections/women',
        '/collections/men',
        '/collections/terrasoft',
    ],
    'product_selectors': {
        'product_link': 'a[href*="/products/"]',
        'product_name': 'h1',
        'price': 'span.price, span.money',
        'description': 'div[class*="description"]',
        'fabric_keywords': ['fabric', 'terrasoft', 'material', 'composition'],
    }
}

# ==================== EXPORT SETTINGS ====================
EXPORT_CONFIG = {
    'csv_filename': 'activewear_output_download.csv',  # Clear filename for downloading
    'json_filename': 'activewear_output_download.json',
    'include_timestamp': True,
    'csv_encoding': 'utf-8',
    'json_indent': 2,
}


# ==================== FABRIC EXTRACTION PATTERNS ====================
FABRIC_PATTERNS = [
    # Percentage-based patterns
    r'(\d+%\s*[a-zA-Z]+(?:\s*[a-zA-Z]+)?)',        # e.g., "79% Nylon"
    # Comma-separated patterns
    r'([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)?(?:,\s*[A-Z][a-zA-Z]+)*)', # e.g., "Nylon, Spandex"
    # Fabric property patterns
    r'(moisture[- ]wicking|quick[- ]dry|breathable|stretchy)',
]

# ==================== OUTPUT FIELDS ====================
OUTPUT_FIELDS = [
    'Brand',
    'Product Name',
    'Price',
    'Fabric Details',  # CRITICAL FIELD
    'Description',
    'URL',
    'Crawled At',
]
