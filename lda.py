# LDA 모델링 패키지
import gensim
from gensim import corpora, models 

# 한국어 처리
from konlpy.tag import Twitter
twitter = Twitter()

import operator

documents = [
    "군사안보지원사령부 닻 올렸다…기무사 시대 마감(종합)",
    "(서울=연합뉴스) 김귀근 이상현 기자 = 국군기무사령부를 대체하는 군사안보지원사령부(이하 안보지원사)가 1일 창설식을 하고 공식 출범했다.",
    "기무사는 1991년 국군보안사령부에서 국군기무사령부로 간판을 바꿔 단지 27년 만에 역사의 뒤안길로 사라졌다.",
    "이날 오전 경기도 과천 옛 기무사 청사에서 송영무 국방부 장관 주관으로 새로운 군 정보부대인 안보지원사 창설식이 개최됐다."
    "송영무 장관은 창설식 훈시에서 기무사는 과거에 대한 반성 없이 정치개입, 민간인 사찰과 같은 불법행위로 군의 명예를 실추시켰으며 국민에게 배신감을 안겨줬다고 지적했다."
    "그러면서 6·25전쟁 당시 창설된 특무부대로부터 방첩부대, 보안사와 최근 기무사에 이르기까지 과거의 부대들은 격동의 현대사 속에서 군의 정치개입이라는 오명을 남겼으며 국민의 신뢰는커녕 지탄과 원망의 대상이었다고 비판했다.",    
    "(과천=연합뉴스) 권준우 기자 = 송영무 국방부장관이 1일 오전 경기도 과천시 국군기무사령부 청사에서 열린 군사안보지원사령부 창설식에서 축사를 하고 있다.",
    "군사안보지원사령부는 부대원의 정치적 중립과 정치활동에 관여하는 모든 행위 금지, 직무 범위를 벗어난 민간인에 대한 정보수집 및 수사 금지를 골자로 한 사령부령에 따라 기무사의 역할을 대신하게 된다. stop@yna.co.kr",
    "송 장관은 오늘을 계기로 과거를 통렬히 반성하고, 희망찬 미래를 향해 나아가야 한다면서 대통령님의 통수이념을 깊이 새겨 국민을 받들어 모시는 봉사의 정신으로 충성해야 하고 헌신해야 한다고 강조했다.",    
    "지난 6일부터 부대 창설준비단장을 해온 남영신(학군 23기) 전 특전사령관(중장)이 초대 사령관을 맡았다. 남 중장은 창설식에서 송 장관으로부터 새로 만든 부대기를 전달받고, 사령관으로서 임무에 들어갔다.",    
    "남영신 사령관은 창설식사를 통해 우리는 군 유일의 보안·방첩 전문기관으로 새롭게 도약하기 위해 그 출발선에 결연한 각오로 서 있다고 말했다.",    
    "그는 이어 국민의 눈높이와 시대적 상황 변화에 맞추어 신뢰받는 조직으로 변모해 나가기 위해서는 먼저, 기초와 기본을 바로 세워야 하겠다면서 새롭게 제정한 부대령과 운영 훈령에 입각하여 전 부대원이 업무 범위를 명확히 이해한 가운데 '해야 할 일'과 '해서는 안 될 일'을 구분해 수행해야 한다고 강조했다.",    
    "취임사 하는 남영신 초대 군사안보지원사령관",
    "취임사 하는 남영신 초대 군사안보지원사령관",
    "(과천=연합뉴스) 권준우 기자 = 1일 오전 경기도 과천시 국군기무사령부 청사에서 열린 군사안보지원사령부 창설식에서 남영신 초대사령관이 취임사를 하고 있다. ",
    "군사안보지원사령부는 부대원의 정치적 중립과 정치활동에 관여하는 모든 행위 금지, 직무 범위를 벗어난 민간인에 대한 정보수집 및 수사 금지를 골자로 한 사령부령에 따라 기무사의 역할을 대신하게 된다. stop@yna.co.kr",
    "그러면서 국민에게 신뢰받는 조직, 군과 군 관련 기관으로부터 전문성을 갖춘 꼭 필요한 조직으로 인정받을 수 있도록 다 함께 노력하자고 당부했다.",    
    "앞서 문재인 대통령이 기무사를 근본적으로 해편(解編)해 과거와 역사적으로 단절된 새로운 사령부를 창설하라고 지시함에 따라 그간 안보지원사(DSSC:Defense Security Support Command) 창설 작업이 진행돼왔다.",    
    "창설준비단은 지난달 21일 부대 창설계획을 문 대통령에게 보고하고 '군사안보지원사령부령'과 이에 따른 '국방부 훈령'을 수차례 토의와 법무 검토 끝에 제정했다.",    
    "이날부터 시행된 군사안보지원사령부령에는 부대원의 정치적 중립과 정치활동에 관여하는 모든 행위 금지, 직무 범위를 벗어난 민간인에 대한 정보수집 및 수사 금지 등의 내용이 담겼다. 방첩업무 및 방산업체를 대상으로 하는 외국·북한의 정보활동 대응 및 군사기밀 유출 방지 등 군 방첩업무 강화 내용도 들어있다.",    
    "국방부는 사령부령에는 정치적 중립과 민간인 사찰, 권한 오·남용 금지 등을 담은 직무 수행 기본원칙을 비롯해 이에 어긋나는 지시에 대해 이의제기 및 거부할 수 있는 근거 조항도 마련되어 있다고 강조했다.",    
    "부대기 넘겨받는 남영신 초대 군사안보지원사령관",
    "부대기 넘겨받는 남영신 초대 군사안보지원사령관",
    "(과천=연합뉴스) 권준우 기자 = 송영무 국방부장관(왼쪽)이 1일 오전 경기도 과천시 국군기무사령부 청사에서 열린 군사안보지원사령부 창설식에 참석, 남영신 초대사령관에게 부대기를 이양하고 있다. ",
    "군사안보지원사령부는 부대원의 정치적 중립과 정치활동에 관여하는 모든 행위 금지, 직무 범위를 벗어난 민간인에 대한 정보수집 및 수사 금지를 골자로 한 사령부령에 따라 기무사의 역할을 대신하게 된다. stop@yna.co.kr",
    "안보지원사 소속 인원은 2천900여명이다. 이는 4천200여명이던 기무사 인원을 30% 이상 감축하라는 국방부 기무사 개혁위원회의 권고에 따른 것이다.",    
    "이를 위해 안보지원사 창설준비단은 현역 간부 군인 위주로 750여명의 기무사 요원을 육·해·공군 원 소속부대로 돌려보냈다. 지난달 24일까지 원대복귀 조치된 인원 중에는 계엄령 문건 작성과 세월호 민간인 사찰, 댓글공작 등 이른바 '3대 불법행위'에 연루된 240여명도 포함됐다.",    
    "아울러 1천300여명인 기무사 소속 병사 중 580여명이 감축된다. 병사 감축은 원대복귀 조치가 아니라 전역하는 병사의 후임을 뽑지 않는 방식으로 이뤄진다.",    
    "참모장은 공군본부 기무부대장이었던 전제용(공사 36기) 준장이 발탁됐다. 감찰실장에는 2급 이상 군무원, 검사, 고위감사공무원 등을 임명할 수 있도록 했으며, 초대 감찰실장은 이용일 부장검사가 파견 형식으로 맡게 됐다.",
]
# 중복 토큰 필터
filterDocuments = []

for i in documents:

    # 문장 토큰화
    tokens = twitter.pos(i, norm=True, stem=True)
    
    # 명사만 추출하지 않고 진행시 거리가 먼 분류가 노출됨
    stem_tokens = [split[0] for split in tokens if split[1] == "Noun"]
       
    filterDocuments.append(stem_tokens)
        

# Dictionary 생성
dictinory = corpora.Dictionary(filterDocuments)

# 토큰으로 생성된 사전 중첩처리
corpus = [dictinory.doc2bow(text) for text in filterDocuments]

# LDA 모델 생성
analysisComplateList = []

for i in range(1, 50):
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = 6, id2word = dictinory, passes = 20)
    
    ldaResults = ldamodel.print_topics(num_topics = 3, num_words = 1)    

    for result in ldaResults:         
        analysisComplateList.append(tuple(result[1].split("*")))

    print(i, " job working..")

sortldaResults = sorted(analysisComplateList, key=operator.itemgetter(0), reverse=True)

results = set()

for result in sortldaResults:
    results.add(result[1])    
    if len(results) == 3: break

print(sortldaResults)
print(results)
