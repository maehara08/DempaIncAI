#sh dempa_eval.sh image1 image2


# sh run.sh ../images/images_mirin/ out_mirin
cmd="python /Users/yutasato/tensorflow/projects/dempa/DeepLearning/dempa_eval.py /Users/yutasato/tensorflow/projects/dempa/DeepLearning/tmp/data.2016-12-17/model.ckpt-10000.meta $1 $2"
$cmd


