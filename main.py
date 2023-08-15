

importing the necessary Python libraries and the dataset:
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

df = pd.read_csv("/content/drive/MyDrive/Flipkart_Amazon Mobile Reviews.csv")
df.head(7)

df.shape

df.describe()

df.info()

df.isnull().sum()

import pandas as pd
import matplotlib.pyplot as plt

# Assuming 'df' is your DataFrame

# Calculate the number of unique product values
unique_products = df['Product Name'].nunique()

# Create a plot
plt.figure(figsize=(10,10))
df['Product Name'].value_counts().plot(kind='bar')
plt.title('Distribution of Products')
plt.xlabel('Product')
plt.ylabel('Number of Reviews')
plt.xticks(rotation=90)
plt.tight_layout()

# Show the plot
plt.show()

print("Number of Unique Products:", unique_products)

# Combine review title and body
df['Review'] = df['Review-Body'] + ' ' + df['Review-Title']

df.head()

df['Review'].iloc[1]

df['Review'].info()

"""DATA CLEANING :"""

df.drop(columns = ['Review-Title','Review-Body'],inplace=True)

df.drop(columns = ['Unnamed: 0'],inplace=True)

df = df.dropna(subset=['Review'])
df.info()

df.head()

import re
ratings = df['rating'].apply(lambda x: float(re.findall(r'\d+\.\d+', x)[0]) if re.findall(r'\d+\.\d+', x) else np.nan)

df['rating'] = df['rating'].str.extract(r'(\d+\.\d+)').astype(float)

df['rating'].head()

df.head()

"""ONE PLUS"""

import pandas as pd

oneplus_reviews = df[df['Product Name'].str.contains('OnePlus', case=False)].copy()
oneplus_reviews['OnePlus_Reviews'] = oneplus_reviews['Review']
oneplus_reviews.drop(columns=['Product Name', 'Review'], inplace=True)
oneplus_reviews

oneplus_reviews.isnull().sum()

"""Text Cleaning :"""

import re
import pandas as pd

def remove_url(text):
    text = re.sub(r"http\S+", "", text)
    return text
oneplus_reviews['OnePlus_Reviews'] = oneplus_reviews['OnePlus_Reviews'].apply(remove_url)
oneplus_reviews

import pandas as pd
import unicodedata as uni
def normalize_text(text):
    return uni.normalize('NFKD', text)
oneplus_reviews['OnePlus_Reviews'] = oneplus_reviews['OnePlus_Reviews'].apply(normalize_text)
oneplus_reviews

!pip install demoji

import pandas as pd
import demoji
def handle_emoji(string):
    emojis = demoji.findall(string)

    for emoji in emojis:
        string = string.replace(emoji, " " + emojis[emoji])

    return string

# Download emoji data (required before using demoji)
demoji.download_codes()


oneplus_reviews['OnePlus_Reviews'] = oneplus_reviews['OnePlus_Reviews'].apply(handle_emoji)

print(oneplus_reviews)

oneplus_reviews['OnePlus_Reviews'].iloc[3]

oneplus_reviews['OnePlus_Reviews'] = oneplus_reviews['OnePlus_Reviews'].str.replace("The media could not be loaded.\n                \n\n\n\n ", "")

oneplus_reviews['OnePlus_Reviews'].iloc[3]

pip install googletrans==4.0.0-rc1

!apt-get -qq install -y python3-langdetect

!pip install textblob

from langdetect import detect
from googletrans import Translator
from textblob import TextBlob


def detect_language(text):
    try:
        lang = detect(text)
        return lang
    except:
        return 'unknown'  # In case of an error in language detection

# Function to translate non-English text to English using Google Translate API
def translate_to_english(text):
    try:
        translator = Translator()
        translation = translator.translate(text, src='auto', dest='en')
        return translation.text
    except:
        return 'translation_failed'  # In case of an error in translation

# Function to perform spelling correction
def correct_spelling(text):
    try:
        blob = TextBlob(text)
        corrected_text = blob.correct()
        return str(corrected_text)
    except:
        return 'correction_failed'  # In case of an error in correction



# Apply language detection to the 'OnePlus_Reviews' column
oneplus_reviews['Language'] = oneplus_reviews['OnePlus_Reviews'].apply(detect_language)

# Filter out non-English reviews
non_english_reviews = oneplus_reviews[oneplus_reviews['Language'] != 'en']

# Translate non-English reviews to English
non_english_reviews['OnePlus_Reviews'] = non_english_reviews['OnePlus_Reviews'].apply(translate_to_english)

# Correct spelling in the translated reviews
non_english_reviews['OnePlus_Reviews'] = non_english_reviews['OnePlus_Reviews'].apply(correct_spelling)

# Update the original DataFrame with translated and corrected reviews
oneplus_reviews.update(non_english_reviews)
oneplus_reviews.drop(columns=['Language'], inplace=True)

oneplus_reviews

oneplus_reviews[:20]

import nltk
nltk.download('vader_lexicon')

pip install vaderSentiment

import nltk
nltk.download('stopwords')

import nltk

# Download the 'wordnet' resource
nltk.download('wordnet')

import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Assuming you have already imported the 'oneplus_reviews' DataFrame

# Lowercasing
oneplus_reviews['OnePlus_Reviews'] = oneplus_reviews['OnePlus_Reviews'].apply(lambda x: x.lower())

# Removing special characters and symbols
oneplus_reviews['OnePlus_Reviews'] = oneplus_reviews['OnePlus_Reviews'].apply(lambda x: re.sub(r'[^a-zA-Z0-9\s]', '', x))

# Stopword removal
stop_words = set(stopwords.words('english'))
oneplus_reviews['OnePlus_Reviews'] = oneplus_reviews['OnePlus_Reviews'].apply(lambda x: ' '.join([word for word in x.split() if word not in stop_words]))

# Lemmatization (optional)
lemmatizer = WordNetLemmatizer()
oneplus_reviews['OnePlus_Reviews'] = oneplus_reviews['OnePlus_Reviews'].apply(lambda x: ' '.join([lemmatizer.lemmatize(word) for word in x.split()]))

# Sentiment analysis using VADER
analyzer = SentimentIntensityAnalyzer()
sentiment_scores = oneplus_reviews['OnePlus_Reviews'].apply(lambda x: analyzer.polarity_scores(x))

# Extracting sentiment scores
oneplus_reviews['Positive_Score'] = sentiment_scores.apply(lambda x: x['pos'])
oneplus_reviews['Negative_Score'] = sentiment_scores.apply(lambda x: x['neg'])
oneplus_reviews['Neutral_Score'] = sentiment_scores.apply(lambda x: x['neu'])
oneplus_reviews['Compound_Score'] = sentiment_scores.apply(lambda x: x['compound'])

# Classify sentiment based on compound score
oneplus_reviews['Sentiment'] = oneplus_reviews['Compound_Score'].apply(lambda x: 'positive' if x >= 0.05 else ('negative' if x <= -0.05 else 'neutral'))

# Print the results
oneplus_reviews

# Assuming you have already processed the 'oneplus_reviews' DataFrame and added the 'Compound_Score' column

# Calculate overall positive and negative percentages
total_reviews = len(oneplus_reviews)
positive_reviews = len(oneplus_reviews[oneplus_reviews['Compound_Score'] >= 0.05])
negative_reviews = len(oneplus_reviews[oneplus_reviews['Compound_Score'] <= -0.05])

positive_percentage = (positive_reviews / total_reviews) * 100
negative_percentage = (negative_reviews / total_reviews) * 100

print(f"Overall Positive Percentage: {positive_percentage:.2f}%")
print(f"Overall Negative Percentage: {negative_percentage:.2f}%")

"""EXPLORATORY DATA ANALYSIS"""

ratings = oneplus_reviews["rating"].value_counts()
numbers = ratings.index
quantity = ratings.values

import plotly.express as px
figure = px.pie(oneplus_reviews,
             values=quantity,
             names=numbers,hole = 0.5)
figure.show()

pip install matplotlib

import pandas as pd
import matplotlib.pyplot as plt

# Assuming you have already processed the 'oneplus_reviews' DataFrame and added the 'Compound_Score' column

# Calculate overall positive and negative percentages
total_reviews = len(oneplus_reviews)
positive_reviews = len(oneplus_reviews[oneplus_reviews['Compound_Score'] >= 0.05])
negative_reviews = len(oneplus_reviews[oneplus_reviews['Compound_Score'] <= -0.05])

positive_percentage = (positive_reviews / total_reviews) * 100
negative_percentage = (negative_reviews / total_reviews) * 100

# Plotting the diagram
labels = ['Positive', 'Negative']
percentages = [positive_percentage, negative_percentage]

plt.bar(labels, percentages, color=['green', 'red'])
plt.ylabel('Percentage')
plt.title('Overall Positive and Negative Percentages')
plt.ylim(0, 100)

# Annotate the bars with the percentage values
for i, v in enumerate(percentages):
    plt.text(i, v + 1, f"{v:.2f}%", ha='center', va='bottom')

plt.show()

import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Assuming you have already processed the 'oneplus_reviews' DataFrame and added the 'OnePlus_Reviews' column

# Combine all the reviews into a single text for word cloud
all_reviews_text = ' '.join(oneplus_reviews['OnePlus_Reviews'])

# Create a word cloud
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_reviews_text)

# Plot the word cloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud for OnePlus Reviews')
plt.show()

pip install transformers[sentencepiece]

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch.nn.functional as F
from transformers import pipeline

# Load Aspect-Based Sentiment Analysis model
absa_tokenizer = AutoTokenizer.from_pretrained("yangheng/deberta-v3-base-absa-v1.1")
absa_model = AutoModelForSequenceClassification \
  .from_pretrained("yangheng/deberta-v3-base-absa-v1.1")

# Load a traditional Sentiment Analysis model
sentiment_model_path = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
sentiment_model = pipeline("sentiment-analysis", model=sentiment_model_path,
                          tokenizer=sentiment_model_path)

sentence='bad battery but screen and camera are good'
aspect = "battery"
inputs = absa_tokenizer(f"[CLS] {sentence} [SEP] {aspect} [SEP]", return_tensors="pt")
outputs = absa_model(**inputs)
probs = F.softmax(outputs.logits, dim=1)
probs = probs.detach().numpy()[0]
print(f"Sentiment of aspect '{aspect}' is:")
for prob, label in zip(probs, ["negative", "neutral", "positive"]):
  print(f"Label {label}: {prob}")
print()


# ABSA of "camera"
aspect = "camera"
inputs = absa_tokenizer(f"[CLS] {sentence} [SEP] {aspect} [SEP]", return_tensors="pt")
outputs = absa_model(**inputs)
probs = F.softmax(outputs.logits, dim=1)
probs = probs.detach().numpy()[0]
print(f"Sentiment of aspect '{aspect}' is:")
for prob, label in zip(probs, ["negative", "neutral", "positive"]):
  print(f"Label {label}: {prob}")
print()


# Overall sentiment of the sentence
sentiment = sentiment_model([sentence])[0]
print(f"Overall sentiment: {sentiment['label']} with score {sentiment['score']}")

"""ASPECT BASED"""

aspect = "camera"
camera_negative=[]
camera_neutral=[]
camera_positive=[]

# Perform aspect-based sentiment analysis for each review
for review in oneplus_reviews['OnePlus_Reviews']:

  if aspect in review:
    inputs = absa_tokenizer(f"[CLS] {review} [SEP] {aspect} [SEP]", return_tensors="pt")
    outputs = absa_model(**inputs)
    probs = F.softmax(outputs.logits, dim=1)
    probs = probs.detach().numpy()[0]
    camera_negative.append(probs[0])
    camera_neutral.append(probs[1])
    camera_positive.append(probs[2])
  else:
    camera_negative.append(0)
    camera_neutral.append(0)
    camera_positive.append(0)

oneplus_reviews['cam_positive']=camera_positive
oneplus_reviews['cam_negative']=camera_negative
oneplus_reviews['cam_neutral']=camera_neutral

