import numpy as np
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense

class SoftMaxTraining:
    def __init__(self):
        self.model = None
        self.X = np.load("training_data/X.npy")
        self.y = np.load("training_data/y.npy")

    def get_model(self):
        return self.model

    def train_model(self):
        X = self.X
        y = self.y

        print('The shape of X is: ' + str(X.shape))
        print('The shape of y is: ' + str(y.shape))

        tf.random.set_seed(1234)  # for consistent results
        model = Sequential(
            [
                tf.keras.Input(shape=(10000,)),
                Dense(1000, activation='relu'),
                Dense(500, activation='relu'),
                Dense(200, activation='relu'),
                Dense(100, activation='relu'),
                Dense(50, activation='relu'),
                Dense(10, activation='linear')
            ])

        model.compile(
            loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),  # softmax: multi-class classification
            optimizer=tf.keras.optimizers.legacy.Adam(learning_rate=0.0001)
        )

        model.fit(X, y, epochs=100)
        self.model = model

if __name__ == '__main__':
    training = SoftMaxTraining()
    training.train_model()
    model = training.get_model()
    model.save('model.h5')

