import os
from keras.datasets import cifar10
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dropout, Flatten, Dense
from keras.losses import categorical_crossentropy
from keras.optimizers import RMSprop
from keras.utils import to_categorical

batch_size = 32
epochs = 2

input_shape = (32, 32, 3)
num_categories = 10

default_kernel_size = (3, 3)
default_pool_size = (2, 2)


def load_and_preprocess_data():
    (x_train, y_train), (x_test, y_test) = cifar10.load_data()

    x_train = x_train.astype('float32') / 255.
    x_test = x_test.astype('float32') / 255.

    y_train = to_categorical(y_train, num_categories)
    y_test = to_categorical(y_test, num_categories)

    return (x_train, y_train), (x_test, y_test)


def create_model():
    model = Sequential()
    model.add(Conv2D(32, kernel_size=default_kernel_size, padding='same', activation='relu', input_shape=input_shape))
    model.add(Conv2D(32, kernel_size=default_kernel_size, activation='relu'))
    model.add(MaxPooling2D(pool_size=default_pool_size))
    model.add(Dropout(0.25))

    model.add(Conv2D(64, kernel_size=default_kernel_size, padding='same', activation='relu'))
    model.add(Conv2D(64, kernel_size=default_kernel_size, activation='relu'))
    model.add(MaxPooling2D(pool_size=default_pool_size))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(512, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(num_categories, activation='softmax'))

    return model


(X_train, Y_train), (X_test, Y_test) = load_and_preprocess_data()
cnn_model = create_model()
cnn_model.summary()

cnn_model.compile(RMSprop(learning_rate=0.0001, decay=1e-6),
                  loss=categorical_crossentropy,
                  metrics=['accuracy'])

cnn_model.fit(X_train, Y_train,
              batch_size=batch_size,
              epochs=epochs,
              validation_data=(X_test, Y_test))

scores = cnn_model.evaluate(X_test, Y_test)
print('Test loss:', scores[0])
print('Test accuracy:', scores[1])

model_path = os.path.join(os.getcwd(), 'saved_models\cnn_cifar10')
cnn_model.save(model_path)
