from selenium import webdriver

# r 뒤에 크롬드라이버 경로 입력
driver = webdriver.Chrome(r'C:\Python\Chromedriver\chromedriver.exe')

driver.implicitly_wait(3)

# 중앙대학교 포탈 로그인 -> 로그인 버튼 누르고 대시보드 전의 링크 복사 후 아래에 붙여넣기
driver.get('https://eclass3.cau.ac.kr//learningx/login?result=')

driver.quit()