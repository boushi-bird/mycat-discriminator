from keras.models import load_model
from keras.preprocessing.image import img_to_array
from PIL import Image as PIL_Image
import numpy
import json

class Discriminator:
  def __init__(self, model_path, labels_path):
    self.model = load_model(model_path)
    self.labels = json.load(open(labels_path))

  def run(self, file_upload):
    image = PIL_Image.open(file_upload.file)
    image = image.resize((100, 100), PIL_Image.NEAREST)
    images = [img_to_array(image)]
    images = numpy.asarray(images).astype('float32') / 255.0

    ratios = self.model.predict(images, batch_size=32, verbose=1)[0]

    answer_ratio = ratios.max()
    answer_index = numpy.where(ratios == answer_ratio)[0][0]
    answer = self.__labeled_ratio(answer_index, answer_ratio)

    all_ratios = []
    for index, ratio in enumerate(ratios):
      all_ratios.append(self.__labeled_ratio(index, ratio))

    return { 'answer': answer, 'all_ratios': all_ratios }

  def __labeled_ratio(self, label_index, numpy_ratio):
    few_digit = 3
    label = self.labels[label_index]
    ratio = round(numpy_ratio.item() * 100, few_digit)
    return { 'label': label, 'ratio': ratio }
