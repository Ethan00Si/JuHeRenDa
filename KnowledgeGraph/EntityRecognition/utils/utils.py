import pandas
import re
import jsonlines
import json
from collections import Counter
import kashgari
from kashgari.utils import load_model

GOLDEN_LENGTH = 403

def getSeperated(segment,idx_range,path,meta_data,news_idx):
    f = open(path,'a+',encoding='utf-8')
    for each in idx_range:
        if each:
            line = segment[int(each)]
            for character in line:
                f.write(character+'\n')
            f.write('\n')
    f.close()
    try:
        department = re.search('(.*?)\.',meta_data['source']).group(1)
    except AttributeError:
        department = meta_data['source']
    g = open('../../data/语料/sample_news_idx/{}.txt'.format(department),'a+',encoding='utf-8')
    g.write('{}'.format(news_idx)+'\n')
    g.close()

def getTrainData_from_line(path):
            
        
    refer_dict ={
        "a":"O",    #Others 无关
        "b":"B-C",  #Conference 会议、讲座、刊物的开始
        "c":"I-C",  #Conference 会议、讲座、刊物的中间
        "d":"B-A",  #Award 奖项的开始
        "e":"I-A",  #Award 奖项的中间
        "f":"B-O",  #Organization 组织的开始
        "g":"I-O",  #Organization 组织的中间
        "h":"B-M",  #Major 专业、课程的开始   
        "i":"I-M",  #Major 专业、课程的中间
        "j":"B-P",  #Position 职位、职称的开始
        "k":"I-P",  #Position 职位、职称的中间
        "l":"B-N",  #Name 人名的开始
        "m":"I-N",  #Name 人名的中间
        "n":"B-D",  #Department 学校、学院、系别的开始
        "o":"I-D",  #Department 学校、学院、系别的中间
        "p":"B-S",  #Scholarship 项目、夏令营、考试等学生活动的开始
        "q":"I-S",  #Scholarship 项目、夏令营、考试等学生活动的中间
        "r":"B-L",  #地点的开始
        "s":"I-L",  #地点的中间
        "t":"O",  #论文的开始
        "u":"O"   #论文的中间
    }

    tag_idx = dict()
    for item in refer_dict.values():
        tag_idx[item] = len(tag_idx)
    
    tag_idx['<START>'] = len(tag_idx)
    tag_idx['<END>'] = len(tag_idx)
    tag_idx['<PAD>'] = len(tag_idx)

    f = open(path,'r',encoding='utf-8-sig')
    trainData = []
    sentence = []
    tags = []
    count = 0
    for line in f:
        if line == '\n':
            if len(sentence) != len(tags):
                #print(sentence)
                print("Dismatch in characters and tags")
                raise IndexError
            if len(sentence) < 5:
                print("Format Error")
                sentence = []
                tags = []
                continue
            trainData.append((sentence,tags))
            sentence = []
            tags = []
            continue
        else:
            sentence.append(line[0].strip())
            if line[1].strip():
                try:
                    tags.append(refer_dict[line[1]])
                except:
                    print(count,sentence)
                    raise KeyError    
            else:
                try:
                    key = line[2]
                    if key.strip():
                        try:
                            tags.append(refer_dict[line[2]])
                        except KeyError:
                            raise KeyError
                            print(count,sentence)
                    else:
                        tags.append('O')
                except IndexError:
                    tags.append('O')
        count += 1
    f.close()

    return trainData,tag_idx

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
    dist = r'../../data/语料/train.txt'
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
            f = open(dist,'r',encoding='utf-8')
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
            
def getSum(path):
    count = 0
    f = open(path,'r',encoding='utf-8')
    for line in f:
        if line == '\n':
            count += 1
        
    f.close()
    print(count)

