import pickle
import tensorflow as tf
import transformers
import tensorflow_addons as tfa
from transformers import TFBertModel
import numpy as np
import time
from tensorflow.keras.preprocessing.sequence import pad_sequences

# ----- Load the encoder

with open('label_encoder.pkl', 'rb') as f:
  encoder = pickle.load(f)

label_count = 15
INPUT_LEN = 20

# ----- Load the model

model = tf.keras.models.load_model('news_categorization_model_v4.h5', custom_objects={'TFBertModel': TFBertModel}, compile=False)

# ----- Predict

def get_predicted_category(text):
    tokenizer = transformers.BertTokenizer.from_pretrained('bert-base-uncased')
    input_ids = [tokenizer.encode(text, add_special_tokens=True)]

    input_padded = pad_sequences(input_ids, maxlen=20, padding='post', value=0)
    input_tensor = tf.convert_to_tensor(input_padded)

    predictions = model.predict(input_tensor)

    predicted_category = np.argmax(predictions, axis=1)
    predicted_category_name = encoder.inverse_transform(predicted_category)
    category = predicted_category_name[0]
    
    log(text, category)
    
    return category

def log(text, category):
   print(f'{time.ctime()}: {text} : {category}')