oneplus_reviews

overall_cam_positive_score = oneplus_reviews['cam_positive'].sum()
count = (oneplus_reviews['cam_positive'] != 0).sum()
oneplus_camera_rating= (overall_cam_positive_score/count)*5
oneplus_camera_rating



aspect = "battery"
battery_negative=[]
battery_neutral=[]
battery_positive=[]

# Perform aspect-based sentiment analysis for each review
for review in oneplus_reviews['OnePlus_Reviews']:

  if aspect in review:
    inputs = absa_tokenizer(f"[CLS] {review} [SEP] {aspect} [SEP]", return_tensors="pt")
    outputs = absa_model(**inputs)
    probs = F.softmax(outputs.logits, dim=1)
    probs = probs.detach().numpy()[0]
    battery_negative.append(probs[0])
    battery_neutral.append(probs[1])
    battery_positive.append(probs[2])
  else:
    battery_negative.append(0)
    battery_neutral.append(0)
    battery_positive.append(0)

oneplus_reviews['battery_positive']=battery_positive
oneplus_reviews['battery_negative']=battery_negative
oneplus_reviews['battery_neutral']=battery_neutral

oneplus_reviews

overall_battery_positive_score = oneplus_reviews['battery_positive'].sum()
count = (oneplus_reviews['battery_positive'] != 0).sum()
oneplus_battery_rating= (overall_battery_positive_score/count)*5
oneplus_battery_rating

asp=['value for money', 'price', 'cost', 'affordable', 'budget', 'inexpensive']

value_for_money_negative=[]
value_for_money_neutral=[]
value_for_money_positive=[]

# Perform aspect-based sentiment analysis for each review
for review in oneplus_reviews['OnePlus_Reviews']:
  flag=0
  for aspect in asp:
    if aspect in review:
      inputs = absa_tokenizer(f"[CLS] {review} [SEP] {aspect} [SEP]", return_tensors="pt")
      outputs = absa_model(**inputs)
      probs = F.softmax(outputs.logits, dim=1)
      probs = probs.detach().numpy()[0]
      value_for_money_negative.append(probs[0])
      value_for_money_neutral.append(probs[1])
      value_for_money_positive.append(probs[2])
      flag=1
      break
  if flag==0:
    value_for_money_negative.append(0)
    value_for_money_neutral.append(0)
    value_for_money_positive.append(0)

oneplus_reviews['value_for_money_positive'] = value_for_money_positive
oneplus_reviews['value_for_money_negative'] = value_for_money_negative
oneplus_reviews['value_for_money_neutral'] = value_for_money_neutral

oneplus_reviews

overall_value_for_money_positive_score = oneplus_reviews['value_for_money_positive'].sum()
count = (oneplus_reviews['value_for_money_positive'] != 0).sum()
oneplus_value_for_money_rating= (overall_value_for_money_positive_score/count)*5
oneplus_value_for_money_rating

asp=['performance', 'speed', 'fast', 'efficient', 'smooth', 'lag', 'hang', 'overheat']
# Initialize empty lists for sentiment values
performance_negative = []
performance_neutral = []
performance_positive = []

# Perform aspect-based sentiment analysis for each review
for review in oneplus_reviews['OnePlus_Reviews']:
    flag = 0
    for aspect in asp:
        if aspect in review:
            inputs = absa_tokenizer(f"[CLS] {review} [SEP] {aspect} [SEP]", return_tensors="pt")
            outputs = absa_model(**inputs)
            probs = F.softmax(outputs.logits, dim=1)
            probs = probs.detach().numpy()[0]
            performance_negative.append(probs[0])
            performance_neutral.append(probs[1])
            performance_positive.append(probs[2])
            flag = 1
            break
    if flag == 0:
        performance_negative.append(0)
        performance_neutral.append(0)
        performance_positive.append(0)

# Replace the old columns with the new 'performance' sentiment values
oneplus_reviews['performance_negative'] = performance_negative
oneplus_reviews['performance_neutral'] = performance_neutral
oneplus_reviews['performance_positive'] = performance_positive

oneplus_reviews

overall_performance_positive_score = oneplus_reviews['performance_positive'].sum()
count = (oneplus_reviews['performance_positive'] != 0).sum()
oneplus_performance_rating= (overall_performance_positive_score/count)*5
oneplus_performance_rating

asp = ['display', 'screen', 'resolution', 'colors', 'brightness', 'quality', 'clarity', 'vivid']

# Initialize empty lists for sentiment values
display_negative = []
display_neutral = []
display_positive = []

# Perform aspect-based sentiment analysis for each review
for review in oneplus_reviews['OnePlus_Reviews']:
    flag = 0
    for aspect in asp:
        if aspect in review:
            inputs = absa_tokenizer(f"[CLS] {review} [SEP] {aspect} [SEP]", return_tensors="pt")
            outputs = absa_model(**inputs)
            probs = F.softmax(outputs.logits, dim=1)
            probs = probs.detach().numpy()[0]
            display_negative.append(probs[0])
            display_neutral.append(probs[1])
            display_positive.append(probs[2])
            flag = 1
            break
    if flag == 0:
        display_negative.append(0)
        display_neutral.append(0)
        display_positive.append(0)

# Replace the old columns with the new 'display' sentiment values
oneplus_reviews['display_negative'] = display_negative
oneplus_reviews['display_neutral'] = display_neutral
oneplus_reviews['display_positive'] = display_positive

oneplus_reviews



overall_display_positive_score = oneplus_reviews['display_positive'].sum()
count = (oneplus_reviews['display_positive'] != 0).sum()
oneplus_display_rating= (overall_display_positive_score/count)*5
oneplus_display_rating

import matplotlib.pyplot as plt

# Labels and ratings
labels = ['Camera', 'Battery', 'Value for Money', 'Display', 'Performance']
ratings = [oneplus_camera_rating, oneplus_battery_rating, oneplus_value_for_money_rating, oneplus_display_rating, oneplus_performance_rating]

# Create a bar plot
plt.figure(figsize=(10, 6))
plt.bar(labels, ratings, color=['blue', 'green', 'orange', 'purple', 'red'])
plt.title('Ratings for Different Aspects')
plt.ylabel('Rating')
plt.ylim(0, 5)
plt.show()



"""SAMSUNG GALAXY"""

samsung_reviews = df[df['Product Name'].str.contains('Samsung Galaxy', case=False)].copy()
samsung_reviews['Samsung_Reviews'] = samsung_reviews['Review']
samsung_reviews.drop(columns=['Product Name', 'Review'], inplace=True)

samsung_reviews

samsung_reviews.isnull().sum()

import re
import pandas as pd

def remove_url(text):
    text = re.sub(r"http\S+", "", text)
    return text
samsung_reviews['Samsung_Reviews'] = samsung_reviews['Samsung_Reviews'].apply(remove_url)
samsung_reviews

import pandas as pd
import unicodedata as uni
def normalize_text(text):
    return uni.normalize('NFKD', text)
samsung_reviews['Samsung_Reviews'] = samsung_reviews['Samsung_Reviews'].apply(normalize_text)
samsung_reviews

!pip install demoji

import demoji
def handle_emoji(string):
    emojis = demoji.findall(string)

    for emoji in emojis:
        string = string.replace(emoji, " " + emojis[emoji])

    return string

# Download emoji data (required before using demoji)
demoji.download_codes()

samsung_reviews['Samsung_Reviews'] =samsung_reviews['Samsung_Reviews'].apply(handle_emoji)

samsung_reviews

samsung_reviews['Samsung_Reviews'] = samsung_reviews['Samsung_Reviews'].str.replace("The media could not be loaded.\n                \n\n\n\n ", "")

pip install googletrans==4.0.0-rc1

!apt-get -qq install -y python3-langdetect

!pip install textblob

from langdetect import detect
from googletrans import Translator
from textblob import TextBlob


def detect_language(text):
    try:
        lang = detect(text)
        return lang
    except:
        return 'unknown'  # In case of an error in language detection

# Function to translate non-English text to English using Google Translate API
def translate_to_english(text):
    try:
        translator = Translator()
        translation = translator.translate(text, src='auto', dest='en')
        return translation.text
    except:
        return 'translation_failed'  # In case of an error in translation

# Function to perform spelling correction
def correct_spelling(text):
    try:
        blob = TextBlob(text)
        corrected_text = blob.correct()
        return str(corrected_text)
    except:
        return 'correction_failed'  # In case of an error in correction



# Apply language detection to the 'samsung_Reviews' column
samsung_reviews['Language'] = samsung_reviews['Samsung_Reviews'].apply(detect_language)

# Filter out non-English reviews
non_english_reviews = samsung_reviews[samsung_reviews['Language'] != 'en']

# Translate non-English reviews to English
non_english_reviews['Samsung_Reviews'] = non_english_reviews['Samsung_Reviews'].apply(translate_to_english)

# Correct spelling in the translated reviews
non_english_reviews['Samsung_Reviews'] = non_english_reviews['Samsung_Reviews'].apply(correct_spelling)

# Update the original DataFrame with translated and corrected reviews
samsung_reviews.update(non_english_reviews)
samsung_reviews.drop(columns=['Language'], inplace=True)

samsung_reviews

import nltk
nltk.download('vader_lexicon')

pip install vaderSentiment

import nltk
nltk.download('stopwords')
import nltk

# Download the 'wordnet' resource
nltk.download('wordnet')

import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Assuming you have already imported the 'samsung_reviews' DataFrame

# Lowercasing
samsung_reviews['Samsung_Reviews'] = samsung_reviews['Samsung_Reviews'].apply(lambda x: x.lower())

# Removing special characters and symbols
samsung_reviews['Samsung_Reviews'] = samsung_reviews['Samsung_Reviews'].apply(lambda x: re.sub(r'[^a-zA-Z0-9\s]', '', x))

# Stopword removal
stop_words = set(stopwords.words('english'))
samsung_reviews['Samsung_Reviews'] = samsung_reviews['Samsung_Reviews'].apply(lambda x: ' '.join([word for word in x.split() if word not in stop_words]))

# Lemmatization (optional)
lemmatizer = WordNetLemmatizer()
samsung_reviews['Samsung_Reviews'] = samsung_reviews['Samsung_Reviews'].apply(lambda x: ' '.join([lemmatizer.lemmatize(word) for word in x.split()]))

# Sentiment analysis using VADER
analyzer = SentimentIntensityAnalyzer()
sentiment_scores = samsung_reviews['Samsung_Reviews'].apply(lambda x: analyzer.polarity_scores(x))

# Extracting sentiment scores
samsung_reviews['Positive_Score'] = sentiment_scores.apply(lambda x: x['pos'])
samsung_reviews['Negative_Score'] = sentiment_scores.apply(lambda x: x['neg'])
samsung_reviews['Neutral_Score'] = sentiment_scores.apply(lambda x: x['neu'])
samsung_reviews['Compound_Score'] = sentiment_scores.apply(lambda x: x['compound'])

# Classify sentiment based on compound score
samsung_reviews['Sentiment'] = samsung_reviews['Compound_Score'].apply(lambda x: 'positive' if x >= 0.05 else ('negative' if x <= -0.05 else 'neutral'))

# Print the results
samsung_reviews

total_reviews = len(samsung_reviews)
positive_reviews = len(samsung_reviews[samsung_reviews['Compound_Score'] >= 0.05])
negative_reviews = len(samsung_reviews[samsung_reviews['Compound_Score'] <= -0.05])

positive_percentage = (positive_reviews / total_reviews) * 100
negative_percentage = (negative_reviews / total_reviews) * 100

print(f"Overall Positive Percentage: {positive_percentage:.2f}%")
print(f"Overall Negative Percentage: {negative_percentage:.2f}%")



ratings = samsung_reviews["rating"].value_counts()
numbers = ratings.index
quantity = ratings.values

