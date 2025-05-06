from flask import Flask, request, render_template
import pickle
import pandas as pd
import re
import tldextract

app = Flask(__name__)

# Load model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

# Extract features
def extract_url_features(url):
    features = {
        "url_length": len(url),
        "num_digits": sum(c.isdigit() for c in url),
        "has_ip": 1 if re.match(r'\d+\.\d+\.\d+\.\d+', url) else 0,
        "num_dots": url.count('.'),
        "num_hyphens": url.count('-'),
        "has_https": 1 if url.startswith("https") else 0,
        "has_at_symbol": 1 if "@" in url else 0,
        "has_suspicious_word": 1 if any(w in url for w in ["login", "verify", "secure", "account"]) else 0,
    }
    domain = tldextract.extract(url).domain
    features["domain_length"] = len(domain)
    return features

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        url = request.form["url"]
        features = extract_url_features(url)
        df = pd.DataFrame([features])
        prediction = model.predict(df)[0]
        result = "🛑 Phishing URL Detected!" if prediction == 1 else "✅ URL is Safe."
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
