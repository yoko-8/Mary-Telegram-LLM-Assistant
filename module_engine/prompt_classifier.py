import os
import joblib

# Load the pre-trained Naive Bayes classifier and vectorizer
current_dir = os.path.dirname(__file__)
nb_classifier = joblib.load(os.path.join(current_dir, 'pickles/naive_bayes_model.pkl'))
vectorizer = joblib.load(os.path.join(current_dir, 'pickles/vectorizer.pkl'))


# Function to classify user input
def classify_user_input(input_text):
    # Vectorize the input text
    input_vector = vectorizer.transform([input_text])

    # Predict the class label
    predicted_class = nb_classifier.predict(input_vector)[0]

    return predicted_class


# Example of how to use the function:
if __name__ == '__main__':
    user_input = input("Enter text for classification: ")
    classification = classify_user_input(user_input)
    print("Classification result:", classification)
