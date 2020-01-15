from model.data_utils import CoNLLDataset
from model.ner_model import NERModel
import sys

def main(model):
    # create instance of config
    if mode=='char':
        from model.config_char import Config
    else:
        from model.config import Config
    config = Config()
    #tf.reset_default_graph()
    # build model
    #config.lr_method = 'sgd'
    model = NERModel(config)
    model.build()
    # model.restore_session("results/crf/model.weights/") # optional, restore weights
    # model.reinitialize_weights("proj")

    # create datasets
    dev   = CoNLLDataset(config.filename_dev, config.processing_word,
                         config.processing_tag, config.max_iter)
    train = CoNLLDataset(config.filename_train, config.processing_word,
                         config.processing_tag, config.max_iter)

    # train model
    model.train(train, dev)
    #model.config.batch_size = 10
    def modeltrain(model):
        # progbar stuff for logging
        batch_size = model.config.batch_size
        nbatches = (len(train) + batch_size - 1) // batch_size
        #prog = Progbar(target=nbatches)
        # iterate over dataset
        N = len(train)
        for i, (words, labels) in enumerate(minibatches(train, batch_size)):
            fd, _ = model.get_feed_dict(words, labels, model.config.lr,
                                       model.config.dropout)
            # _, train_loss, summary = self.sess.run(
            # [self.train_op, self.loss, self.merged], feed_dict=fd)
            _, train_loss = model.sess.run([model.train_op, model.loss], feed_dict=fd)
            #prog.update(i + 1, [("train loss", train_loss)])
            if i%100==0:
                print('train %d steps of total %d with train_loss is %0.4f'%(i,N,train_loss))
            # tensorboard
            # if i % 10 == 0:
            # self.file_writer.add_summary(summary, epoch*nbatches + i)
        metrics = model.run_evaluate(dev)
        msg = " - ".join(["{} {:04.2f}".format(k, v)
                          for k, v in metrics.items()])
        model.logger.info(msg)

        return metrics["f1"]
if __name__ == "__main__":
    mode = sys.argv[1]
    main(mode)
