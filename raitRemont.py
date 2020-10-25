from IPython.core.display import display, HTML
from tensorflow.keras.models import load_model, Model
from tensorflow.keras.utils import get_file
from tensorflow.keras.layers import GlobalAveragePooling2D, BatchNormalization, Activation, Dense, Dropout
from tensorflow.keras.preprocessing import image
import numpy as np
import efficientnet.tfkeras as efn
from urllib.request import urlopen
import cv2


def build_model_efficientnet():
    pretrained_model = efn.EfficientNetB0(weights='imagenet', include_top=False)
    pretrained_model.trainable = False
    x = pretrained_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(512, activation='relu')(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
    x = Dropout(0.5)(x)
    predictions = Dense(2, activation='softmax')(x)
    model = Model(inputs=pretrained_model.input, outputs=predictions)

    # lr=1e-4
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    model.summary()
    return model


### LOADING MODEL
model = build_model_efficientnet()
# model = load_model('./cian_model_01_B0.h5')
weights_path = get_file(fname='cian_model_01_B0.h5',
                        origin='https://fancyshot.com/wp-content/uploads/model/cian_model_01_B0.h5')
model.load_weights(weights_path)
print('Model Loaded!')


def _fast_expand(img):
    img = image.img_to_array(img) / 255.0
    img = np.expand_dims(img, axis=0)
    return img


def pseudo_download_image(url):
    #     print(f'[INFO] Downloading {url}')
    resp = urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    return image


def predict_image(url):
    img_size = 320
    #     open_cv_image = cv2.imread(img_path)
    open_cv_image = pseudo_download_image(url)
    open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2RGB)
    test_image = cv2.resize(open_cv_image, (img_size, img_size))
    orig_image = _fast_expand(test_image)
    result_orig = model.predict(orig_image, batch_size=1)

    #     classes = ['bad', 'good']
    # result_idx = np.argmax(result_orig)
    result_val = list(result_orig[0])

    return result_val


def rate_room(photos):
    data = {'score': [0, 0]}
    total_score = [0, 0]
    for url in photos:
        data['score'] = predict_image(url)
        total_score = [a + b for a, b in zip(total_score, data['score'])]

    final_score = [x / len(photos) for x in total_score]
    return final_score.index(max(final_score))
