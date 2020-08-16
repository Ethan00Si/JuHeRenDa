import pandas
import re
import jsonlines

def getSeperated(segment,idx_range,path,meta_data,news_idx):
    f = open(path,'a+',encoding='utf-8')
    for each in idx_range:
        
        line = segment[int(each)]
        for character in line:
            f.write(character+'\n')
        f.write('\n')
    f.close()
    department = re.search('(.*?)\.',meta_data['source']).group(1)
    g = open('D:/codes/Pt_Pytorch/data/corpus/{}.txt'.format(department),'a+',encoding='utf-8')
    g.write('{}'.format(news_idx)+'\n')
    g.close()

def getTrainData_from_line(path):
            
        
    refer_dict ={ 
        "a":"O",    #Others 无关
        "b":"B-C",  #Conference 会议、讲座、期刊、刊物的开始
        "c":"I-C",  #Conference 会议、讲座、期刊、刊物的中间
        "d":"B-A",  #Award 奖项的开始
        "e":"I-A",  #Award 奖项的中间
        "f":"B-O",  #Organization 组织的开始
        "g":"I-O",  #Organization 组织的中间
        "h":"B-M",  #Major 专业的开始   
        "i":"I-M",  #Major 专业的中间
        "j":"B-P",  #Position 职位、职称的开始
        "k":"I-P",  #Position 职位、职称的中间
        "l":"B-N",  #Name 人名的开始
        "m":"I-N",  #Name 人名的中间
        "n":"B-D",  #Department 学校、学院、系别的开始
        "o":"I-D",  #Department 学校、学院、系别的中间
        "p":"B-S",  #Scholarship 项目、学生活动、奖学金的开始
        "q":"I-S"   #Scholarship 项目、学生活动、奖学金的中间
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

def manual_sampling(path):
    data = pandas.read_csv(path)
    dist = r'D:\codes\Pt_Pytorch\data\corpus\train_taobao.txt'
    sentence = data.content
    start = input("index:")
    i = int(start)
    while 1:
        i += 1
        segment = re.split("；|。",sentence[i])
        print('******************************{}******************************'.format(i))
        for index,each in enumerate(segment):
            print(index,each)
        prompt = input()
        if prompt == 'sum':
            count = 0
            f = open(r'D:\codes\Pt_Pytorch\data\corpus\train_taobao.txt','r',encoding='utf-8')
            for line in f:
                #print(line)
                if line == '\n':
                    count += 1
            f.close()
            print(count)
            i -= 1
        elif prompt == 'exit':
            break
        elif prompt == '':
            continue
        else:
            idx_range = re.split(' +',prompt.strip())
            #print(idx_range)
            getSeperated(segment,idx_range,dist,data.loc[0,:],i)
    return
            