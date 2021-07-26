# HAE

#### How About Exercise?(Back-end)
#### [How About Exercise?(Android)](https://github.com/jnfuture0/HAE_Android)
#### This is a project from 2020.07 ~ 2020.08
- using Django

---

### DOCMUENTS
- [요구사항분석서(SRA)](https://github.com/KimUJin3359/HAE/blob/master/document/%EC%9A%94%EA%B5%AC%EC%82%AC%ED%95%AD%EB%B6%84%EC%84%9D.pdf)
- [요구사항명세서(SRS)](https://github.com/KimUJin3359/HAE/blob/master/document/%EC%9A%94%EA%B5%AC%EC%82%AC%ED%95%AD%EB%AA%85%EC%84%B8.pdf)
- [1st demo](https://github.com/KimUJin3359/HAE/blob/master/document/1%EC%B0%A8%20%EC%8B%9C%EC%95%88.pdf)
- [시스템테스트 계획서(STP)](https://github.com/KimUJin3359/HAE/blob/master/document/%EC%8B%9C%EC%8A%A4%ED%85%9C%ED%85%8C%EC%8A%A4%ED%8A%B8%EA%B3%84%ED%9A%8D.pdf)
- [설계서(SDS)](https://github.com/KimUJin3359/HAE/blob/master/document/%EC%86%8C%ED%94%84%ED%8A%B8%EC%9B%A8%EC%96%B4%EB%94%94%EC%9E%90%EC%9D%B8%EB%AA%85%EC%84%B8.pdf)
- [최종 포스터](https://github.com/KimUJin3359/HAE/blob/master/document/HAE_%ED%8F%AC%EC%8A%A4%ED%84%B0.pdf)

---

### 프로젝트 개요
![SW경진대회_작품설명서_HAE (1)_page-0003](https://user-images.githubusercontent.com/50474972/109842392-6021e880-7c8d-11eb-849d-fa9466f064e7.jpg)

### 작품 구성
![SW경진대회_작품설명서_HAE (1)_page-0004](https://user-images.githubusercontent.com/50474972/109842471-73cd4f00-7c8d-11eb-8640-7ad16526691f.jpg)
![SW경진대회_작품설명서_HAE (1)_page-0005](https://user-images.githubusercontent.com/50474972/109842485-75971280-7c8d-11eb-951f-f7ba86b2772c.jpg)

### 결과물
![SW경진대회_작품설명서_HAE (1)_page-0007](https://user-images.githubusercontent.com/50474972/109842623-995a5880-7c8d-11eb-9a76-6e6bf4cf421f.jpg)

#### [영상 링크](https://www.youtube.com/watch?v=NVYHjHHro0A&feature=youtu.be)

---

### 관련 코드
- [DB_model](https://github.com/KimUJin3359/HAE_back_end/blob/master/HAE_DB/models.py)
  - 데이터베이스 모델 설정
  - 관련 기능 설정
- [DB_serializer](https://github.com/KimUJin3359/HAE_back_end/blob/master/HAE_DB/serializers.py)
  - data를 받아오기 위한 설정
- [DB_views](https://github.com/KimUJin3359/HAE_back_end/blob/master/HAE_DB/views.py)
  - 각 기능에 맞춰 작업을 수행(조회, 생성, 수정, 삭제)
  - 후에 알게된 것이지만 데이터를 일괄 업데이트 할 때는 PUT, 개별로 업데이트 할 때는 PATCH 사용

---

### AWS 서버 설정 시 발생한 오류
```
File "/usr/local/lib/python3.9/subprocess.py", line 528, in run
    raise CalledProcessError(retcode, process.args, subprocess.CalledProcessError: Command '('lsb_release', '-a')' returned non-zero exit status 1.
```
- 해결 lsb_release 재연동 : $ sudo ln -s /usr/share/pyshared/lsb_release.py /usr/local/lib/python3.9/site-packages/lsb_release.py
