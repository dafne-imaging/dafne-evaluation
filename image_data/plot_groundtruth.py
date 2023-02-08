#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 17:04:05 2023

@author: Francesco Santini
"""

import sys
import numpy as np
import matplotlib.pyplot as plt

mask_bundle_file = sys.argv[1]

LEG_LABELS = {
    1: 'Soleus',
    2: 'Gastrocnemius Medialis',
    3: 'Gastrocnemius Lateralis',
    4: 'Tibialis Anterior',
    5: 'Extensor Longus Digitorum',
    6: 'Peroneus'
}

def find_contour(mask):
    # calculate the gradient of the mask
    g = np.gradient(mask)
    # get the sum of the gradient in both directions. This will give a thick contour
    c = (np.abs(g[0])+np.abs(g[1]))>0
    # return the portion of the contour inside the mask
    return (c*(mask>0)).astype(np.uint8)

masks_bundle = np.load(mask_bundle_file)

mask_dictionary = {}

# merge left and right if necessary
for mask_name in masks_bundle:
    if mask_name.endswith('_R'):
        continue
    if mask_name.endswith('_L'):
        mask_dictionary[mask_name[:-2]] = masks_bundle[mask_name] + masks_bundle[mask_name[:-1]+'R']
    else:
        mask_dictionary[mask_name] = masks_bundle[mask_name]
    sz = masks_bundle[mask_name].shape

# find the contours
contour_dictionary = {}
for mask_name in mask_dictionary:
    contour_dictionary[mask_name] = find_contour(mask_dictionary[mask_name][:,:,0])

# plot the contours
accumulated_contours = np.zeros(sz[:2], dtype=np.int32)
for val, label in LEG_LABELS.items():
    contour = contour_dictionary[label]
    # remove overlap
    contour = np.logical_and(contour, accumulated_contours == 0)
    accumulated_contours += (contour*val)

alpha = np.zeros_like(accumulated_contours, dtype=np.float32)
alpha[accumulated_contours > 0] = 1.0

plt.imshow(accumulated_contours, alpha=alpha, cmap='jet', interpolation='none')
plt.gca().set_axis_off()
plt.savefig('groundtruth.png', bbox_inches='tight', pad_inches=0, transparent=True)
plt.show()
