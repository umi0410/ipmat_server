# ipmat: python django와 docker를 이용한 API server 

> ipmat 프로젝트는 사전에 입력한 음식 데이터를 바탕으로 월드컵 형식으로 랜덤하게 음식을 추천받을 수 있고,
> 서로의 입맛에 대한 퀴즈를 내어볼 수 있는 Android, Django project입니다.
> 
> 본 프로젝트는 2019.07 - 2019.08 동안 개발되어 약 1,000 건의 다운로드 성과를 기록한 뒤,
> 마무리되었습니다.

![preview1](preview1.jpg)![preview2](preview2.jpg)

## 🌟 사용한 기술

- Python Django

- AWS
  - EC2
  - RDS
  - S3

- MySQL

- Android Studio Java

- Docker, Docker compose, Docker swarm, ECR

- Nginx

## 🏗️ 애플리케이션 구조

### 1. Server

`Django` 를 바탕으로 `API Server` 을 구축한다. API Server를 통해 Android Application과 소통한다.

`Django`는 DB로 `AWS RDS`의 `MySQL` 을 이용한다. 사진을 저장하는 저장소로는 `S3` 를 이용한다.

AWS의 ECR을 이용해 이미지를 만들어 Push하고, 별 다른 설정 없이 docker command를 이용해 새 버전을 배포한다.

```bash
docker run --name -d ipmat-server -p 8001:8000
```

### 2. Client

클라이언트는 Android studio와 JAVA를 이용한 Android Application이다. Django server의
API를 이용해 앱에 여러 정보를 표시한다.

## 📜 Requirements

### 1. Python packages

```bash
$ pip install -r requirements.txt
``` 

### 2. Environment variables

사용하는 Environmental variables는 
  * `.env`, 
  * `.production.env`

~~이 두 파일은 `ipmat-upload` 버킷에 프라이빗하게 업로드 해두었다. 
혹시라도 이 파일들을 완전히 분실하게 된다면 골치아프겠지만, 
이러한 상황을 대비해 S3 버킷에 업로드해둔 것이다.
`.env`와 `.production.env`는 private repository라도 **추후에 public으로 바꿀 때를 대비해 Github에 공개하지 말 것**~~

(_이 당시엔 private한 내용을 보관하기위해 S3의 priviate bucket에 credential들을 보관하곤했는데
지나고보니 바람직한 방법은 아니었던 것 같다. - 2020.11.10_)

환경변수 파일은 어차피 ECR의 이미지 속에 들어있으므로 서버에 Deploy할 시에는 따로 환경변수 파일이 필요없다.

## 🚀 How to run the server

### Option 1. Docker swarm

저렴하게 서버를 돌리기 위해 서버 인스턴스를 단 1대만 이용하지만 `docker swarm` 을 이용해
단일 호스트 내에 2개 이상의 container replica를 돌림으로써 무중단 배포를 가능케했다. 
또한 healthcheck을 통한 healthy한 컨테이너의 replica 수를 유지했다.

#### service가 존재하지 않는 경우) service를 만든다.

> docker-compose.yml로 stack을 이용해 service를 만드는 방법도 있지만, 
> 이걸 이용하면 결국 서버에서 git clone을 통해 해당 yml file을 받는 등의 행위를 해야하고
> 서버가 state를 갖게 된다.
> docker command만으로 서버를 돌리는 것이 목표이므로 cli 에서 바로 service를 만든다.

```bash
$ docker service create --name ipmat-server -p 8001:8000 \
--replicas 2 \
--health-cmd='curl -sS http://localhost:8000 || exit 1' \
--health-timeout=5s \
--health-retries=2 \
--health-interval=10s \
325498511266.dkr.ecr.ap-northeast-2.amazonaws.com/ipmat-server:stable
```

목표 중 하나가 **무중단 배포**였던만큼 **service를 삭제하는 일은 가급적 없어야한다.**

#### service가 존재하는 경우) 해당 service의 image를 업데이트한다.

