import os

from flask import Flask, request, jsonify, render_template
from src.process_answers import process_user_inputs, get_user_output, compute_closest_laptop  # Import processing function
from src.create_db import create_db
from src.plotting.spider_chart import plot_spider_chart
import pandas as pd
app = Flask(__name__)

@app.route('/')
def home():
    # Render the HTML form
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Collect form inputs
    form_data = {
        "price_range": request.form.get("price_range", "No preference"),
        "charger_type": request.form.get("charger_type", "No preference"),
        "color": request.form.get("color", "No preference"),
        "graphics_card": int(request.form.get("graphics_card", 0)),
        "battery_lifetime": int(request.form.get("battery_lifetime", 0)),
        "usage_description": request.form.get("usage_description", "").strip()
    }


    # Create laptop database if not created yet
    # TODO: Webscrape some page and get data
    if os.path.exists('res/laptop_db.csv'):
        db_df = pd.read_csv('res/laptop_db.csv')
    else:
        create_db()
        db_df = pd.read_csv('res/laptop_db.csv')
    
    # Get User data metrics as in laptop database
    # TODO: implement API calls to chatGPT
    user_df = get_user_output(form_data)

    best_laptop, best_laptop_name, top_five_laptops = compute_closest_laptop(
        db_df,
        user_df
    )

    top_five_table = top_five_laptops.to_html(classes='top-five-table', index=False)


    # Generate the spider chart and get the file path
    chart_path = plot_spider_chart(best_laptop, user_df)
        
    # Render the result template with the chart
    return render_template(
        'result.html', 
        chart_path=chart_path,
        laptop_name=best_laptop_name,
        top_five_table=top_five_table
    )


if __name__ == '__main__':
    app.run(debug=True)
