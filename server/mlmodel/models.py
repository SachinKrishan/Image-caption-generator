from django.db import models
import os
import pickle
import numpy as np

import keras
from keras.applications.vgg16 import VGG16, preprocess_input
from keras.applications.resnet import preprocess_input
from keras.applications.resnet import ResNet101, ResNet152, ResNet50
from keras.preprocessing.image import load_img, img_to_array
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Model, load_model


# Create your models here.
class CaptionModel:
    def __init__(self):
        self.cnn_model = ResNet50()
        self.max_length = 35 # max number of words in a caption
        # restructure the model
        self.cnn_model = Model(inputs=self.cnn_model.inputs, outputs=self.cnn_model.layers[-2].output)
        self.model = load_model('mlmodel/saved_weights/best_model_resnet_20.h5')
        with open('mlmodel/saved_weights/tokenizer.pickle', 'rb') as handle:
            self.tokenizer = pickle.load(handle)

    def idx_to_word(self, integer, tokenizer):
        for word, index in tokenizer.word_index.items():
            if index == integer:
                return word
        return None

    def predict_caption(self, model, image, tokenizer, max_length):
        # add start tag for generation process
        in_text = 'startseq'
        # iterate over the max length of sequence
        for i in range(max_length):
            # encode input sequence
            sequence = tokenizer.texts_to_sequences([in_text])[0]
            # pad the sequence
            sequence = pad_sequences([sequence], max_length)
            # predict next word
            yhat = model.predict([image, sequence], verbose=0)
            # get index with high probability
            yhat = np.argmax(yhat)
            # convert index to word
            word = self.idx_to_word(yhat, tokenizer)
            # stop if word not found
            if word is None:
                break
            # append word as input for generating next word
            in_text += " " + word
            # stop if we reach end tag
            if word == 'endseq':
                break

        return in_text

      
    def generate_caption(self, image):
        # Preprocess image and perform model inference
        # Replace this with your actual preprocessing and inference code
        # caption = self.model.predict(image)
        image = img_to_array(image)
        # reshape data for model
        image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
        # preprocess image for vgg
        image = preprocess_input(image)
        # extract features
        feature = self.cnn_model.predict(image, verbose=0)
        # predict from the trained model
        caption = self.predict_caption(self.model, feature, self.tokenizer, self.max_length)

        return caption