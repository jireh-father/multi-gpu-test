import tensorflow as tf
import json

bn_decay = 0.997
bn_epsilon = 1e-5


def build_model(inputs, num_classes, is_training, model_conf=None):
    endpoints = {}
    filters = 100
    kernel_size = 5
    pool_size = 2
    conv_layers = 7

    for i in range(conv_layers):
        inputs = tf.layers.conv2d(inputs, filters, kernel_size, activation=tf.nn.relu)
        inputs = tf.layers.max_pooling2d(inputs, pool_size, 1)
        inputs = tf.layers.batch_normalization(inputs=inputs, axis=3, momentum=bn_decay, epsilon=bn_epsilon,
                                               center=True, scale=True, training=is_training, fused=True,
                                               name="batch" + str(i))

    # nets = tf.layers.conv2d(inputs, 1, 1, activation=tf.nn.relu)
    # nets = tf.layers.batch_normalization(inputs=inputs, axis=3, momentum=bn_decay, epsilon=bn_epsilon,
    #                                        center=True, scale=True, training=is_training, fused=True,
    #                                        name="batch")
    nets = tf.reduce_mean(inputs, axis=3)

    shape = nets.get_shape()
    nets = tf.reshape(nets, [-1, shape[1], shape[1], 1])
    endpoints["last_conv"] = nets
    tf.summary.image("mean_feature_map", nets, 10)
    shape = nets.get_shape()
    nets = tf.layers.conv2d(nets, 100, (shape[1], shape[1]), activation=tf.nn.relu)
    shape = nets.get_shape()

    flatten = tf.reshape(nets, [-1, shape[1] * shape[1] * shape[3]])
    fc = tf.layers.dense(flatten, 50, activation=tf.nn.relu)
    logits = tf.layers.dense(fc, num_classes)
    endpoints["logits"] = logits

    return logits, endpoints


build_model.default_image_size = 90
build_model.default_last_conv_name = "last_conv"
