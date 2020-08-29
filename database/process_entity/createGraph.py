from py2neo import Graph,Node,Relationship
import jsonlines
import os

def create_teacher_nodes(json_path=r"D:\codes\Pt_MarkDown\大创\teachers"):
    
    graph = Graph('bolt://localhost:7687',username='neo4j',password='123456')
    id_node = 0
    #id_relation = -1
    for dir_path,dir_name,file_list in os.walk(json_path):
        for filename in file_list:
            if os.path.splitext(filename)[1]=='.json':
                with open('/'.join([dir_path,filename]),'r',encoding='utf-8') as f:
                    teachers = []

                    for item in jsonlines.Reader(f):
                        teacher = Node('Teacher',var=item['name'],id=id_node)
                        
                        id_node += 1
                        
                        for prop in list(item.keys()):
                            if prop != 'name':
                                teacher[prop] = item[prop]
                        
                        teachers.append(teacher)
                        graph.create(teacher)

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
                                        graph.create(r)
                                        id_node += 1
                        
                        except:
                            
                            print('%s have no major' % item['name'])
                        '''
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
                                        posNode = Node('Position',var=position)
                                        r = Relationship(teacher,'position_is',posNode,id=-2)
                                        graph.create(r)
                        
                        except:
                            
                            print('%s have no position' % item['name'])

                        #职称
                        try:
                            for title in item['title']:
                                if title:
                                #major = Node('Major',var=item['major'])
                                    posNode = graph.nodes.match('Title',var=title).first()
                                    if posNode:
                                        r = Relationship(teacher,'title_is',posNode,id=-3)
                                        graph.create(r)
                                    else:
                                        posNode = Node('Title',var=title)
                                        r = Relationship(teacher,'title_is',posNode,id=-3)
                                        graph.create(r)
                        
                        except:
                            
                            print('%s have no title' % item['name'])
                        '''
                        '''
                        #联系方式
                        if item['email'] or item['phone'] or item['fax'] or item['office'] or item['homepage']:
                            contactNode = Node('Contact')
                            try:

                        
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
                                        posNode = Node('email',var=email)
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
                                        posNode = Node('office',var=office)
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
                                        posNode = Node('phone',var=phone)
                                        r = Relationship(teacher,'phone_is',posNode)
                                        graph.create(r)
                        
                        except:
                            print('%s have no phone' % item['name'])
                        '''

                    department = Node('Department',var=teachers[0]['department'],id=id_node)
                    graph.create(department)
                    id_node += 1

                    for teacher in teachers:
                        r = Relationship(teacher,'in',department,id=-4)
                        graph.create(r)
    return id_node

def create_lab_nodes(id_start,json_path=r"../../data/词典/labs"):
    
    graph = Graph('bolt://localhost:7687',username='neo4j',password='123456')
    id_node = id_start
    id_relation = -1
    for dir_path,dir_name,file_list in os.walk(json_path):
        for filename in file_list:
            if os.path.splitext(filename)[1]=='.json':
                with open('/'.join([dir_path,filename]),'r',encoding='utf-8') as f:
                    for item in jsonlines.Reader(f):
                        lab = Node('Lab',var=item['lab'],url=item['url'],id=id_node)
                        graph.create(lab)

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