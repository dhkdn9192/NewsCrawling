NewsCrawling Python code
======================
# 1. NewsCraling Project
## 1.1. 개요
특정 전자신문의 뉴스 페이지로부터 뉴스를 크롤링하는 파이썬 코드. 뉴스 웹 URL과 읽어올 페이지 수, 뉴스 게시일자 등을 파라미터로 입력하여 뉴스를 크롤링한다. 읽어온 뉴스 데이터는 텍스트이며 json 파일로 저장한다.

## 1.2. 소스코드 별 기능
### 1.2.1. NewsCrawlingNaeil.py
[내일신문](http://www.naeil.com/news_list/?cate=01003000)의 웹페이지로부터 뉴스를 크롤링한다. 입력 URL은 정치 섹션, 경제 섹션 등 특정 섹션에 접속하는 URL 주소이다.
읽어올 수 있는 섹션 종류는 다음과 같다.
    1. 정치 : [http://www.naeil.com/news_list/?cate=01002000](http://www.naeil.com/news_list/?cate=01002000)
    2. 경제 : [http://www.naeil.com/news_list/?cate=01003000](http://www.naeil.com/news_list/?cate=01003000)
    3. 세계 : [http://www.naeil.com/news_list/?cate=01004000](http://www.naeil.com/news_list/?cate=01004000)
    4. 사회 : [http://www.naeil.com/news_list/?cate=01003000](http://www.naeil.com/news_list/?cate=01003000)

### 1.2.2. NewsCrawlingDigitaltimes.py
[디지털타임스](http://www.dt.co.kr/article_list.html?gcd=1&scd=100&lcd=2401)의 웹페이지로부터 뉴스를 크롤링한다. 입력 URL은 정치 섹션, 경제 섹션 등 특정 섹션에 접속하는 URL 주소이다.
읽어올 수 있는 섹션 종류는 다음과 같다.
    1. 정치 : [http://www.dt.co.kr/article_list.html?gcd=1&scd=100&lcd=2401](http://www.dt.co.kr/article_list.html?gcd=1&scd=100&lcd=2401)
    2. 정보통신컨텐츠 : [http://www.dt.co.kr/article_list.html?gcd=1&scd=100&lcd=2001](http://www.dt.co.kr/article_list.html?gcd=1&scd=100&lcd=2001)
    3. 산업 : [http://www.dt.co.kr/article_list.html?gcd=1&scd=100&lcd=2201](http://www.dt.co.kr/article_list.html?gcd=1&scd=100&lcd=2201)
    4. IT중기 : [http://www.dt.co.kr/article_list.html?gcd=1&scd=100&lcd=2101](http://www.dt.co.kr/article_list.html?gcd=1&scd=100&lcd=2101)
    5. 과학유통건설 : [http://www.dt.co.kr/article_list.html?gcd=1&scd=100&lcd=2801](http://www.dt.co.kr/article_list.html?gcd=1&scd=100&lcd=2801)
    6. 경제금융증권 : [http://www.dt.co.kr/article_list.html?gcd=1&scd=100&lcd=3101](http://www.dt.co.kr/article_list.html?gcd=1&scd=100&lcd=3101)
    7. 문화연예 : [http://www.dt.co.kr/article_list.html?gcd=1&scd=100&lcd=2501](http://www.dt.co.kr/article_list.html?gcd=1&scd=100&lcd=2501)
    8. 오피니언 : [http://www.dt.co.kr/article_list.html?gcd=1&scd=100&lcd=0201](http://www.dt.co.kr/article_list.html?gcd=1&scd=100&lcd=0201)

