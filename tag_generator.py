from bs4 import BeautifulSoup
from hazm import *
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
from constants import STOPWORDS, PUNCTUATIONS


def prepare_body(body):
    soup = BeautifulSoup(body, "html.parser")
    paragraphs = soup.find_all("p", class_="md-block-unstyled")
    text = ""
    for p in paragraphs:
        text += p.get_text() + "\n"
    return text


def extract_tags(body, top_n=5):
    normalized_text = Normalizer().normalize(body)
    sentences = sent_tokenize(normalized_text)
    tokenized_sentences = [word_tokenize(sentence) for sentence in sentences]
    filtered_words = [
        [word for word in sentence if word not in set(PUNCTUATIONS)]
        for sentence in tokenized_sentences
    ]
    sentences = []
    for sentence in filtered_words:
        words = []
        for word in sentence:
            if "_" in word:
                words.extend(word.split("_"))
            if "\u200c" in word:
                words.extend(word.split("\u200c"))
            else:
                words.append(word)
        sentences.append(words)
    filtered_words = [
        [word for word in sentence if word not in set(STOPWORDS)] for sentence in sentences
    ]
    lemmatizer = Lemmatizer()
    lemmatized_words = [
        [
            lemmatizer.lemmatize(word).split("#")[1]
            if "#" in lemmatizer.lemmatize(word)
            else lemmatizer.lemmatize(word)
            for word in sentence
        ]
        for sentence in filtered_words
    ]
    flattened_words = [word for sentence in lemmatized_words for word in sentence]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([" ".join(flattened_words)])
    normalized_matrix = normalize(tfidf_matrix)
    scores = normalized_matrix.sum(axis=0)
    top_indices = scores.argsort()[0, -top_n:][::-1]
    feature_names = vectorizer.get_feature_names_out()
    tags = [feature_names[index] for index in top_indices][0][0]
    return tags
