# Tender Scraper Project

A web scraping tool to collect tender/procurement opportunities from various Asia-Pacific tender listing websites.

## Supported Sources

- **APAC Tenders** (apactenders.com)
- **BidsInfo**
- **Global Tenders**
- **Tender Impulse**

## Quick Start

### 1. Install Dependencies

```bash
cd tender-proj
pip install -r requirements.txt
```

Or use the Makefile:
```bash
make install
```

### 2. Run the Scraper

Open Jupyter Notebook:
```bash
jupyter notebook
```

Then navigate to the tender source you want to scrape:
- `apac_tenders/web-scrap.ipynb`
- `bidsInfo/web-scrap.ipynb`
- `global_tenders/web-scrap.ipynb`
- `tender_impulse/web-scrap.ipynb`

In the notebook, run all cells: **Cell → Run All**

## How to Configure URLs to Scrape

### Option 1: Edit the URL in Cell 2

Open the notebook and modify the `LIST_URL` variable in **Cell 2**:

```python
# Scrape all tenders (default)
LIST_URL = "https://apactenders.com/tenders/"

# Scrape specific page
LIST_URL = "https://apactenders.com/tenders/page/2/"

# Filter by country
LIST_URL = "https://apactenders.com/tenders/?country=philippines"
LIST_URL = "https://apactenders.com/tenders/?country=singapore"
LIST_URL = "https://apactenders.com/tenders/?country=bangladesh"

# Search by keyword
LIST_URL = "https://apactenders.com/?s=construction"
LIST_URL = "https://apactenders.com/?s=IT+equipment"
```

### Option 2: Scrape Multiple Pages

To scrape multiple pages, modify **Cell 2** to add:

```python
LIST_URL = "https://apactenders.com/tenders/"
MAX_PAGES = 5  # Scrape first 5 pages
```

Then update **Cell 4** to loop through pages (see example in the notebook).

## How to Read the Results

After running the scraper, results are saved in the `output/` folder for each source:

### 1. JSON Output (Main Results)

File: `output/scrap_output.json`

```json
[
  {
    "no": 1,
    "title": "Request for Bids: Supply and Delivery of Equipment",
    "organization": "HOSPITAL NAME",
    "country": "Philippines",
    "publish_date": "November 26, 2025 12:00 AM",
    "deadline_date": "December 4, 2025 1:00 pm",
    "detail_url": "https://apactenders.com/tender/..."
  },
  ...
]
```

**Fields Extracted:**
- `no` - Sequential number
- `title` - Tender title/description
- `organization` - Issuing organization
- `country` - Country of tender
- `publish_date` - Publication date
- `deadline_date` - Submission deadline
- `detail_url` - Full tender details URL

### 2. HTML Output (For Debugging)

File: `output/listing_page.html`

Contains the raw HTML of the scraped page for inspection and debugging.

## Read Results with Python

```python
import json

# Load the scraped data
with open('output/scrap_output.json', 'r', encoding='utf-8') as f:
    tenders = json.load(f)

# Print all tender titles
for tender in tenders:
    print(f"{tender['no']}. {tender['title']}")
    print(f"   Organization: {tender['organization']}")
    print(f"   Deadline: {tender['deadline_date']}")
    print(f"   URL: {tender['detail_url']}")
    print()
```

## Read Results with Command Line

```bash
# Pretty print the JSON
cat output/scrap_output.json | python -m json.tool

# Count total tenders
cat output/scrap_output.json | python -c "import json, sys; print(len(json.load(sys.stdin)))"

# Filter by country (e.g., Philippines)
cat output/scrap_output.json | python -c "import json, sys; tenders = json.load(sys.stdin); print([t['title'] for t in tenders if 'Philippines' in t['country']])"
```

## Project Structure

```
tender-proj/
├── README.md
├── requirements.txt
├── Makefile
├── apac_tenders/
│   ├── web-scrap.ipynb
│   └── output/
│       ├── listing_page.html
│       └── scrap_output.json
├── bidsInfo/
│   ├── web-scrap.ipynb
│   └── output/
├── global_tenders/
│   ├── web-scrap.ipynb
│   └── output/
└── tender_impulse/
    ├── web-scrap.ipynb
    └── output/
```

## Dependencies

- `requests` - HTTP requests to fetch web pages
- `beautifulsoup4` - HTML parsing and data extraction
- `selenium` - Browser automation for JavaScript-rendered content
- `webdriver_manager` - Automatic browser driver management

## Tips

1. **Respect Rate Limits**: Add delays between requests to avoid overwhelming the servers
2. **Check robots.txt**: Ensure scraping is allowed by the website
3. **User-Agent**: The scraper includes a proper User-Agent header
4. **Error Handling**: Check the HTML output if JSON results look incomplete

## Troubleshooting

**Issue**: Empty or incomplete results
- **Solution**: Check `output/listing_page.html` to verify the page structure
- The website may have changed its HTML structure

**Issue**: Connection errors
- **Solution**: Check your internet connection and verify the URL is accessible

**Issue**: Missing data fields
- **Solution**: Some tenders may not have all fields (country, deadline, etc.)

## Next Steps

- Add email notifications for new tenders
- Set up scheduled scraping (cron job)
- Add filtering by tender value or category
- Export to CSV or Excel format

