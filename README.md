# 🏡 Immovlan Scraper

A robust Scrapy project to extract detailed real-estate property data from immovlan.be. This repository acts as a scraping helper tool to produce principal property data from project links that have been obtained previously. The associated analysis repo can be found here: <https://github.com/Hamideh-B-H/immo-eliza-team-horses-analysis>

---

## 📁 Project Structure
```markdown
immovlan-scraper-project/
│
├── logs/
│  ├── immovlan.log
│  └── scrapy.log
│
├── output/
│  ├── error_output.csv
│  ├── properties_data.csv
│  └── test_data.csv
│
├── src/
│  ├── spiders/
│  │ ├── __init__.py
│  │ └── immovlan_spider.py
│  │
│  ├── __init__.py
│  ├── items.py
│  ├── middlewares.py
│  ├── pipelines.py
│  └── settings.py
│
├── project_urls.csv
├── README.md
├── requirements.txt
└── scrapy.cfg
```

---

## ⚙️ Installation

```bash
pip install -r requirements.txt
```

---

## 🚀 Usage
1. Prepare a text file containing your project URLs (one per line). Example: start_urls.txt
2. Run the spider:
```bash
scrapy crawl immovlan -o output/properties_data.csv
```
3. To test only a few records:
```bash
scrapy crawl immovlan -a limit=10 -o output/test_data.csv
```

--- 

## 📊 Output
- All extracted data → output/properties_data.csv
- Failed requests → output/error_output.csv
- Test data → output/test_data.csv
- Logs → logs/immovlan_spider.log
- Logs → logs/scrapy.log

--- 

## 🧠 Notes
- Missing fields are written as None.
- The scraper respects robots.txt and polite crawling delays.
- Easily extendable for new fields or output formats.

