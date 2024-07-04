import joblib
import sys


def load_model():
    """
    Load the trained spam detection model and vectorizer from disk.

    Returns:
        tuple: A tuple containing the loaded model and vectorizer.
    """
    model = joblib.load("spam_detector_model.pkl")
    vectorizer = joblib.load("spam_detector_vectorizer.pkl")

    return model, vectorizer


def predict(text):
    """
    Predict whether a given text is spam or not.

    Args:
        text (str): The text to be predicted.

    Returns:
        str: The prediction result, either "spam" or "not spam".
    """
    model, vectorizer = load_model()
    text = vectorizer.transform([text])
    prediction = model.predict(text)

    return "spam" if prediction[0] == 1 else "not spam"


if __name__ == "__main__":
    text = sys.argv[1]
    prediction = predict(text)
    print(f"The message is: {prediction}")
