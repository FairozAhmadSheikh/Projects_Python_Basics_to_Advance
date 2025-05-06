# pip install pandas scikit-learn tldextract
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

# Sample Training Script (with dummy dataset)
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Dummy dataset
data = [
    {"url": "https://secure-login.com", "label": 1},
    {"url": "https://www.google.com", "label": 0},
    {"url": "http://192.168.0.1/login", "label": 1},
    {"url": "https://paypal.com.verify-user.com", "label": 1},
    {"url": "https://github.com", "label": 0}
]

# Feature extraction
df = pd.DataFrame(data)
features = df["url"].apply(extract_url_features).apply(pd.Series)
X = features
y = df["label"]

# Train model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
clf = RandomForestClassifier()
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

print("✅ Classification Report:\n", classification_report(y_test, y_pred))

#  Live Detection

cdn 2 
def detect_phishing(url, model):
    features = extract_url_features(url)
    df = pd.DataFrame([features])
    result = model.predict(df)[0]
    print("🛑 Phishing URL!" if result == 1 else "✅ Legitimate URL.")