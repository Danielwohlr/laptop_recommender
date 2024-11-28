from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('form.html')  # Create this HTML with the questions.

@app.route('/submit', methods=['POST'])
def submit():
    user_answers = request.form  # Get user inputs
    # Process answers later
    return "Processing your recommendations!"

if __name__ == '__main__':
    app.run(debug=True)
