import requests

def get_access_token():
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
            print("===============================================")
            i=i+1

get_charts()

print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
try:
    chart_id = input("請貼上想聽的音樂排行榜ID: ")
    get_charts_tracks(chart_id)
except KeyError:
    print("請貼上正確的音樂排行榜ID")
