import re
import jsonlines
import pandas
import json
import os

def processMajors(path):
    majors = set()
    for dir_path,dir_name,file_list in os.walk('../../../crawlers/teacher_each_school/crawler/teacher'):
        for filename in file_list:
            if os.path.splitext(filename)[1]=='.json':
                with open('/'.join([dir_path,filename]),'r',encoding='utf-8') as f:
                    majors_sub = []
                    g = open('../../../data/teachers/%s'.format(filename),'w',encoding='utf-8')
                    h = open('../../../data/词典/majors/'+re.search('teachers_(.*).json',filename).group(1)+'_majors.txt','w',encoding='utf-8')
                    for teacher in jsonlines.Reader(f):
                        try:
                            for major in teacher['major']:
                                subset = re.split('，|、|；|和|与',major)
                                for index,val in enumerate(subset):
                                    subset[index] = re.sub('[a-z]|[0-9]|[()-。,/等●《》（）]|（.*）|.*\.|\s|[A-Z]|课程|新兴领域|博客.*|张瑞君.*|主要讲授|主要研究','',val)
                                majors_sub += subset
                                teacher['major'] = subset
                        except KeyError:
                            pass
                    
                    line = json.dumps(teacher,ensure_ascii=False)+'\n'
                    g.write(line)
                    
                    for item in set(majors_sub):
                        h.write(item+'\n')

                    g.close()
                    h.close()
    
    '''
    f = open(path,'r',encoding='utf-8')
    g = open('../../../data/词典/majors/'+re.search('teachers_(.*).json',path).group(1)+'_majors.txt','w',encoding='utf-8')
    h = open('../../../data/teachers/teachers_'+re.search('teachers_(.*).json',path).group(1)+'.json','w',encoding='utf-8')
    for teacher in jsonlines.Reader(f):
        try:
            for major in teacher['major']:
                subset = re.split('，|、|；|和|与',major)
                for index,val in enumerate(subset):
                    subset[index] = re.sub('[a-z]|[0-9]|[()-。,/等●《》（）]|（.*）|.*\.|\s|[A-Z]|课程|新兴领域|博客.*|张瑞君.*|主要讲授|主要研究','',val)
                majors += subset
                teacher['major'] = subset
        except KeyError:
            pass
        
        line = json.dumps(teacher,ensure_ascii=False)+'\n'
        h.write(line)
    majorSet = set(majors)
    for each in majorSet:
        if each:
            g.write(each+'\n')
    
    f.close()
    g.close()
    h.close()
    '''
    return
'''
def process_majors(path):
    with open(path,'r',encoding='utf-8') as f:
        path_new = re.search('(teachers_.*).json',path).group(1)+'_pro.json'
        with open(path_new,'w',encoding='utf-8') as g:
            for teacher in jsonlines.Reader(f):
                try:
                    majorLine = teacher['major']
                    if majorLine:
                        majors = re.split('，|、|；|和|与',majorLine)
                        majorSet = set(majors)
                        majorList = []
                        for major in majorSet:
                            major_1 = re.sub('[a-z]|[0-9]|[()-。,/等●《》（）]|（.*）|.*\.|\s|[A-Z]|课程|新兴领域|博客.*|张瑞君.*|主要讲授|主要研究','',major)
                            majorList.append(major_1)
                        teacher['major'] = majorList
                except:
                    pass
                line = json.dumps(teacher,ensure_ascii=False)+'\n'
                g.write(line)

    return getMajors(path_new)

def process_titles(path):
    with open(path,'r',encoding='utf-8') as f:
        path_new = re.search('(teachers_.*).json',path).group(1)+'.json'
        g = open(path_new,'w',encoding='utf-8')
        for teacher in jsonlines.Reader(f):
            try:
                teacher['title'] = re.sub(' | ','',teacher['title'])
            except:
                pass
            line = json.dumps(teacher,ensure_ascii=False)+'\n'
            g.write(line)
        g.close()

def getMajors(path):
    g = open('../../../data/词典/majors/'+re.search('teachers_(.*)_pro.json',path).group(1)+'_majors.txt','w',encoding='utf-8')
    majorList = []
    with open(path,'r',encoding='utf-8') as f:
        for teacher in jsonlines.Reader(f):
            try:
                majorList += teacher['major']
            except:
                continue
    majorSet = set(majorList)
    for major in majorSet:
        if major != '':
            g.write(major+'\n')

    g.close()
'''
def getTeacherName():
    #得到学院所有老师名字
    for dir_path,dir_name,file_list in os.walk('../../../data/teachers'):
        for filename in file_list:
            if os.path.splitext(filename)[1]=='.json':
                with open('/'.join([dir_path,filename]),'r',encoding='utf-8') as f:
                    g = open('../../../data/词典/names/{}.txt'.format(re.search('teachers_(.*).json',filename).group(1)),'w',encoding='utf-8')
                    for teacher in jsonlines.Reader(f):
                        name = teacher['name']
                        g.write(name+'\n')
                    g.close()

    '''
    with open(path,'r',encoding='utf-8') as f:
        g = open('../../../data/词典/names/{}.txt'.format(re.search('teachers_(.*).json',path).group(1)),'w',encoding='utf-8')
        for teacher in jsonlines.Reader(f):
            if type(teacher['name'])==list:
                name = teacher['name'][0]
            else:
                name = teacher['name']

    ''' 
        

