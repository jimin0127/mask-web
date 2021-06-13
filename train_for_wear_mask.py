#마스크 착용 여부 판별 훈련하기
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Flatten, BatchNormalization
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.preprocessing.image import load_img, img_to_array


path_dir1 = 'img/nomask/'
path_dir2 = 'img/mask/'

file_list1 = os.listdir(path_dir1)
file_list2 = os.listdir(path_dir2)

file_list1_num = len(file_list1)
file_list2_num = len(file_list2)

file_num = file_list1_num + file_list2_num

# 이미지 전처리
num = 0
all_img = np.float32(np.zeros((file_num, 224, 224, 3))) # 크기가 정해져 있고 모든 값이 0인 배열
all_label = np.float64(np.zeros((file_num, 1)))

# nomask 안에 사진 하나씩 꺼내오기
for img_name in file_list1:
    img_path = path_dir1+img_name
    img = load_img(img_path, target_size=(224, 224)) # 이미지를 224,224 픽셀 크기로 불러오기

    x = img_to_array(img) # img_to_array 함수를 씌우면 이미지를 NumPy 배열로 변환
    x = np.expand_dims(x, axis = 0) # 배열 (array)에 차원을 추가하기
    x = preprocess_input(x) # 모델에 필요한 형식에 이미지를 적절하게 맞추기 위함 (samples, size1,size2,channels)로 만들기
    all_img[num, :, :, :] = x

    all_label[num] = 0  # nomask
    num = num+1

for img_name in file_list2:
    img_path = path_dir2+img_name
    img = load_img(img_path, target_size=(224, 224))

    x = img_to_array(img)
    x = np.expand_dims(x, axis = 0)
    x = preprocess_input(x)
    all_img[num, :, :, :] = x

    all_label[num] = 1 #mask
    num = num + 1


# 적절하게 훈련되게 하기 위해 데이터 셋 섞기
n_elem = all_label.shape[0]
indices = np.random.choice(n_elem, size=n_elem, replace=False)

all_label = all_label[indices]
all_img = all_img[indices]


# 훈련셋 테스트 셋 분할
num_train = int(np.round(all_label.shape[0]*0.8))
num_test = int(np.round(all_label.shape[0]*0.2))

train_img = all_img[0:num_train, :, :, :]
test_img = all_img[num_train:, :, :, :]

train_label = all_label[0:num_train]
test_label = all_label[num_train:]


# 사전 학습 모델 만들기
IMG_SHAPE = (224, 224, 3)

base_model = ResNet50(input_shape = IMG_SHAPE, weights='imagenet', include_top=False)
base_model.trainable = False
base_model.summary()
print("Number of layers in the base model: ", len(base_model.layers))

flatten_layer = Flatten()
dense_layer1 = Dense(128, activation='relu')
bn_layer1 = BatchNormalization()
dense_layer2 = Dense(1, activation=tf.nn.sigmoid)

model = Sequential([
    base_model,
    flatten_layer,
    dense_layer1,
    bn_layer1,
    dense_layer2,
])

base_learning_rate = 0.001
model.compile(optimizer=tf.keras.optimizers.Adam(lr=base_learning_rate),
              loss='binary_crossentropy',
              metrics=['accuracy'])
model.summary()

# 모델 학습시키기
model.fit(train_img, train_label, epochs=10, batch_size=12, validation_data=(test_img, test_label))

# 모델 저장하기
model.save("model.h5")

print("Saved model to disk")