```bash
$ $(aws ecr get-login --no-include-email) && \
docker pull 325498511266.dkr.ecr.ap-northeast-2.amazonaws.com/ipmat-server:stable && \
docker service update --image 325498511266.dkr.ecr.ap-northeast-2.amazonaws.com/ipmat-server:stable ipmat-server --force
```

같은 태그(ipmat-server:stable)의 이미지로 업데이트 하는 것이므로 --force 옵션을 붙여준다.

### Option 2. 단순 컨테이너 run 방식

`aws configure`후에 `$(aws ecr get-login --no-include-email)` 을 통해 ECR에 접근할 수 있도록 로그인한다.

**1. 서버를 실제로 run**

```bash
$ docker run -d --name ipmat --rm -p 8001:8000 --env IPMAT_MODE=production \
  325498511266.dkr.ecr.ap-northeast-2.amazonaws.com/ipmat-server:stable
```

**2. 디버깅을 위해 서버를 run**

```bash
$ docker run --name ipmat --rm -p 8001:8000 --env IPMAT_MODE=development \
  325498511266.dkr.ecr.ap-northeast-2.amazonaws.com/ipmat-server:stable
```

## 📆 작업 내역

- **20190826**

  nav와 action bar, toolbar 등의 설정을 Activity 마다 복붙형식으로 했었는데, 이를 DrawerSetter 클래스를 정의하여 깔끔하게 구현해놓음

  Exam Delete 기능을 추가함

- **20190828**

  난잡하게 LinearLayout과 ImageView를 겹쳐서 진행하던 FoodExam을 CardView를 이용해서 깔끔하게 정리함.

  Instagram 먹킷리스트 유저들과 연결해서 Food Images 가져옴

- **20190830**

  cardView를 통해 깔끔하게 정리하고 food_name 잘 보이게 수정. RoundCorner, Shadow 적용함.

- **20190902**

  Logo 와 Icon 및 디자인 조금 더 깔끔하게 변경

- **20190905**

  s3와 Django Backend를 연동함

- **20190907**

  FoodBookList 자체가 클릭 이벤트 받게 고침.

  ExamList Delete, ExamDetail Login, Singup 등등의 Activity에서 불필요하게 Activity가 남겨지던 것들 정리

  ParticipantCount, FoodBookPlayCount 반영함.

- **20190908**

  두 개의 액티비티에 Admob을 달았음.

  Worldcup 진행 시 인스타 아이디가 아래쪽은 바뀌지 않는 버그가 있었는데, 그거랑 자잘한 버그 수정.

- **20190909 플레이스토어에 출시**

  마지막 Activity인 경우 Back press 2번하게 수정함.

  sub_image와 sub_creator 추가함.

- **201910**

  docker-compose를 이용해 nginx와 묶어봄.

- **202002**

  서버를 이전하는 과정에서 이 프로젝트의 경우 Docker을 이용하는 데에 적절하도록 구조가 잡혀있었기에,
  서버 컴퓨터의 구조를 더럽히지 않고 간단히 docker를 이용하기로 결정.

  ECR을 통해 Private repository를 이용한다.

- **20200308**

  과거에 docker-compose를 이용해 nginx와 묶는 작업을 하곤했는데, 그럴 필요성을 못느껴 단일 container로 run 하는 방식을 이용했었다.

  docker swarm을 다루게되면서 healthcheck기능과 자동 loadbalancling 기능을 이용하면 좋을 것 같다고 판단하여 한 호스트 내에서 2개 이상의 컨테이너를 run 시키면서 
  무중단배포와 health check후 replica의 수를 유지하는 작업을 이뤄냈다.

- **202003xx**

  docker swarm을 통해 replica를 2개 이상 띄우자 CPU Credit을 많이 사용하게 되었고,
  CPU Credit을 모두 소진 시에 서버가 원활히 동작하지 못해 다시 docker-compose로 롤백하게되었다.