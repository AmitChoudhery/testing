from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

# Your Free Astrology API key (make sure it's valid)
API_KEY = "pbACoZ5eJd1kcvVpI1kRoaARoZ0GHOSL2IQaknnF"

# URL for Free Astrology API (replace with the actual API URL)
API_URL = "https://api.freeastrologyapi.com/v1/kundli"  # Example URL, replace with real API URL

# Function to fetch Kundli data from the API
def fetch_kundli(dob, tob, place):
    # Make an API request to fetch Kundli data
    response = requests.post(API_URL, json={
        "dob": dob,
        "tob": tob,
        "place": place,
        "api_key": API_KEY
    })
    
    if response.status_code == 200:
        return response.json()  # Return the API response as a JSON
    else:
        return {"error": "Failed to fetch Kundli data from the API."}

@app.route('/')
def home():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Amit Data Astro Vastu Expert</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                padding: 20px;
            }
            form {
                margin-top: 20px;
            }
            input {
                margin: 5px;
                padding: 10px;
                font-size: 16px;
            }
            button {
                padding: 10px 20px;
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                cursor: pointer;
            }
            button:hover {
                background-color: #45a049;
            }
            #result {
                margin-top: 20px;
                font-size: 16px;
            }
        </style>
    </head>
    <body>
        <h1>Welcome to Amit Data Astro Vastu Expert</h1>
        <form id="kundli-form">
            <input type="date" id="dob" name="dob" required placeholder="Date of Birth">
            <input type="time" id="tob" name="tob" required placeholder="Time of Birth">
            <input type="text" id="place" name="place" required placeholder="Place of Birth">
            <button type="submit">Generate Kundli</button>
        </form>

        <div id="result">
            <!-- Generated Kundli data will be displayed here -->
        </div>

        <script>
            const form = document.getElementById('kundli-form');
            form.onsubmit = async (e) => {
                e.preventDefault();
                const formData = new FormData(form);
                const response = await fetch('/generate_kundli', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        dob: formData.get('dob'),
                        tob: formData.get('tob'),
                        place: formData.get('place'),
                    }),
                });
                const result = await response.json();
                document.getElementById('result').innerHTML = JSON.stringify(result, null, 2);
            };
        </script>
    </body>
    </html>
    ''')

@app.route('/generate_kundli', methods=['POST'])
def generate_kundli():
    data = request.get_json()
    dob = data.get('dob')
    tob = data.get('tob')
    place = data.get('place')

    if not dob or not tob or not place:
        return jsonify({"error": "Missing required fields"}), 400
    
    # Call the function to fetch Kundli data using the API
    kundli_data = fetch_kundli(dob, tob, place)
    
    # Return the response (Kundli data) to the frontend
    return jsonify(kundli_data)

if __name__ == '__main__':
    app.run(debug=True)
