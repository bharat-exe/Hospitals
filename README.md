 


# Healthcare & Hospital Competitor Analysis
 
A Python-based web scraping and competitor analysis project that collects hospital listing information from Google Maps, analyzes healthcare competitor websites, exports data into CSV files, and generates a structured Markdown report.
 
## Project Overview
 
This project analyzes local hospitals in Hyderabad and major healthcare competitors to understand their digital presence, services, features, and potential market opportunities.
 
The project consists of three Python scripts:
 
- `scraper.py` — Scrapes hospital listings from Google Maps.

- `competitors.py` — Extracts information from healthcare competitor websites.

- `analysis.py` — Generates a competitor analysis report using the collected CSV data.
 
## Features
 
- Hospital data collection from Google Maps

- Hospital names, ratings, review counts, details, and URLs

- Healthcare competitor website analysis

- Page title and meta description extraction

- H1 and H2 heading extraction

- Automatic detection of digital healthcare features

- CSV data export

- Automated Markdown report generation

- SWOT-style competitor analysis and market opportunity identification
 
## Technologies Used
 
- **Python** — Core programming language

- **Playwright** — Browser automation and web scraping

- **CSV** — Structured data storage

- **Markdown** — Report generation

- **Google Maps** — Hospital listing source
 
## Project Structure
 
```text

Healthcare-Competitor-Analysis/

│

├── scraper.py

├── competitors.py

├── analysis.py

├── hospitals.csv

├── competitors.csv

├── COMPETITOR_ANALYSIS.md

└── README.md

```

### Step 1: Scrape Hospital Data
 
```bash

python scraper.py

```
 
The script searches for hospitals in Hyderabad and attempts to collect up to 20 listings.
 
**Output:** `hospitals.csv`
 
Collected fields:
 
- Hospital name

- Rating

- Review count

- Details

- Google Maps URL
 
### Step 2: Scrape Competitor Websites
 
```bash

python competitors.py

```
 
The script analyzes the websites of selected healthcare companies and extracts page titles, meta descriptions, headings, and detected digital features.
 
**Output:** `competitors.csv`
 
### Step 3: Generate the Analysis Report
 
```bash

python analysis.py

```
 
This script reads the hospital and competitor CSV files and generates a Markdown report.
 
**Output:** `COMPETITOR_ANALYSIS.md`
 
### Recommended Execution Order
 
1. Run `scraper.py`.

2. Run `competitors.py`.

3. Run `analysis.py`.
 
## Competitors Analyzed
 
The project includes the following healthcare platforms and hospital chains:
 
| Competitor | Category |

|---|---|

| Practo | HealthTech Aggregator |

| Apollo Hospitals | Hospital Chain |

| Yashoda Hospitals | Hospital Chain |

| KIMS Hospitals | Hospital Chain |

| CARE Hospitals | Hospital Chain |

| Lybrate | HealthTech Aggregator |

| MediBuddy | Digital Healthcare Platform |
 
## Analysis Report
 
The generated report includes:
 
- Executive summary

- Competitor feature and positioning matrix

- Local hospital landscape

- Competitor tiers and SWOT-style analysis

- Strengths and weaknesses

- Identified market gaps

- Strategic opportunities for digital healthcare services
