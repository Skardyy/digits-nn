import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import to_categorical
import numpy as np
from keras.models import load_model

def create_and_train_model():
    # Load and preprocess the data
    (train_images, train_labels), (test_images, test_labels) = mnist.load_data()
    train_images = train_images.reshape((60000, 28 * 28)).astype('float32') / 255
    test_images = test_images.reshape((10000, 28 * 28)).astype('float32') / 255
    train_labels = to_categorical(train_labels)
    test_labels = to_categorical(test_labels)

    # Create the neural network
    model = Sequential()
    model.add(Dense(128, input_dim=28 * 28, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(10, activation='softmax'))

    # Compile and train the model
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    model.fit(train_images, train_labels, epochs=10, batch_size=32, validation_data=(test_images, test_labels))

    # Save the trained model
    model.save('mnist_model.h5')

create_and_train_model()

def load_saved_model():
    return load_model('mnist_model.h5')

loaded_model = load_saved_model()

def predict_digit(model, flat_image):
    input_image = np.array(flat_image).reshape(1, 28 * 28) / 255
    predictions = model.predict(input_image)
    result = np.argmax(predictions)
    return result

# Example usage
flat_image = [0, 0, ..., 0]  # Replace with your 28x28 flattened image
predicted_digit = predict_digit(loaded_model, flat_image)
print(predicted_digit)
