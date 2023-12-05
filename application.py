from flask import Flask, render_template, request
import numpy as np
import tensorflow as tf
from keras.models import load_model
from PIL import Image
import io
import base64

app = Flask(__name__)

def make_prediction(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))
    image_array = np.array(image)[:, :, 3] # convert the image to a NumPy array

    model = load_model('./models/model.h5')
    logits = model.predict(image_array.reshape(1, 10000))  # logits
    probabilities = tf.nn.softmax(logits)  # probabilities

    print(f" Logits: {logits}")
    print(f" Probabilities: {probabilities}")

    yhat = np.argmax(probabilities)  # predicted value with largest probability
    print(f" Prediction: {yhat}")
    print(f" Confidence: {int(probabilities[0, yhat] * 10000) / 100}%")
    return yhat, (int(probabilities[0, yhat] * 100))

def make_prediction_mnist(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))
    image = np.array(image.resize((28, 28)))
    image_array = np.array(image)[:, :, 3]

    model = load_model('./models/model_mnist.h5')
    logits = model.predict(image_array.reshape(1, 28, 28, 1))  # logits
    probabilities = tf.nn.softmax(logits)  # probabilities

    print(f" Logits: {logits}")
    print(f" Probabilities: {probabilities}")

    yhat = np.argmax(probabilities)  # predicted value with largest probability
    print(f" Prediction: {yhat}")
    print(f" Confidence: {int(probabilities[0, yhat] * 10000) / 100}%")
    return yhat, (int(probabilities[0, yhat] * 100))


def dump_input_image_to_temp_file(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))
    image_array = np.array(image)[:, :, 3]
    temp_file_path = 'static/images/image.png'
    Image.fromarray(image_array).save(temp_file_path)
    return temp_file_path


@app.route('/', methods=['GET', 'POST'])
def get_user_input():
    return render_template("getUserInput.html")


@app.route('/result', methods=['GET', 'POST'])
def show_result():
    data = request.json

    # Decode the Base64 image data
    base64_data = data.split(',')[1]
    image_bytes = base64.b64decode(base64_data)

    temp_file_path = dump_input_image_to_temp_file(image_bytes)
    [prediction, confidence] = make_prediction(image_bytes)

    return render_template("showResult.html", prediction=prediction, confidence=confidence, image_file_path=temp_file_path)

if __name__ == '__main__':
    app.run(debug=True, port=5002)


