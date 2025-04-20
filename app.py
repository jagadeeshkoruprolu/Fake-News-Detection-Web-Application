from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Setup Gemini
genai.configure(api_key="AIzaSyB64sScNJOuwl7NUWxBYDA2QggwXquDbgg")  # << Your real key here

# Load correct model
model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_news', methods=['POST'])
def check_news():
    try:
        data = request.get_json()
        news_text = data.get('news')

        if not news_text:
            return jsonify({'result': 'Error: No news text received.'})

        # Ask Gemini model
        prompt = f"Check if the following news is true or fake. Only answer with 'True' or 'False'. News:\n\n{news_text}"

        response = model.generate_content(prompt)

        result = response.text.strip().lower()

        # Make it clean
        if 'true' in result:
            return jsonify({'result': 'True'})
        elif 'false' in result:
            return jsonify({'result': 'False'})
        else:
            return jsonify({'result': 'Could not determine.'})

    except Exception as e:
        return jsonify({'result': f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

