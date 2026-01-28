from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/submit-contact', methods=['POST'])
def submit_contact():
    data = request.json
    # In a real application, you would save this to a database or email it
    print(f"Contact form submitted: {data}")
    return jsonify({'status': 'success', 'message': 'Thank you for contacting us!'})

if __name__ == '__main__':
    app.run(debug=True)
