import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
import joblib


def load_data():
    """
    Load the SMS spam dataset from a URL and preprocess the data.

    Returns:
    data (DataFrame): Preprocessed SMS spam dataset with columns 'label' and 'text'.
                      The 'label' column is mapped to 0 for 'ham' and 1 for 'spam'.
    """
    url = "https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv"
    data = pd.read_csv(url, sep="\t", header=None, names=['label', 'text'])
    data["label"] = data["label"].map({"ham": 0, "spam": 1})

    return data


def train(data):
    """
    Train a spam detection model using Naive Bayes classifier.

    Args:
    data (DataFrame): Preprocessed SMS spam dataset.

    Returns:
    accuracy (float): Accuracy of the trained model on the test data.
    report (str): Classification report of the trained model on the test data.
    """
    x = data["text"]
    y = data["label"]
    vectorizer = TfidfVectorizer()
    x = vectorizer.fit_transform(x)
    xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.2)
    model = MultinomialNB()
    model.fit(xtrain, ytrain)
    ypred = model.predict(xtest)
    accuracy = accuracy_score(ytest, ypred)
    report = classification_report(ytest, ypred)

    joblib.dump(model, "spam_detector_model.pkl")
    joblib.dump(vectorizer, "spam_detector_vectorizer.pkl")

    return accuracy, report


if __name__ == "__main__":
    data = load_data()
    accuracy, report = train(data)
    print(f"Accuracy: {accuracy}")
    print(f"Classification Report: {report}")