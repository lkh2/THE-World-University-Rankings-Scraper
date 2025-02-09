import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def scrape_THE_detailed_rankings():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # Load THE World University Rankings page, feel free to change the URL to scrape other years or subjects
        url = 'https://www.timeshighereducation.com/world-university-rankings/latest/world-ranking#!/length/-1/sort_by/rank/sort_order/asc/cols/scores'
        driver.get(url)
        
        table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'datatable-1'))
        )
        
        data = []
        rows = [row for row in table.find_elements(By.CSS_SELECTOR, 'tr.js-row') 
            if 'institution-disabled' not in row.get_attribute('class') 
            and 'rankings-reporter' not in row.get_attribute('class')]
        
        for row in rows:
            try:
                # Extract name and country 
                name_cell = row.find_element(By.CSS_SELECTOR, 'td.name')
                name = name_cell.find_element(By.CSS_SELECTOR, '.ranking-institution-title').text.strip()
                country = name_cell.find_element(By.CSS_SELECTOR, '.location').text.strip()
                
                # Extract scores
                scores = {
                    'citations': float(row.find_element(By.CSS_SELECTOR, 'td.citations-score').text or 0),
                    'industry': float(row.find_element(By.CSS_SELECTOR, 'td.industry_income-score').text or 0),
                    'international': float(row.find_element(By.CSS_SELECTOR, 'td.international_outlook-score').text or 0),
                    'research': float(row.find_element(By.CSS_SELECTOR, 'td.research-score').text or 0),
                    'teaching': float(row.find_element(By.CSS_SELECTOR, 'td.teaching-score').text or 0)
                }
                    
                # Calculate overall score using the specified weights
                overall_score = (
                    scores['teaching'] * 0.295 +
                    scores['research'] * 0.29 +
                    scores['citations'] * 0.30 +
                    scores['international'] * 0.075 +
                    scores['industry'] * 0.04
                )
                
                data.append({
                    'Name': name,
                    'Country': country,
                    'Overall Score': overall_score,
                    'Research Quality': scores['citations'],
                    'Industry': scores['industry'],
                    'International Outlook': scores['international'],
                    'Research Environment': scores['research'],
                    'Teaching': scores['teaching']
                })
            except Exception as e:
                print(f"Error processing row: {e}")
                continue
        
        # Create DataFrame and sort by Overall Score
        df = pd.DataFrame(data)
        df = df.sort_values('Overall Score', ascending=False)
        
        # Add Rank column based on Overall Score
        df['Rank'] = range(1, len(df) + 1)
        
        # Reorder columns
        df = df[['Name', 'Country', 'Rank', 'Overall Score', 'Research Quality', 
                'Industry', 'International Outlook', 'Research Environment', 'Teaching']]
        
        return df
    
    finally:
        driver.quit()

# Execute scraping and save results
rankings_df = scrape_THE_detailed_rankings()
print(rankings_df)
rankings_df.to_csv('the_detailed_rankings.csv', index=False)
