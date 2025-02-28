# Movie Scrapper

## Overview
The Movie Scrapper is a Python-based project designed to scrape movie reviews and perform sentiment analysis on them. This repository contains scripts that fetch reviews from specified URLs, analyze the sentiments of the reviews, and store the results in CSV files for further analysis.

## Features
- **Review Scraping**: Extracts movie reviews from specified websites.
- **Sentiment Analysis**: Uses a trained neural network model to classify reviews as positive or negative.
- **Data Storage**: Saves scraped reviews and sentiment results into CSV files for easy access and analysis.

## Files Included
- `scrappresse.py`: Script for scraping reviews from a specific movie review site, handling pagination and storing data in a CSV file.
- `scrapes.py`: A more structured script for scraping reviews, designed to avoid duplicates and manage multiple URLs effectively. Outputs data to a CSV file.
- `predic.py`: Implements a sentiment analysis model using PyTorch. Trains on predefined datasets and predicts sentiments of scraped reviews.

## Requirements
To run this project, you need the following Python packages installed:
- `requests`
- `beautifulsoup4`
- `torch`
- `pandas`
- `scikit-learn`

You can install the necessary packages using pip:

```bash
pip install requests beautifulsoup4 torch pandas scikit-learn
```
## Usage
1. **Set Up URLs**: Create a file named `url.txt` in the root directory and list the URLs of movie reviews you want to scrape.
2. **Run the Scraping Scripts**: Execute either `scrappresse.py` or `scrapes.py` to begin scraping reviews.
   ```bash
   python scrappresse.py
   ```
   ```bash
   python scrapes.py
   ```
3. **Train the Sentiment Model**: Run `predic.py` to train the sentiment analysis model using the predefined dataset.
   ```bash
   python predic.py
   ```
4. **Analyze Results**: The results will be saved in `criticrate.csv` and `films-critic.csv` for your review.
