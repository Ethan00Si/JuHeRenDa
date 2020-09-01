import re
import jsonlines
import pandas
import json
import os
from py2neo import Graph,Node,Relationship

# 一次性完成教师信息的读取、处理、写入新文件；
# 将title和position合并，将姓名、专业、职务扩充进入相应位置的字典
def processTeachers(path='../../crawlers/teacher_each_school/crawler'):

    positions = []
    position_txt = open('../../data/词典/positions.txt','w',encoding='utf-8')
    
    for dir_path,dir_name,file_list in os.walk(path):
        for filename in file_list:
            if os.path.splitext(filename)[1]=='.json':
                with open('/'.join([dir_path,filename]),'r',encoding='utf-8') as f:
                    
                    g = open('../../data/teachers/%s' % filename,'w',encoding='utf-8')
                    major_txt = open('../../data/词典/majors/'+re.search('teachers_(.*).json',filename).group(1)+'_majors.txt','w',encoding='utf-8')
                    name_txt = open('../../data/词典/names/{}.txt'.format(re.search('teachers_(.*).json',filename).group(1)),'w',encoding='utf-8')

                    majors = []

                    for teacher in jsonlines.Reader(f):
                        major_pro = []
                        try:
                            major_list = teacher['major']
                            if major_list:
                                for major in major_list:
                                    subset = re.split('，|、|；|和|与',major)
                                    for val in subset:
                                        val = re.sub('[a-z]|[0-9]|[()-。,/等●《》（）]|（.*）|.*\.|\s|[A-Z]|课程|新兴领域|博客.*|张瑞君.*|主要讲授|主要研究','',val)
                                        if val:
                                            major_pro.append(val)
                                            if val not in majors:
                                                majors.append(val)
                                                major_txt.write(val+'\n')

                                    teacher['major'] = major_pro
                        except KeyError:
                            pass
                        
                        position_pro = set()
                        #title_pro = []
                        try:
                            title = teacher['title']
                            if title:
                                #print(title)
                                title_list = re.split('，|、| |/|。|；',title)

                                for tit in title_list:
                                    tit = re.sub(' |\s|[a-zA-Z:\?/男无\.=0-9《》]|\&|_','',tit)
                                    if tit:
                                        position_pro.add(tit)
                                        # 加入所有职称的集合
                                        if tit not in positions:
                                            positions.append(tit)
                                            position_txt.write(tit+'\n')
                            teacher['title'] = position_pro
                            del teacher['title']
                        except KeyError:
                            pass
                        
                        try:
                            position = teacher['position']
                            if position:
                                pos_list = re.split('，|、| |/|。|；',position)
                                
                                for pos in pos_list:
                                    pos = re.sub(' |\s|[a-zA-Z:\?/男无\.=0-9&_]','',pos)
                                    if pos:
                                        position_pro.add(pos)
                                        
                                        # 加入所有职称的集合
                                        if pos not in positions:
                                            positions.append(pos)
                                            position_txt.write(pos+'\n')
                                            
                                
                        except KeyError:
                            pass

                        teacher['position'] = list(position_pro)

                        try:
                            email = item['email']
                            email = re.sub(' ','',email)
                            email = re.sub('AT','@',email)
                            teacher['email'] = email

                        except KeyError:
                            pass

                        for prop in list(teacher.keys()):
                            if not teacher[prop]:
                                del teacher[prop]
                        
                        line = json.dumps(teacher,ensure_ascii=False)+'\n'
                        g.write(line)

                        name = teacher['name']
                        name_txt.write(name+'\n')

                    
                    g.close()
                    major_txt.close()
                    name_txt.close()
                    
    position_txt.close()
    return

def getLabs(path='../../data/词典/labs'):
    for dir_path,dir_name,file_list in os.walk(path):
        for filename in file_list:
            if os.path.splitext(filename)[1]=='.json':
                with open(path,'r',encoding='utf-8') as f:
                    g = open('../../data/词典/labs/'+re.search('labs_(.*).json',filename).group(1)+'txt','w',encoding='utf-8')
                    for lab in jsonlines.Reader(f):
                        g.write(lab['lab']+'\n')
                    g.close()
#合并各院的教师名进入一个txt
def mergeName():

    g = open('../../data/词典/names/names.txt','w',encoding='utf-8')
    dic = set()
    for dir_path,dir_name,file_list in os.walk('../../data/词典/names/'):
        for filename in file_list:
            if os.path.splitext(filename)[1]=='.txt':
                with open('/'.join([dir_path,filename]),'r',encoding='utf-8') as f:
                    for line in f:
                        dic.add(line.strip())
    for item in dic:
        g.write(item+'\n')
    g.close()

