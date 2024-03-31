import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split

import pandas as pd

# Load the dataset
data = pd.read_csv('sent_train.csv',encoding='unicode_escape')
data = data.dropna(subset=['text'])
X = data['text']
y = data['sentiment']

# Convert sentiment labels to numerical values
sentiment_mapping = {'positive': 2, 'negative': 0, 'neutral': 1}
y = y.map(sentiment_mapping)

# Split the data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Convert text to numerical features
vectorizer = CountVectorizer()
X_train_vectorized = vectorizer.fit_transform(X_train)
X_test_vectorized = vectorizer.transform(X_test)

# Train the Naive Bayes classifier
classifier = MultinomialNB()
classifier.fit(X_train_vectorized, y_train)

# Predict sentiment on the test set
y_pred = classifier.predict(X_test_vectorized)

# Evaluate the model
from sklearn.metrics import accuracy_score, classification_report
print('Accuracy:', accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Predict sentiment on new data
# new_text = ['This product is amazing!', 'I hate this service.', 'It was okay.']
# new_text_vectorized = vectorizer.transform(new_text)
# new_sentiment = classifier.predict(new_text_vectorized)
# print('Predicted sentiment:', new_sentiment)

# Save the trained model
with open('sentiment_model.pkl', 'wb') as f:
    pickle.dump(classifier, f)

# Save the vectorizer
with open('vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)