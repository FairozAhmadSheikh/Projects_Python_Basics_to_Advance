# pip install flask transformers torch

from flask import Flask, render_template, request
from transformers import pipeline

app = Flask(__name__)
generator = pipeline("text-generation", model="gpt2")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        topic = request.form["topic"]
        prompt = f"Write a detailed blog article about: {topic}"
        result = generator(prompt, max_length=512, num_return_sequences=1)
        content = result[0]["generated_text"]
        return render_template("index.html", topic=topic, content=content)
    return render_template("index.html", topic=None, content=None)

if __name__ == "__main__":
    app.run(debug=True)



# HTML 
<!DOCTYPE html>
<html>
<head>
    <title>AI Blog Generator</title>
    <style>
        body { font-family: Arial; margin: 40px; background: #f8f9fa; }
        textarea, input { width: 100%; padding: 10px; margin-top: 10px; }
        .container { max-width: 800px; margin: auto; }
        .card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <h1>🧠 AI Blog Article Generator</h1>
            <form method="POST">
                <label for="topic">Enter a topic:</label>
                <input type="text" id="topic" name="topic" required>
                <button type="submit">Generate</button>
            </form>
            {% if content %}
                <hr>
                <h2>📝 Blog on "{{ topic }}"</h2>
                <p>{{ content }}</p>
            {% endif %}
        </div>
    </div>
</body>
</html>


#