import time
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')   # Suppress Matplotlib warnings

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'    # Suppress TensorFlow logging (1)
import pathlib
import tensorflow as tf

tf.get_logger().setLevel('ERROR')           # Suppress TensorFlow logging (2)

from PIL import Image

# Enable GPU dynamic memory allocation
gpus = tf.config.experimental.list_physical_devices('GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)

def read_images(label):
    images_dir = os.path.join(CUR_DIR,'../test_images')
    file_path = os.path.join(images_dir, label)
    image_paths = []
    for file in os.listdir(file_path):
        image_path = os.path.join(file_path, file)
        print(image_path)
        image_paths.append(str(image_path))
    return image_paths

def load_image_into_numpy_array(path):
    return np.array(Image.open(path))

def create_path(path):
    if not os.path.exists(path):
        os.makedirs(path)

if __name__ == "__main__":
    LABEL = 'demo'
    CUR_DIR = str(pathlib.Path(__file__).parent.resolve())
    IMAGE_PATHS = read_images(LABEL)
    PATH_TO_MODEL_DIR = os.path.join(CUR_DIR,'../training_demo\exported-models\my_model')
    PATH_TO_LABELS = os.path.join(CUR_DIR,'../training_demo/annotations/label_map.pbtxt')
    PATH_TO_SAVED_MODEL = PATH_TO_MODEL_DIR + "/saved_model"
    OUTPUT_PATH = os.path.join(CUR_DIR,'../output_prediction')
    OUTPUT_PATH = os.path.join(OUTPUT_PATH, LABEL)
    create_path(OUTPUT_PATH)

    # Load the model
    print('Loading model...', end='')
    start_time = time.time()

    # Load saved model and build the detection function
    detect_fn = tf.saved_model.load(PATH_TO_SAVED_MODEL)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print('Done! Took {} seconds'.format(elapsed_time))

    #Load the label
    category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS,
                                                                    use_display_name=True)

    if len(IMAGE_PATHS) == 0:
        print('No images found')
    for image_path in IMAGE_PATHS:

        print('Running inference for {}... '.format(image_path), end='')

        image_np = load_image_into_numpy_array(image_path)

        # Things to try:
        # Flip horizontally
        # image_np = np.fliplr(image_np).copy()

        # Convert image to grayscale
        # image_np = np.tile(
        #     np.mean(image_np, 2, keepdims=True), (1, 1, 3)).astype(np.uint8)

        # The input needs to be a tensor, convert it using `tf.convert_to_tensor`.
        input_tensor = tf.convert_to_tensor(image_np)
        # The model expects a batch of images, so add an axis with `tf.newaxis`.
        input_tensor = input_tensor[tf.newaxis, ...]

        # input_tensor = np.expand_dims(image_np, 0)
        try:
            detections = detect_fn(input_tensor)
        except ValueError:
            print('Error')
            continue

        # All outputs are batches tensors.
        # Convert to numpy arrays, and take index [0] to remove the batch dimension.
        # We're only interested in the first num_detections.
        num_detections = int(detections.pop('num_detections'))
        detections = {key: value[0, :num_detections].numpy()
                        for key, value in detections.items()}
        detections['num_detections'] = num_detections

        # detection_classes should be ints.
        detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

        image_np_with_detections = image_np.copy()

        viz_utils.visualize_boxes_and_labels_on_image_array(
                image_np_with_detections,
                detections['detection_boxes'],
                detections['detection_classes'],
                detections['detection_scores'],
                category_index,
                use_normalized_coordinates=True,
                max_boxes_to_draw=200,
                min_score_thresh=.30,
                agnostic_mode=False)

        # image = Image.fromarray(image_np_with_detections, 'RGB')
        # image.show()
        plt.figure()
        plt.imshow(image_np_with_detections)
        
        plt.savefig(os.path.join(OUTPUT_PATH, os.path.basename(image_path)))
        # plt.show()

        print('Done')


