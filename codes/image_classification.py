#!/usr/bin/env python3

import argparse
import io
import sys
import datetime
from PIL import Image

from aiy.vision.inference import ImageInference
from aiy.vision.models import foodtype_model

def read_stdin():
    return io.BytesIO(sys.stdin.buffer.read())


def classify(FilePath):
    #parser = argparse.ArgumentParser()
    #parser.add_argument('--input', '-i', dest='input', required=True)
    #args = parser.parse_args()

    with ImageInference(foodtype_model.model()) as inference:
        image = Image.open(FilePath)
        classes = foodtype_model.get_classes(
            inference.run(image), max_num_objects=5, object_prob_threshold=0.1)
        for i, (label, score) in enumerate(classes):
            if i==0:
                return label
                #print('Result : %s (prob=%f)' % (label, score))


if __name__ == '__main__':
    classify("/home/pi/codes/2018-09-04 21:28:38.257503.jpg")

