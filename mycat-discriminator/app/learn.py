if __name__ == '__main__':

  import json
  import sys
  from os import listdir
  from os.path import exists, join as path_join

  import numpy
  from keras.preprocessing.image import load_img, img_to_array
  from keras.utils import np_utils

  from model import create_model
  from setting import env, env_path

  model_path = env_path('STORED_MODEL')
  labels_path = env_path('STORED_LABELS')
  learn_epochs = int(env('LEARN_EPOCHS'))

  if (exists(model_path) or exists(labels_path)):
    print('files already exists.')
    sys.exit(0)

  learn_images_path = env_path('LEARN_IMAGES_PATH')

  # 表示用ラベル
  labels = []
  # 学習データ・画像データ
  x_train = []
  # 学習データ・カテゴリラベル
  y_train = []

  # ディレクトリをlabelとしてデータセット作成
  for label in listdir(learn_images_path):
    if (label.startswith('.')):
      continue
    image_dir = path_join(learn_images_path, label)
    for file_name in listdir(image_dir):
      if (file_name.startswith('.')):
        continue
      if (not file_name.lower().endswith('.jpg') and not file_name.lower().endswith('.jpeg')):
        continue
      if (label not in labels):
        labels.append(label)
      file_path = path_join(image_dir, file_name)
      image = load_img(file_path, target_size=(100,100))

      # 学習データ格納
      x_train.append(img_to_array(image))
      y_train.append(labels.index(label))

  # 学習データをnumpy配列に変換
  x_train = numpy.asarray(x_train).astype('float32') / 255.0
  y_train = np_utils.to_categorical(numpy.asarray(y_train))

  model = create_model(x_train.shape[1:], len(labels))
  model.fit(x_train, y_train, batch_size=32, verbose=1, epochs=learn_epochs, validation_split=0.1)
  model.save(model_path)
  json.dump(labels, open(labels_path, 'w'))
