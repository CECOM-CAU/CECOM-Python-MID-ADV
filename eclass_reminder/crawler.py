from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re




# 12h str > 24h datetime객체로 변환
def convert_to_24h(ddline_str):
    
    ampm, time  = ddline_str.split()
    time_str = (time + 'AM') if ampm == "오전" else (time + 'PM')

    return datetime.strptime(time_str, '%I:%M%p')



# 마감일 datetime 객체 생성
def get_whole_datetime(next_day, time_24h):
    
    year = next_day.year
    month = next_day.month
    day = next_day.day
    hour = time_24h.hour
    minute = time_24h.minute
    
    return datetime(year, month, day, hour, minute)



# 하루 일정 가져오기
def get_event_info(span_date, next_day):

    event_list = []
    div_agday = span_date.find_parent('div')
    div_agevents = div_agday.find_next_sibling('div')
    li_event = div_agevents.find_all('li')
    
    for event in li_event:
        course_title = event.find(string=re.compile('캘린더'))
        course_title = course_title.replace('캘린더', '').strip()
        event_title = event.find('span',class_='agenda-event__title')
        event_title = event_title.string.strip()
        ddline_str = event.find('div',class_='agenda-event__time')
        ddline_str = ddline_str.string.replace("마감", "").strip()
        ddline = get_whole_datetime(next_day, convert_to_24h(ddline_str))
        
        event_list.append({'course_title': course_title, 
                           'event_title': event_title, 
                           'ddline': ddline})
    return(event_list)



# 오늘날짜로부터 +3일(총 4일_임시)까지의 일정 가져오기.
def get_4d_schedule(page_source):

		schedule = []
		today = datetime.today()
		calendar_html = page_source
		soup = BeautifulSoup(calendar_html, 'html.parser')
		date_tags = soup.select('h3.agenda-date span:nth-child(1)')[:4]
		
		for i in range(4):
				next_day = today + timedelta(days=i)
				date_string = f"{next_day.month}월 {next_day.day}일"
				
				for tag in date_tags:
						if date_string in tag.string:
								schedule.append(get_event_info(tag, next_day))
								break
                
		return(schedule)
