import kashgari
import numpy
from utils.utils import getTrainData_from_line,getTrainData_from_json
from kashgari.embeddings import BERTEmbedding
from kashgari.tasks.labeling import BiLSTM_CRF_Model
import re

def train_BiLSTM_CRF(path):
    train_data,_ = getTrainData_from_line(path)
    train_x = []
    train_y = []
    for coup in train_data:
        train_x.append(coup[0])
        train_y.append(coup[1])
    
    model = BiLSTM_CRF_Model()
    model.fit(train_x,train_y,epochs=100,batch_size=64)
    print(model.evaluate(train_x,train_y))
    return model

def train_BERT_BiLSTM_CRF(path):
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

def evaluate(model):
    print(model.predict('窦 志 成 参 加 教 研 会'.split(' ')))
