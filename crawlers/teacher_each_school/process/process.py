import re
import jsonlines
import pandas
import json

def process_majors(path):
    with open(path,'r',encoding='utf-8') as f:
        path_new = re.search('(teachers_.*).json',path).group(1)+'_pro.json'
        with open(path_new,'w',encoding='utf-8') as g:
            for teacher in jsonlines.Reader(f):
                try:
                    majorLine = teacher['major']
                    if majorLine is not None:
                        majors = re.split('，|、|；',majorLine)
                        majorSet = set(majors)
                        majorList = []
                        for major in majorSet:
                            major_1 = re.sub('[a-z]|[0-9]|[()-。,/等●]|（.*）|.*\.|\s|[A-Z]|新兴领域|博客.*|张瑞君.*','',major)
                            majorList.append(major_1)
                        teacher['major'] = majorList
                except:
                    pass
                line = json.dumps(teacher,ensure_ascii=False)+'\n'
                g.write(line)

    return getMajors(path_new)

def getMajors(path):
    g = open(re.search('teachers_(.*)_pro.json',path).group(1)+'_majors.txt','w',encoding='utf-8')
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

def getTeacherName(path):
    #得到学院所有老师名字
    with open(path,'r',encoding='utf-8') as f:
        g = open('../../../data/词典/names/{}.txt'.format(re.search('teachers_(.*).json',path).group(1)),'w',encoding='utf-8')
        for teacher in jsonlines.Reader(f):
            name = teacher['name']
            g.write(name+'\n')
        g.close()

def getPosition(path):
    with open(path,'r',encoding='utf-8') as f:
        g = open('../../../data/词典/titles/{}.txt'.format(re.search('teachers_(.*).json',path).group(1)),'w',encoding='utf-8')
        for teacher in jsonlines.Reader(f):
            try:
                position = teacher['position']
                g.write(name+'\n')
        g.close()