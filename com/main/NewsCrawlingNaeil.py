
"""
2017/12/05 Tue
0.개발환경
  - 파이썬 버전 : Python3.6.3
  - 필요 패키지 : beautifulsoup4(4.6.0), lxml(4.1.1), urllib3(1.22), requests(2.18.4)
    * 설치 방법(윈도우,리눅스 공통) : pip install {패키지명}

1.내일신문에 대한 뉴스 크롤링 코드
  - 내일신문의 특정 섹션 페이지(정치,경제,etc)의 URL을 입력하면 뉴스 리스트의 기사들을 읽고 지정한 날짜(default:오늘날짜)인 것만 크롤링한다
  - 결과는 json 파일로 저장한다
  - 크롤링 실행방법 : 코드 하단의 getNewsNaeil 함수에 원하는 파라미터를 입력하여 실행한다

2.뉴스크롤링 결과 json 파일
  - naeil.json 형태의 이름으로 저장된다
  - url         : 해당 뉴스 기사의 url주소
  - date        : 뉴스가 게재된 날짜
  - title       : 뉴스 타이틀
  - reporter    : 뉴스 게시자(기자)
  - body        : 뉴스 본문
"""

import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import datetime
import json
# import os


# definition
NOT_FOUND = "NOT_FOUND"


# 주어진 url로부터 html응답 코드를 받아와 BeautifulSoup 타입으로 반환하는 함수
def getBeautifulSoup(url):
    response = requests.get(url)                    # 입력된 url로 request 요청 및 html 코드 수신
    plainText = response.text                       # html 소스코드를 텍스트로 변환
    soup = BeautifulSoup(plainText, "lxml")         # BeautifulSoup 객체로 보기 쉽게 변환하여 반환
    return soup


# 태그 트리 중에서 특정 태그(br 태그 등)들을 제거하는 함수
def removeTag(soup: BeautifulSoup, tag):
    for sp in soup.findAll(tag):
        sp.extract()                                # parent 태그로부터 현재 자식 태그들을 제거한다.


# 기사의 유료/무료 여부를 반환하는 함수
def isCharged(tags):
    chargeTags = tags.select(".pay")                # 태그 중 class가 pay인 것을 추출
    tagLen = len(chargeTags)                        # 추출된 태그 수 계산
    if tagLen > 0:                                  # pay 태그가 존재하면 유료기사로 판단
        return 1    # Charged
    else:
        return 0    # for Free


# 입력받은 태그들에서 href(대상 하이퍼링크) 경로를 추출하는 함수
def getHrefFromTag(tags, urlprefix):
    targetTag = tags.find('a', href=True)           # 태그 이름이 a인 것을 하나 추출
    return urlprefix + targetTag['href']            # 태그 내의 href 필드 값을 urlprefix와 합쳐 반환


# href가 가리키는 뉴스기사 페이지로부터 뉴스 타이틀 추출하는 함수
def getTitleFromHref(soup: BeautifulSoup):
    articleTag = soup.select(".articleArea")[0]     # 뉴스기사 항목에 해당하는 태그 트리 추출
    h3Tag = articleTag.select("h3")                 # h3 태그를 추출(타이틀 태그)
    if len(h3Tag) > 0:
        titleList = h3Tag[0].contents               # 타이틀 문자열 추출(list)
        if len(titleList) > 0:
            return str(titleList[0])                # 문자열 형태로 반환(elem)
    return NOT_FOUND


# href가 가리키는 뉴스기사 페이지로부터 뉴스 본문을 추출하는 함수
def getBodyFromHref(soup: BeautifulSoup):
    articleTag = soup.select(".article")[0]                     # 뉴스기사 본문에 해당하는 태그 트리 추출
    removeTag(articleTag, 'br')                                 # step1으로부터 불필요한 br 태그들 제거
    textList = articleTag.findAll(text=True, recursive=True)    # 태그들로부터 텍스트 내용만 재귀적으로 추출한 리스트
    fullText = ''.join(textList)                                # list to string
    return fullText


# href가 가리키는 뉴스기사 페이지로부터 뉴스 일자를 추출하는 함수
def getTimeFromHref(soup: BeautifulSoup):
    articleTag = soup.select(".articleArea")[0]                 # 기사 본문 영역 태그 추출
    dateTag = articleTag.select(".date")[0]                     # 본문 중 게재 일자 태그 추출
    dateContents = dateTag.contents                             # 내용 추출 (2017-12-05 11:35:22 게재)
    if len(dateContents) > 0:
        date = str(dateContents[0]).split(' ')[0]               # 날짜 부분만 문자열로 반환 (2017-12-05)
        return date
    return NOT_FOUND


# href가 가리키는 뉴스기사 페이지로부터 뉴스 게시자를 추출하는 함수
def getReporterFromHref(soup: BeautifulSoup):
    reporterTag = soup.select(".byLine")[0]                     # class가 byLine인 태그 추출
    reporterTagList = reporterTag.contents                      # 태그의 내용 추출(list)
    if len(reporterTagList) > 0:                                # 태그 리스트의 원소가 존재할 경우에만 내용 추출
        reporterList = reporterTag.findAll(text=True, recursive=True)   # 텍스트 추출(list)
        reporter = ''.join(reporterList)                                # list to string
        return reporter
    return NOT_FOUND


# 지정된 json 파일명으로 데이터 저장하는 함수
def appendDataToJsonFile(data, filename):
    with open('data/'+filename, 'a', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)
        f.write('\n')       # 각 json 데이터 사이 띄워서 저장하기
        f.close()


