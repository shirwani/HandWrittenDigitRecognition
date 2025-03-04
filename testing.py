import tensorflow as tf
from keras.models import load_model
from utils import *


cfg = get_configs()

def testing(dataset):
    X_file_path = cfg[dataset]['manual']['X_file_path']
    y_file_path = cfg[dataset]['manual']['y_file_path']
    modelname   = cfg['model']['manual']['file']
    num_px      = cfg['image']['manual']['num_px']

    X = np.load(X_file_path)
    y = np.load(y_file_path)
    #print('The shape of X is: ' + str(X.shape))
    #print('The shape of y is: ' + str(y.shape))

    model = load_model('./models/' + modelname)

    logits = model.predict(X)  # logits
    probabilities = tf.nn.softmax(logits)  # probabilities

    i = 0
    misses = 0
    for p in probabilities:
        yhat = np.argmax(p)
        if y[i][0] != yhat:
            misses += 1
            print(f" Expected: {y[i][0]} -- Predicted: {yhat} -- Confidence: {int(p[yhat] * 10000) / 100}%")

        i += 1

    accuracy = round((i - misses)/i * 10000)/100
    return accuracy

if __name__ == '__main__':
    training_accuracy = testing('training')
    cv_accuracy = testing('cv')

    print(f"Training accuracy: {training_accuracy}% ")
    print(f"Cross-validation accuracy: {cv_accuracy}% ")
