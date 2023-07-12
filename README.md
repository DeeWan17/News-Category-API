# News Category Prediction Based on News Headline

There are 15 news categories:
- ACTIVISM & EQUALITY
- CRIME
- CULTURE
- ECONOMY
- ENTERTAINMENT
- FOOD & DRINK
- HEALTH
- LIFESTYLE
- MISCELLANEOUS
- POLITICS
- SCIENCE & TECH
- SPORTS
- STYLE & BEAUTY
- TRAVEL
- WORLD NEWS

A neural network has successfully been trained to assign these categories to any news headlines. The training dataset: https://www.kaggle.com/datasets/rmisra/news-category-dataset

Beware that no AI is 100 percent accurate.

# News Category Prediction API

To get a prediction, simply use an API call:

```https://news-category-app.azurewebsites.net/api/predict?headline={ENTER YOUR HEADLINE}```

Output is a plain text with the category name.

# Running News Category Prediction Model Locally 
If you want to predict news category locally (as opposed to relying on API), you can download these two files:

https://1drv.ms/u/s!AnYA0l4HK_zfgXDBD_wZ2mxhOOfd?e=GyyDMJ - *h5 keras model

https://1drv.ms/u/s!AnYA0l4HK_zfgXGLfqrUMwKm75HT?e=4oroxA - Python pickle file that holds sklearn.preprocessing.LabelEncoder

Example code of actually using this model on Python:
```python
from pickle import load as pload
import numpy as np
from transformers import TFBertModel
from transformers import BertTokenizer
from tensorflow.keras.models import load_model
from tensorflow import convert_to_tensor
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Load the label encoder
with open('predict/label_encoder.pkl', 'rb') as f:
    encoder = pload(f)

INPUT_LEN = 20 # Must be 20

# Load the pre-trained model
model = load_model('predict/news_categorization_model_v4.h5', custom_objects={'TFBertModel': TFBertModel}, compile=False)

# Function to predict the category of a text
def get_predicted_category(text):
    # Initialize the BERT tokenizer
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    
    # Tokenize the input text
    input_ids = [tokenizer.encode(text, add_special_tokens=True)]

    # Pad the input sequence to a fixed length
    input_padded = pad_sequences(input_ids, maxlen=INPUT_LEN, padding='post', value=0)
    input_tensor = convert_to_tensor(input_padded)

    # Perform prediction using the loaded model
    predictions = model.predict(input_tensor)

    # Get the predicted category
    predicted_category = np.argmax(predictions, axis=1)
    predicted_category_name = encoder.inverse_transform(predicted_category)
    category = predicted_category_name[0]
    
    return category
```