def mergeMajor():

    g = open('../../data/词典/majors/majors.txt','w',encoding='utf-8')
    dic = set()
    for dir_path,dir_name,file_list in os.walk('../../data/词典/majors/'):
        for filename in file_list:
            if os.path.splitext(filename)[1]=='.txt':
                with open('/'.join([dir_path,filename]),'r',encoding='utf-8') as f:
                    for line in f:
                        dic.add(line.strip())
    for item in dic:
        g.write(item+'\n')
    g.close()

#合并所有字典文件夹下的txt，进入dictionary.txt
def mergeDict():
    g = open(r'../../data/语料/dictionary.txt','r',encoding='utf-8')
    dic = set()
    for line in g:
        dic.add(line.strip())
    g.close

    g = open(r'../../data/语料/dictionary.txt','w',encoding='utf-8')

    for dir_path,dir_name,file_list in os.walk(r'D:\repositories\DaChuang\data\词典'):
        for filename in file_list:
            if os.path.splitext(filename)[1]=='.txt':
                with open('/'.join([dir_path,filename]),'r',encoding='utf-8') as f:
                    for line in f:
                        dic.add(line.strip())
    for item in dic:
        g.write(item+'\n')
    g.close()

def process():
    processTeachers()
    getLabs()
    mergeName()
    mergeDict()

def create_teacher_nodes(json_path='../../data/teachers'):
    
    entity2id={}

    graph = Graph('bolt://localhost:7687',username='neo4j',password='123456')
    id_node = 0
    #id_relation = -1

    #f = open('entity_total')
    for dir_path,dir_name,file_list in os.walk(json_path):
        for filename in file_list:
            if os.path.splitext(filename)[1]=='.json':
                with open('/'.join([dir_path,filename]),'r',encoding='utf-8') as f:
                    teachers = []

                    for item in jsonlines.Reader(f):
                        teacher = Node('Teacher',var=item['name'],id=id_node)
                        
                        entity2id[item['name']] = id_node
                        
                        for prop in list(item.keys()):
                            if prop != 'name':
                                teacher[prop] = item[prop]
                        
                        teachers.append(teacher)
                        graph.create(teacher)
                        id_node += 1

                        try:
                            for major in item['major']:
                                if major:
                                    
                                    majorNode = graph.nodes.match('Major',var=major).first()
                                    if majorNode:
                                        r = Relationship(teacher,'major_in',majorNode,id=-1)
                                        graph.create(r)
                                    else:
                                        majorNode = Node('Major',var=major,id=id_node)
                                        r = Relationship(teacher,'major_in',majorNode,id=-1)
                                        
                                        if major not in entity2id:
                                            entity2id[major] = id_node
                                        
                                        graph.create(r)
                                        id_node += 1
                        
                        except:
                            
                            print('%s have no major' % item['name'])
                        
                        #职位
                        try:
                            for position in item['position']:
                                if position:
                                #major = Node('Major',var=item['major'])
                                    posNode = graph.nodes.match('Position',var=position).first()
                                    if posNode:
                                        r = Relationship(teacher,'position_is',posNode,id=-2)
                                        graph.create(r)
                                    else:
                                        posNode = Node('Position',var=position,id=id_node)
                                        r = Relationship(teacher,'position_is',posNode,id=-2)
                                        graph.create(r)
                                        id_node += 1
                        except:
                            
                            print('%s have no position' % item['name'])
                        
                        #联系方式
                        #if item['email'] or item['phone'] or item['fax'] or item['office'] or item['homepage']:
                        #    contactNode = Node('Contact')
                        #    try:

                        '''
                        #邮箱
                        try:
                            for email in item['email']:
                                if email:
                                #major = Node('Major',var=item['major'])
                                    posNode = graph.nodes.match('email',var=email).first()
                                    if posNode:
                                        r = Relationship(teacher,'email_is',posNode)
                                        graph.create(r)
                                    else:
                                        posNode = Node('Email',var=email)
                                        r = Relationship(teacher,'email_is',posNode)
                                        graph.create(r)
                        
                        except:
                            
                            print('%s have no email' % item['name'])

                        #办公室
                        try:
                            for office in item['office']:
                                if office:
                                #major = Node('Major',var=item['major'])
                                    posNode = graph.nodes.match('office',var=office).first()
                                    if posNode:
                                        r = Relationship(teacher,'office_is',posNode)
                                        graph.create(r)
                                    else:
                                        posNode = Node('Office',var=office)
                                        r = Relationship(teacher,'office_is',posNode)
                                        graph.create(r)
                        
                        except:
                            
                            print('%s have no office' % item['name'])
                        
                        #电话
                        try:
                            for phone in item['phone']:
                                if phone:
                                #major = Node('Major',var=item['major'])
                                    posNode = graph.nodes.match('phone',var=phone).first()
                                    if posNode:
                                        r = Relationship(teacher,'phone_is',posNode)
                                        graph.create(r)
                                    else:
                                        posNode = Node('Phone',var=phone)
                                        r = Relationship(teacher,'phone_is',posNode)
                                        graph.create(r)
                        
                        except:
                            print('%s have no phone' % item['name'])
                        '''
                    department = teachers[0]['department']
                    departNode = Node('Department',var=department,id=id_node)
                    
                    entity2id[department] = id_node

                    graph.create(departNode)
                    id_node += 1

                    for teacher in teachers:
                        r = Relationship(teacher,'in',departNode,id=-4)
                        graph.create(r)
    return id_node,entity2id

