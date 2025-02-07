# Google Scholar Literature Scraper

This library is designed to scrape, store, and process bibliographic data from Google Scholar. It consists of two main components:  

- **`data_scraper.py`**: Scrapes academic data and saves each entry as a pickle file.  
- **`data_handler.py`**: Reads and processes the stored pickle files, extracting relevant metadata and generating structured outputs.  

## Installation  

Ensure you have Python 3 installed and [install scholarly](https://scholarly.readthedocs.io/en/stable/quickstart.html#fill).

## Usage

1. Modify `config.json` to add the desired queries before running the scraper. This file should contain the search terms or parameters you want to use when collecting data.


2. Run  **`data_scraper.py`** script to collect and store academic data into pickle files.

```bash
python data_scraper.py
```

3. Run **`data_handler.py`** script to read and process the stored entries.

```bash
python data_handler.py
```

This will generate structured outputs in multiple formats:

- JSON (`scholar_results.json`)
- CSV (`scholar_results.csv`)
- BibTeX (`scholar_results.bib`)

