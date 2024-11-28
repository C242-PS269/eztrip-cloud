import tensorflow as tf
import numpy as np
import os


from flask import Flask, request, jsonify
from config import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.log()

# Initialize Flask app
app = Flask(__name__)

# Load the trained TensorFlow model (.h5)
model = tf.keras.models.load_model(os.getenv('MODEL_PATH'))

# Recompile the model (optional, only if you want to suppress the warning)
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])


@app.route('/')
def home():
    return "TensorFlow Model API is running!"

if __name__ == '__main__':
    app.run(host=os.getenv('HOST'), port=os.getenv('PORT'))