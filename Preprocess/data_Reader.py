import re
import os
import glob
import numpy as np
import sys
import torch
from skimage import io

class DataReader(torch.utils.data.Dataset):
    def __init__(self, image_folder, transform=None, label_width=1, numerize_labels=True, class_dict=None):
        """
            image_folder<str> -> Folder which Contain images only
            labels_width<int> -> How many chars per label
            numerize_labels<bool> -> Make str labels represented in numbers
            classes_dict<dict> -> To numerize_labels [Required only when numerize_labels is True]
        """
        self.root = image_folder
        self.files = glob.glob(self.root+"/*.jpg")
        self.labels = None
        self.transform = transform
        self.label_width = label_width
        self.class_dict = class_dict
        self.__xtraLabels()
        if numerize_labels:
            self.__numerize_labels()
    
    def __len__(self):
        return len(self.labels)

    @property
    def classes(self):
        return list(self.class_dict.keys())

    def __getitem__(self, idx):
        image = io.imread(self.files[idx])
        if self.transform:
            image = self.transform(image)
        # sample = {'features':image,'label':self.labels[idx]}
        return image,self.labels[idx]

    def __xtraLabels(self):
        self.labels = np.array([re.sub(self.root,"",x)[:self.label_width] for x in self.files])

    def __numerize_labels(self):
        if self.class_dict is None:
            raise RuntimeError("classes_dict is None, unable to numerize_labels!")
        if len(self.class_dict) == 0:
            raise RuntimeError("classes_dict is Emplty, unable to numerize labels!")
        if self.labels is None:
            raise ValueError("Labels is Empty!")
        labels = []
        _temp = [','.join(x) for x in self.labels]
        _temp = np.array([x.split(',') for x in _temp])
        origin_shape = _temp.shape
        for label in _temp.ravel():
            labels.append(self.class_dict[label])
        if self.label_width == 1:
            self.labels = np.array(labels).ravel()
        else:
            self.labels = np.array(labels).reshape(*origin_shape)

