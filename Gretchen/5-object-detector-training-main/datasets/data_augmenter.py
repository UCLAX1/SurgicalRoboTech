#!/usr/bin/env python3
#
# First Steps in Programming a Humanoid AI Robot
#
# Image data augmenter
# This program applies an image modification pipeline N times to all *.jpg images in an input folder and saves 
# the modified images in a designated output folder.
#
# Usage: python data_augmenter.py <input folder> <output folder> <number of augmented images per image>
#
# (C) 2023, Computer Systems and Platforms Laboratory, Seoul National University
#

import os
import sys
import argparse
import numpy as np
import imgaug.augmenters as iaa
from imgaug import BoundingBox, BoundingBoxesOnImage
from PIL import Image, ImageDraw


# image augmentation pipeline
# the rotations are kept close to rectangular axes do minimixe bbox inflation
iaug = iaa.Sequential([
    iaa.Fliplr(0.5),                                       # 50% chance to flop horizontally
    iaa.Sometimes(0.2, iaa.Affine(rotate=(-10,  10))),     # 20% chance to rotate randomly between -10 and  10 degrees
    iaa.Sometimes(0.2, iaa.Affine(rotate=( 80, 100))),     # 20% chance to rotate randomly between  80 and 100 degrees
    iaa.Sometimes(0.2, iaa.Affine(rotate=(260, 280))),     # 20% chance to rotate randomly between 260 and 280 degrees
    iaa.Multiply((0.8, 1.2), per_channel=0.2),             # change brightness
    iaa.Sometimes(0.25, iaa.Dropout((0.01, 0.1), per_channel=0.5)), # 25% chance for a 10% dropout
    iaa.Sometimes(0.5, iaa.GaussianBlur(sigma=(0, 0.5))),  # 25% chance to blur the image
    iaa.AdditiveGaussianNoise(scale=(0, 0.05*255))         # add gaussian noise
])

def read_annotations(filename, image_width, image_height):
    bboxes = None

    if os.path.isfile(filename) and os.access(filename, os.R_OK):
        with open(filename, "r") as file:
            annotations = file.read().strip().split("\n")

        bboxes = []
        for annotation in annotations:
            class_id, x_center, y_center, width, height = map(float, annotation.split())

            # Convert relative coordinates to absolute coordinates
            x_center *= image_width
            y_center *= image_height
            width *= image_width
            height *= image_height

            # Create an imgaug BoundingBox object
            bbox = BoundingBox(x1=x_center - width / 2, y1=y_center - height / 2,
                               x2=x_center + width / 2, y2=y_center + height / 2,
                               label=int(class_id))
            bboxes.append(bbox)

    return bboxes


def write_annotations(filename, image_width, image_height, bboxes):
    annots = []
    for bbox in bboxes:
        # Convert the bounding box back to relative coordinates
        x_center = (bbox.x1 + bbox.x2) / (2 * image_width)
        y_center = (bbox.y1 + bbox.y2) / (2 * image_height)
        width = (bbox.x2 - bbox.x1) / image_width
        height = (bbox.y2 - bbox.y1) / image_height

        # Format the updated annotation line
        annot = f"{bbox.label} {x_center} {y_center} {width} {height}"
        annots.append(annot)

    # Save the updated annotations to a corresponding .txt file
    with open(filename, "w") as file:
        file.write("\n".join(annots))


def show_annotations(image, bboxes, color):
    # Create drawing context
    canvas = ImageDraw.Draw(image)

    # Draw all bounding boxes
    for bbox in bboxes:
        canvas.rectangle([(bbox.x1, bbox.y1), (bbox.x2, bbox.y2)], outline=color)


def augment_images(input_folder, output_folder, num_augmentations, show_boxes):
    # Iterate through each image in the folder
    for filename in os.listdir(input_folder):

        # Assuming JPEG images
        if filename.endswith(".jpg"):
            ifn = os.path.join(input_folder, filename)
            afn = os.path.join(input_folder, os.path.splitext(filename)[0] + ".txt")

            # Only process files we can read
            if os.path.isfile(ifn) and os.access(ifn, os.R_OK):
                print(f"Processing {filename}...")

                # Load the image and corresponding annotations
                img = Image.open(ifn)
                bbx = read_annotations(afn, img.width, img.height)

                # if requested, draw bounding boxes directly onto image
                if show_boxes == True:
                    show_annotations(img, bbx, (0,255,0))

                # Apply the augmentation pipeline N times
                for i in range(num_augmentations):
                    aifn = f"{os.path.splitext(filename)[0]}_{i+1}.jpg"  # Adjust filename format as needed
                    aifn = os.path.join(output_folder, aifn)
                    print(f"  {aifn}")

                    # Apply augmentation pipeline to image and bounding boxes
                    aimg, abbx = iaug(image=np.array(img), bounding_boxes=bbx)

                    # Convert numpy array back to PIL.Image
                    aimg = Image.fromarray(aimg)

                    # if requested, draw modified bounding boxes directly onto image
                    if show_boxes == True:
                        show_annotations(aimg, abbx, (255,0,0))

                    # Save the augmented image
                    aimg.save(aifn)

                    # Save the augmented bounding boxes (pass original or augmented image dimensions?)
                    write_annotations(os.path.splitext(aifn)[0] + ".txt", img.width, img.height, abbx)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Image augmentation program")
    parser.add_argument("input_folder", help="Path to the input folder")
    parser.add_argument("output_folder", help="Path to the output folder")
    parser.add_argument("num_augmentations", type=int, help="Number of augmentations per image")
    # for illustrative purposes (do not enable when generating images for training!)
    parser.add_argument("-s", "--show-boxes", action="store_true", default=False, help="Show bounding boxes")
    args = parser.parse_args()

    # Run the image augmentation
    augment_images(args.input_folder, args.output_folder, args.num_augmentations, args.show_boxes)

