import json
import preprocess
from add_to_database import add_news
from cut_words import cut_words
from feature_matrix import construct_matrix
from process_entity.process_to_neo import getEntity_from_neo

def main():
    '''
     读需要进行处理读文件列表
    '''
    ini = 'utils/file_names.json'
    files = list()
    with open(ini, 'r') as fin:
        tmp = json.load(fin)
        files = tmp['files']
    
    tmp_files = list()
    file_path_list = list() #相对于大床路径的列表
    for file in files:
        file_path = file['path']
        file_path_list.append(file_path)
        # 先去读取配置文件
        config_file = dict()
        with open(file['config'],'r') as fin:
            config_file = json.load(fin)


        tmp_files.append((file_path, config_file["art_type"]))
        
        '''
        删除奇怪的字符 ' '  '\r'  '\n'
        将'nan'  'NULL'替换为空（这是默认情况）（如果你的数据还有什么特殊的字符需要处理，请加入到配置文件中）
        '''
        #preprocess.delete(file_path, config_file["special_characters"])
        #preprocess.modify_time(file_path,config_file['date_position'],config_file['date_format'] )
    
    for path in file_path_list:
        getEntity_from_neo(path)

    '''
    将新闻添加到数据库中
    '''
    
    #add_news(tmp_files)

    '''
    切词
    '''
    #cut_words(file_path_list)

    '''
    训练tfidf
    '''
    #construct_matrix()


if __name__ == "__main__":
    main()

    
