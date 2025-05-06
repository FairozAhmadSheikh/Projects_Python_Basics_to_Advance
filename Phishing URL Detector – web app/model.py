import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
import re
import tldextract

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

# Sample dataset
data = [
    {"url": "https://secure-login.com", "label": 1},
    {"url": "https://www.google.com", "label": 0},
    {"url": "http://192.168.0.1/login", "label": 1},
    {"url": "https://paypal.com.verify-user.com", "label": 1},
    {"url": "https://github.com", "label": 0}
]

df = pd.DataFrame(data)
X = df["url"].apply(extract_url_features).apply(pd.Series)
y = df["label"]

model = RandomForestClassifier()
model.fit(X, y)

# Save model
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)
