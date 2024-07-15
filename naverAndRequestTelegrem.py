import asyncio
import requests
from bs4 import BeautifulSoup as bs
from telegram import Bot
import schedule
import time
import tracemalloc



# 2. 새로운 네이버 뉴스 기사 링크를 받아온다.
def get_new_links(query, old_links=[]):
    # 네이버-> 키워드검색-> 뉴스 텝-> 최신순
     url =f'https://search.naver.com/search.naver?where=news&query={query}&sm=tab_opt&sort=1&photo=0&field=0&pd=0&ds=&de=&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Add%2Cp%3Aall&is_sug_officeid=0'
     
     # html 문서 받아서 parsing
     response=requests.get(url)
     soup = bs(response.text,'html.parser')
     title_tag=soup.title
     #print(f"test 확인 :: {title_tag.string}")

     #해당 페이지의 뉴스 기사 링크가 포함된 html 요소 추출
     news_titles = soup.select('a.news_tit')

     #요소에서 링크만 추출해서 리스트로 저장
     list_links = [i.attrs['href'] for i in news_titles]

     #기존의 링크와 신규 링크를 비교해서 새로운 링크만 저장 
     new_links = [link for link in list_links if link not in old_links]

     return new_links


# 새로운 네이버 뉴스 기사가 있을 때 텔레그램으로 전송하는 함수
async def send_telegram_links(query):
     #토큰을 변수에 저장 
     bot_token = '7038615438:AAFgcCFKpO7FlOlLLOcXO8ETPlNcOt7yg80' #내가 발급한 토큰
     bot = Bot(token=bot_token)

     # 함수 내 처리된 리스트를 함수 외부에서 참조
     global old_links

     #위에서 정의한 함수 실행
     new_links = get_new_links(query,old_links)
     
     #새로운 매세지가 있으면 링크 전송 
     if new_links:
          await bot.sendMessage(chat_id=chat_id, text='방금 업데이트 된 ' + f"{query} 주제의 크롤링입니다.")
          for link in new_links:
               await bot.sendMessage(chat_id=chat_id,text=link)
     else:
          pass
     # 기존의 링크를 계속 축척
     old_links += new_links.copy()


#실제 프로그램 구동 
if __name__ == '__main__':

     #토큰을 변수에 저장 
     bot_token = '7038615438:AAFgcCFKpO7FlOlLLOcXO8ETPlNcOt7yg80' #내가 발급한 토큰
     bot = Bot(token=bot_token)

     # 가장 최근에 온 메세지의 정보 중, chat id만 가져옴 (이 chat id는 사용자(나)의 계정 id임)
     #chat_id = bot.getUpdates()[-1].message.chat.id
     chat_id = '5772781230'

     # 4.검색 키워드 설정 
     queries = ["에이직랜드","두산에너빌리티","삼성전자"]
     #queries = ["에이직랜드","두산에너빌리티","한중앤시에스"]

     async def job():
          for query in queries:
               await send_telegram_links(query)

     for query in queries:
          #위에서 얻은 chat id로 bot이 메세지를 보냄
          asyncio.run(bot.send_message(chat_id=chat_id, text=f"{query}를 주제로 뉴스 기사 크롤링이 시작되었습니다.22"))
          #5.기존에 보냈던 링크를 담아둘 리스트 만들기
          old_links = []
          # 주기적 실행과 관련된 코드(hours는 시,minutes는 분, seconds는 초)
          # 스케줄 설정 (10초마다 실행)\
          schedule.every(10).seconds.do(lambda q=query : asyncio.run(send_telegram_links(q)))
          
     while True:
          schedule.run_pending()
          time.sleep(1)
       



