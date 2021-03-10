import cv2
import numpy as np
import os
import sys
import tensorflow as tf
import csv

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )
    final={}
    for num_cp_layer in range(1,4):
        for filter_size in range(2,5):
            for filter_num in range(10,50,10):
                for p_size in range(2,5):
                    for num_hidden in range(1,4):
                        for size_hidden in range(200,500,100):
                            for d_o in [0.3,0.5]:
                                # Get a compiled neural network
                                model = get_model(num_cp_layer,filter_size,filter_num,p_size,num_hidden,size_hidden,d_o)
                                

                                # Fit model on training data
                                model.fit(x_train, y_train, epochs=EPOCHS)

                                # Evaluate neural network performance
                                evals = model.evaluate(x_test,  y_test, verbose=2)
                                print(evals)
                                resultsdict = dict(zip(model.metrics_names, evals))
                                final[(num_cp_layer,filter_size,filter_num,p_size,num_hidden,size_hidden,d_o)] = resultsdict
    final["names"] = "num_cp_layer,filter_size,filter_num,p_size,num_hidden,size_hidden,drop_out"
    w = csv.writer(open("output.csv", "w"))
    for key, val in final.items():
        w.writerow([key, val])

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    images = []
    labels = []

    # resize image
    # read as numpy.ndarray
    
    for folder in os.listdir(data_dir):#folder is a category
        for img in os.listdir(os.path.join(data_dir, folder)):
            
            nd_arr = cv2.imread(os.path.join(data_dir, folder, img)) #opens image as np.ndarray
            nd_arr = cv2.resize(nd_arr, (IMG_WIDTH, IMG_HEIGHT)) #resize to width and height as specified

            # Append Resized Image and its label to lists
            images.append(nd_arr)
            labels.append(int(folder))
    
    #return ([ndarray,ndarray,ndarray, ndarray,ndarray,ndarray],[0,0,0,1,1,1])
    return (images, labels)

    raise NotImplementedError


def get_model(num_cp_layer,filter_size,filter_num,p_size,num_hidden,size_hidden,d_o):
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """

    model = tf.keras.models.Sequential()
    for i in range(num_cp_layer):
        model.add(tf.keras.layers.Conv2D(
                filter_num, (filter_size, filter_size), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)
            ))
                    # Max-pooling layer, using 2x2 pool size
        model.add(tf.keras.layers.MaxPooling2D(pool_size=(p_size, p_size)))
                    # Flatten units
    model.add(tf.keras.layers.Flatten())
    
    for i in range(num_hidden):
        #model.add(tf.keras.layers.Dense(size_hidden, activation="relu"))
        model.add(tf.keras.layers.Dense(size_hidden, activation="sigmoid"))
    model.add(tf.keras.layers.Dropout(d_o))
    model.add(tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax"))

    
    model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

    # Return model for training and testing
    return model
    raise NotImplementedError
"""
        # Max-pooling layer, using 2x2 pool size
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
    [

        # Convolutional layer. Learn 32 filters using a 3x3 kernel
        tf.keras.layers.Conv2D(
            32, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)
        ),

        # Max-pooling layer, using 2x2 pool size
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

        # Flatten units
        tf.keras.layers.Flatten(),

        # Add a hidden layer with dropout
        tf.keras.layers.Dense(200, activation="relu"),
        tf.keras.layers.Dense(400, activation="sigmoid"),
        tf.keras.layers.Dropout(0.3),
"""
        # add output layer with 43 output units
    
    




if __name__ == "__main__":
    main()
