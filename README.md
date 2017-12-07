NewsCrawling Python code
======================
# 1. NewsCraling Project
## 1.1. 개요
특정 전자신문의 뉴스 페이지로부터 뉴스를 크롤링하는 파이썬 코드. 뉴스 웹 URL과 읽어올 페이지 수, 뉴스 게시일자 등을 파라미터로 입력하여 뉴스를 크롤링한다. 읽어온 뉴스 데이터는 텍스트이며 json 파일로 저장한다.

## 1.2. 소스코드 별 기능
### 1.2.1. NewsCrawlingNaeil.py
[내일신문](http://www.naeil.com/news_list/?cate=01003000)의 웹페이지로부터 뉴스를 크롤링한다. 입력 URL은 정치 섹션, 경제 섹션 등 특정 섹션에 접속하는 URL 주소이다.

#### 내일신문으로부터 읽어올 수 있는 섹션 종류(NewsSection URL)
    1. 정치 (http://www.naeil.com/news_list/?cate=01002000)
    2. 경제 (http://www.naeil.com/news_list/?cate=01003000)
    3. 세계 (http://www.naeil.com/news_list/?cate=01004000)
    4. 사회 (http://www.naeil.com/news_list/?cate=01003000)

### 1.2.2. NewsCrawlingDigitaltimes.py
[디지털타임스](http://www.dt.co.kr/article_list.html?gcd=1&scd=100&lcd=2401)의 웹페이지로부터 뉴스를 크롤링한다. 입력 URL은 정치 섹션, 경제 섹션 등 특정 섹션에 접속하는 URL 주소이다.

#### 디지털타임스로부터 읽어올 수 있는 섹션 종류(NewsSection URL)
    1. 정치 (http://www.dt.co.kr/article_list.html?gcd=1&scd=100&lcd=2401)
    2. 정보통신컨텐츠 (http://www.dt.co.kr/article_list.html?gcd=1&scd=100&lcd=2001)
    3. 산업 (http://www.dt.co.kr/article_list.html?gcd=1&scd=100&lcd=2201)
    4. IT중기 (http://www.dt.co.kr/article_list.html?gcd=1&scd=100&lcd=2101)
    5. 과학유통건설 (http://www.dt.co.kr/article_list.html?gcd=1&scd=100&lcd=2801)
    6. 경제금융증권 (http://www.dt.co.kr/article_list.html?gcd=1&scd=100&lcd=3101)
    7. 문화연예 (http://www.dt.co.kr/article_list.html?gcd=1&scd=100&lcd=2501)
    8. 오피니언 (http://www.dt.co.kr/article_list.html?gcd=1&scd=100&lcd=0201)

## 1.3. 실행함수 파라미터 명세
    크롤링 실행함수(getNewsNaeil, getNewsDigitaltimes)는 공통적으로 아래의 입력 파라미터를 받는다
    url         : 대상 뉴스 웹 URL. 섹션 메뉴 클릭 시 접속하게 되는 뉴스 리스트 URL을 의미
    filename    : 결과를 저장할 json 파일명
    date        : 크롤링할 뉴스의 일자(예시 '2017-12-05') (default: 금일 날짜)
    maxpage     : 읽어올 총 페이지 수. 1페이지부터 읽어옴 (default: 10)
    isTestmode  : 실행 결과를 표준출력으로 보고자 할 때 True로 입력. (default: False)

## 1.4. 결과파일(json) 명세
    결과 파일은 json 포맷으로 저장되며 아래의 필드들을 갖는다
    digitaltimes.json 형태의 이름으로 저장된다
    url         : 해당 뉴스 기사의 url주소
    date        : 뉴스가 게재된 날짜
    title       : 뉴스 타이틀
    reporter    : 뉴스 게시자(기자)
    body        : 뉴스 본문

## 1.5. 개발환경
    파이썬 버전 : Python3.6.3
    필요 패키지 : beautifulsoup4(4.6.0), lxml(4.1.1), urllib3(1.22), requests(2.18.4)
     * 설치 방법(윈도우,리눅스 공통) : pip install {패키지명}

