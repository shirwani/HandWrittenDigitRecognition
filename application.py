from flask import Flask, render_template, request
import tensorflow as tf
from keras.models import load_model
from PIL import Image
import io
import base64
from utils import *
import os


cfg = get_configs()
#num_px    = cfg['image']['mnist']['num_px']
#modelname = cfg['model']['mnist']['file']

model  = cfg['model']['manual']['file']
num_px = cfg['image']['manual']['num_px']

# Get modelname from environment variable MODEL or from config.json
modelname = os.getenv("MODEL", model)


app = Flask(__name__)


##################################################
# Use the model that uses the hand-created dataset
##################################################
def make_prediction(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))
    img_array = image_to_matrix(image)
    img_array = img_array.reshape(1, 10000)  # convert image array to a ow vector -> (1, 10000,)

    # print(f"The shape of img_array: {img_array.shape}")

    model = load_model('./models/' + modelname)
    logits = model.predict(img_array)  # logits
    probabilities = tf.nn.softmax(logits)  # probabilities
    return probabilities


###########################################
# Use the model that uses the MNIST dataset
###########################################
def make_prediction_mnist(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))
    image = np.array(image.resize((num_px, num_px)))
    image_array = np.array(image)[:, :, 3]

    model = load_model('./models/'+modelname)
    logits = model.predict(image_array.reshape(1, num_px, num_px, 1))  # logits
    probabilities = tf.nn.softmax(logits)  # probabilities

    print(f" Logits: {logits}")
    print(f" Probabilities: {probabilities}")

    yhat = np.argmax(probabilities)  # predicted value with largest probability
    print(f" Prediction: {yhat}")
    print(f" Confidence: {int(probabilities[0, yhat] * 10000) / 100}%")
    return yhat, (int(probabilities[0, yhat] * 100))


###############################
# Dump input image to temp file
###############################
def dump_input_image_to_temp_file(image_bytes):
    temp_file_path = cfg['temp_file_path']
    image = Image.open(io.BytesIO(image_bytes))
    image_array = np.array(image)[:, :, 3]
    Image.fromarray(image_array).save(temp_file_path)
    return temp_file_path


################
# Get user input
################
@app.route('/', methods=['GET', 'POST'])
def get_user_input():
    return render_template("getUserInput.html", model=modelname)


#############
# Show result
#############
@app.route('/result', methods=['GET', 'POST'])
def show_result():
    data = request.json

    # Decode the Base64 image data
    base64_data = data.split(',')[1]
    image_bytes = base64.b64decode(base64_data)
    temp_file_path = dump_input_image_to_temp_file(image_bytes)

    probabilities = make_prediction(image_bytes)
    prediction = np.argmax(probabilities) # predicted value with largest probability
    confidence = str(int(probabilities[0, prediction] * 10000) / 100)


    return render_template("showResult.html",
                           prediction=prediction,
                           confidence=confidence,
                           image_file_path=temp_file_path)

if __name__ == '__main__':
    port = cfg['flask-app']['port']
    app.run(debug=True, port=port)


