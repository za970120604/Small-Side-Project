def get_access_token():
    import requests
    #API網址    
    url = "https://account.kkbox.com/oauth2/token" 
    #標頭
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "account.kkbox.com"
    }
    #參數
    data = {
        "grant_type": "client_credentials",
        "client_id": "86e924b75db3ee54c66e947419299540",
        "client_secret": "811f4a337bd1ff2678d4acb3334f382a"
    }
    access_token = requests.post(url, headers=headers, data=data)
    return access_token.json()["access_token"]
def get_charts():
    import requests
    #取得存取憑證
    access_token = get_access_token() 
    #取得音樂排行榜列表API網址
    url = "https://api.kkbox.com/v1.1/charts"
    #標頭
    headers = {
        "accept": "application/json",
        "authorization": "Bearer " + access_token  #帶著存取憑證
    }
    #參數
    params = {
        "territory": "TW"  #台灣領域  
    }
    response = requests.get(url, headers=headers, params=params)
    result = response.json()["data"]
    
    for item in result:
        if item["title"]=="綜合新歌即時榜" or item["title"]=="華語新歌日榜" or item["title"]=="西洋新歌日榜" or item["title"]=="韓語新歌日榜" or item["title"]=="日語新歌日榜" or item["title"]=="台語新歌日榜":
            print(item["title"])
def get_charts_tracks(chart_title):
    import requests
    #取得存取憑證
    access_token = get_access_token() 
    #取得音樂排行榜列表API網址
    url = "https://api.kkbox.com/v1.1/charts"
    #標頭
    headers = {
        "accept": "application/json",
        "authorization": "Bearer " + access_token  #帶著存取憑證
    }
    #參數
    params = {
        "territory": "TW"  #台灣領域  
    }
    response1 = requests.get(url, headers=headers, params=params)
    result1 = response1.json()["data"]
    chart_id=""
    for item in result1:
        if item["title"]==chart_title:
            chart_id=item["id"]
            break
    #取得音樂排行榜列表中的歌曲API網址
    url = "https://api.kkbox.com/v1.1/charts/" + chart_id + "/tracks"
    #標頭
    headers = {
        "accept": "application/json",
        "authorization": "Bearer " + access_token
    }
    #參數
    params = {
        "territory": "TW"  #台灣領域
    }
    response = requests.get(url, headers=headers, params=params)
    result = response.json()["data"]
    i=1
    for item in result:
        if i<= 10:
            print("TOP",i,":")
            print("歌曲:",item["name"])
            print("演唱歌手:",item["album"]["artist"]["name"])
            print("==================================================================================================")
            i=i+1
    print("\n")
######################################################################################################################################################
def print_search_result_on_YT():
    from googleapiclient.discovery import build
    api_key="AIzaSyABbL_w6i7lcFcD1mQ9azub_CPD57WhnpQ"
    youtube=build('youtube','v3',developerKey=api_key)

    print("\n")
    print("請使用搜尋引擎:")
    while(1):
        query1=input("請繼續搜尋您有興趣的新歌:")
        if len(query1)==0:
            print("歌曲為必須輸入的條件!!")
            continue
        else:
            break
    while(1):
        query2=input("請輸入這首新歌的歌手或樂團:")
        if len(query2)==0:
            print("演出者為必須輸入的條件!!")
            continue
        else:
            break
    query=query1+" "+query2
    query_1=query+" official"
    request=youtube.search().list(part='snippet',order="relevance", q=query_1,maxResults=5,type='video')
    response=request.execute()
    print("您的搜尋字:",query)
    print("\n")
    print("此歌曲的官方版本搜尋結果如下(按下ctrl+c並點擊網址可察看影片):")
    i=1

    if len(response["items"])!=0:
        for item in (response["items"]):
            print(str(i)+".",end=" ")
            print(item['snippet']['title'])
            print("影片網址: "+"https://www.youtube.com/watch?v="+item['id']['videoId'])
            i=i+1
        print_live(query2)
        return query2
    else:
        print("沒有搜尋結果,請調整搜尋字!!")
        return "none"
