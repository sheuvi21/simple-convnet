from keras.datasets import cifar10
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from keras.callbacks import TensorBoard, EarlyStopping
from keras.utils import to_categorical


(X_train, y_train), (X_test, y_test) = cifar10.load_data()


model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(32, 32, 3)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(32, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(10, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])


tb = TensorBoard(log_dir='./logs')
early = EarlyStopping(monitor='loss', mode='min', min_delta=0.001, patience=3)

model.fit(X_train / 255.0, to_categorical(y_train), epochs=60, verbose=0, callbacks=[tb, early])


score = model.evaluate(X_test / 255.0, to_categorical(y_test))
print(score)


model.save('cifar10_model.h5')
