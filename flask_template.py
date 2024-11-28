from flask import Flask, request, jsonify, render_template
from process_answers import process_user_inputs  # Import processing function

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

    # Process inputs using the helper module
    metrics = process_user_inputs(form_data)

    # Return processed metrics as a JSON response
    return jsonify({
        "form_data": form_data,
        "metrics": metrics
    })

if __name__ == '__main__':
    app.run(debug=True)