import plotly.express as px
figure = px.pie(samsung_reviews,
             values=quantity,
             names=numbers,hole = 0.5)
figure.show()

import pandas as pd
import matplotlib.pyplot as plt

# Assuming you have already processed the 'samsung_reviews' DataFrame and added the 'Compound_Score' column

# Calculate overall positive and negative percentages
total_reviews = len(samsung_reviews)
positive_reviews = len(samsung_reviews[samsung_reviews['Compound_Score'] >= 0.05])
negative_reviews = len(samsung_reviews[samsung_reviews['Compound_Score'] <= -0.05])

positive_percentage = (positive_reviews / total_reviews) * 100
negative_percentage = (negative_reviews / total_reviews) * 100

# Plotting the diagram
labels = ['Positive', 'Negative']
percentages = [positive_percentage, negative_percentage]

plt.bar(labels, percentages, color=['green', 'red'])
plt.ylabel('Percentage')
plt.title('Overall Positive and Negative Percentages')
plt.ylim(0, 100)

# Annotate the bars with the percentage values
for i, v in enumerate(percentages):
    plt.text(i, v + 1, f"{v:.2f}%", ha='center', va='bottom')

plt.show()

pip install transformers[sentencepiece]

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch.nn.functional as F
from transformers import pipeline

# Load Aspect-Based Sentiment Analysis model
absa_tokenizer = AutoTokenizer.from_pretrained("yangheng/deberta-v3-base-absa-v1.1")
absa_model = AutoModelForSequenceClassification \
  .from_pretrained("yangheng/deberta-v3-base-absa-v1.1")

# Load a traditional Sentiment Analysis model
sentiment_model_path = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
sentiment_model = pipeline("sentiment-analysis", model=sentiment_model_path,
                          tokenizer=sentiment_model_path)

aspect = "camera"
camera_negative=[]
camera_neutral=[]
camera_positive=[]

# Perform aspect-based sentiment analysis for each review
for review in samsung_reviews['Samsung_Reviews']:

  if aspect in review:
    inputs = absa_tokenizer(f"[CLS] {review} [SEP] {aspect} [SEP]", return_tensors="pt")
    outputs = absa_model(**inputs)
    probs = F.softmax(outputs.logits, dim=1)
    probs = probs.detach().numpy()[0]
    camera_negative.append(probs[0])
    camera_neutral.append(probs[1])
    camera_positive.append(probs[2])
  else:
    camera_negative.append(0)
    camera_neutral.append(0)
    camera_positive.append(0)

samsung_reviews['cam_positive']=camera_positive
samsung_reviews['cam_negative']=camera_negative
samsung_reviews['cam_neutral']=camera_neutral
samsung_reviews

overall_cam_positive_score = samsung_reviews['cam_positive'].sum()
count = (samsung_reviews['cam_positive'] != 0).sum()
samsung_camera_rating= (overall_cam_positive_score/count)*5

samsung_camera_rating

aspect = "battery"
battery_negative=[]
battery_neutral=[]
battery_positive=[]

# Perform aspect-based sentiment analysis for each review
for review in samsung_reviews['Samsung_Reviews']:

  if aspect in review:
    inputs = absa_tokenizer(f"[CLS] {review} [SEP] {aspect} [SEP]", return_tensors="pt")
    outputs = absa_model(**inputs)
    probs = F.softmax(outputs.logits, dim=1)
    probs = probs.detach().numpy()[0]
    battery_negative.append(probs[0])
    battery_neutral.append(probs[1])
    battery_positive.append(probs[2])
  else:
    battery_negative.append(0)
    battery_neutral.append(0)
    battery_positive.append(0)

samsung_reviews['battery_positive']=battery_positive
samsung_reviews['battery_negative']=battery_negative
samsung_reviews['battery_neutral']=battery_neutral
samsung_reviews

overall_battery_positive_score = samsung_reviews['battery_positive'].sum()
count = (samsung_reviews['battery_positive'] != 0).sum()
samsung_battery_rating= (overall_battery_positive_score/count)*5

samsung_battery_rating

asp=['value for money', 'price', 'cost','worth', 'affordable', 'budget', 'inexpensive']

value_for_money_negative=[]
value_for_money_neutral=[]
value_for_money_positive=[]

# Perform aspect-based sentiment analysis for each review
for review in samsung_reviews['Samsung_Reviews']:
  flag=0
  for aspect in asp:
    if aspect in review:
      inputs = absa_tokenizer(f"[CLS] {review} [SEP] {aspect} [SEP]", return_tensors="pt")
      outputs = absa_model(**inputs)
      probs = F.softmax(outputs.logits, dim=1)
      probs = probs.detach().numpy()[0]
      value_for_money_negative.append(probs[0])
      value_for_money_neutral.append(probs[1])
      value_for_money_positive.append(probs[2])
      flag=1
      break
  if flag==0:
    value_for_money_negative.append(0)
    value_for_money_neutral.append(0)
    value_for_money_positive.append(0)

samsung_reviews['value_for_money_positive'] = value_for_money_positive
samsung_reviews['value_for_money_negative'] = value_for_money_negative
samsung_reviews['value_for_money_neutral'] = value_for_money_neutral
samsung_reviews

overall_value_for_money_positive_score = samsung_reviews['value_for_money_positive'].sum()
count = (samsung_reviews['value_for_money_positive'] != 0).sum()
samsung_value_for_money_rating= (overall_value_for_money_positive_score/count)*5
samsung_value_for_money_rating

asp=['performance', 'speed', 'fast', 'efficient', 'smooth', 'lag', 'hang', 'overheat']
# Initialize empty lists for sentiment values
performance_negative = []
performance_neutral = []
performance_positive = []

# Perform aspect-based sentiment analysis for each review
for review in samsung_reviews['Samsung_Reviews']:
    flag = 0
    for aspect in asp:
        if aspect in review:
            inputs = absa_tokenizer(f"[CLS] {review} [SEP] {aspect} [SEP]", return_tensors="pt")
            outputs = absa_model(**inputs)
            probs = F.softmax(outputs.logits, dim=1)
            probs = probs.detach().numpy()[0]
            performance_negative.append(probs[0])
            performance_neutral.append(probs[1])
            performance_positive.append(probs[2])
            flag = 1
            break
    if flag == 0:
        performance_negative.append(0)
        performance_neutral.append(0)
        performance_positive.append(0)

# Replace the old columns with the new 'performance' sentiment values
samsung_reviews['performance_negative'] = performance_negative
samsung_reviews['performance_neutral'] = performance_neutral
samsung_reviews['performance_positive'] = performance_positive

samsung_reviews

overall_performance_positive_score = samsung_reviews['performance_positive'].sum()
count = (samsung_reviews['performance_positive'] != 0).sum()
samsung_performance_rating= (overall_performance_positive_score/count)*5
samsung_performance_rating

asp = ['display', 'screen', 'resolution', 'colors', 'brightness', 'quality', 'clarity', 'vivid']

# Initialize empty lists for sentiment values
display_negative = []
display_neutral = []
display_positive = []

# Perform aspect-based sentiment analysis for each review
for review in samsung_reviews['Samsung_Reviews']:
    flag = 0
    for aspect in asp:
        if aspect in review:
            inputs = absa_tokenizer(f"[CLS] {review} [SEP] {aspect} [SEP]", return_tensors="pt")
            outputs = absa_model(**inputs)
            probs = F.softmax(outputs.logits, dim=1)
            probs = probs.detach().numpy()[0]
            display_negative.append(probs[0])
            display_neutral.append(probs[1])
            display_positive.append(probs[2])
            flag = 1
            break
    if flag == 0:
        display_negative.append(0)
        display_neutral.append(0)
        display_positive.append(0)

# Replace the old columns with the new 'display' sentiment values
samsung_reviews['display_negative'] = display_negative
samsung_reviews['display_neutral'] = display_neutral
samsung_reviews['display_positive'] = display_positive

samsung_reviews

overall_display_positive_score = samsung_reviews['display_positive'].sum()
count = (samsung_reviews['display_positive'] != 0).sum()
samsung_display_rating= (overall_display_positive_score/count)*5
samsung_display_rating

import matplotlib.pyplot as plt

# Labels and ratings
labels = ['Camera', 'Battery', 'Value for Money', 'Display', 'Performance']
ratings = [samsung_camera_rating, samsung_battery_rating, samsung_value_for_money_rating, samsung_display_rating, samsung_performance_rating]

# Create a bar plot
plt.figure(figsize=(10, 6))
plt.bar(labels, ratings, color=['blue', 'green', 'orange', 'purple', 'red'])
plt.title('Ratings for Different Aspects')
plt.ylabel('Rating')
plt.ylim(0, 5)
plt.show()

"""Redmi 9"""

redmi_9_reviews = df[df['Product Name'].str.contains('Redmi 9', case=False)].copy()
redmi_9_reviews['redmi_9_Reviews'] = redmi_9_reviews['Review']
redmi_9_reviews.drop(columns=['Product Name', 'Review'], inplace=True)

redmi_9_reviews

import re
import pandas as pd

def remove_url(text):
    text = re.sub(r"http\S+", "", text)
    return text
redmi_9_reviews['redmi_9_Reviews'] = redmi_9_reviews['redmi_9_Reviews'].apply(remove_url)
redmi_9_reviews

import re
import pandas as pd

def remove_url(text):
    text = re.sub(r"http\S+", "", text)
    return text
redmi_9_reviews['redmi_9_Reviews'] = redmi_9_reviews['redmi_9_Reviews'].apply(remove_url)
redmi_9_reviews

!pip install demoji

import pandas as pd
import demoji
def handle_emoji(string):
    emojis = demoji.findall(string)

    for emoji in emojis:
        string = string.replace(emoji, " " + emojis[emoji])

    return string

# Download emoji data (required before using demoji)
demoji.download_codes()


redmi_9_reviews['redmi_9_Reviews'] = redmi_9_reviews['redmi_9_Reviews'].apply(handle_emoji)

redmi_9_reviews

redmi_9_reviews['redmi_9_Reviews'] = redmi_9_reviews['redmi_9_Reviews'].str.replace("The media could not be loaded.\n                \n\n\n\n ", "")

pip install googletrans==4.0.0-rc1

!apt-get -qq install -y python3-langdetect

!pip install textblob

from langdetect import detect
from googletrans import Translator
from textblob import TextBlob


def detect_language(text):
    try:
        lang = detect(text)
        return lang
    except:
        return 'unknown'  # In case of an error in language detection

# Function to translate non-English text to English using Google Translate API
def translate_to_english(text):
    try:
        translator = Translator()
        translation = translator.translate(text, src='auto', dest='en')
        return translation.text
    except:
        return 'translation_failed'  # In case of an error in translation

# Function to perform spelling correction
def correct_spelling(text):
    try:
        blob = TextBlob(text)
        corrected_text = blob.correct()
        return str(corrected_text)
    except:
        return 'correction_failed'  # In case of an error in correction



# Apply language detection to the 'redmi_9_Reviews' column
redmi_9_reviews['Language'] = redmi_9_reviews['redmi_9_Reviews'].apply(detect_language)

# Filter out non-English reviews
non_english_reviews = redmi_9_reviews[redmi_9_reviews['Language'] != 'en']

# Translate non-English reviews to English
non_english_reviews['redmi_9_Reviews'] = non_english_reviews['redmi_9_Reviews'].apply(translate_to_english)

# Correct spelling in the translated reviews
non_english_reviews['redmi_9_Reviews'] = non_english_reviews['redmi_9_Reviews'].apply(correct_spelling)

# Update the original DataFrame with translated and corrected reviews
redmi_9_reviews.update(non_english_reviews)
redmi_9_reviews.drop(columns=['Language'], inplace=True)

redmi_9_reviews

import nltk
nltk.download('vader_lexicon')

pip install vaderSentiment

import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Assuming you have already imported the 'redmi_9_reviews' DataFrame