def print_live(singer):
    from googleapiclient.discovery import build
    api_key="AIzaSyABbL_w6i7lcFcD1mQ9azub_CPD57WhnpQ"
    youtube=build('youtube','v3',developerKey=api_key)
    request=youtube.search().list(part='snippet',order="relevance", q=singer+" live",maxResults=5,type='video')
    response=request.execute()
    print("\n")
    print("此歌手(團體)現場表現如下(按下ctrl+c並點擊網址可察看網址):")
    i=1

    if len(response["items"])!=0:
        for item in (response["items"]):
            print(str(i)+".",end=" ")
            print(item['snippet']['title'])
            print("影片網址: "+"https://www.youtube.com/watch?v="+item['id']['videoId'])
            i=i+1
    else:
        print("沒有搜尋結果,請調整搜尋字!!")
#########################################################################################################################################################
def ticket_info(query_name):
    while(1):
        print("\n")
        c1=commands()
        if c1=='Y':
            from bs4 import BeautifulSoup
            import requests
            import re
            import json 
            print("\n")
            print("相關購票資訊:")
            if query_name!="none":
                while(1):
                    url="https://www.stubhub.tw/search/index?q="+query_name
                    response=requests.get(url)
                    soup = BeautifulSoup(response.text, "html.parser")
                    page_to_scrape=[]
                    try:
                        page_to_scrape=re.findall("<a href=\"https:\/\/www\.stubhub\.tw\/.*\/ca.*\n.*<span class=\"tit-evento\">",soup.prettify())[0].split("\n")
                        names=re.findall("<a href=\"https:\/\/www\.stubhub\.tw\/.*\/ca.*\n.*<span class=\"tit-evento\">.*\n(.*)",soup.prettify())
                    except IndexError:
                        print("抱歉,沒有這位歌手或這個團體!!")
                        print("===================the end=============================")
                        print("請繼續您的探索:")
                        print("\n")
                        break

                    i=1
                    for name in names:
                        print("您的第",i,"順位stubhub 搜尋結果:",name.replace("    ",""))
                        i=i+1
                    print("根據第一個搜尋字所得到的購票資訊如下:")
                    print("\n")
                    url1=page_to_scrape[0].replace("<a href=\"","")
                    url1=url1.replace("\">","")
                    response1=requests.get(url1)
                    soup1 = BeautifulSoup(response1.text, "html.parser")
                    res=re.findall("<script type=\"application\/ld\+json\">(.*?)<\/script>",str(soup1),flags=re.DOTALL)
                    if len(res) !=0:
                        print("此位歌手或此團體的近期演唱會活動如下(按下ctrl+c並點擊網址可引導至購票網站):")
                        i=1
                        for item in res:
                            item=item.replace("\n","")
                            item1=json.loads(item)
                            print(str(i)+".",end="")
                            print("活動名稱:",item1["name"])
                            try:
                                print("舉辦地點:",item1["location"]["address"]["addressCountry"],item1["location"]["address"]["addressLocality"],"---",item1["location"]["name"])
                            except KeyError:
                                print("The place to hold the concert has not been chosen!!")
                            try:
                                print("日期:",item1["startDate"])
                            except KeyError:
                                print("The concert's date has not been chosen!!")
                            try:
                                print("價格: 自",item1["offers"]['price'],end=" ")
                                print(item1["offers"]["priceCurrency"],"起")
                            except KeyError:
                                print("The ticket's price has not been decided!!")
                            print("購票網址:",item1["url"])
                            print("========================================================================")
                            i=i+1
                        print("不是您所預想的歌手或團體嗎?請試試看他種搜尋關鍵字!!")
                        print("===================the end=============================")
                        print("請繼續您的探索:")
                        print("\n")
                        break        
                    else:
                        print("很抱歉,這位歌手或此團體並無近期活動!!(或是嘗試輸入更精確地演唱歌手或團體!!)")
                        print("===================the end=============================")
                        print("請繼續您的探索:")
                        print("\n")
                        break   
            else:
                print("沒有購票資訊!!")
            break
        elif c1=='B':
            break
        else:
            print('請輸入正確的指令!!')
            continue
                
            
########################################################################################################################################################
def commands():
    command=input("是否要進一步探索?如果要的話請按下\'Y\';如果要回到排行榜資訊顯示處請按下\'B\':")
    return command
############################################################################################################################################################
def chart_id_get():
    chart_id = input("請貼上想聽的音樂排行榜: ")
    return chart_id
##########################################################################################################################################################
while(1):
    while(1):
        try:
            get_charts()
            get_charts_tracks(chart_id_get())
            break
        except KeyError:
            print("請貼上正確的音樂排行榜名字!!")
            continue
    while(1):
        c=commands()
        if c=='Y':
            ticket_info(print_search_result_on_YT())
            break
        elif c=='B':
            break
        else:
            print('請輸入正確的指令!!')