"""
[핵심 함수] 내일신문의 특정 섹션에서 뉴스를 크롤링하여 json으로 저장하는 함수
  - url         : 대상 뉴스 웹 URL. 섹션 메뉴 클릭 시 접속하게 되는 뉴스 리스트 URL을 의미
  - filename    : 결과를 저장할 json 파일명
  - date        : 크롤링할 뉴스의 일자(예시 '2017-12-05') (default: 금일 날짜)
  - maxpage     : 읽어올 총 페이지 수. 1페이지부터 읽어옴 (default: 10)
  - isTestmode  : 실행 결과를 표준출력으로 보고자 할 때 True로 입력. (default: False)
"""
def getNewsNaeil(url, filename, date="", maxpage=10, isTestmode=False):

    # 뉴스 일짜 미입력 시 오늘 날짜로 설정 (예시 '2017-12-05')
    if date == "":
        date = '{0:%Y-%m-%d}'.format(datetime.datetime.now())

    # url로부터 path 이하를 제외한 온전한 url 주소를 추출
    urlObject = urlparse(url)
    urlPrefix = urlObject.scheme + '://' + urlObject.netloc

    page = 1    # 페이지 인덱스 초기화

    # 주어진 페이지 수만큼 반복
    while page <= maxpage:

        current_url = url + '&tpage=' + str(page)       # 현재 페이지의 url 생성
        soup = getBeautifulSoup(current_url)            # 현재 페이지의 html을 추출

        # 뉴스 리스트인 태그들에 대해서 반복문 수행(class가 newsList08인것들 추출)
        for tags in soup.select(".newsList08"):

            # 기사가 무료기사일 경우에만 추출 실행
            if isCharged(tags) == 0:
                data = {}                                   # 파일 덤프를 위한 buffer
                href = getHrefFromTag(tags, urlPrefix)      # 각 기사의 href(대상 하이퍼링크 주소) 추출
                hrefSoup = getBeautifulSoup(href)           # 추출한 href에 대해 다시 html정보 추출
                newsDate = getTimeFromHref(hrefSoup)        # 추출한 href에 대해 뉴스 일자를 추출 (YYYY-MM-dd)

                # 대상 날짜의 뉴스보다 최신 뉴스일 경우
                # if newsDate > date:
                #     print("[INFO] news date is ealier than target date (page:", page, ")")

                # 대상 날짜의 뉴스가 더이상 없을 경우 종료
                if newsDate < date:
                    # print("\n[FINISHED] No more news! (page:", page, ")\n")
                    return

                # 대상 날짜와 읽어온 뉴스 게시일 동일할 경우에만 이하를 수행(newsDate == date)
                elif newsDate == date:
                    # json 파일 dump를 위한 key-value 쌍 입력
                    data['url'] = href
                    data['date'] = newsDate
                    data['title'] = getTitleFromHref(hrefSoup)          # 추출한 href에 대해 뉴스 타이틀 추출
                    data['reporter'] = getReporterFromHref(hrefSoup)    # 추출한 href에 대해 뉴스 게시자를 추출
                    data['body'] = getBodyFromHref(hrefSoup)            # 추출한 href에 대해 뉴스 본문을 추출

                    if isTestmode:
                        print("=========================================================================")
                        print(">> URL      : ", data['url'])
                        print(">> date     : ", data['date'])
                        print(">> title    : ", data['title'])
                        print(">> reporter : ", data['reporter'])
                        print(">> body \n", data['body'])

                    # 크롤링 결과를 json 파일에 저장하기(append)
                    appendDataToJsonFile(data, filename)

        # 다음 페이지 읽기
        page += 1


# --------------------------------------------------------------------------------------
# ------------------------------------- Main Field -------------------------------------
# --------------------------------------------------------------------------------------

# (1) 위에서 정의한 함수를 호출하여 내일신문에 대한 뉴스 크롤링을 실행한다.

targetUrl = 'http://www.naeil.com/news_list/?cate=01003000' # 경제
# targetUrl = 'http://www.naeil.com/news_list/?cate=01004000' # 세계
# targetUrl = 'http://www.naeil.com/news_list/?cate=01003000' # 사회
# targetUrl = 'http://www.naeil.com/news_list/?cate=01002000' # 정치



# 뉴스 크롤링 실행
getNewsNaeil(url=targetUrl,             # param 1) 내일신문 섹션 별 url. 읽어올 섹션만 주석을 해제한다.
             filename='naeil.json',     # param 2) 뉴스 크롤링 결과를 저장할 파일명. json 포맷으로 저장한다.
             date="2017-12-06",         # param 3) 크롤링할 뉴스 날짜. (default: 금일 날짜)
             #maxpage=10,               # param 4) 읽어올 뉴스 페이지 수. (default: 10)
             isTestmode=True)           # param 5) 결과를 표준출력을 보려면 True (default: False)




# (2) Main Field에서 실행한 결과 파일을 읽어 표준출력하여 확인한다.

# # 저장된 json 파일 열어서 json 리스트로 읽기
# with open(targetFileName, encoding='utf-8') as fp:
#     loadedList = [json.loads(line) for line in fp]      # json 데이터들의 리스트
#
# # 읽은 json 리스트 출력하기
# for line in loadedList:
#     print(line)
#
# print(" * json 리스트 중 0번째 라인, 'url' 필드값 읽기 -> ", loadedList[0]['url'])