# Lowercasing
redmi_9_reviews['redmi_9_Reviews'] = redmi_9_reviews['redmi_9_Reviews'].apply(lambda x: x.lower())

# Removing special characters and symbols
redmi_9_reviews['redmi_9_Reviews'] = redmi_9_reviews['redmi_9_Reviews'].apply(lambda x: re.sub(r'[^a-zA-Z0-9\s]', '', x))

# Stopword removal
stop_words = set(stopwords.words('english'))
redmi_9_reviews['redmi_9_Reviews'] = redmi_9_reviews['redmi_9_Reviews'].apply(lambda x: ' '.join([word for word in x.split() if word not in stop_words]))

# Lemmatization (optional)
lemmatizer = WordNetLemmatizer()
redmi_9_reviews['redmi_9_Reviews'] = redmi_9_reviews['redmi_9_Reviews'].apply(lambda x: ' '.join([lemmatizer.lemmatize(word) for word in x.split()]))

# Sentiment analysis using VADER
analyzer = SentimentIntensityAnalyzer()
sentiment_scores = redmi_9_reviews['redmi_9_Reviews'].apply(lambda x: analyzer.polarity_scores(x))

# Extracting sentiment scores
redmi_9_reviews['Positive_Score'] = sentiment_scores.apply(lambda x: x['pos'])
redmi_9_reviews['Negative_Score'] = sentiment_scores.apply(lambda x: x['neg'])
redmi_9_reviews['Neutral_Score'] = sentiment_scores.apply(lambda x: x['neu'])
redmi_9_reviews['Compound_Score'] = sentiment_scores.apply(lambda x: x['compound'])

# Classify sentiment based on compound score
redmi_9_reviews['Sentiment'] = redmi_9_reviews['Compound_Score'].apply(lambda x: 'positive' if x >= 0.05 else ('negative' if x <= -0.05 else 'neutral'))

# Print the results
redmi_9_reviews

total_reviews = len(redmi_9_reviews)
positive_reviews = len(redmi_9_reviews[redmi_9_reviews['Compound_Score'] >= 0.05])
negative_reviews = len(redmi_9_reviews[redmi_9_reviews['Compound_Score'] <= -0.05])

positive_percentage = (positive_reviews / total_reviews) * 100
negative_percentage = (negative_reviews / total_reviews) * 100

print(f"Overall Positive Percentage: {positive_percentage:.2f}%")
print(f"Overall Negative Percentage: {negative_percentage:.2f}%")

ratings = redmi_9_reviews["rating"].value_counts()
numbers = ratings.index
quantity = ratings.values

import plotly.express as px
figure = px.pie(redmi_9_reviews,
             values=quantity,
             names=numbers,hole = 0.5)
figure.show()

import pandas as pd
import matplotlib.pyplot as plt

# Assuming you have already processed the 'redmi_9_reviews' DataFrame and added the 'Compound_Score' column

# Calculate overall positive and negative percentages
total_reviews = len(redmi_9_reviews)
positive_reviews = len(redmi_9_reviews[redmi_9_reviews['Compound_Score'] >= 0.05])
negative_reviews = len(redmi_9_reviews[redmi_9_reviews['Compound_Score'] <= -0.05])

positive_percentage = (positive_reviews / total_reviews) * 100
negative_percentage = (negative_reviews / total_reviews) * 100

# Plotting the diagram
labels = ['Positive', 'Negative']
percentages = [positive_percentage, negative_percentage]

plt.bar(labels, percentages, color=['green', 'red'])
plt.ylabel('Percentage')
plt.title('Overall Positive and Negative Percentages')
plt.ylim(0, 100)

# Annotate the bars with the percentage values
for i, v in enumerate(percentages):
    plt.text(i, v + 1, f"{v:.2f}%", ha='center', va='bottom')

plt.show()

pip install transformers[sentencepiece]

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch.nn.functional as F
from transformers import pipeline

# Load Aspect-Based Sentiment Analysis model
absa_tokenizer = AutoTokenizer.from_pretrained("yangheng/deberta-v3-base-absa-v1.1")
absa_model = AutoModelForSequenceClassification \
  .from_pretrained("yangheng/deberta-v3-base-absa-v1.1")

# Load a traditional Sentiment Analysis model
sentiment_model_path = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
sentiment_model = pipeline("sentiment-analysis", model=sentiment_model_path,
                          tokenizer=sentiment_model_path)

aspect = "camera"
camera_negative=[]
camera_neutral=[]
camera_positive=[]

# Perform aspect-based sentiment analysis for each review
for review in redmi_9_reviews['redmi_9_Reviews']:

  if aspect in review:
    inputs = absa_tokenizer(f"[CLS] {review} [SEP] {aspect} [SEP]", return_tensors="pt")
    outputs = absa_model(**inputs)
    probs = F.softmax(outputs.logits, dim=1)
    probs = probs.detach().numpy()[0]
    camera_negative.append(probs[0])
    camera_neutral.append(probs[1])
    camera_positive.append(probs[2])
  else:
    camera_negative.append(0)
    camera_neutral.append(0)
    camera_positive.append(0)

redmi_9_reviews['cam_positive']=camera_positive
redmi_9_reviews['cam_negative']=camera_negative
redmi_9_reviews['cam_neutral']=camera_neutral
redmi_9_reviews

overall_cam_positive_score = redmi_9_reviews['cam_positive'].sum()
count = (redmi_9_reviews['cam_positive'] != 0).sum()
redmi_9_camera_rating= (overall_cam_positive_score/count)*5
redmi_9_camera_rating

aspect = "battery"
battery_negative=[]
battery_neutral=[]
battery_positive=[]

# Perform aspect-based sentiment analysis for each review
for review in redmi_9_reviews['redmi_9_Reviews']:

  if aspect in review:
    inputs = absa_tokenizer(f"[CLS] {review} [SEP] {aspect} [SEP]", return_tensors="pt")
    outputs = absa_model(**inputs)
    probs = F.softmax(outputs.logits, dim=1)
    probs = probs.detach().numpy()[0]
    battery_negative.append(probs[0])
    battery_neutral.append(probs[1])
    battery_positive.append(probs[2])
  else:
    battery_negative.append(0)
    battery_neutral.append(0)
    battery_positive.append(0)

redmi_9_reviews['battery_positive']=battery_positive
redmi_9_reviews['battery_negative']=battery_negative
redmi_9_reviews['battery_neutral']=battery_neutral

overall_battery_positive_score = redmi_9_reviews['battery_positive'].sum()
count = (redmi_9_reviews['battery_positive'] != 0).sum()
redmi_9_battery_rating= (overall_battery_positive_score/count)*5
redmi_9_battery_rating

asp=['value for money', 'price', 'cost','worth', 'affordable', 'budget', 'inexpensive']

value_for_money_negative=[]
value_for_money_neutral=[]
value_for_money_positive=[]

# Perform aspect-based sentiment analysis for each review
for review in redmi_9_reviews['redmi_9_Reviews']:
  flag=0
  for aspect in asp:
    if aspect in review:
      inputs = absa_tokenizer(f"[CLS] {review} [SEP] {aspect} [SEP]", return_tensors="pt")
      outputs = absa_model(**inputs)
      probs = F.softmax(outputs.logits, dim=1)
      probs = probs.detach().numpy()[0]
      value_for_money_negative.append(probs[0])
      value_for_money_neutral.append(probs[1])
      value_for_money_positive.append(probs[2])
      flag=1
      break
  if flag==0:
    value_for_money_negative.append(0)
    value_for_money_neutral.append(0)
    value_for_money_positive.append(0)

redmi_9_reviews['value_for_money_positive'] = value_for_money_positive
redmi_9_reviews['value_for_money_negative'] = value_for_money_negative
redmi_9_reviews['value_for_money_neutral'] = value_for_money_neutral
redmi_9_reviews

overall_value_for_money_positive_score = redmi_9_reviews['value_for_money_positive'].sum()
count = (redmi_9_reviews['value_for_money_positive'] != 0).sum()
redmi_9_value_for_money_rating= (overall_value_for_money_positive_score/count)*5
redmi_9_value_for_money_rating

asp=['performance', 'speed', 'fast', 'efficient', 'smooth', 'lag', 'hang', 'overheat']
# Initialize empty lists for sentiment values
performance_negative = []
performance_neutral = []
performance_positive = []

# Perform aspect-based sentiment analysis for each review
for review in redmi_9_reviews['redmi_9_Reviews']:
    flag = 0
    for aspect in asp:
        if aspect in review:
            inputs = absa_tokenizer(f"[CLS] {review} [SEP] {aspect} [SEP]", return_tensors="pt")
            outputs = absa_model(**inputs)
            probs = F.softmax(outputs.logits, dim=1)
            probs = probs.detach().numpy()[0]
            performance_negative.append(probs[0])
            performance_neutral.append(probs[1])
            performance_positive.append(probs[2])
            flag = 1
            break
    if flag == 0:
        performance_negative.append(0)
        performance_neutral.append(0)
        performance_positive.append(0)

# Replace the old columns with the new 'performance' sentiment values
redmi_9_reviews['performance_negative'] = performance_negative
redmi_9_reviews['performance_neutral'] = performance_neutral
redmi_9_reviews['performance_positive'] = performance_positive
redmi_9_reviews

overall_performance_positive_score = redmi_9_reviews['performance_positive'].sum()
count = (redmi_9_reviews['performance_positive'] != 0).sum()
redmi_9_performance_rating= (overall_performance_positive_score/count)*5
redmi_9_performance_rating

asp = ['display', 'screen', 'resolution', 'colors', 'brightness', 'quality', 'clarity', 'vivid']

# Initialize empty lists for sentiment values
display_negative = []
display_neutral = []
display_positive = []

# Perform aspect-based sentiment analysis for each review
for review in redmi_9_reviews['redmi_9_Reviews']:
    flag = 0
    for aspect in asp:
        if aspect in review:
            inputs = absa_tokenizer(f"[CLS] {review} [SEP] {aspect} [SEP]", return_tensors="pt")
            outputs = absa_model(**inputs)
            probs = F.softmax(outputs.logits, dim=1)
            probs = probs.detach().numpy()[0]
            display_negative.append(probs[0])
            display_neutral.append(probs[1])
            display_positive.append(probs[2])
            flag = 1
            break
    if flag == 0:
        display_negative.append(0)
        display_neutral.append(0)
        display_positive.append(0)

# Replace the old columns with the new 'display' sentiment values
redmi_9_reviews['display_negative'] = display_negative
redmi_9_reviews['display_neutral'] = display_neutral
redmi_9_reviews['display_positive'] = display_positive

overall_display_positive_score = redmi_9_reviews['display_positive'].sum()
count = (redmi_9_reviews['display_positive'] != 0).sum()
redmi_9_display_rating= (overall_display_positive_score/count)*5
redmi_9_display_rating

labels = ['Camera', 'Battery', 'Value for Money', 'Display', 'Performance']
ratings = [redmi_9_camera_rating, redmi_9_battery_rating, redmi_9_value_for_money_rating, redmi_9_display_rating, redmi_9_performance_rating]

# Create a bar plot
plt.figure(figsize=(10, 6))
plt.bar(labels, ratings, color=['blue', 'green', 'orange', 'purple', 'red'])
plt.title('Ratings for Different Aspects')
plt.ylabel('Rating')
plt.ylim(0, 5)
plt.show()

"""REDMI 10 PRIME"""

# Filter Redmi 10 Prime reviews
redmi_10_prime_reviews = df[df['Product Name'].str.contains('Redmi 10 Prime', case=False)].copy()
redmi_10_prime_reviews['redmi_10_prime_Reviews'] = redmi_10_prime_reviews['Review']
redmi_10_prime_reviews.drop(columns=['Product Name', 'Review'], inplace=True)
redmi_10_prime_reviews

import re
import pandas as pd

def remove_url(text):
    text = re.sub(r"http\S+", "", text)
    return text
