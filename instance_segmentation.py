#!/usr/bin/env python3
"""
 Copyright (c) 2019 Intel Corporation

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


import cv2
import numpy as np
from openvino.inference_engine import IECore


def main(input_pic="test1.jpg",
         labels_file_name="coco_labels.txt",
         model_xml="instance-segmentation-security-0083.xml",
         model_bin="instance-segmentation-security-0083.bin"):
    # Plugin initialization for specified device and load extensions library if specified.
    ie = IECore()

    # Read IR
    net = ie.read_network(model_xml, model_bin)

    required_input_keys = {'im_data', 'im_info'}
    required_output_keys = {'boxes', 'scores', 'classes', 'raw_masks'}

    n, c, h, w = net.inputs['im_data'].shape

    exec_net = ie.load_network(network=net, device_name='CPU', num_requests=2)
    
    frame = cv2.imread(input_pic)

    with open(labels_file_name, 'rt') as labels_file:
        class_labels = labels_file.read().splitlines()

    # Resize the image to keep the same aspect ratio and to fit it to a window of a target size.
    scale_x = scale_y = min(h / frame.shape[0], w / frame.shape[1])
    input_image = cv2.resize(frame, None, fx=scale_x, fy=scale_y)

    input_image_size = input_image.shape[:2]
    input_image = np.pad(input_image, ((0, h - input_image_size[0]),
                                        (0, w - input_image_size[1]),
                                        (  0, 0)),
                            mode='constant', constant_values=0)
    # Change data layout from HWC to CHW.
    input_image = input_image.transpose((2, 0, 1))
    input_image = input_image.reshape((n, c, h, w)).astype(np.float32)
    input_image_info = np.asarray([[input_image_size[0], input_image_size[1], 1]], dtype=np.float32)

    # Run the net.
    outputs = exec_net.infer({'im_data': input_image, 'im_info': input_image_info})

    # Parse detection results of the current request
    scores = outputs['scores']
    classes = outputs['classes'].astype(np.uint32)

    # Filter out detections with low confidence.
    detections_filter = scores > 0.5
    scores = scores[detections_filter]
    classes = classes[detections_filter]

    labels = dict()

    for label_id in classes:
        label = class_labels[label_id]

        if label not in labels:
            labels[label] = 1
        else:
            labels[label] += 1

    print(labels)
    return labels


if __name__ == '__main__':
    main()
