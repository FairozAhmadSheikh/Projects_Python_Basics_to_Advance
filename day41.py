# pip install pandas scikit-learn xgboost pefile

import pefile
import os

def extract_features(file_path):
    try:
        pe = pefile.PE(file_path)
        features = {
            'SizeOfCode': pe.OPTIONAL_HEADER.SizeOfCode,
            'SizeOfInitializedData': pe.OPTIONAL_HEADER.SizeOfInitializedData,
            'SizeOfUninitializedData': pe.OPTIONAL_HEADER.SizeOfUninitializedData,
            'AddressOfEntryPoint': pe.OPTIONAL_HEADER.AddressOfEntryPoint,
            'BaseOfCode': pe.OPTIONAL_HEADER.BaseOfCode,
            'ImageBase': pe.OPTIONAL_HEADER.ImageBase,
            'Subsystem': pe.OPTIONAL_HEADER.Subsystem,
            'DllCharacteristics': pe.OPTIONAL_HEADER.DllCharacteristics,
            'SizeOfImage': pe.OPTIONAL_HEADER.SizeOfImage,
            'NumberOfSections': len(pe.sections)
        }
        return features
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load extracted features CSV
df = pd.read_csv("malware_dataset.csv")
X = df.drop("label", axis=1)
y = df["label"]  # 0 = benign, 1 = malware

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

# Train model
clf = RandomForestClassifier()
clf.fit(X_train, y_train)

# Evaluate
y_pred = clf.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred)*100:.2f}%")

def predict_file(file_path, model):
    features = extract_features(file_path)
    if features:
        df = pd.DataFrame([features])
        result = model.predict(df)[0]
        print("🛑 Malware Detected!" if result == 1 else "✅ File is Clean.")
    else:
        print("Could not analyze file.")
