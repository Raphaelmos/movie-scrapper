import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from bs4 import BeautifulSoup
import requests

# Define the neural network model
class SentimentClassifier(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(SentimentClassifier, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, output_size)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return self.sigmoid(x)

# Function to generate dataset
def generate_critic_dataset():
    positive_critics = [
        "Un film magistral qui nous coupe le souffle.",
        "Un pur régal pour les amoureux de cinéma.",
        "Un chef-d'oeuvre qui restera dans les annales.",
        "Un bijou de scénario et de réalisation.",
        "Impossible de détacher ses yeux de l'écran."
    ]
    negative_critics = [
        "Un navet complet à éviter à tout prix.",
        "Je me suis endormi tellement c'était ennuyeux.",
        "Les personnages sont plats et le scénario prévisible.",
        "Un gâchis, je suis sorti déçu de la salle.",
        "Même pas digne d'un film de série B."
    ]

    critics = positive_critics + negative_critics
    labels = [1] * len(positive_critics) + [0] * len(negative_critics)

    df = pd.DataFrame({'Critic': critics, 'Sentiment': labels})

    return df


# Function to get movie critics from Allocine
def get_movie_critics(movie_url):
    response = requests.get(movie_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    critics = soup.find_all('div', class_="content-txt review-card-content")
    critics_texts = [critic.text for critic in critics]
    return critics_texts

# Function to train the sentiment classifier
def train_sentiment_classifier(df, vectorizer):
    X = vectorizer.transform(df['Critic']).toarray()
    y = df['Sentiment'].values

    input_size = X.shape[1]
    hidden_size = 64
    output_size = 1

    model = SentimentClassifier(input_size, hidden_size, output_size)
    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    dataset = TensorDataset(torch.tensor(X, dtype=torch.float32), torch.tensor(y, dtype=torch.float32))
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

    num_epochs = 10
    for epoch in range(num_epochs):
        for inputs, targets in dataloader:
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, targets.unsqueeze(1))
            loss.backward()
            optimizer.step()

    return model

# Function to predict sentiment
def predict_sentiment(model, vectorizer, critic, rating):
    critic_vector = vectorizer.transform([critic]).toarray()
    critic_tensor = torch.tensor(critic_vector, dtype=torch.float32)
    with torch.no_grad():
        output = model(critic_tensor)
        prediction = torch.round(output).item()
    if rating >= 2.5 or prediction == 1:
        return '+'
    else:
        return '-'


movie_df = pd.read_csv('movid.csv')

critic_df = generate_critic_dataset()


vectorizer = TfidfVectorizer()
vectorizer.fit(critic_df['Critic'])
model = train_sentiment_classifier(critic_df, vectorizer)


with open('criticrate.csv', 'w', encoding='utf-8') as file:
    for index, row in movie_df.iterrows():
        movie_name = row['Titre']
        movie_url = row['URL']
        movie_rating = row['Note'].replace(',', '.') if pd.notnull(row['Note']) else '0.0'  # Replace comma with dot
        movie_rating = float(movie_rating)  # Convert rating to float
        sentiment = '+' if movie_rating >= 3 else '-'
        if pd.notnull(movie_name) and pd.notnull(movie_url):
            print(f"Analysing critics for {movie_name}")
            critics = get_movie_critics(movie_url)
            for critic in critics:
                file.write(f"{sentiment}: {critic}\n")
