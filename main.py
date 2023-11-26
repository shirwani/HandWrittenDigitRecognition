from flask import Flask, render_template, request
import numpy as np
import tensorflow as tf
from keras.models import load_model
from PIL import Image
import io
import base64

app = Flask(__name__)

def make_prediction(model, image_of_digit):
    logits = model.predict(image_of_digit.reshape(1, 10000))  # logits
    probabilities = tf.nn.softmax(logits)  # probabilities

    print(f" Logits: {logits}")
    print(f" Probabilities: {probabilities}")

    yhat = np.argmax(probabilities)  # predicted value with largest probability
    print(f" Prediction: {yhat}")
    print(f" Confidence: {int(probabilities[0, yhat] * 10000) / 100}%")
    return yhat, (int(probabilities[0, yhat] * 100))


@app.route('/', methods=['GET', 'POST'])
def get_user_input():
    return render_template("getUserInput.html")

@app.route('/result', methods=['GET', 'POST'])
def show_result():
    data = request.json

    # Decode the Base64 image data
    base64_data = data.split(',')[1]
    image_bytes = base64.b64decode(base64_data)

    # Open the image using PIL
    image = Image.open(io.BytesIO(image_bytes))

    # Convert the image to a NumPy array
    image_array = np.array(image)[:, :, 3]

    temp_file_path = 'static/images/image.png'
    Image.fromarray(image_array).save(temp_file_path)

    model = load_model('model.h5')
    [prediction, confidence] = make_prediction(model, image_array)

    return render_template("showResult.html", prediction=prediction, confidence=confidence, image_file_path=temp_file_path)

if __name__ == '__main__':
    app.run(debug=True, port=5002)
