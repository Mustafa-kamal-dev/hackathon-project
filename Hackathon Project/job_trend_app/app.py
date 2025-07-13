# app.py
from flask import Flask, render_template, request
import pandas as pd
from scraper import scrape_linkedin_jobs
# from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    data = None
    if request.method == 'POST':
        title = request.form['title']
        location = request.form['location']
        df = scrape_linkedin_jobs(title, location)
        
        # Analysis
        top_titles = df['title'].value_counts().head(5)
        top_companies = df['company'].value_counts().head(5)
        top_locations = df['location'].value_counts().head(5)

        data = {
            'titles': top_titles.to_dict(),
            'companies': top_companies.to_dict(),
            'locations': top_locations.to_dict(),
            'jobs': df.head(10).to_dict(orient='records')  # Show first 10 jobs
        }

    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
