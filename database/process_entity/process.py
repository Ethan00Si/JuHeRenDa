import re
import jsonlines
import pandas
import json
import os

def processTeachers(path=r'D:\codes\Pt_MarkDown\大创\teachers'):

    positions = []
    position_txt = open('../../data/词典/positions.txt','w',encoding='utf-8')
    
    for dir_path,dir_name,file_list in os.walk(path):
        for filename in file_list:
            if os.path.splitext(filename)[1]=='.json':
                with open('/'.join([dir_path,filename]),'r',encoding='utf-8') as f:
                    majors_sub = []
                    g = open('../../data/teachers/%s' % filename,'w',encoding='utf-8')
                    major_txt = open('../../data/词典/majors/'+re.search('teachers_(.*).json',filename).group(1)+'_majors.txt','w',encoding='utf-8')
                    name_txt = open('../../data/词典/names/{}.txt'.format(re.search('teachers_(.*).json',filename).group(1)),'w',encoding='utf-8')

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
                        
                        position_pro = []
                        try:
                            title = teacher['title']
                            if title:
                                title_list = re.split('，|、| |/|。|；',title)

                                for tit in title_list:
                                    tit = re.sub(' |\s|[a-zA-Z:\?/男无\.=0-9《》]|\&|_','',tit)
                                    if tit:
                                        position_pro.append(tit)
                                        # 加入所有职称的集合
                                        if tit not in positions:
                                            positions.append(tit)
                                            position_txt.write(tit+'\n')
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
                                        position_pro.append(pos)
                                        
                                        # 加入所有职称的集合
                                        if pos not in positions:
                                            positions.append(pos)
                                            position_txt.write(pos+'\n')
                                            
                                
                        except KeyError:
                            pass

                        teacher['position'] = position_pro

                        
                        for prop in list(teacher.keys()):
                            if not teacher[prop]:
                                del teacher[prop]
                        
                        line = json.dumps(teacher,ensure_ascii=False)+'\n'
                        g.write(line)

                        name = teacher['name']
                        name_txt.write(name+'\n')

                    
                    for item in set(majors_sub):
                        if item:
                            major_txt.write(item+'\n')
                    
                    g.close()
                    major_txt.close()
                    name_txt.close()
                    
    position_txt.close()
    return

def merge():

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