#!/usr/bin/env python3
"""
Quick Start Script for Activewear Crawler
Run this file directly in VS Code to start crawling
"""

from activewear_crawler import ActivewearCrawler
import sys

def main():
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║        ACTIVEWEAR CRAWLER - FABRIC DETAILS EXTRACTOR         ║
    ║                                                              ║
    ║  Crawls: Kica, BlissClub, SilverTraq, Terra-active          ║
    ║  Focus: FABRIC DETAILS + Product Information                ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

    print("\nSelect crawl mode:")
    print("1. Full Crawl (All brands, all categories) - RECOMMENDED")
    print("2. Kica Active only")
    print("3. BlissClub only")
    print("4. SilverTraq only")
    print("5. Terra-active only")
    print("6. Custom selection")
    print("0. Exit")

    try:
        choice = input("\nEnter your choice (0-6): ").strip()

        if choice == "0":
            print("\nExiting...")
            sys.exit(0)

        # Initialize crawler
        print("\nInitializing crawler...")
        crawler = ActivewearCrawler(headless=True)

        if choice == "1":
            print("\n🚀 Starting FULL CRAWL...")
            crawler.run_full_crawl()

        elif choice == "2":
            print("\n🚀 Crawling Kica Active...")
            crawler.crawl_kica()
            crawler.export_to_csv("kica_products.csv")
            crawler.export_to_json("kica_products.json")

        elif choice == "3":
            print("\n🚀 Crawling BlissClub...")
            crawler.crawl_blissclub()
            crawler.export_to_csv("blissclub_products.csv")
            crawler.export_to_json("blissclub_products.json")

        elif choice == "4":
            print("\n🚀 Crawling SilverTraq...")
            crawler.crawl_silvertraq()
            crawler.export_to_csv("silvertraq_products.csv")
            crawler.export_to_json("silvertraq_products.json")

        elif choice == "5":
            print("\n🚀 Crawling Terra-active...")
            crawler.crawl_terractive()
            crawler.export_to_csv("terractive_products.csv")
            crawler.export_to_json("terractive_products.json")

        elif choice == "6":
            print("\n📋 Custom Selection:")
            brands = []

            if input("Crawl Kica? (y/n): ").lower() == 'y':
                brands.append('kica')
            if input("Crawl BlissClub? (y/n): ").lower() == 'y':
                brands.append('blissclub')
            if input("Crawl SilverTraq? (y/n): ").lower() == 'y':
                brands.append('silvertraq')
            if input("Crawl Terra-active? (y/n): ").lower() == 'y':
                brands.append('terractive')

            if not brands:
                print("\n⚠️  No brands selected!")
                return

            print(f"\n🚀 Starting crawl for: {', '.join(brands)}")

            for brand in brands:
                if brand == 'kica':
                    crawler.crawl_kica()
                elif brand == 'blissclub':
                    crawler.crawl_blissclub()
                elif brand == 'silvertraq':
                    crawler.crawl_silvertraq()
                elif brand == 'terractive':
                    crawler.crawl_terractive()

            crawler.export_to_csv("custom_products.csv")
            crawler.export_to_json("custom_products.json")

        else:
            print("\n⚠️  Invalid choice!")
            return

        print("\n" + "="*60)
        print("✅ CRAWL COMPLETED SUCCESSFULLY!")
        print(f"📊 Total products extracted: {len(crawler.results)}")
        print("📁 Check your output files for results")
        print("="*60)

    except KeyboardInterrupt:
        print("\n\n⚠️  Crawl interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error occurred: {str(e)}")
        print("\nPlease check:")
        print("- Chrome and ChromeDriver are installed")
        print("- Internet connection is stable")
        print("- Required packages are installed (see README)")
        sys.exit(1)

if __name__ == "__main__":
    main()
