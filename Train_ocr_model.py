from matplotlib import image
from matplotlib import pyplot
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, Flatten
from mnist import MNIST
from sklearn.utils import shuffle

emndata = MNIST('dataset/')
emndata1 = MNIST('dataset/')

emndata.select_emnist('digits')
emndata1.select_emnist('letters')

#Load datasets
xTrain, yTrain = emndata.load_training()
xTest,yTest = emndata.load_testing()

xTrain1, yTrain1 = emndata1.load_training()
xTest1,yTest1 = emndata1.load_testing()

#Join Datasets into one list
xTrain = xTrain+xTrain1
#Reshape for input
xTrain = np.array(xTrain,np.float32)
xTrain = xTrain.reshape(xTrain.shape[0], 28, 28, 1)

#Join Datasets into one list
xTest = xTest+xTest1
#Reshape for input
xTest = np.array(xTest,np.float32)
xTest = xTest.reshape(xTest.shape[0], 28, 28, 1)

for n in range(len(yTrain)):
  yTrain[n]=yTrain[n]+27 #increment label by 27 since keras requires concurent integer labels

for n in range(len(yTest)):
  yTest[n]=yTest[n]+27#increment label by 27 since keras requires concurent integer labels

#Join Datasets into one list
yTrain = yTrain+yTrain1 #first set contains Letters labels (1-26) and second digits ( 27-37 )
yTest = yTest+yTest1

#Reshape for input
yTrain=np.array(yTrain, np.integer)
yTrain = yTrain.reshape(yTrain.shape[0], 1)
yTrain= yTrain-1 #keras requires concurent integer labels starting from '0'

#Reshape for input
yTest=np.array(yTest, np.integer)
yTest = yTest.reshape(yTest.shape[0], 1)
yTest= yTest-1 #keras requires concurent integer labels starting from '0'

# Shuffle newly jointed dataset
xTrain,yTrain = shuffle(xTrain,yTrain,random_state=0)
input_shape = (28, 28, 1)

yTrain = tf.keras.utils.to_categorical(yTrain,36)
yTest = tf.keras.utils.to_categorical(yTest,36)

# Noramlize Training and Test sets
xTrain /= 255.
xTest /= 255.

#Setting up CNN structure
model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3),activation='relu',input_shape=input_shape))
# 64 3x3 kernels
model.add(Conv2D(64, (3, 3), activation='relu'))
# 128 3x3 kernels
model.add(Conv2D(128, (3, 3), activation='relu'))
# Reduce by taking the max of each 2x2 block
model.add(MaxPooling2D(pool_size=(2, 2)))
# Dropout to avoid overfitting
model.add(Dropout(0.25))
# Flatten the results to one dimension for passing into our final layer
model.add(Flatten())
# A hidden layer to learn with
model.add(Dense(128, activation='relu'))
# Another dropout
model.add(Dropout(0.5))
# Final categorization from 0-36 with softmax
model.add(Dense(36, activation='softmax'))

model.summary()

model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

history = model.fit(xTrain, yTrain,
                    batch_size=32,
                    epochs=10,
                    verbose=2,
                    validation_data=(xTest, yTest))

model.save('modelComb3.h5')

# Evaluate the model using Accuracy and Loss
score = model.evaluate(xTest, yTest, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

# Plot training & validation accuracy values
pyplot.plot(history.history['accuracy'])
pyplot.plot(history.history['val_accuracy'])
pyplot.title('Model accuracy')
pyplot.ylabel('Accuracy')
pyplot.xlabel('Epoch')
pyplot.legend(['Train', 'Test'], loc='upper left')
pyplot.show()

# Plot training & validation loss values
pyplot.plot(history.history['loss'])
pyplot.plot(history.history['val_loss'])
pyplot.title('Model loss')
pyplot.ylabel('Loss')
pyplot.xlabel('Epoch')
pyplot.legend(['Train', 'Test'], loc='upper left')
pyplot.show()
