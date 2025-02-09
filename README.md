# Times Higher Education World University Rankings Scraper
This repository contains a Python script for scraping the Times Higher Education World University Rankings data and converting it into a CSV file. The script navigates the THE website, extracts the relevant ranking data, and processes it for easy analysis and visualization.

## Setup Requirements

Before running the scraping scripts, ensure:

1. **Ranking URL**
   - Navigate to the THE rankings page
   - Click "show all entries" at the bottom of the table
   - Verify the URL contains `#!/length/-1`
   - Copy the updated URL if needed

2. **Ranking Weights**
   - Current weights based on [THE 2025 methodology](https://www.timeshighereducation.com/sites/default/files/breaking_news_files/the_2025_world_university_rankings_methodology.pdf#page=14):
     - Teaching (29.5%)
     - Research Environment (29%)
     - Research Quality/Citations (30%)
     - International Outlook (7.5%)
     - Industry Income (4%)
   - If methodology changes, updates it accordingly
  
## Requirements

```bash
pip install pandas selenium webdriver-manager
