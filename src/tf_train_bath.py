import tensorflow as tf
import numpy as np

def generate_data():
    num = 25
    label = np.asarray(range(0, num))
    images = np.asarray(range(0, num))
    #images = np.random.random([num, 5, 5, 3])
    print('label size :{}, image size {}'.format(label.shape, images.shape))
    return label, images

def get_batch_data():

    label, images = generate_data()
    input_queue = tf.train.slice_input_producer([label, images], shuffle=False)
    image_batch, label_batch = tf.train.shuffle_batch(input_queue, batch_size=10, num_threads=1, capacity=128, min_after_dequeue=64)
    return image_batch, label_batch

input_holder = tf.placeholder(tf.int32, [None])
label_holder = tf.placeholder(tf.int32, [None])

image_batch, label_batch = get_batch_data()

outputs = tf.add(input_holder, label_holder)


with tf.Session() as sess:
    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(sess, coord)
    i = 0
    try:
        while not coord.should_stop():
            image_batch_v, label_batch_v = sess.run([image_batch, label_batch])
            outputs_v = sess.run([outputs], {input_holder:image_batch_v, label_holder:label_batch_v})
            i += 1
            print(image_batch_v, label_batch_v, outputs_v)

            if i>4:
                break
    except tf.errors.OutOfRangeError:
        print("done")
    finally:
        coord.request_stop()
    coord.join(threads)
