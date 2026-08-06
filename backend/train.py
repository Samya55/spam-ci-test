import os
import urllib.request
import zipfile
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib

DATA_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/00228/smsspamcollection.zip"
DATA_ZIP = "smsspamcollection.zip"
DATA_FILE = "SMSSpamCollection"
MODEL_DIR = os.path.dirname(os.path.abspath(__file__))

def download_and_extract_data():
    if not os.path.exists(DATA_FILE):
        print("Downloading dataset...")
        urllib.request.urlretrieve(DATA_URL, DATA_ZIP)
        print("Extracting dataset...")
        with zipfile.ZipFile(DATA_ZIP, 'r') as zip_ref:
            zip_ref.extractall(".")
        os.remove(DATA_ZIP)
        print("Dataset ready.")

def train_model():
    print("Loading data...")
    import csv
    
    df = pd.read_csv(DATA_FILE, sep='\t', header=None, names=['label', 'text'], quoting=csv.QUOTE_NONE)
    
    
    X = df['text']
    y = df['label']

    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Vectorizing text...")
    vectorizer = TfidfVectorizer(stop_words='english')
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    print("Training Naive Bayes model...")
    model = MultinomialNB()
    model.fit(X_train_vec, y_train)

    print("Evaluating model...")
    y_pred = model.predict(X_test_vec)
    acc = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {acc:.4f}")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

    
    vectorizer_path = os.path.join(MODEL_DIR, "vectorizer.pkl")
    model_path = os.path.join(MODEL_DIR, "model.pkl")
    joblib.dump(vectorizer, vectorizer_path)
    joblib.dump(model, model_path)
    print(f"Saved vectorizer to {vectorizer_path}")
    print(f"Saved model to {model_path}")

if __name__ == "__main__":
    download_and_extract_data()
    train_model()