def create_lab_nodes(id_start,entity2id,json_path=r"../../data/词典/labs"):
    
    graph = Graph('bolt://localhost:7687',username='neo4j',password='123456')
    id_node = id_start
    #id_relation = -1

    for dir_path,dir_name,file_list in os.walk(json_path):
        for filename in file_list:
            if os.path.splitext(filename)[1]=='.json':
                with open('/'.join([dir_path,filename]),'r',encoding='utf-8') as f:
                    for item in jsonlines.Reader(f):
                        lab = Node('Lab',var=item['lab'],id=id_node)
                        
                        entity2id[item['lab']] = id_node

                        try:
                            lab['url'] = item['url']
                        except KeyError:
                            print("lab %s has no url" %item['lab'])

                        graph.create(lab)
                        id_node += 1

                        try:
                            for member in item['members']:
                                if member:
                                    #print(major)
                                
                                    memberNode = graph.nodes.match('Teacher',var=member,department=item['department']).first()
                                    if memberNode:
                                        r = Relationship(memberNode,'work_in',lab,id=-5)
                                        graph.create(r)
                                    else:
                                        print('wrong menber %s in %s' % (member,lab))
                        except:
                            print("lab %s has no members" % item['lab'])
    return id_node,entity2id

def create_graph(path='../../data/teachers'):
    _id,_entity2id = create_teacher_nodes(path)
    _id,_entity2id = create_lab_nodes(_id,_entity2id)
    line = json.dumps(_entity2id,ensure_ascii=False)
    f = open('entity2id.json','w',encoding='utf-8')
    f.write(line)
    f.close()

def getEntity_from_neo(path):

    data = pandas.read_csv(path,encoding='utf-8')

    titles = data.title
    names = open('/data/词典/names/names.txt','r',encoding='utf-8')
    #majors = open('/data/词典/names/majors.txt','r',encoding='utf-8')
    f = open(r'/utils/process_entity/entity2id.json','r',encoding='utf-8')

    entity2id = json.loads(f.read(),encoding='utf-8')
    name_list = []

    f.close()

    for line in names:
        name_list.append(line.strip())

    for index,title in enumerate(titles):
        entity_id_list = []
        entity_idx_list = []
        for name in name_list:
            match = re.search(name,title)
            if match:
                entity = match.group()
                #只加了信息和经济两个学院的老师，所以肯定有在字典里但不在entity2id里的内容
                try:
                    entity_id = entity2id[entity]
                    entity_idx = match.span()
                    entity_id_list.append(str(entity_id))
                    entity_idx_list.append(str(entity_idx[0])+','+str(entity_idx[1]))
                except:
                    pass
        
        if entity_id_list:
            data.loc[index,'entity_id'] = ' '.join(entity_id_list)
            data.loc[index,'entity_idx'] = ' '.join(entity_idx_list)
            data.loc[index,'relation_id'] = ''
        else:
            data.loc[index,'entity_id'] = ''
            data.loc[index,'entity_idx'] = ''
            data.loc[index,'relation_id'] = ''
    
    data.to_csv(path,index=False)

    return