redmi_10_prime_reviews['redmi_10_prime_Reviews'] = redmi_10_prime_reviews['redmi_10_prime_Reviews'].apply(remove_url)
redmi_10_prime_reviews

!pip install demoji

import pandas as pd
import demoji
def handle_emoji(string):
    emojis = demoji.findall(string)

    for emoji in emojis:
        string = string.replace(emoji, " " + emojis[emoji])

    return string

# Download emoji data (required before using demoji)
demoji.download_codes()


redmi_10_prime_reviews['redmi_10_prime_Reviews'] = redmi_10_prime_reviews['redmi_10_prime_Reviews'].apply(handle_emoji)

redmi_10_prime_reviews

redmi_10_prime_reviews['redmi_10_prime_Reviews'] = redmi_10_prime_reviews['redmi_10_prime_Reviews'].str.replace("The media could not be loaded.\n                \n\n\n\n ", "")

pip install googletrans==4.0.0-rc1

!apt-get -qq install -y python3-langdetect

from langdetect import detect
from googletrans import Translator
from textblob import TextBlob


def detect_language(text):
    try:
        lang = detect(text)
        return lang
    except:
        return 'unknown'  # In case of an error in language detection

# Function to translate non-English text to English using Google Translate API
def translate_to_english(text):
    try:
        translator = Translator()
        translation = translator.translate(text, src='auto', dest='en')
        return translation.text
    except:
        return 'translation_failed'  # In case of an error in translation

# Function to perform spelling correction
def correct_spelling(text):
    try:
        blob = TextBlob(text)
        corrected_text = blob.correct()
        return str(corrected_text)
    except:
        return 'correction_failed'  # In case of an error in correction



# Apply language detection to the 'redmi_10_prime_Reviews' column
redmi_10_prime_reviews['Language'] = redmi_10_prime_reviews['redmi_10_prime_Reviews'].apply(detect_language)

# Filter out non-English reviews
non_english_reviews = redmi_10_prime_reviews[redmi_10_prime_reviews['Language'] != 'en']

# Translate non-English reviews to English
non_english_reviews['redmi_10_prime_Reviews'] = non_english_reviews['redmi_10_prime_Reviews'].apply(translate_to_english)

# Correct spelling in the translated reviews
non_english_reviews['redmi_10_prime_Reviews'] = non_english_reviews['redmi_10_prime_Reviews'].apply(correct_spelling)

# Update the original DataFrame with translated and corrected reviews
redmi_10_prime_reviews.update(non_english_reviews)
redmi_10_prime_reviews.drop(columns=['Language'], inplace=True)

redmi_10_prime_reviews

import nltk
nltk.download('vader_lexicon')

pip install vaderSentiment

import nltk
nltk.download('stopwords')

nltk.download('wordnet')

import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Assuming you have already imported the 'redmi_10_prime_reviews' DataFrame

# Lowercasing
redmi_10_prime_reviews['redmi_10_prime_Reviews'] = redmi_10_prime_reviews['redmi_10_prime_Reviews'].apply(lambda x: x.lower())

# Removing special characters and symbols
redmi_10_prime_reviews['redmi_10_prime_Reviews'] = redmi_10_prime_reviews['redmi_10_prime_Reviews'].apply(lambda x: re.sub(r'[^a-zA-Z0-9\s]', '', x))

# Stopword removal
stop_words = set(stopwords.words('english'))
redmi_10_prime_reviews['redmi_10_prime_Reviews'] = redmi_10_prime_reviews['redmi_10_prime_Reviews'].apply(lambda x: ' '.join([word for word in x.split() if word not in stop_words]))

# Lemmatization (optional)
lemmatizer = WordNetLemmatizer()
redmi_10_prime_reviews['redmi_10_prime_Reviews'] = redmi_10_prime_reviews['redmi_10_prime_Reviews'].apply(lambda x: ' '.join([lemmatizer.lemmatize(word) for word in x.split()]))

# Sentiment analysis using VADER
analyzer = SentimentIntensityAnalyzer()
sentiment_scores = redmi_10_prime_reviews['redmi_10_prime_Reviews'].apply(lambda x: analyzer.polarity_scores(x))

# Extracting sentiment scores
redmi_10_prime_reviews['Positive_Score'] = sentiment_scores.apply(lambda x: x['pos'])
redmi_10_prime_reviews['Negative_Score'] = sentiment_scores.apply(lambda x: x['neg'])
redmi_10_prime_reviews['Neutral_Score'] = sentiment_scores.apply(lambda x: x['neu'])
redmi_10_prime_reviews['Compound_Score'] = sentiment_scores.apply(lambda x: x['compound'])

# Classify sentiment based on compound score
redmi_10_prime_reviews['Sentiment'] = redmi_10_prime_reviews['Compound_Score'].apply(lambda x: 'positive' if x >= 0.05 else ('negative' if x <= -0.05 else 'neutral'))

# Print the results
redmi_10_prime_reviews

total_reviews = len(redmi_10_prime_reviews)
positive_reviews = len(redmi_10_prime_reviews[redmi_10_prime_reviews['Compound_Score'] >= 0.05])
negative_reviews = len(redmi_10_prime_reviews[redmi_10_prime_reviews['Compound_Score'] <= -0.05])

positive_percentage = (positive_reviews / total_reviews) * 100
negative_percentage = (negative_reviews / total_reviews) * 100

print(f"Overall Positive Percentage: {positive_percentage:.2f}%")
print(f"Overall Negative Percentage: {negative_percentage:.2f}%")

ratings = redmi_10_prime_reviews["rating"].value_counts()
numbers = ratings.index
quantity = ratings.values

import plotly.express as px
figure = px.pie(redmi_10_prime_reviews,
             values=quantity,
             names=numbers,hole = 0.5)
figure.show()

import pandas as pd
import matplotlib.pyplot as plt

total_reviews = len(redmi_10_prime_reviews)
positive_reviews = len(redmi_10_prime_reviews[redmi_10_prime_reviews['Compound_Score'] >= 0.05])
negative_reviews = len(redmi_10_prime_reviews[redmi_10_prime_reviews['Compound_Score'] <= -0.05])

positive_percentage = (positive_reviews / total_reviews) * 100
negative_percentage = (negative_reviews / total_reviews) * 100

# Plotting the diagram
labels = ['Positive', 'Negative']
percentages = [positive_percentage, negative_percentage]

plt.bar(labels, percentages, color=['green', 'red'])
plt.ylabel('Percentage')
plt.title('Overall Positive and Negative Percentages')
plt.ylim(0, 100)

# Annotate the bars with the percentage values
for i, v in enumerate(percentages):
    plt.text(i, v + 1, f"{v:.2f}%", ha='center', va='bottom')

plt.show()

pip install transformers[sentencepiece]

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch.nn.functional as F
from transformers import pipeline

# Load Aspect-Based Sentiment Analysis model
absa_tokenizer = AutoTokenizer.from_pretrained("yangheng/deberta-v3-base-absa-v1.1")
absa_model = AutoModelForSequenceClassification \
  .from_pretrained("yangheng/deberta-v3-base-absa-v1.1")

# Load a traditional Sentiment Analysis model
sentiment_model_path = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
sentiment_model = pipeline("sentiment-analysis", model=sentiment_model_path,
                          tokenizer=sentiment_model_path)

aspect = "camera"
camera_negative=[]
camera_neutral=[]
camera_positive=[]

# Perform aspect-based sentiment analysis for each review
for review in redmi_10_prime_reviews['redmi_10_prime_Reviews']:

  if aspect in review:
    inputs = absa_tokenizer(f"[CLS] {review} [SEP] {aspect} [SEP]", return_tensors="pt")
    outputs = absa_model(**inputs)
    probs = F.softmax(outputs.logits, dim=1)
    probs = probs.detach().numpy()[0]
    camera_negative.append(probs[0])
    camera_neutral.append(probs[1])
    camera_positive.append(probs[2])
  else:
    camera_negative.append(0)
    camera_neutral.append(0)
    camera_positive.append(0)

redmi_10_prime_reviews['cam_positive']=camera_positive
redmi_10_prime_reviews['cam_negative']=camera_negative
redmi_10_prime_reviews['cam_neutral']=camera_neutral

redmi_10_prime_reviews

overall_cam_positive_score = redmi_10_prime_reviews['cam_positive'].sum()
count = (redmi_10_prime_reviews['cam_positive'] != 0).sum()
redmi_10_prime_camera_rating= (overall_cam_positive_score/count)*5
redmi_10_prime_camera_rating

asp=['value for money', 'price', 'cost','worth', 'affordable', 'budget', 'inexpensive']

value_for_money_negative=[]
value_for_money_neutral=[]
value_for_money_positive=[]

# Perform aspect-based sentiment analysis for each review
for review in redmi_10_prime_reviews['redmi_10_prime_Reviews']:
  flag=0
  for aspect in asp:
    if aspect in review:
      inputs = absa_tokenizer(f"[CLS] {review} [SEP] {aspect} [SEP]", return_tensors="pt")
      outputs = absa_model(**inputs)
      probs = F.softmax(outputs.logits, dim=1)
      probs = probs.detach().numpy()[0]
      value_for_money_negative.append(probs[0])
      value_for_money_neutral.append(probs[1])
      value_for_money_positive.append(probs[2])
      flag=1
      break
  if flag==0:
    value_for_money_negative.append(0)
    value_for_money_neutral.append(0)
    value_for_money_positive.append(0)

redmi_10_prime_reviews['value_for_money_positive'] = value_for_money_positive
redmi_10_prime_reviews['value_for_money_negative'] = value_for_money_negative
redmi_10_prime_reviews['value_for_money_neutral'] = value_for_money_neutral
redmi_10_prime_reviews

overall_value_for_money_positive_score = redmi_10_prime_reviews['value_for_money_positive'].sum()
count = (redmi_10_prime_reviews['value_for_money_positive'] != 0).sum()
redmi_10_prime_value_for_money_rating= (overall_value_for_money_positive_score/count)*5
redmi_10_prime_value_for_money_rating

aspect = "battery"
battery_negative=[]
battery_neutral=[]
battery_positive=[]

# Perform aspect-based sentiment analysis for each review
for review in redmi_10_prime_reviews['redmi_10_prime_Reviews']:

  if aspect in review:
    inputs = absa_tokenizer(f"[CLS] {review} [SEP] {aspect} [SEP]", return_tensors="pt")
    outputs = absa_model(**inputs)
    probs = F.softmax(outputs.logits, dim=1)
    probs = probs.detach().numpy()[0]
    battery_negative.append(probs[0])
    battery_neutral.append(probs[1])
    battery_positive.append(probs[2])
  else:
    battery_negative.append(0)
    battery_neutral.append(0)
    battery_positive.append(0)
redmi_10_prime_reviews['battery_positive']=battery_positive
redmi_10_prime_reviews['battery_negative']=battery_negative
redmi_10_prime_reviews['battery_neutral']=battery_neutral

overall_battery_positive_score = redmi_10_prime_reviews['battery_positive'].sum()
count = (redmi_10_prime_reviews['battery_positive'] != 0).sum()
redmi_10_prime_battery_rating= (overall_battery_positive_score/count)*5
redmi_10_prime_battery_rating

asp=['performance', 'speed', 'fast', 'efficient', 'smooth', 'lag', 'hang', 'overheat']
# Initialize empty lists for sentiment values
performance_negative = []
performance_neutral = []
performance_positive = []

# Perform aspect-based sentiment analysis for each review
for review in redmi_10_prime_reviews['redmi_10_prime_Reviews']:
    flag = 0
    for aspect in asp:
        if aspect in review:
            inputs = absa_tokenizer(f"[CLS] {review} [SEP] {aspect} [SEP]", return_tensors="pt")
            outputs = absa_model(**inputs)
            probs = F.softmax(outputs.logits, dim=1)
            probs = probs.detach().numpy()[0]
            performance_negative.append(probs[0])
            performance_neutral.append(probs[1])
            performance_positive.append(probs[2])
            flag = 1
            break
    if flag == 0:
        performance_negative.append(0)
        performance_neutral.append(0)
        performance_positive.append(0)

