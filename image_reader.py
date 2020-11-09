#!/usr/bin/python

import numpy
from PIL import Image
import os
import shutil
import scipy
from scipy.misc import toimage, imsave

'''
This function doesnt work. PIL Image.fromarray doesnt show the image correctly
Using scipy's image show instead
'''
def show_image(input_image):
    img_array = numpy.array(input_image)
    img = Image.fromarray(img_array, 'RGB')
    img.show() THIS DOESNT SHOW THE IMAGE CORRECTLY
    return img

'''
Create a folder to save images
'''
def create_saved_images_folder():
    save_images_path = './saved_images'
    if os.path.exists(save_images_path):
        print('Deleting {}'.format(save_images_path))
        shutil.rmtree(save_images_path)

    print('Creating {}'.format(save_images_path))
    os.mkdir(save_images_path)

'''
Load numpy files
'''
def load_data():
    path = 'Fold 1/images/fold1/'
    images_file = 'images.npy'
    image_types_file = 'types.npy'


    images = numpy.load(path + images_file)
    image_types = numpy.load(path + image_types_file)
    return images, image_types


'''
Common function to show and save images
'''
def show_images(images, indices):
    save_images_path = './saved_images'
    len_images = len(indices)
    print("We have {} images".format(len_images))
    for i in indices:
        img_array = numpy.array(images[i])
        toimage(img_array).show()
        save = raw_input('Do you want to save this image? (y/n/q to quit) ')
        if save.lower() == 'y':
            imsave(save_images_path + '/Image_' + str(i) + '.png', img_array)
        if save.lower() == 'q':
            break

'''
Browse all images in fold1
'''
def browse_images():
    create_saved_images_folder()
    images, image_types = load_data()
    indices = [x for x in range(len(images))]
    show_images(images, indices)
    

'''
Filter the images based on a type
This filters based on skin type
'''
def browse_skin_images():
    create_saved_images_folder()
    images, image_types = load_data()
    skin_indices = []
    for k,v in enumerate(image_types):
        if v.lower() == 'skin':
            print('{} : {}'.format(k, v))
            skin_indices.append(k)
    show_images(images, skin_indices)


if __name__ == '__main__':
    option = raw_input('Enter 1 for browse images, 2 for skin images, q to quit: ')
    if option == '1':
        print('Browsing all images in Fold1')
        browse_images()
    elif option == '2':
        print('Browsing all images with skin images')
        browse_skin_images()
    elif option.lower() == 'q':
        print('Bye')
    else:
        print('Incorrect input. Bye.')
