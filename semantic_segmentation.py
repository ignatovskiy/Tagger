#!/usr/bin/env python
"""
 Copyright (C) 2018-2019 Intel Corporation

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""
from __future__ import print_function
from collections import defaultdict
import cv2
import numpy as np
from openvino.inference_engine import IECore


def main(image_name="test1.jpg",
         model_xml="semantic-segmentation-adas-0001.xml",
         model_bin="semantic-segmentation-adas-0001.bin"):
    
    ie = IECore()
    # Read IR

    net = ie.read_network(model_xml, model_bin)

    input_blob = next(iter(net.inputs))
    out_blob = next(iter(net.outputs))
    net.batch_size = 1

    # NB: This is required to load the image as uint8 np.array
    #     Without this step the input blob is loaded in FP32 precision,
    #     this requires additional operation and more memory.
    net.inputs[input_blob].precision = "U8"

    # Read and pre-process input images
    n, c, h, w = net.inputs[input_blob].shape
    images = np.ndarray(shape=(n, c, h, w))

    for i in range(n):
        image = cv2.imread(image_name)
        assert image.dtype == np.uint8
        if image.shape[:-1] != (h, w):
            image = cv2.resize(image, (w, h))
        image = image.transpose((2, 0, 1))  # Change data layout from HWC to CHW
        images[i] = image

    # Loading model to the plugin
    exec_net = ie.load_network(network=net, device_name="CPU")

    # Start sync inference
    res = exec_net.infer(inputs={input_blob: images})

    # Processing output blob
    res = res[out_blob].tolist()[0]

    all_size = len(res) * len(res[0]) * len(res[0][0])

    counter_dict = defaultdict(float)

    for i in range(len(res)):
        for j in range(len(res[0])):
            for k in range(len(res[0][0])):
                counter_dict[res[i][j][k]] += 1

    for number in counter_dict:
        number_area = counter_dict[number]
        counter_dict[number] = number_area / all_size * 100

    labels_dict = {"vegetation": counter_dict[8] + counter_dict[9],
                   "water/road": counter_dict[0],
                   "buildings": counter_dict[2],
                   "sky": counter_dict[10]}

    print(labels_dict)


if __name__ == '__main__':
    main()
