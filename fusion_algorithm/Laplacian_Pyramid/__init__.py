import numpy as np
import cv2
from .pyramid import get_pyramid_fusion

ENERGY_SOBEL = "sobel"
ENERGY_LAPLACIAN = "laplacian"

CHOICE_PYRAMID = "pyramid"
CHOICE_MAX = "max"
CHOICE_AVERAGE = "average"

def stack_focus(
    images,
    choice = CHOICE_PYRAMID,
    energy = ENERGY_LAPLACIAN,
    pyramid_min_size = 32,
    kernel_size = 5,
    blur_size = 5,
    smooth_size = 32
):
    images = np.array(images, dtype=images[0].dtype)
    aligned_images = images
    gray_images = np.zeros(images.shape[:-1], dtype=np.uint8)
    gray_images[0] = cv2.cvtColor(images[0], cv2.COLOR_RGB2GRAY)
    gray_images[1] = cv2.cvtColor(images[1], cv2.COLOR_RGB2GRAY)

    if choice == CHOICE_PYRAMID:
        stacked_image = get_pyramid_fusion(aligned_images, pyramid_min_size)
        return cv2.convertScaleAbs(stacked_image)

    if energy == ENERGY_SOBEL:
        energy_map = get_sobel_map(gray_images)
    else:
        energy_map = get_laplacian_map(gray_images, kernel_size, blur_size)

    if smooth_size > 0:
        energy_map = smooth_energy_map(energy_map, smooth_size)

    focus_map = get_focus_map(energy_map, choice)
    stacked_image = blend(aligned_images, focus_map)
    return cv2.convertScaleAbs(stacked_image)


def get_sobel_map(images):
    energies = np.zeros(images.shape, dtype=np.float32)
    for index in range(images.shape[0]):
        image = images[index]
        energies[index] = np.abs(cv2.Sobel(image, cv2.CV_64F, 1, 0)) + np.abs(cv2.Sobel(image, cv2.CV_64F, 0, 1))
            
    return energies

def get_laplacian_map(images, kernel_size, blur_size):
    laplacian = np.zeros(images.shape, dtype=np.float32)
    for index in range(images.shape[0]):
        gaussian = cv2.GaussianBlur(images[index], (blur_size, blur_size), 0)
        laplacian[index] = np.abs(cv2.Laplacian(gaussian, cv2.CV_64F, ksize = kernel_size))
        
    return laplacian

def smooth_energy_map(energies, smooth_size):
    smoothed = np.zeros(energies.shape, dtype=energies.dtype)
    if (smooth_size > 0):
        for index in range(energies.shape[0]):
            smoothed[index] = cv2.bilateralFilter(energies[index], smooth_size, 25, 25)
            
    return smoothed

def get_focus_map(energies, choice):
    if (choice == CHOICE_AVERAGE):
        tile_shape = np.array(energies.shape)
        tile_shape[1:] = 1

        sum_energies = np.tile(np.sum(energies, axis=0), tile_shape)
        return np.divide(energies, sum_energies, where=sum_energies!=0)
    
    focus_map = np.zeros(energies.shape, dtype=np.float64)
    best_layer = np.argmax(energies, axis=0)
    for index in range(energies.shape[0]):
        focus_map[index] = best_layer == index

    return focus_map

def blend(images, focus_map):
    return np.sum(images.astype(np.float64) * focus_map[:, :, :, np.newaxis], axis=0).astype(images.dtype)
