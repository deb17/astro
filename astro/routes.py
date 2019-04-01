from flask import render_template

from astro import app
from astro.scrape import main

@app.route('/')
@app.route('/index')
def index():

    scraped_data = main()
    return render_template('index.html', data=scraped_data)
