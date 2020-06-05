import numpy as np
import tensorflow as tf
from scipy import misc
import imageio
from PIL import Image
import os
from skimage.color import rgb2gray
import argparse
import sys
import tempfile
import matplotlib.pyplot as plt
import time

## the path needs to be displaced with your own path
def get_block(block_size, label_idx, true_num, attr_name):
  file = open("list_attr_celeba.txt", "r")
  file.readline()
  file.readline()
  path = "/mnt/members/weiting/celebA/img_align_celeba/"
  arr = os.listdir(path)

  celeb_images = np.zeros((block_size, 784*3))
  celeb_labels = []
  sum_true = 0
  sum_false = 0
  for idx, filenames in enumerate(arr):
    if idx > 62000:
      string = file.readline()
      splitStr = string.split()

      if (int(splitStr[label_idx]) == 1):
        if sum_true < true_num:
          image_file = path+filenames
          image = imageio.imread(image_file)
          img = Image.fromarray(image).resize((28,28))
          img = np.asarray(img, dtype=np.float32)
          celeb_images[(sum_true+sum_false),0:2352] = img.flatten()

          labels = [0,1]
          celeb_labels.append(labels)
          sum_true += 1
      else:
        if sum_false < (block_size-true_num):
          image_file = path+filenames
          image = imageio.imread(image_file)
          img = Image.fromarray(image).resize((28,28))
          img = np.asarray(img, dtype=np.float32)
          celeb_images[(sum_true+sum_false),0:2352] = img.flatten()

          labels = [1,0]
          celeb_labels.append(labels)
          sum_false += 1

      if sum_false==(block_size-true_num) and sum_true==true_num:
        break


  np.save((attr_name+"_images.npy"), celeb_images)
  np.save((attr_name+"_labels.npy"), celeb_labels)
  print(celeb_images.shape)
  print(len(celeb_labels))
  print(attr_name, "Successfully")

  return celeb_images, celeb_labels

def get_testset(label_idx):
  file = open("list_attr_celeba.txt", "r")
  file.readline()
  file.readline()
  path = "/mnt/members/weiting/celebA/img_align_celeba/"
  arr = os.listdir(path)

  celeb_images = np.zeros((5000, 784*3))
  celeb_labels = []
  sum_false = 0
  sum_true = 0
  for idx, filenames in enumerate(arr):
    string = file.readline()
    splitStr = string.split()

    if (int(splitStr[label_idx]) == 1):
      if sum_true < 4000:
        image_file = path+filenames
        image = imageio.imread(image_file)
        img = Image.fromarray(image).resize((28,28))
        img = np.asarray(img, dtype=np.float32)
        celeb_images[(sum_true+sum_false),0:2352] = img.flatten()

        labels = [0,1]
        celeb_labels.append(labels)
        sum_true += 1
    else:
      if sum_false < 1000:
        image_file = path+filenames
        image = imageio.imread(image_file)
        img = Image.fromarray(image).resize((28,28))
        img = np.asarray(img, dtype=np.float32)
        celeb_images[(sum_true+sum_false),0:2352] = img.flatten()

        labels = [1,0]
        celeb_labels.append(labels)
        sum_false += 1

    if sum_false==4000 and sum_true==1000:
      print(idx)
      break
  np.save(("test_images.npy"), celeb_images)
  np.save(("test_labels.npy"), celeb_labels)
  print(celeb_images.shape)
  print(celeb_images[0])
  print(len(celeb_labels))

  return celeb_images, celeb_labels


if __name__=='__main__':
	testset_size = 10000
	block_size = 5000
	modelattr_idx = 23  ## mustache attritube
	bald_images, bald_labels = get_block(5, block_size, modelattr_idx, "bald")
	blackhair_images, blackhair_labels = get_block(9, block_size, modelattr_idx, "blackhair", testset_size)
	bushybrow_images, bushybrow_labels = get_block(13, block_size, modelattr_idx, "bushybrow", testset_size)
	male_images, male_labels = get_block(21, block_size, modelattr_idx, "male", testset_size)
	mustache_images, mustache_labels = get_block(23, block_size, modelattr_idx, "mustache")
	earrings_images, earrings_labels = get_block(35, block_size, modelattr_idx, "earring", testset_size)
	_, _ = get_block(block_size, modelattr_idx, 10, 'block1')
	_, _ = get_block(block_size, modelattr_idx, 100, 'block2')
	_, _ = get_block(block_size, modelattr_idx, 1000, 'block3')
	_, _ = get_block(block_size, modelattr_idx, 2500, 'block4')
	_, _ = get_block(block_size, modelattr_idx, 4000, 'block5')
	_, _ = get_block(block_size, modelattr_idx, 4900, 'block6')

	test_images, test_labels = get_testset(modelattr_idx)