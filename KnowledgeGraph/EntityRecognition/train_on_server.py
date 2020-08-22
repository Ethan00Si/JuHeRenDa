import kashgari
import numpy
from utils.utils import getTrainData_from_line,getTrainData_from_json
from kashgari.embeddings import BERTEmbedding
from kashgari.tasks.labeling import BiLSTM_CRF_Model
import re
import random

def train_BiLSTM_CRF(devision=0.9,epoch=100,path='/home/peitian_zhang/data/corpus/labeled_train.txt'):
    train_data,_ = getTrainData_from_line(path)
    train_x = []
    train_y = []
    for coup in train_data:
        train_x.append(coup[0])
        train_y.append(coup[1])
    
    model = BiLSTM_CRF_Model()
    model.fit(train_x[:int(len(train_x)*devision)+1],train_y[:int(len(train_x)*devision)+1],epochs=epoch,batch_size=64)
    print('---------evaluate on train---------\n{}'.format(model.evaluate(train_x,train_y)))
    print('---------evaluate on test----------\n{}'.format(model.evaluate(train_x[int(len(train_x)*devision)+1:],train_y[int(len(train_x)*devision)+1:])))
    return model

def train_BERT_BiLSTM_CRF(path='/home/peitian_zhang/data/corpus/labeled_train.txt'):
    train_data,_ = getTrainData_from_line(path)
    train_x = []
    train_y = []
    for coup in train_data:
        train_x.append(coup[0])
        train_y.append(coup[1])
    
    bert = BERTEmbedding(model_folder='/home/peitian_zhang/data/chinese_L-12_H-768_A-12',sequence_length=400,task=kashgari.LABELING)
    model = BiLSTM_CRF_Model(bert)

    model.fit(train_x,train_y,epochs=100,batch_size=64)
    print(model.evaluate(train_x,train_y))
    return model

def predict(model,sentence):
    test = []
    for character in sentence:
        test.append(character)
    
    print(model.predict([test]))

def contrast(model,train_x,train_y):
    index = random.choice(range(0,len(train_x)))
    pred = model.predict([train_x[index]])
    print("predict:%s,\n,target:%s" % pred[0],train_y[index])
