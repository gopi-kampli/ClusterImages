from keras.applications.vgg19 import VGG19
from keras.applications.vgg19 import preprocess_input
from keras.preprocessing.image import load_img
from keras_preprocessing.image import list_pictures
from keras.preprocessing.image import img_to_array
import numpy as np
import umap
import hdbscan
import os
from shutil import move


'''
Script to Cluster Similar Images into different folders
Useful for Separating Peoples, Places, Screenshots and Memes
'''


class ClusterImages():

    def __init__(self):
        #Loading VGG19 Trained Model
        self.model_vgg19 = VGG19(weights='imagenet', include_top=False)


    def _extract_image_features(self, img):
        #Loading Images with three channels and reducing it to target size of 512x512
        image = load_img(img, color_mode='rgb',target_size=(512, 512))
        x = img_to_array(image)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        features = self.model_vgg19.predict(x)
        flat_features = features.flatten()

        return flat_features


    def _extract_cluster_labels(self,image_features):
        #Embed features to Vertical stack
        image_embeddings = np.vstack(image_features)

        # Dimensional reduction using UMAP
        umap_array = umap.UMAP(
            n_neighbors=3,
            min_dist=0.0,
            n_components=2,
            random_state=42,
        ).fit_transform(image_embeddings)

        # Clustering Reduced Dimensional features into different labels with HDBScan
        labels = hdbscan.HDBSCAN(
            min_samples=5,
            min_cluster_size=5,
        ).fit_predict(umap_array)

        return labels

    
    def cluster_to_folders(self, directory):
        image_directory = directory

        #Getting All ImagePaths in the Directory and Subdirectories
        images = list_pictures(image_directory)
        flat_features = []
        temp = []

        for image in images:
            try:
                #Extracting Features using VGG19Architecture
                flat_features.append(self._extract_image_features(image))
                temp.append(image)
            except:
                continue

        #removing unreadible files from list
        images = temp

        #Extracting labels
        labels = self._extract_cluster_labels(flat_features)


        #Moving image clusters to different folders
        for i in range(len(images)):

            save_path = directory + '\\'+ str(labels[i])+'\\'

            if not os.path.exists(save_path):
                os.makedirs(save_path)

            image_path = str(images[i])
            image_name = image_path.replace(image_directory,'')
            image_name = image_name[image_name.index('\\')+1:]

            move(images[i],  save_path+image_name)


if __name__ == "__main__":
    cluster_images = ClusterImages()
    #Clustering all images from current directory
    cluster_images.cluster_to_folders('..\\')

