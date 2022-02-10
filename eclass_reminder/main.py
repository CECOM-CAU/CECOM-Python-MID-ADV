from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
from crawler import get_4d_schedule
import requests


# r 뒤에 크롬드라이버 경로 입력
driver = webdriver.Chrome(r'C:/Users/USER/Desktop/cecom/chromedriver_win32/chromedriver.exe')

driver.implicitly_wait(3)

# 중앙대학교 포탈 로그인 -> 로그인 버튼 누르고 대시보드 전의 링크 복사 후 아래에 붙여넣기
driver.get('https://eclass3.cau.ac.kr//learningx/login?result=')

# 캘린더 > '일정' 버튼 클릭
calendar_btn = driver.find_element(By.ID, 'global_nav_calendar_link')
calendar_btn.click()

driver.implicitly_wait(2)

agenda_btn = driver.find_element(By.ID, 'agenda')
agenda_btn.click()

#슬랙봇으로 메시지 보내기(slack_sdk는 현재 사용할 수 없어 함수 이용)
def post_message(token, channel, text):
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )
    print(response)

'''
1. 슬랙봇 생성(https://dsbook.tistory.com/290 등 참고)
2. 만든 앱 이용할 채널에 추가(채널 진입 -> 오른쪽 위 클릭 -> 통합 -> 앱 -> 앱 추가)
'''
 
#슬랙봇 토큰 정보 입력
myToken = "xoxb-****"

# 크롤링 정보(오늘~향후 3일 스케줄) 받아와서 챗봇 메세지 생성
def main():
	
		schedule = get_4d_schedule(driver.page_source)
		driver.quit()
		today = datetime.today()
		
		for event_list in schedule: 
        #챗봇 메세지1_브리핑 용
				month, day = event_list[0]['ddline'].month, event_list[0]['ddline'].day
				mssg_brief = f"{month}월 {day}일까지 마감인 과제: {len(event_list)}개"
				# 메세지 출력
				post_message(myToken, "#채널명", mssg_brief)
				
				for event in event_list:
						time_left = event['ddline'] - today
						days_left = time_left.days
						hours_left = time_left.seconds // 3600
            #챗봇 메세지2_마감시간 알림 용
						mssg_detail = f"{event['course_title']}: {event['event_title']}의 마감까지 {days_left}일 {hours_left}시간 남음."
						# 메세지 출력
						post_message(myToken, "#채널명", mssg_detail)
