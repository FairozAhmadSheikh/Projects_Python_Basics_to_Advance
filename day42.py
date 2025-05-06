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