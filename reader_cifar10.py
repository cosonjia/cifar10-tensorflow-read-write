import tensorflow as tf

# 文件路径列表
filelist = ['data/train.tfrecord']
# 定义文件队列
file_queue = tf.train.string_input_producer(filelist,
                                            num_epochs=None,
                                            shuffle=True)
# 通过TFRcordReader对象读取tfrecord文件
reader = tf.TFRecordReader()
# 返回文件名和文件
_, ex = reader.read(file_queue)

# 需要对序列化的数据进行解码
feature = {
    'image': tf.FixedLenFeature([], tf.string),  # byte型的解码成string型
    'label': tf.FixedLenFeature([], tf.int64)
}

batchsize = 2

batch = tf.train.shuffle_batch([ex], batchsize, capacity=batchsize * 10,
                               min_after_dequeue=batchsize * 5)

# 反序列化数据
example = tf.parse_example(batch, features=feature)

image = example['image']
label = example['label']

# 对byte数据解码成uint8类型的数据
image = tf.decode_raw(image, tf.uint8)
# 需要reshape，否则是一个向量
image = tf.reshape(image, [-1, 32, 32, 3])

with tf.Session() as sess:
    # 线程的协调器
    coord = tf.train.Coordinator()

    sess.run(tf.local_variables_initializer())
    threads = tf.train.start_queue_runners(sess, coord)

    for i in range(1):
        # image_bth, _ = sess.run([image, label])
        # import cv2
        # cv2.imshow("image", image_bth[0, ...])
        # cv2.waitKey(0)
        print(sess.run(label))  # 会打印一个batchsize数量的lable

    # 请求线程结束
    coord.request_stop()
    # 等待线程终止
    coord.join(threads)
