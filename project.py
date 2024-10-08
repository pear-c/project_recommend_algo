# -*- coding: utf-8 -*-
"""소실 테스트

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1sNyhMtNgp2ZoKhwE6GOasQT6MeIehxgo
"""

!pip install JPype1==0.7.0
!apt-get install -y openjdk-8-jdk-headless -qq > /dev/null
import os
os.environ['JAVA_HOME'] = '/usr/lib/jvm/java-8-openjdk-amd64'
!pip install konlpy

# sklearn 설치
from sklearn.feature_extraction.text import CountVectorizer

# CountBectorizer : 텍스트의 feature 추출 모듈
# min_df : 단어장에 포함되기 위한 최소 빈도

# 한번만 등장해도 단어장에 포함시킴
vectorizer = CountVectorizer(min_df = 1)

# 모집중인 프로젝트
contents = [
    '가상 현실(VR)을 이용하여, 실제 현실의 쇼핑을 할 수 있게 하는 앱',
    '간단한 미션과, 힌트를 통해 주어진 문제를 풀어 방을 탈출 하는 게임',
    '일주일의 식단을 건강하게 유지하기 위해 식사 계획을 대신 해주는 웹사이트',
    '애완 동물의 전반적인 관리를 대신해주는 앱',
    '사용자가 입력한 글 내에서, 유사한 단어들을 알려주는 어플',
    '다른 사람들과 음식 레시피를 공유하고, 식재료에 대한 정보를 얻을 수 있는 앱',
    '친환경적인 여행을 계획할 수 있는 플랫폼',
    '다양한 프로젝트의 정보를 한눈에 확인할 수 있는 서비스',
    '사용자가 입력한 정보를 바탕으로, 가장 유사한 프로젝트를 추천해주는 어플'
]

# 이전에 사용자가 참여한 프로젝트(비교할 프로젝트)
new_post = ['사용자가 입력한 정보를 통해, 가장 유사한 프로젝트 항목을 알려주는 어플']

# 띄어쓰기를 기준으로 문장 요소를 나누고 저장
# 결과는 벡터화의 기준
X = vectorizer.fit_transform(contents)
feature_names = vectorizer.get_feature_names_out()
print(feature_names)


Y = X.toarray().transpose()
print(Y)

new_post_vec = vectorizer.transform(new_post)
print(new_post_vec.toarray())

import scipy as sp
def dist_raw(v1, v2):
    delta = v1 - v2
    return sp.linalg.norm(delta.toarray())

best_dist = 65535 # 임의의 큰 값 설정
best_i = None # 가장 비슷한 문장의 인덱스

# 모든 문장에 대해 거리 계산
for i in range(9):
    post_vec = X.getrow(i)

    # 함수 호출(거리 계산)
    d = dist_raw(post_vec, new_post_vec)

    print("== Post %i with dist=%.2f : %s" %(i,d,contents[i]))

    if d < best_dist:
        best_dist = d
        best_i = i

# 가장 가까운 문장 결과
print()
print("==> Best %i with dist=%.2f : %s"%(best_i, best_dist, contents[best_i]))

# 형태소 분석기
import konlpy
from konlpy.tag import Okt
from sklearn.feature_extraction.text import TfidfVectorizer

t = Okt()
vectorizer = TfidfVectorizer(min_df = 1, decode_error='ignore')

# 형태소 기준으로 토큰화
contents_tokens = [t.morphs(row) for row in contents]


# 띄어쓰기로 구분하여 하나의 문장으로 만들기
contents_for_vectorize = []

for content in contents_tokens:
    sentence = ''
    for word in content:
        sentence = sentence + ' ' + word

    contents_for_vectorize.append(sentence)

# 벡터
X = vectorizer.fit_transform(contents_for_vectorize)
X.toarray().transpose()

# new 문장을 형태소 기준으로 토큰화
new_post = ['사용자가 입력한 정보를 통해, 가장 유사한 프로젝트 항목을 알려주는 어플']

new_post_tokens = [t.morphs(row) for row in new_post]

# new 문장 벡터화 준비
new_post_for_vectorize = []

for content in new_post_tokens:
    sentence = ''
    for word in content:
        sentence = sentence + ' ' + word

    new_post_for_vectorize.append(sentence)

new_post_vec = vectorizer.transform(new_post_for_vectorize)

print(new_post_for_vectorize)
print(new_post_vec.toarray())

best_doc = None
best_dist = 65535
best_i = None

for i in range(9):
    post_vec = X.getrow(i)

    d = dist_raw(post_vec, new_post_vec)

    print('== Post %i with dist=%.2f : %s' %(i,d,contents[i]))

    if d<best_dist:
        best_dist = d
        best_i = i

print()
print("==> Best %i with dist=%.2f : %s" %(best_i, best_dist, contents[best_i]))
print('-->', new_post)
print('---->', contents[best_i])

def tfidf(t, d, D):
    tf = float(d.count(t)) / sum(d.count(w) for w in set(d))
    idf = sp.log(float(len(D)) / len([doc for doc in D if t in doc]))
    return tf, idf

from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer(min_df=1, decode_error='ignore')

# 토큰화
contents_tokens = [t.morphs(row) for row in contents]

contents_for_vectorize = []

for content in contents_tokens:
    sentence = ''
    for word in content:
        sentence = sentence + ' ' + word

    contents_for_vectorize.append(sentence)

# tf-idf 벡터화
X = vectorizer.fit_transform(contents_for_vectorize)
num_samples, num_features = X.shape
print(num_samples, num_features)

# new 문장 토큰화

new_post = ['사용자가 입력한 정보를 통해, 가장 유사한 프로젝트 항목을 알려주는 어플']

new_post_tokens = [t.morphs(row) for row in new_post]

new_post_for_vectorize = []

for content in new_post_tokens:
    sentence = ''
    for word in content:
        sentence = sentence + ' ' + word

    new_post_for_vectorize.append(sentence)

print(new_post_for_vectorize)

new_post_vec = vectorizer.transform(new_post_for_vectorize)
print(new_post_vec)

# 유사도 검사

best_doc = None
best_dist = 65535
best_i = None

for i in range(0,num_samples):
    post_vec = X.getrow(i)

    # 함수호출
    d = dist_raw(post_vec, new_post_vec)

    print("== Post %i with dist=%.2f  : %s" %(i,d,contents[i]))

    if d<best_dist:
        best_dist = d
        best_i = i

print("Best post is %i, dist = %.2f " % (best_i, best_dist))
print('-->', new_post)
print('---->', contents[best_i])