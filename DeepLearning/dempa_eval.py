#!/usr/bin/env python
# ! -*- coding: utf-8 -*-

import sys
import numpy as np
import tensorflow as tf  # cv2より前にimportするとcv2.imreadになぜか失敗する(Noneを返す)
import dempa_input
import dempa_model

# python /Users/yutasato/tensorflow/projects/dempa/DeepLearning/dempa_

def evaluation(imgpath, ckpt_path):
    tf.reset_default_graph()

    jpeg = tf.read_file(imgpath)
    image = tf.image.decode_jpeg(jpeg, channels=3)
    image = tf.cast(image, tf.float32)
    image.set_shape([dempa_input.IMAGE_SIZE, dempa_input.IMAGE_SIZE, 3])
    image = tf.image.resize_images(image, dempa_input.DST_INPUT_SIZE, dempa_input.DST_INPUT_SIZE)
    image = tf.image.per_image_whitening(image)
    image = tf.reshape(image, [-1, dempa_input.DST_INPUT_SIZE * dempa_input.DST_INPUT_SIZE * 3])
    print image

    logits = dempa_model.inference_deep(image, 1.0, dempa_input.DST_INPUT_SIZE, dempa_input.NUM_CLASS)

    sess = tf.InteractiveSession()
    saver = tf.train.Saver()
    sess.run(tf.initialize_all_variables())
    if ckpt_path:
        saver.restore(sess, ckpt_path)

    softmax = logits.eval()

    result = softmax[0]
    rates = [round(n * 100.0, 1) for n in result]
    print rates

    pred = np.argmax(result)
    print dempa_input.MEMBER_NAMES[pred]

    members = []
    for idx, rate in enumerate(rates):
        name = dempa_input.MEMBER_NAMES[idx]
        members.append({
            'name_ascii': name[1],
            'name': name[0],
            'rate': rate
        })
    rank = sorted(members, key=lambda x: x['rate'], reverse=True)

    return (rank, pred)


def execute(imgpaths, img_root_dir, ckpt_path):
    res = []
    for imgpath in imgpaths:
        #(rank, pred) = evaluation('/' + imgpath, ckpt_path)
        (rank, pred) = evaluation(img_root_dir + '/' + imgpath, ckpt_path)
        res.append({
            'file': imgpath,
            'top_member_id': pred,
            'rank': rank
        })
    return res


if __name__ == '__main__':
    ckpt_path = sys.argv[1]
    imgfile1 = sys.argv[2]
    imgfile2 = sys.argv[3]
    # main([imgfile], ckpt_path)
    # main2(imgfile1, ckpt_path)
    print execute([imgfile1, imgfile2], '.', ckpt_path)
