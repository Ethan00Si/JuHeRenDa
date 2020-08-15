import pandas
import re
import jsonlines

def getSeperated(lines,path):
    f = open(path,'a+',encoding='utf-8')
    for line in lines:
        for character in line:
            f.write(character+'\n')
        f.write('\n')
    f.close()

def getTrainData_from_line(path):
            
        
    refer_dict = {
        "a":"O",    #无关
        "b":"B-C",  #会议、讲座、期刊的开始
        "c":"I-C",  #会议、讲座、期刊的中间
        "d":"B-A",  #奖项的开始
        "e":"I-A",  #奖项的中间
        "f":"B-O",  #组织的开始
        "g":"I-O",  #组织的中间
        "h":"B-M",  #专业的开始   
        "i":"I-M",  #专业的中间
        "j":"B-P",  #职位、职称的开始
        "k":"I-P", #职位、职称的中间
        "l":"B-N",  #人名的开始
        "m":"I-N"   #人名的中间
    }

    f = open(path,'r',encoding='utf-8')
    trainData = []
    sentence = []
    tags = []
    for line in f:
        if line == '\n':
            print(len(sentence),len(tags))
            trainData.append((sentence,tags))
            sentence = []
            tags = []
            continue
        else:
            sentence.append(line[0].strip())
            try:
                key = line[2]
                if key.strip():
                    tags.append(refer_dict[line[2]])
            except IndexError:
                tags.append('O')
    f.close()

    return trainData

def getTrainData_from_json(path,start,end):
    f = open(path,'r',encoding='utf-8')
    train_data = []
    for line in jsonlines.Reader(f):
        _sentence = []
        _tags = []

        qualified = False
        text = line['text']
        labels = line['label']
        tags = ['O']*len(text)
        try:
            for each in labels['organization']:
                e_range = labels['organization'][each][0]
                tags[e_range[0]] = 'B-O'
                for index in range(e_range[0]+1,e_range[1]+1):
                    tags[index] = 'I-O'
            qualified = True
        except:
            pass
        try:
            for each in labels['book']:
                e_range = labels['book'][each][0]
                tags[e_range[0]] = 'B-C'
                for index in range(e_range[0]+1,e_range[1]+1):
                    tags[index] = 'I-C'
            qualified = True
        except:
            pass
        if qualified:
            for index in range(len(text)):
                _sentence.append(text[index])
                _tags.append(tags[index])
            train_data.append((_sentence,_tags))
    f.close()
    return train_data[start:end]
