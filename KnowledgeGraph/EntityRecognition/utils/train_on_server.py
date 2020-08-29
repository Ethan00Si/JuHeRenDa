import kashgari
import numpy
from .utils import getTrainData_from_line,getTrainData_from_json
from kashgari.embeddings import BERTEmbedding
from kashgari.tasks.labeling import BiLSTM_CRF_Model
from kashgari.utils import load_model
import re
import random

def getTrain(path):
    train_data,_ = getTrainData_from_line(path)
    train_x = []
    train_y = []
    for coup in train_data:
        train_x.append(coup[0])
        train_y.append(coup[1])
    return train_x,train_y

def train_BiLSTM_CRF(train_test_devide=0.9,epoch=100,path='/home/peitian_zhang/data/corpus/labeled_train.txt'):
    
    train_x,train_y = getTrain(path)
    model = BiLSTM_CRF_Model()

    x = train_x[:int(len(train_x)*train_test_devide)+1]
    y = train_y[:int(len(train_x)*train_test_devide)+1]
    
    model.fit(x,y,x,y,epochs=epoch,batch_size=64)
    print('---------evaluate on train---------\n{}'.format(model.evaluate(train_x,train_y)))
    print('---------evaluate on test----------\n{}'.format(model.evaluate(train_x[int(len(train_x)*train_test_devide)+1:],train_y[int(len(train_x)*train_test_devide)+1:])))
    try:
        model.save('/home/peitian_zhang/models/bert_epoch_{}'.format(epoch))
        print('Success in saving!')
    except:
        pass
    return model

def train_BERT_BiLSTM_CRF(train_test_devide=0.9,epoch=20,path='/home/peitian_zhang/data/corpus/labeled_train.txt'):
    train_x,train_y = getTrain(path)
    x = train_x[:int(len(train_x)*train_test_devide)+1]
    y = train_y[:int(len(train_x)*train_test_devide)+1]

    bert = BERTEmbedding(model_folder='/home/peitian_zhang/data/chinese_L-12_H-768_A-12',sequence_length=400,task=kashgari.LABELING)
    model = BiLSTM_CRF_Model(bert)

    model.fit(x,y,x,y,epochs=epoch,batch_size=64)

    print('---------evaluate on train---------\n{}'.format(model.evaluate(train_x,train_y)))
    print('---------evaluate on test----------\n{}'.format(model.evaluate(train_x[int(len(train_x)*train_test_devide)+1:],train_y[int(len(train_x)*train_test_devide)+1:])))
    try:
        model.save('/home/peitian_zhang/models/bert_epoch_{}'.format(epoch))
        print('Success in saving!')
    except:
        pass
    return model

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