# Replace the old columns with the new 'performance' sentiment values
redmi_10_prime_reviews['performance_negative'] = performance_negative
redmi_10_prime_reviews['performance_neutral'] = performance_neutral
redmi_10_prime_reviews['performance_positive'] = performance_positive

overall_performance_positive_score = redmi_10_prime_reviews['performance_positive'].sum()
count = (redmi_10_prime_reviews['performance_positive'] != 0).sum()
redmi_10_prime_performance_rating= (overall_performance_positive_score/count)*5
redmi_10_prime_performance_rating

asp = ['display', 'screen', 'resolution', 'colors', 'brightness', 'quality', 'clarity', 'vivid']

# Initialize empty lists for sentiment values
display_negative = []
display_neutral = []
display_positive = []

# Perform aspect-based sentiment analysis for each review
for review in redmi_10_prime_reviews['redmi_10_prime_Reviews']:
    flag = 0
    for aspect in asp:
        if aspect in review:
            inputs = absa_tokenizer(f"[CLS] {review} [SEP] {aspect} [SEP]", return_tensors="pt")
            outputs = absa_model(**inputs)
            probs = F.softmax(outputs.logits, dim=1)
            probs = probs.detach().numpy()[0]
            display_negative.append(probs[0])
            display_neutral.append(probs[1])
            display_positive.append(probs[2])
            flag = 1
            break
    if flag == 0:
        display_negative.append(0)
        display_neutral.append(0)
        display_positive.append(0)

# Replace the old columns with the new 'display' sentiment values
redmi_10_prime_reviews['display_negative'] = display_negative
redmi_10_prime_reviews['display_neutral'] = display_neutral
redmi_10_prime_reviews['display_positive'] = display_positive
redmi_10_prime_reviews

overall_display_positive_score = redmi_10_prime_reviews['display_positive'].sum()
count = (redmi_10_prime_reviews['display_positive'] != 0).sum()
redmi_10_prime_display_rating= (overall_display_positive_score/count)*5
redmi_10_prime_display_rating

import matplotlib.pyplot as plt

# Labels and ratings
labels = ['Camera', 'Battery', 'Value for Money', 'Display', 'Performance']
ratings = [redmi_10_prime_camera_rating, redmi_10_prime_battery_rating, redmi_10_prime_value_for_money_rating, redmi_10_prime_display_rating, redmi_10_prime_performance_rating]

# Create a bar plot
plt.figure(figsize=(10, 6))
plt.bar(labels, ratings, color=['blue', 'green', 'orange', 'purple', 'red'])
plt.title('Ratings for Different Aspects')
plt.ylabel('Rating')
plt.ylim(0, 5)
plt.show()

"""OPPO A31 MOBILES"""

# Filter OPPO A31 mobile reviews
oppo_A31_reviews = df[df['Product Name'].str.contains('OPPO A31', case=False)].copy()
oppo_A31_reviews['oppo_A31_Reviews'] = oppo_A31_reviews['Review']
oppo_A31_reviews.drop(columns=['Product Name', 'Review'], inplace=True)

oppo_A31_reviews

oppo_A31_reviews.isnull().sum

import re
import pandas as pd

def remove_url(text):
    text = re.sub(r"http\S+", "", text)
    return text
oppo_A31_reviews['oppo_A31_Reviews'] = oppo_A31_reviews['oppo_A31_Reviews'].apply(remove_url)
oppo_A31_reviews

!pip install demoji

import pandas as pd
import demoji
def handle_emoji(string):
    emojis = demoji.findall(string)

    for emoji in emojis:
        string = string.replace(emoji, " " + emojis[emoji])

    return string

# Download emoji data (required before using demoji)
demoji.download_codes()


oppo_A31_reviews['oppo_A31_Reviews'] = oppo_A31_reviews['oppo_A31_Reviews'].apply(handle_emoji)

oppo_A31_reviews

oppo_A31_reviews['oppo_A31_Reviews'] = oppo_A31_reviews['oppo_A31_Reviews'].str.replace("The media could not be loaded.\n                \n\n\n\n ", "")

pip install googletrans==4.0.0-rc1

!apt-get -qq install -y python3-langdetect

from langdetect import detect
from googletrans import Translator
from textblob import TextBlob


def detect_language(text):
    try:
        lang = detect(text)
        return lang
    except:
        return 'unknown'  # In case of an error in language detection

# Function to translate non-English text to English using Google Translate API
def translate_to_english(text):
    try:
        translator = Translator()
        translation = translator.translate(text, src='auto', dest='en')
        return translation.text
    except:
        return 'translation_failed'  # In case of an error in translation

# Function to perform spelling correction
def correct_spelling(text):
    try:
        blob = TextBlob(text)
        corrected_text = blob.correct()
        return str(corrected_text)
    except:
        return 'correction_failed'  # In case of an error in correction



# Apply language detection to the 'oppo_A31_Reviews' column
oppo_A31_reviews['Language'] = oppo_A31_reviews['oppo_A31_Reviews'].apply(detect_language)

# Filter out non-English reviews
non_english_reviews = oppo_A31_reviews[oppo_A31_reviews['Language'] != 'en']

# Translate non-English reviews to English
non_english_reviews['oppo_A31_Reviews'] = non_english_reviews['oppo_A31_Reviews'].apply(translate_to_english)

# Correct spelling in the translated reviews
non_english_reviews['oppo_A31_Reviews'] = non_english_reviews['oppo_A31_Reviews'].apply(correct_spelling)

# Update the original DataFrame with translated and corrected reviews
oppo_A31_reviews.update(non_english_reviews)
oppo_A31_reviews.drop(columns=['Language'], inplace=True)

oppo_A31_reviews

import nltk
nltk.download('vader_lexicon')

pip install vaderSentiment

import nltk
nltk.download('stopwords')

import nltk

# Download the 'wordnet' resource
nltk.download('wordnet')

import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Assuming you have already imported the 'oppo_A31_reviews' DataFrame

# Lowercasing
oppo_A31_reviews['oppo_A31_Reviews'] = oppo_A31_reviews['oppo_A31_Reviews'].apply(lambda x: x.lower())

# Removing special characters and symbols
oppo_A31_reviews['oppo_A31_Reviews'] = oppo_A31_reviews['oppo_A31_Reviews'].apply(lambda x: re.sub(r'[^a-zA-Z0-9\s]', '', x))

# Stopword removal
stop_words = set(stopwords.words('english'))
oppo_A31_reviews['oppo_A31_Reviews'] = oppo_A31_reviews['oppo_A31_Reviews'].apply(lambda x: ' '.join([word for word in x.split() if word not in stop_words]))

# Lemmatization (optional)
lemmatizer = WordNetLemmatizer()
oppo_A31_reviews['oppo_A31_Reviews'] = oppo_A31_reviews['oppo_A31_Reviews'].apply(lambda x: ' '.join([lemmatizer.lemmatize(word) for word in x.split()]))

# Sentiment analysis using VADER
analyzer = SentimentIntensityAnalyzer()
sentiment_scores = oppo_A31_reviews['oppo_A31_Reviews'].apply(lambda x: analyzer.polarity_scores(x))

# Extracting sentiment scores
oppo_A31_reviews['Positive_Score'] = sentiment_scores.apply(lambda x: x['pos'])
oppo_A31_reviews['Negative_Score'] = sentiment_scores.apply(lambda x: x['neg'])
oppo_A31_reviews['Neutral_Score'] = sentiment_scores.apply(lambda x: x['neu'])
oppo_A31_reviews['Compound_Score'] = sentiment_scores.apply(lambda x: x['compound'])

# Classify sentiment based on compound score
oppo_A31_reviews['Sentiment'] = oppo_A31_reviews['Compound_Score'].apply(lambda x: 'positive' if x >= 0.05 else ('negative' if x <= -0.05 else 'neutral'))

# Print the results
oppo_A31_reviews

total_reviews = len(oppo_A31_reviews)
positive_reviews = len(oppo_A31_reviews[oppo_A31_reviews['Compound_Score'] >= 0.05])
negative_reviews = len(oppo_A31_reviews[oppo_A31_reviews['Compound_Score'] <= -0.05])

positive_percentage = (positive_reviews / total_reviews) * 100
negative_percentage = (negative_reviews / total_reviews) * 100

print(f"Overall Positive Percentage: {positive_percentage:.2f}%")
print(f"Overall Negative Percentage: {negative_percentage:.2f}%")

ratings = oppo_A31_reviews["rating"].value_counts()
numbers = ratings.index
quantity = ratings.values

import plotly.express as px
figure = px.pie(oppo_A31_reviews,
             values=quantity,
             names=numbers,hole = 0.5)
figure.show()

import pandas as pd
import matplotlib.pyplot as plt

# Assuming you have already processed the 'oppo_A31_reviews' DataFrame and added the 'Compound_Score' column

# Calculate overall positive and negative percentages
total_reviews = len(oppo_A31_reviews)
positive_reviews = len(oppo_A31_reviews[oppo_A31_reviews['Compound_Score'] >= 0.05])
negative_reviews = len(oppo_A31_reviews[oppo_A31_reviews['Compound_Score'] <= -0.05])

positive_percentage = (positive_reviews / total_reviews) * 100
negative_percentage = (negative_reviews / total_reviews) * 100

# Plotting the diagram
labels = ['Positive', 'Negative']
percentages = [positive_percentage, negative_percentage]

plt.bar(labels, percentages, color=['green', 'red'])
plt.ylabel('Percentage')
plt.title('Overall Positive and Negative Percentages')
plt.ylim(0, 100)

# Annotate the bars with the percentage values
for i, v in enumerate(percentages):
    plt.text(i, v + 1, f"{v:.2f}%", ha='center', va='bottom')

plt.show()

pip install transformers[sentencepiece]

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch.nn.functional as F
from transformers import pipeline

# Load Aspect-Based Sentiment Analysis model
absa_tokenizer = AutoTokenizer.from_pretrained("yangheng/deberta-v3-base-absa-v1.1")
absa_model = AutoModelForSequenceClassification \
  .from_pretrained("yangheng/deberta-v3-base-absa-v1.1")

# Load a traditional Sentiment Analysis model
sentiment_model_path = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
sentiment_model = pipeline("sentiment-analysis", model=sentiment_model_path,
                          tokenizer=sentiment_model_path)

aspect = "camera"
camera_negative=[]
camera_neutral=[]
camera_positive=[]

# Perform aspect-based sentiment analysis for each review
for review in oppo_A31_reviews['oppo_A31_Reviews']:

  if aspect in review:
    inputs = absa_tokenizer(f"[CLS] {review} [SEP] {aspect} [SEP]", return_tensors="pt")
    outputs = absa_model(**inputs)
    probs = F.softmax(outputs.logits, dim=1)
    probs = probs.detach().numpy()[0]
    camera_negative.append(probs[0])
    camera_neutral.append(probs[1])
    camera_positive.append(probs[2])
  else:
    camera_negative.append(0)
    camera_neutral.append(0)
    camera_positive.append(0)

oppo_A31_reviews['cam_positive']=camera_positive
oppo_A31_reviews['cam_negative']=camera_negative
oppo_A31_reviews['cam_neutral']=camera_neutral

oppo_A31_reviews

aspect = "battery"
battery_negative=[]
battery_neutral=[]
battery_positive=[]

# Perform aspect-based sentiment analysis for each review
for review in oppo_A31_reviews['oppo_A31_Reviews']:

  if aspect in review:
    inputs = absa_tokenizer(f"[CLS] {review} [SEP] {aspect} [SEP]", return_tensors="pt")
    outputs = absa_model(**inputs)
    probs = F.softmax(outputs.logits, dim=1)
    probs = probs.detach().numpy()[0]
    battery_negative.append(probs[0])
    battery_neutral.append(probs[1])
    battery_positive.append(probs[2])
  else:
    battery_negative.append(0)
    battery_neutral.append(0)
    battery_positive.append(0)