#注意使用a+，因为positions.txt中我删除了一个“兼”字
def getPositions():
    positions = []
    g = open('../../../data/词典/positions.txt','w',encoding='utf-8')
    g.seek(0)
    for line in g:
        if line != '\n':
            positions.append(line.strip())

    for dir_path,dir_name,file_list in os.walk('../../../data/teachers'):
        for filename in file_list:
            if os.path.splitext(filename)[1]=='.json':
                with open('/'.join([dir_path,filename]),'r',encoding='utf-8') as f:
                    for teacher in jsonlines.Reader(f):
                        try:
                            position = teacher['position']
                            pos_list = re.split('，|、| |/|。|；',position)
                            for pos in pos_list:
                                pos = re.sub(' |\s|[a-zA-Z:\?/男无\.=0-9&_]','',pos)
                                if pos and pos not in positions:
                                    positions.append(pos)
                                    g.write(pos+'\n')
                        except:
                            pass
                        position = teacher['title']
                        if position:
                            pos_list = re.split('，|、| |/|。|；',position)
                            for pos in pos_list:
                                pos = re.sub(' |\s|[a-zA-Z:\?/男无\.=0-9《》]|\&|_','',pos)
                                if pos and pos not in positions:
                                    positions.append(pos)
                                    g.write(pos+'\n')
    g.close()
    '''
    g = open('../../../data/词典/position.txt','r',encoding='utf-8')
    h = open('../../../data/词典/positions.txt','w',encoding='utf-8')

    for line in g:
        text = re.sub('\s|[a-zA-Z:\?/男]','',line)
        if text:
            h.write(text+'\n')
    g.close()
    h.close()
    '''
def getLabs(path):
    with open(path,'r',encoding='utf-8') as f:
        g = open('../../../data/词典/labs/{}.txt'.format(re.search('labs_(.*).json',path).group(1)),'w',encoding='utf-8')
        for lab in jsonlines.Reader(f):
            g.write(lab['lab']+'\n')
        g.close()

def mergeDict():
    g = open(r'../../../data/语料/dictionary.txt','r',encoding='utf-8')
    dic = set()
    for line in g:
        dic.add(line.strip())
    g.close

    g = open(r'../../../data/语料/dictionary.txt','w',encoding='utf-8')

    for dir_path,dir_name,file_list in os.walk(r'D:\repositories\DaChuang\data\词典'):
        for filename in file_list:
            if os.path.splitext(filename)[1]=='.txt':
                with open('/'.join([dir_path,filename]),'r',encoding='utf-8') as f:
                    for line in f:
                        dic.add(line.strip())
    for item in dic:
        g.write(item+'\n')
    g.close()