######################### Implement of Entity Recognition ###########################
def getEntity_from_NER(model,data):
    refer_dict ={
        "C":"Conference",  #Conference 会议、讲座、刊物的开始
        "A":"Award",  #Award 奖项的开始
        "O":"Organization",  #Organization 组织的开始
        "M":"Major",  #Major 专业、课程的开始   
        "P":"Position",  #Position 职位、职称的开始
        "N":"Name",  #Name 人名的开始
        "D":"Department",  #Department 学校、学院、系别的开始
        "S":"Scholarship",  #Scholarship 项目、夏令营、考试等学生活动的开始
        "L":"Location",  #地点的开始
    }

    #f是entity对应的id，遇到新的就扩充
    f = open(r'D:\repositories\DaChuang\utils\process_entity\entity2id.json','r',encoding='utf-8')
    #g是新识别出的entity的json文件，一行是一个entity
    g = open('entity_foreign.json','a',encoding='utf-8')

    entity2id = json.loads(f.read(),encoding='utf-8')
    f.close()

    data.reset_index(drop=True, inplace=True)
    titles = data['title']

    text = [[char for char in title] for title in titles]
    pred_tags = model.predict(text)
    entities = []
    
    for idx,couple in enumerate(zip(titles,pred_tags)):
        session = []
        indexes = []
        entity_each = []
        #entity_var = ''
        for index,char in enumerate(couple[1]):
            if char != 'O' and char[0] != 'B':
                session.append(char[2])
                indexes.append(index)
                #entity_var += char
            
            elif char[0] == 'B':
                if len(session) > 1:
                    #print(session)
                    session_count = Counter(session)
                    #应对不在refer_dict中，即想排除的实体
                    try:
                        entity = refer_dict[session_count.most_common(1)[0][0]]
                        cover = (indexes[0],indexes[-1]+1)
                        var = couple[0][cover[0]:cover[1]]
                        entity_each.append((entity,var,cover))
                    except:
                        pass
                session = [char[2]]
                indexes = [index]    
                    #entity_var = [char]
            
            else:
                if len(session) > 1:
                    #print(session)
                    session_count = Counter(session)
                    #应对不在refer_dict中，即想排除的实体
                    try:
                        entity = refer_dict[session_count.most_common(1)[0][0]]
                        cover = (indexes[0],indexes[-1]+1)
                        var = couple[0][cover[0]:cover[1]]
                        entity_each.append((entity,var,cover))
                    except:
                        pass
                    session = []
                    indexes = []
        if len(session) > 1:
            session_count = Counter(session)
            #应对不在refer_dict中，即想排除的实体
            try:
                entity = refer_dict[session_count.most_common(1)[0][0]]
                cover = (indexes[0],indexes[-1]+1)
                var = couple[0][cover[0]:cover[1]]
                entity_each.append((entity,var,cover))
            except:
                pass
        
        if entity_each:
            entities.append(entity_each)
            entity_id_list = []
            entity_idx_list = []
            for each in entity_each:
                
                if each[0] == 'Name':
                    continue

                entity_dic = {}

                #cover = each[1]
                entity_var = each[1]

                try:
                    entity_id = entity2id[entity_var]
                except KeyError:
                    entity_id = len(entity2id)
                    entity2id[entity_var] = entity_id
                
                entity_dic['var'] = entity_var
                entity_dic['type'] = each[0]
                entity_dic['id'] = entity_id
                #新的实体写入json，方便日后修改
                g.write(json.dumps(entity_dic,ensure_ascii=False) + '\n')
                

                entity_id_list.append(str(entity_id))
                entity_idx_list.append(str(cover[0]) + ',' + str(cover[1]))

        data.loc[idx,'entity_id'] = ' '.join(entity_id_list)
        data.loc[idx,'entity_idx'] = ' '.join(entity_idx_list)
        
        '''关系抽取
        # title:标题内容
        # entity_each:该标题中所有实体的列表，列表元素为(entity_type,entity_var,entity_span)
        # 其中entity_type为实体类型,entity_var为实体值,entity_span为实体所在的位置
        
        '''

    g.close()
    f = open(r'D:\repositories\DaChuang\utils\process_entity\entity2id_new.json','w',encoding='utf-8')
    line = json.dumps(entity2id,ensure_ascii=False)
    f.write(line)
    f.close()
    

    return data,entities


if __name__ == "__main__":
    model = load_model(r'D:\Ubuntu\rootfs\home\pt\models\BILSTM_CRF_epoch_100.model')
    data = pandas.read_csv(r'D:\repositories\DaChuang\data\news_each_school\info_output.csv',encoding='utf-8')
    a = data.loc[0:5,:]
    data,entities = getEntity_from_NER(model,data)
    print(entities)
    print(data)