oppo_A31_reviews['battery_positive']=battery_positive
oppo_A31_reviews['battery_negative']=battery_negative
oppo_A31_reviews['battery_neutral']=battery_neutral

oppo_A31_reviews

asp=['value for money', 'price', 'cost','worth', 'affordable', 'budget', 'inexpensive']

value_for_money_negative=[]
value_for_money_neutral=[]
value_for_money_positive=[]

# Perform aspect-based sentiment analysis for each review
for review in oppo_A31_reviews['oppo_A31_Reviews']:
  flag=0
  for aspect in asp:
    if aspect in review:
      inputs = absa_tokenizer(f"[CLS] {review} [SEP] {aspect} [SEP]", return_tensors="pt")
      outputs = absa_model(**inputs)
      probs = F.softmax(outputs.logits, dim=1)
      probs = probs.detach().numpy()[0]
      value_for_money_negative.append(probs[0])
      value_for_money_neutral.append(probs[1])
      value_for_money_positive.append(probs[2])
      flag=1
      break
  if flag==0:
    value_for_money_negative.append(0)
    value_for_money_neutral.append(0)
    value_for_money_positive.append(0)

oppo_A31_reviews['value_for_money_positive'] = value_for_money_positive
oppo_A31_reviews['value_for_money_negative'] = value_for_money_negative
oppo_A31_reviews['value_for_money_neutral'] = value_for_money_neutral
oppo_A31_reviews

asp=['performance', 'speed', 'fast', 'efficient', 'smooth', 'lag', 'hang', 'overheat']
# Initialize empty lists for sentiment values
performance_negative = []
performance_neutral = []
performance_positive = []

# Perform aspect-based sentiment analysis for each review
for review in oppo_A31_reviews['oppo_A31_Reviews']:
    flag = 0
    for aspect in asp:
        if aspect in review:
            inputs = absa_tokenizer(f"[CLS] {review} [SEP] {aspect} [SEP]", return_tensors="pt")
            outputs = absa_model(**inputs)
            probs = F.softmax(outputs.logits, dim=1)
            probs = probs.detach().numpy()[0]
            performance_negative.append(probs[0])
            performance_neutral.append(probs[1])
            performance_positive.append(probs[2])
            flag = 1
            break
    if flag == 0:
        performance_negative.append(0)
        performance_neutral.append(0)
        performance_positive.append(0)

# Replace the old columns with the new 'performance' sentiment values
oppo_A31_reviews['performance_negative'] = performance_negative
oppo_A31_reviews['performance_neutral'] = performance_neutral
oppo_A31_reviews['performance_positive'] = performance_positive

oppo_A31_reviews

asp = ['display', 'screen', 'resolution', 'colors', 'brightness', 'quality', 'clarity', 'vivid']

# Initialize empty lists for sentiment values
display_negative = []
display_neutral = []
display_positive = []

# Perform aspect-based sentiment analysis for each review
for review in oppo_A31_reviews['oppo_A31_Reviews']:
    flag = 0
    for aspect in asp:
        if aspect in review:
            inputs = absa_tokenizer(f"[CLS] {review} [SEP] {aspect} [SEP]", return_tensors="pt")
            outputs = absa_model(**inputs)
            probs = F.softmax(outputs.logits, dim=1)
            probs = probs.detach().numpy()[0]
            display_negative.append(probs[0])
            display_neutral.append(probs[1])
            display_positive.append(probs[2])
            flag = 1
            break
    if flag == 0:
        display_negative.append(0)
        display_neutral.append(0)
        display_positive.append(0)

# Replace the old columns with the new 'display' sentiment values
oppo_A31_reviews['display_negative'] = display_negative
oppo_A31_reviews['display_neutral'] = display_neutral
oppo_A31_reviews['display_positive'] = display_positive

oppo_A31_reviews

overall_cam_positive_score = oppo_A31_reviews['cam_positive'].sum()
count = (oppo_A31_reviews['cam_positive'] != 0).sum()
camera_rating= (overall_cam_positive_score/count)*5

camera_rating

overall_battery_positive_score = oppo_A31_reviews['battery_positive'].sum()
count = (oppo_A31_reviews['battery_positive'] != 0).sum()
battery_rating= (overall_battery_positive_score/count)*5

battery_rating

overall_display_positive_score = oppo_A31_reviews['display_positive'].sum()
count = (oppo_A31_reviews['display_positive'] != 0).sum()
display_rating= (overall_display_positive_score/count)*5
display_rating

overall_value_for_money_positive_score = oppo_A31_reviews['value_for_money_positive'].sum()
count = (oppo_A31_reviews['value_for_money_positive'] != 0).sum()
value_for_money_rating= (overall_value_for_money_positive_score/count)*5
value_for_money_rating

overall_performance_positive_score = oppo_A31_reviews['performance_positive'].sum()
count = (oppo_A31_reviews['performance_positive'] != 0).sum()
performance_rating= (overall_performance_positive_score/count)*5
performance_rating

import matplotlib.pyplot as plt

# Labels and ratings
labels = ['Camera', 'Battery', 'Value for Money', 'Display', 'Performance']
ratings = [oppo_A31_camera_rating, oppo_A31_battery_rating, oppo_A31_value_for_money_rating, oppo_A31_display_rating, oppo_A31_performance_rating]

# Create a bar plot
plt.figure(figsize=(10, 6))
plt.bar(labels, ratings, color=['blue', 'green', 'orange', 'purple', 'red'])
plt.title('Ratings for Different Aspects')
plt.ylabel('Rating')
plt.ylim(0, 5)
plt.show()

"""Redmi Note 11"""

# Filter Redmi Note 11 reviews
redmi_note_11_reviews = df[df['Product Name'].str.contains('Redmi Note 11', case=False)].copy()
redmi_note_11_reviews['redmi_note_11_Reviews'] = redmi_note_11_reviews['Review']
redmi_note_11_reviews.drop(columns=['Product Name', 'Review'], inplace=True)
redmi_note_11_reviews

redmi_note_11_reviews.isnull().sum()

import re
import pandas as pd

def remove_url(text):
    text = re.sub(r"http\S+", "", text)
    return text
redmi_note_11_reviews['redmi_note_11_Reviews'] = redmi_note_11_reviews['redmi_note_11_Reviews'].apply(remove_url)
redmi_note_11_reviews

import pandas as pd
import unicodedata as uni
def normalize_text(text):
    return uni.normalize('NFKD', text)
redmi_note_11_reviews['redmi_note_11_Reviews'] = redmi_note_11_reviews['redmi_note_11_Reviews'].apply(normalize_text)
redmi_note_11_reviews

!pip install demoji

import pandas as pd
import demoji
def handle_emoji(string):
    emojis = demoji.findall(string)

    for emoji in emojis:
        string = string.replace(emoji, " " + emojis[emoji])

    return string

# Download emoji data (required before using demoji)
demoji.download_codes()


redmi_note_11_reviews['redmi_note_11_Reviews'] = redmi_note_11_reviews['redmi_note_11_Reviews'].apply(handle_emoji)

print(redmi_note_11_reviews)

redmi_note_11_reviews['redmi_note_11_Reviews'] = redmi_note_11_reviews['redmi_note_11_Reviews'].str.replace("The media could not be loaded.\n                \n\n\n\n ", "")

pip install googletrans==4.0.0-rc1

!apt-get -qq install -y python3-langdetect

!pip install textblob

from langdetect import detect
from googletrans import Translator
from textblob import TextBlob


def detect_language(text):
    try:
        lang = detect(text)
        return lang
    except:
        return 'unknown'  # In case of an error in language detection

# Function to translate non-English text to English using Google Translate API
def translate_to_english(text):
    try:
        translator = Translator()
        translation = translator.translate(text, src='auto', dest='en')
        return translation.text
    except:
        return 'translation_failed'  # In case of an error in translation

# Function to perform spelling correction
def correct_spelling(text):
    try:
        blob = TextBlob(text)
        corrected_text = blob.correct()
        return str(corrected_text)
    except:
        return 'correction_failed'  # In case of an error in correction



# Apply language detection to the 'redmi_note_11_Reviews' column
redmi_note_11_reviews['Language'] = redmi_note_11_reviews['redmi_note_11_Reviews'].apply(detect_language)

# Filter out non-English reviews
non_english_reviews = redmi_note_11_reviews[redmi_note_11_reviews['Language'] != 'en']

# Translate non-English reviews to English
non_english_reviews['redmi_note_11_Reviews'] = non_english_reviews['redmi_note_11_Reviews'].apply(translate_to_english)

# Correct spelling in the translated reviews
non_english_reviews['redmi_note_11_Reviews'] = non_english_reviews['redmi_note_11_Reviews'].apply(correct_spelling)

# Update the original DataFrame with translated and corrected reviews
redmi_note_11_reviews.update(non_english_reviews)
redmi_note_11_reviews.drop(columns=['Language'], inplace=True)

redmi_note_11_reviews



import nltk
nltk.download('vader_lexicon')

pip install vaderSentiment

import nltk
nltk.download('stopwords')

import nltk

# Download the 'wordnet' resource
nltk.download('wordnet')

import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Assuming you have already imported the 'redmi_note_11_reviews' DataFrame

# Lowercasing
redmi_note_11_reviews['redmi_note_11_Reviews'] = redmi_note_11_reviews['redmi_note_11_Reviews'].apply(lambda x: x.lower())

# Removing special characters and symbols
redmi_note_11_reviews['redmi_note_11_Reviews'] = redmi_note_11_reviews['redmi_note_11_Reviews'].apply(lambda x: re.sub(r'[^a-zA-Z0-9\s]', '', x))

# Stopword removal
stop_words = set(stopwords.words('english'))
redmi_note_11_reviews['redmi_note_11_Reviews'] = redmi_note_11_reviews['redmi_note_11_Reviews'].apply(lambda x: ' '.join([word for word in x.split() if word not in stop_words]))

# Lemmatization (optional)
lemmatizer = WordNetLemmatizer()
redmi_note_11_reviews['redmi_note_11_Reviews'] = redmi_note_11_reviews['redmi_note_11_Reviews'].apply(lambda x: ' '.join([lemmatizer.lemmatize(word) for word in x.split()]))

# Sentiment analysis using VADER
analyzer = SentimentIntensityAnalyzer()
sentiment_scores = redmi_note_11_reviews['redmi_note_11_Reviews'].apply(lambda x: analyzer.polarity_scores(x))

# Extracting sentiment scores
redmi_note_11_reviews['Positive_Score'] = sentiment_scores.apply(lambda x: x['pos'])
redmi_note_11_reviews['Negative_Score'] = sentiment_scores.apply(lambda x: x['neg'])
redmi_note_11_reviews['Neutral_Score'] = sentiment_scores.apply(lambda x: x['neu'])
redmi_note_11_reviews['Compound_Score'] = sentiment_scores.apply(lambda x: x['compound'])

# Classify sentiment based on compound score
redmi_note_11_reviews['Sentiment'] = redmi_note_11_reviews['Compound_Score'].apply(lambda x: 'positive' if x >= 0.05 else ('negative' if x <= -0.05 else 'neutral'))

# Print the results
redmi_note_11_reviews

total_reviews = len(redmi_note_11_reviews)
positive_reviews = len(redmi_note_11_reviews[redmi_note_11_reviews['Compound_Score'] >= 0.05])
negative_reviews = len(redmi_note_11_reviews[redmi_note_11_reviews['Compound_Score'] <= -0.05])

positive_percentage = (positive_reviews / total_reviews) * 100
negative_percentage = (negative_reviews / total_reviews) * 100

print(f"Overall Positive Percentage: {positive_percentage:.2f}%")
print(f"Overall Negative Percentage: {negative_percentage:.2f}%")

ratings = redmi_note_11_reviews["rating"].value_counts()
numbers = ratings.index
quantity = ratings.values

