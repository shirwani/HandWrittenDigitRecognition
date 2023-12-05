import numpy as np
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense
from tensorflow.keras import layers, models

def load_data():
    X = np.load("datasets/X.npy")
    y = np.load("datasets/y.npy")
    return X, y


def train_model():
    X, y = load_data()

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
    model.save('./models/model.h5')

def train_model_mnist():
    # Path to your local mnist.npz file
    mnist_path = './training_data/mnist.npz'

    # Load the data using numpy
    with np.load(mnist_path, allow_pickle=True) as data:
        train_images, train_labels = data['x_train'], data['y_train']
        test_images, test_labels = data['x_test'], data['y_test']

    # Preprocess the data
    train_images = train_images.reshape((len(train_images), 28, 28, 1)).astype('float32') / 255.0
    test_images = test_images.reshape((len(test_images), 28, 28, 1)).astype('float32') / 255.0

    # Convert labels to one-hot encoding
    train_labels = tf.keras.utils.to_categorical(train_labels)
    test_labels = tf.keras.utils.to_categorical(test_labels)

    # Build the model
    model = models.Sequential()
    model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.Flatten())
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(10, activation='softmax'))

    # Compile the model
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    # Train the model
    model.fit(train_images, train_labels, epochs=5, batch_size=64, validation_split=0.2)

    # Evaluate the model
    test_loss, test_acc = model.evaluate(test_images, test_labels)
    print(f'Test accuracy: {test_acc}')

    model.save('./models/model_mnist.h5')


if __name__ == '__main__':
    train_model()
    #train_model_mnist()
