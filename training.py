import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense
from tensorflow.keras import layers, models
from utils import *


cfg = get_configs()

########################################
# Train model using hand-crafted dataset
########################################
def train_model():
    print("Initiating training...")
    X_file_path   = cfg['training']['manual']['X_file_path']
    y_file_path   = cfg['training']['manual']['y_file_path']
    learning_rate = cfg['training']['manual']['learning_rate']
    epochs        = cfg['training']['manual']['epochs']
    num_px        = cfg['image']['manual']['num_px']

    X = np.load(X_file_path)
    y = np.load(y_file_path)
    print('The shape of X is: ' + str(X.shape))
    print('The shape of y is: ' + str(y.shape))

    tf.random.set_seed(1234)  # for consistent results
    model = Sequential(
        [
            tf.keras.Input(shape=(num_px * num_px,)),
            Dense(700,  activation='relu',   kernel_regularizer=tf.keras.regularizers.l2(0.001)),
            Dense(500,  activation='relu',   kernel_regularizer=tf.keras.regularizers.l2(0.001)),
            Dense(250,  activation='relu',   kernel_regularizer=tf.keras.regularizers.l2(0.001)),
            Dense(50,   activation='relu',   kernel_regularizer=tf.keras.regularizers.l2(0.001)),
            Dense(10,   activation='linear', kernel_regularizer=tf.keras.regularizers.l2(0.001))
        ])

    model.compile(
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),  # softmax: multi-class classification
        optimizer=tf.keras.optimizers.legacy.Adam(learning_rate=learning_rate)
    )

    model.fit(X, y, epochs=epochs)

    # Save the model
    modelname = 'm_' + get_date_time_str() + '.h5'

    if 'model' not in cfg:
        cfg['model'] = dict()

    if 'manual' not in cfg['model']:
        cfg['model']['manual'] = dict()

    cfg['model']['manual']['file'] = modelname
    with open('config.json', 'w') as file:
        json.dump(cfg, file, indent=4)

    model.save('./models/' + modelname)


#################################
# Train model using MNIST dataset
#################################
def train_model_mnist():
    print("Initiating mnist training...")

    mnist_path       = cfg['training']['mnist']['data_path']
    epochs           = cfg['training']['mnist']['epochs']
    batch_size       = cfg['training']['mnist']['batch_size']
    validation_split = cfg['training']['mnist']['validation_split']
    num_px           = cfg['image']['mnist']['num_px']

    # Load the data using numpy
    with np.load(mnist_path, allow_pickle=True) as data:
        train_images, train_labels = data['x_train'], data['y_train']
        test_images, test_labels = data['x_test'], data['y_test']

    # Preprocess the data
    train_images = train_images.reshape((len(train_images), num_px, num_px, 1)).astype('float32') / 255.0
    test_images = test_images.reshape((len(test_images), num_px, num_px, 1)).astype('float32') / 255.0

    # Convert labels to one-hot encoding
    train_labels = tf.keras.utils.to_categorical(train_labels)
    test_labels = tf.keras.utils.to_categorical(test_labels)

    # Build the model
    model = models.Sequential()
    model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(num_px, num_px, 1)))
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
    model.fit(train_images, train_labels, epochs=epochs, batch_size=batch_size, validation_split=validation_split)

    print(type(test_images), test_images.shape)

    # Evaluate the model
    test_loss, test_acc = model.evaluate(test_images, test_labels)
    print("Accuracy: {}%".format(round(test_acc * 100)))

    # Save the model
    modelname = 'mnist_' + get_date_time_str() + '.h5'

    if 'model' not in cfg:
        cfg['model'] = dict()

    if 'mnist' not in cfg['model']:
        cfg['model']['mnist'] = dict()

    cfg['model']['mnist']['file'] = modelname
    with open('config.json', 'w') as file:
        json.dump(cfg, file, indent=4)

    model.save('./models/' + modelname)


if __name__ == '__main__':
    train_model()
    #train_model_mnist()
