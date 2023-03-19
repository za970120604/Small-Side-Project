from googleapiclient.discovery import build
def print_search_result_on_YT():
    api_key="AIzaSyABbL_w6i7lcFcD1mQ9azub_CPD57WhnpQ"
    youtube=build('youtube','v3',developerKey=api_key)


    query1=input("請繼續搜尋您有興趣的新歌:")
    query2=input("請輸入這首新歌的歌手或樂團:")
    query=query1+" "+query2
    query_1=query+" official"
    request=youtube.search().list(part='snippet',order="relevance", q=query_1,maxResults=5,type='video')
    response=request.execute()

    print("\n")

    print("您的搜尋字:",query)
    print("\n")
    print("搜尋結果如下:")
    i=1
    for item in (response["items"]):
        print(str(i)+".",end=" ")
        print(item['snippet']['title'])
        print("影片網址: "+"https://www.youtube.com/watch?v="+item['id']['videoId'])
        i=i+1

    print_live(query2)

    return query2

def print_live(singer):
    api_key="AIzaSyABbL_w6i7lcFcD1mQ9azub_CPD57WhnpQ"
    youtube=build('youtube','v3',developerKey=api_key)

    request=youtube.search().list(part='snippet',order="relevance", q=singer+" live",maxResults=5,type='video')
    response=request.execute()

    print("\n")
    print("此歌手(團體)現場表現如下:")

    i=1
    for item in (response["items"]):
        print(str(i)+".",end=" ")
        print(item['snippet']['title'])
        print("影片網址: "+"https://www.youtube.com/watch?v="+item['id']['videoId'])
        i=i+1



print_search_result_on_YT()
