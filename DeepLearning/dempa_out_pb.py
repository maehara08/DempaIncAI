#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import tensorflow as tf
from tensorflow.python.framework import graph_util
from datetime import datetime
import time
import os

import dempa_input
import dempa_model


LOGDIR = './tmp/data.%s' % datetime.now().isoformat()
print LOGDIR

flags = tf.app.flags
FLAGS = flags.FLAGS
flags.DEFINE_string('train', 'members.csv', 'File name of train data')
flags.DEFINE_string('test', 'test2.txt', 'File name of train data')
flags.DEFINE_string('train_dir', LOGDIR, 'Directory to put the training data.')
flags.DEFINE_integer('max_steps', 100000, 'Number of steps to run trainer.')
flags.DEFINE_integer('batch_size', 120, 'Batch size Must divide evenly into the dataset sizes.')
flags.DEFINE_float('learning_rate', 1e-4, 'Initial learning rate.')

def main(ckpt = None):
    with tf.Graph().as_default() as graph:
        keep_prob = tf.placeholder("float")
        #
        # dempa_input.load_data([FLAGS.train], FLAGS.batch_size, shuffle=True, distored=True)
        # # images, labels, _ = dempa_input.load_data()

        images, labels, _ = dempa_input.load_data([FLAGS.train], FLAGS.batch_size, shuffle=True, distored=True)
        logits = dempa_model.inference_deep(images, keep_prob, dempa_input.DST_INPUT_SIZE, dempa_input.NUM_CLASS)
        loss_value = dempa_model.loss(logits, labels)
        train_op = dempa_model.training(loss_value, FLAGS.learning_rate)
        acc = dempa_model.accuracy(logits, labels)

        saver = tf.train.Saver(max_to_keep=0)
        sess = tf.Session()
        sess.run(tf.initialize_all_variables())
        if ckpt:
            print 'restore ckpt', ckpt
            saver.restore(sess, ckpt)

        tf.train.start_queue_runners(sess)

        summary_op = tf.merge_all_summaries()
        summary_writer = tf.train.SummaryWriter(FLAGS.train_dir, sess.graph_def)
        graph_def = graph_util.convert_variables_to_constants(
            sess,
            graph.as_graph_def(),
        ['softmax/Softmax'])  # 出力層の名前を指定
        # プロトコルバッファ出力
        tf.train.write_graph(graph_def, '.',
                             'graph.pb', as_text=False)

        # for step in range(FLAGS.max_steps):
        #     start_time = time.time()
        #     _, loss_result, acc_res = sess.run([train_op, loss_value, acc], feed_dict={keep_prob: 0.99})
        #     duration = time.time() - start_time
        #
        #     if step % 10 == 0:
        #         num_examples_per_step = FLAGS.batch_size
        #         examples_per_sec = num_examples_per_step / duration
        #         sec_per_batch = float(duration)
        #         format_str = ('%s: step %d, loss = %.2f (%.1f examples/sec; %.3f sec/batch)')
        #         print (format_str % (datetime.now(), step, loss_result, examples_per_sec, sec_per_batch))
        #         print 'acc_res', acc_res
        #
        #     if step % 100 == 0:
        #         summary_str = sess.run(summary_op, feed_dict={keep_prob: 1.0})
        #         summary_writer.add_summary(summary_str, step)
        #
        #     if step % 1000 == 0 or (step + 1) == FLAGS.max_steps or loss_result == 0:
        #         checkpoint_path = os.path.join(FLAGS.train_dir, 'model.ckpt')
        #         saver.save(sess, checkpoint_path, global_step=step)

                # graph_def = graph_util.convert_variables_to_constants(sess, graph.as_graph_def(),
                #                                                       ['softmax'])  # 出力層の名前を指定
                # # graph_def = graph.as_graph_def()
                # # プロトコルバッファ出力
                # tf.train.write_graph(graph_def, '.',
                #                      'graph.pb', as_text=False)

            # if loss_result == 0:
            #     print('loss is zero')
            #     break


if __name__ == '__main__':
    main("./tmp/data.2016-12-17/model.ckpt-10000")
    # main(sys.argv[1])
