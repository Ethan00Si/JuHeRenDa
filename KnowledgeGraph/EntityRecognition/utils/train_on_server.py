import kashgari
import numpy
from .utils import getTrainData_from_line,getTrainData_from_json
from kashgari.embeddings import BERTEmbedding
from kashgari.tasks.labeling import BiLSTM_CRF_Model
from kashgari.utils import load_model
import re
import random

def getTrain(path='/home/peitian_zhang/data/corpus/labeled_train.txt'):
    train_data,_ = getTrainData_from_line(path)
    train_x = []
    train_y = []
    for coup in train_data:
        train_x.append(coup[0])
        train_y.append(coup[1])
    return train_x,train_y

def train_BiLSTM_CRF(train_test_devide=0.9,epoch=100,path='/home/peitian_zhang/data/corpus/labeled_train.txt'):
    
    train_x,train_y = getTrain(path)
    model = BiLSTM_CRF_Model(sequence_length=400)

    x = train_x[:int(len(train_x)*train_test_devide)+1]
    y = train_y[:int(len(train_x)*train_test_devide)+1]
    
    model.fit(x,y,x,y,epochs=epoch,batch_size=64)
    print('---------evaluate on train---------\n{}'.format(model.evaluate(train_x,train_y)))
    print('---------evaluate on test----------\n{}'.format(model.evaluate(train_x[int(len(train_x)*train_test_devide)+1:],train_y[int(len(train_x)*train_test_devide)+1:])))
    return model

def train_BERT_BiLSTM_CRF(train_test_devide=0.9,epoch=20,path='/home/peitian_zhang/data/corpus/labeled_train.txt'):
    train_x,train_y = getTrain(path)
    x = train_x[:int(len(train_x)*train_test_devide)+1]
    y = train_y[:int(len(train_x)*train_test_devide)+1]

    bert = BERTEmbedding(model_folder='/home/peitian_zhang/data/chinese_L-12_H-768_A-12',sequence_length=400,task=kashgari.LABELING)
    model = BiLSTM_CRF_Model(bert)

    model.fit(x,y,x,y,epochs=epoch,batch_size=64)

    print(model.evaluate(train_x,train_y))
    return train_x,train_y,model

def self_BiLSTM_CRF():
    START_TAG = "<START>"
    STOP_TAG = "<END>"
    PAD_TAG = "<PAD>"
    EMBEDDING_DIM = 300
    HIDDEN_DIM = 256
    
    training_data,tag_to_ix = getTrainData_from_line(r'..\..\data\语料\labeled_train.txt')
    print(tag_to_ix)
    word_to_ix = {}
    word_to_ix['<PAD>'] = 0
    for sentence, tags in training_data[:-50]:
        for word in sentence:
            if word not in word_to_ix:
                word_to_ix[word] = len(word_to_ix)

    model = BiLSTM_CRF_MODIFY_PARALLEL(len(word_to_ix), tag_to_ix, EMBEDDING_DIM, HIDDEN_DIM)
    optimizer = optim.SGD(model.parameters(), lr=0.01, weight_decay=1e-4)

    # Check predictions before training
    with torch.no_grad():
        precheck_sent = prepare_sequence(training_data[-1][0], word_to_ix)
        precheck_tags = torch.tensor([tag_to_ix[t] for t in training_data[0][1]], dtype=torch.long)
        print(model(precheck_sent))

    # Make sure prepare_sequence from earlier in the LSTM section is loaded
    for epoch in range(50):
        # Step 1. Remember that Pytorch accumulates gradients.
        # We need to clear them out before each instance
        model.zero_grad()
        # Step 2. Get our batch inputs ready for the network, that is,
        # turn them into Tensors of word indices.
        # If training_data can't be included in one batch, you need to sample them to build a batch
        sentence_in_pad, targets_pad = prepare_sequence_batch(training_data[0:-1], word_to_ix, tag_to_ix)
        # Step 3. Run our forward pass.
        loss = model.neg_log_likelihood_parallel(sentence_in_pad, targets_pad)
        # Step 4. Compute the loss, gradients, and update the parameters by
        # calling optimizer.step()
        loss.backward()
        optimizer.step()

    # Check predictions after training
    with torch.no_grad():
        #for i in (len(training_data)):
        precheck_sent = prepare_sequence(training_data[-49][0], word_to_ix)
        print("predict:{}\n target:{}".format(model(precheck_sent),
                                                  prepare_sequence(training_data[-49][1], tag_to_ix)))

def predict(model,sentences):
    test = [[char for char in sentence] for sentence in sentences]
    print(test)
    pred = model.predict(test)

    for index,line in enumerate(test):
        for char,tag in zip(line,pred[index]):
            print("{}---{}\n".format(char,tag))

def contrast(model,path='/home/peitian_zhang/data/corpus/labeled_train.txt'):
    train_x,train_y = getTrain(path)
    index = random.choice(range(0,len(train_x)))
    pred = model.predict([train_x[index]])[0]

    for tag,target in zip(pred,train_y[index]):
        print("{},{}\n".format(tag,target))

def load(path):
    load_model(path)

if __name__ == "__main__":
    model = load_model(r'D:\Ubuntu\rootfs\home\pt\models\bilstm+crf_epoch_100.model') 
    x,y =getTrain(path=r'D:\repositories\DaChuang\data\语料\train.txt')
    predict(model,x[-10:-5])