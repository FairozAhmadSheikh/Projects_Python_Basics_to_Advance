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