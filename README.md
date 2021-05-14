# 인테리어 커머스 사이트 SweetHome
> ### 원스톱 인테리어 플랫폼 오늘의 집을 모티브로 한 프로젝트입니다.

👇 아래 이미지를 클릭하시면 시연 영상이 재생됩니다.
[![SweetHome](https://media.vlpt.us/images/c_hyun403/post/057f55b9-bd7d-42f6-bca6-b9b563a1c2fd/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA%202021-03-01%20%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE%209.58.38.png)](https://www.youtube.com/watch?v=wpD3biBt4GY&feature=youtu.be)

### 개발일정
- 기간 : 2021.02.15 ~ 2021.03.12 (12일)
- 구성원 : 프론트 3명, 백엔드 4명

### 기술 스택
- Language: Python
- Framework: Django
- Database: MySQL
- AWS(EC2, RDS)
- Bcrypt, JWT

### API 문서
https://documenter.getpostman.com/view/14759380/TzRVf6et

### 담당 구현 기능
- 관계형 데이터베이스 모델링, MySQL 연동
- csv 데이터 파일 및 파이썬 db_uploader 작성
- 카테고리, 상품 리스트, 상세 페이지 조회 API 구현
- 쿼리 스트링과 딕셔너리를 활용한 다중 필터링 및 정렬 구현
- select_related, prefetch_related 메소드를 적용한 쿼리 최적화
- List Comprehension을 적용한 조회 성능 향상

### 백엔드 구현 기능
Goals : 하나의 cycle 완성하기
> 유저의 회원가입/로그인 -> SNS 기능 둘러보기 (탐색) -> 스토어에서 상품 고르기 (발견) -> 장바구니에 담기 (구매) -> 최종 결제하기

**공통**
- modeling
- db_uploader작성 & CSV 파일 생성(백업용)

**user app**
- 회원가입 로직
- 로그인 로직
- 비밀번호 암호화, 토큰 발행
- 회원 유효성 판단(login_decorator 작성)
- 비회원용 login_decorator (non_user_accept_decorator)작성

**posting app**
- 상품 조건별 정렬 & filtering
- 회원유저와 posting간의 `좋아요` 기능 구현
- 회원유저와 posting간의 `스크랩` 기능 구현
- 회원 유저가 로그인 했을 경우 `좋아요`, `스크랩` 상태 반영하여 게시물 데이터 전송

**product app**
- 카테고리별 상품 나열
- 상품 조건별 정렬 & filtering
- 상품 상세페이지 조회
- 상품 리뷰 조회(조건별 정렬)

**order app**
- 장바구니에 상품 담기
- 장바구니 내역 조회
- 장바구니 수량 변경 및 이에 대한 조회


# Reference
- 이 프로젝트는 <a href="https://ohou.se/store?utm_source=brand_google&utm_medium=cpc&utm_campaign=commerce&utm_content=e&utm_term=%EC%98%A4%EB%8A%98%EC%9D%98%EC%A7%91&source=14&affect_type=UtmUrl&gclid=Cj0KCQiAvvKBBhCXARIsACTePW-OH_Ghcoi3Hc5h91keYYbu6vNnk21lW688iQLrykOVE4ARC9_uxKQaAj6UEALw_wcB">오늘의 집</a> 사이트를 참조하여 학습목적으로 만들었습니다.
- 실무수준의 프로젝트이지만 학습용으로 만들었기 때문에 이 코드를 활용하여 이득을 취하거나 무단 배포할 경우 법적으로 문제될 수 있습니다.
- 이 프로젝트에서 사용하고 있는 사진 대부분은 위코드에서 구매한 것이므로 해당 프로젝트 외부인이 사용할 수 없습니다.