import plotly.express as px
figure = px.pie(redmi_note_11_reviews,
             values=quantity,
             names=numbers,hole = 0.5)
figure.show()

pip install matplotlib

import pandas as pd
import matplotlib.pyplot as plt

# Assuming you have already processed the 'redmi_note_11_reviews' DataFrame and added the 'Compound_Score' column

# Calculate overall positive and negative percentages
total_reviews = len(redmi_note_11_reviews)
positive_reviews = len(redmi_note_11_reviews[redmi_note_11_reviews['Compound_Score'] >= 0.05])
negative_reviews = len(redmi_note_11_reviews[redmi_note_11_reviews['Compound_Score'] <= -0.05])

positive_percentage = (positive_reviews / total_reviews) * 100
negative_percentage = (negative_reviews / total_reviews) * 100

# Plotting the diagram
labels = ['Positive', 'Negative']
percentages = [positive_percentage, negative_percentage]

plt.bar(labels, percentages, color=['green', 'red'])
plt.ylabel('Percentage')
plt.title('Overall Positive and Negative Percentages')
plt.ylim(0, 100)

# Annotate the bars with the percentage values
for i, v in enumerate(percentages):
    plt.text(i, v + 1, f"{v:.2f}%", ha='center', va='bottom')

plt.show()

import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Assuming you have already processed the 'redmi_note_11_reviews' DataFrame and added the 'redmi_note_11_Reviews' column

# Combine all the reviews into a single text for word cloud
all_reviews_text = ' '.join(redmi_note_11_reviews['redmi_note_11_Reviews'])

# Create a word cloud
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_reviews_text)

# Plot the word cloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud for redmi_note_11 Reviews')
plt.show()

pip install transformers[sentencepiece]

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch.nn.functional as F
from transformers import pipeline

# Load Aspect-Based Sentiment Analysis model
absa_tokenizer = AutoTokenizer.from_pretrained("yangheng/deberta-v3-base-absa-v1.1")
absa_model = AutoModelForSequenceClassification \
  .from_pretrained("yangheng/deberta-v3-base-absa-v1.1")

# Load a traditional Sentiment Analysis model
sentiment_model_path = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
sentiment_model = pipeline("sentiment-analysis", model=sentiment_model_path,
                          tokenizer=sentiment_model_path)

aspect = "camera"
camera_negative=[]
camera_neutral=[]
camera_positive=[]

# Perform aspect-based sentiment analysis for each review
for review in redmi_note_11_reviews['redmi_note_11_Reviews']:

  if aspect in review:
    inputs = absa_tokenizer(f"[CLS] {review} [SEP] {aspect} [SEP]", return_tensors="pt")
    outputs = absa_model(**inputs)
    probs = F.softmax(outputs.logits, dim=1)
    probs = probs.detach().numpy()[0]
    camera_negative.append(probs[0])
    camera_neutral.append(probs[1])
    camera_positive.append(probs[2])
  else:
    camera_negative.append(0)
    camera_neutral.append(0)
    camera_positive.append(0)
redmi_note_11_reviews['cam_positive']=camera_positive
redmi_note_11_reviews['cam_negative']=camera_negative
redmi_note_11_reviews['cam_neutral']=camera_neutral

redmi_note_11_reviews

aspect = "battery"
battery_negative=[]
battery_neutral=[]
battery_positive=[]

# Perform aspect-based sentiment analysis for each review
for review in redmi_note_11_reviews['redmi_note_11_Reviews']:

  if aspect in review:
    inputs = absa_tokenizer(f"[CLS] {review} [SEP] {aspect} [SEP]", return_tensors="pt")
    outputs = absa_model(**inputs)
    probs = F.softmax(outputs.logits, dim=1)
    probs = probs.detach().numpy()[0]
    battery_negative.append(probs[0])
    battery_neutral.append(probs[1])
    battery_positive.append(probs[2])
  else:
    battery_negative.append(0)
    battery_neutral.append(0)
    battery_positive.append(0)

redmi_note_11_reviews['battery_positive']=battery_positive
redmi_note_11_reviews['battery_negative']=battery_negative
redmi_note_11_reviews['battery_neutral']=battery_neutral

asp=['value for money', 'price', 'cost', 'affordable', 'budget', 'inexpensive']

value_for_money_negative=[]
value_for_money_neutral=[]
value_for_money_positive=[]

# Perform aspect-based sentiment analysis for each review
for review in redmi_note_11_reviews['redmi_note_11_Reviews']:
  flag=0
  for aspect in asp:
    if aspect in review:
      inputs = absa_tokenizer(f"[CLS] {review} [SEP] {aspect} [SEP]", return_tensors="pt")
      outputs = absa_model(**inputs)
      probs = F.softmax(outputs.logits, dim=1)
      probs = probs.detach().numpy()[0]
      value_for_money_negative.append(probs[0])
      value_for_money_neutral.append(probs[1])
      value_for_money_positive.append(probs[2])
      flag=1
      break
  if flag==0:
    value_for_money_negative.append(0)
    value_for_money_neutral.append(0)
    value_for_money_positive.append(0)

redmi_note_11_reviews['value_for_money_positive'] = value_for_money_positive
redmi_note_11_reviews['value_for_money_negative'] = value_for_money_negative
redmi_note_11_reviews['value_for_money_neutral'] = value_for_money_neutral

asp=['performance', 'speed', 'fast', 'efficient', 'smooth', 'lag', 'hang', 'overheat']
# Initialize empty lists for sentiment values
performance_negative = []
performance_neutral = []
performance_positive = []

# Perform aspect-based sentiment analysis for each review
for review in redmi_note_11_reviews['redmi_note_11_Reviews']:
    flag = 0
    for aspect in asp:
        if aspect in review:
            inputs = absa_tokenizer(f"[CLS] {review} [SEP] {aspect} [SEP]", return_tensors="pt")
            outputs = absa_model(**inputs)
            probs = F.softmax(outputs.logits, dim=1)
            probs = probs.detach().numpy()[0]
            performance_negative.append(probs[0])
            performance_neutral.append(probs[1])
            performance_positive.append(probs[2])
            flag = 1
            break
    if flag == 0:
        performance_negative.append(0)
        performance_neutral.append(0)
        performance_positive.append(0)

# Replace the old columns with the new 'performance' sentiment values
redmi_note_11_reviews['performance_negative'] = performance_negative
redmi_note_11_reviews['performance_neutral'] = performance_neutral
redmi_note_11_reviews['performance_positive'] = performance_positive

asp = ['display', 'screen', 'resolution', 'colors', 'brightness', 'quality', 'clarity', 'vivid']

# Initialize empty lists for sentiment values
display_negative = []
display_neutral = []
display_positive = []

# Perform aspect-based sentiment analysis for each review
for review in redmi_note_11_reviews['redmi_note_11_Reviews']:
    flag = 0
    for aspect in asp:
        if aspect in review:
            inputs = absa_tokenizer(f"[CLS] {review} [SEP] {aspect} [SEP]", return_tensors="pt")
            outputs = absa_model(**inputs)
            probs = F.softmax(outputs.logits, dim=1)
            probs = probs.detach().numpy()[0]
            display_negative.append(probs[0])
            display_neutral.append(probs[1])
            display_positive.append(probs[2])
            flag = 1
            break
    if flag == 0:
        display_negative.append(0)
        display_neutral.append(0)
        display_positive.append(0)

# Replace the old columns with the new 'display' sentiment values
redmi_note_11_reviews['display_negative'] = display_negative
redmi_note_11_reviews['display_neutral'] = display_neutral
redmi_note_11_reviews['display_positive'] = display_positive

redmi_note_11_reviews

overall_cam_positive_score = redmi_note_11_reviews['cam_positive'].sum()
count = (redmi_note_11_reviews['cam_positive'] != 0).sum()
redmi_note_11_camera_rating= (overall_cam_positive_score/count)*5
redmi_note_11_camera_rating

overall_battery_positive_score = redmi_note_11_reviews['battery_positive'].sum()
count = (redmi_note_11_reviews['battery_positive'] != 0).sum()
redmi_note_11_battery_rating= (overall_battery_positive_score/count)*5
redmi_note_11_battery_rating

overall_value_for_money_positive_score = redmi_note_11_reviews['value_for_money_positive'].sum()
count = (redmi_note_11_reviews['value_for_money_positive'] != 0).sum()
redmi_note_11_value_for_money_rating= (overall_value_for_money_positive_score/count)*5
redmi_note_11_value_for_money_rating

overall_performance_positive_score = redmi_note_11_reviews['performance_positive'].sum()
count = (redmi_note_11_reviews['performance_positive'] != 0).sum()
redmi_note_11_performance_rating= (overall_performance_positive_score/count)*5
redmi_note_11_performance_rating

overall_display_positive_score = redmi_note_11_reviews['display_positive'].sum()
count = (redmi_note_11_reviews['display_positive'] != 0).sum()
redmi_note_11_display_rating= (overall_display_positive_score/count)*5
redmi_note_11_display_rating

import matplotlib.pyplot as plt

# Labels and ratings
labels = ['Camera', 'Battery', 'Value for Money', 'Display', 'Performance']
ratings = [redmi_note_11_camera_rating, redmi_note_11_battery_rating, redmi_note_11_value_for_money_rating, redmi_note_11_display_rating, redmi_note_11_performance_rating]

# Create a bar plot
plt.figure(figsize=(10, 6))
plt.bar(labels, ratings, color=['blue', 'green', 'orange', 'purple', 'red'])
plt.title('Ratings for Different Aspects')
plt.ylabel('Rating')
plt.ylim(0, 5)
plt.show()

"""Overall Rankings

Camera
"""

import matplotlib.pyplot as plt

# Ratings for different products
ratings = {
    'OnePlus': {
        'Camera': 3.332593146651315,
        'Battery': 3.025227813014906,
        'Value for Money': 3.886736977258919,
        'Performance': 3.3784112322364503,
        'Display': 3.2368427787421266
    },
    'Samsung': {
        'Camera': 3.568961570642527,
        'Battery': 3.649028642696526,
        'Value for Money': 3.7154214422582097,
        'Performance': 2.0503714850489576,
        'Display': 3.064590644349777
    },
    'Redmi 9': {
        'Camera': 2.5494576799765767,
        'Battery': 3.648883234178939,
        'Value for Money': 4.000211316855559,
        'Performance': 2.285026423693377,
        'Display': 2.374769131528576
    },
    'Redmi 10 Prime': {
        'Camera': 2.168311012977094,
        'Battery': 3.4219609496026533,
        'Value for Money': 3.6629244674349297,
        'Performance': 2.3032808487620464,
        'Display': 2.227949720157662
    },
    'OPPO A31': {
        'Camera': 3.146689432492816,
        'Battery': 3.315446892276339,
        'Value for Money': 4.138420489627086,
        'Performance': 2.361778264463693,
        'Display': 2.759407183066544
    },
    'Redmi Note 11': {
        'Camera': 2.344477954695356,
        'Battery': 3.595528710756912,
        'Value for Money': 4.028606343230925,
        'Performance': 2.5078191400785927,
        'Display': 2.860209102865534
    }
}

# Aspects to plot
aspects = list(ratings['OnePlus'].keys())

# Create subplots for different aspects
fig, axes = plt.subplots(nrows=len(aspects), ncols=1, figsize=(8, 16))

for idx, aspect in enumerate(aspects):
    product_ratings = [rating[aspect] for rating in ratings.values()]
    product_names = list(ratings.keys())

    # Create a bar plot for each aspect
    axes[idx].bar(product_names, product_ratings, color='blue')
    axes[idx].set_title(f'{aspect} Ratings for Different Products')
    axes[idx].set_ylabel('Rating')
    axes[idx].set_ylim(0, 5)

# Adjust spacing and layout
plt.tight_layout()
plt.xticks(rotation=45)

# Show the plots
plt.show()
