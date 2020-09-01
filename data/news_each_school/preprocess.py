import pandas as pd


def shancu(file_path):
    
    read_pandas = pd.read_csv(file_path)
    tmp_pandas = pd.DataFrame(columns=('datetime','source','url','title','content'))
    
    titles = dict()
       
    news_titles = []
    news_dates = []
    news_contents = []
    news_urls = []
    news_sources = []
    

    for i,item in enumerate(read_pandas['title']):
        
        if not titles.__contains__(str(item)):
            titles[str(item)] = 1
            title = read_pandas['title'][i]
            date = read_pandas['datetime'][i]
            content = read_pandas['content'][i]
            url = read_pandas['url'][i]
            source = read_pandas['source'][i]

            news_titles.append(title)
            news_dates.append(date)
            news_contents.append(content)
            news_urls.append(url)
            news_sources.append(source)
        else:
            pass
        print(i,end='\r')
    
    news_pd = pd.DataFrame(
        {'datetime': news_dates, 'source': news_sources, 'url': news_urls, 'title': news_titles, 'content': news_contents})
    

    news_pd.to_csv(file_path, index=False)

name_list = [
    "ai_output.csv",
"chem_output.csv",
"econ_output.csv",
"finance_output.csv",
"info_output.csv",
"international_output.csv",
"irm_output.csv",
"journal_output.csv",
"law_output.csv",
"math_output.csv",
"philosophe_output.csv",
"physical_output.csv",
"psy_output.csv",
"rmbs_output.csv",
"social_output.csv",
"tong_ji_output.csv",
"wenxue_output.csv"

]


for file_name in name_list:
    shancu(file_name)