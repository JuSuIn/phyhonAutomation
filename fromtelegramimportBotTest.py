import asyncio
from telegram import Bot

async def main():
    # 텔레그램 봇 토큰
    bot_token = '7038615438:AAFgcCFKpO7FlOlLLOcXO8ETPlNcOt7yg80'

    # 봇 인스턴스 생성
    bot = Bot(token=bot_token)

    # 채팅 ID와 메시지 정의
    chat_id = '5772781230'
    message = 'check!!!!!!!!!!!! '
   #  message = 'Hello, this is a test message from my Telegram bot!'

    # 메시지 전송 (비동기 함수 호출)
    await bot.send_message(chat_id=chat_id, text=message)

# 이벤트 루프 실행
if __name__ == '__main__':
    asyncio.run(main())