import io
import tensorflow as tf
import glob
import random

f = open("videoIdsAndLabels.txt","a")

path = "data/*.tfrecord"
for filename in glob.glob(path):
  tfrecords_filename = filename
  opts = tf.python_io.TFRecordOptions(tf.python_io.TFRecordCompressionType.NONE)
  record_iterator = tf.python_io.tf_record_iterator(path=tfrecords_filename.format(0), options=opts)
  img_string = ""
  for string_record in record_iterator:
      example = tf.train.Example()
      example.ParseFromString(string_record)
      video_id = (example.features.feature['video_id']
                                   .bytes_list
                                   .value[0])
      labels = (example.features.feature['labels']
                               .int64_list
                               .value)
      if (random.random() < 0.1):
        f.write(video_id.decode("utf-8"))
        f.write(" ")
        f.write(str(labels))
        f.write("\n")
f.close()