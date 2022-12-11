# R6Helper

## 프로젝트 참여자

| 학과         | 학번     | 이름   |
| ------------ | -------- | ------ |
| 컴퓨터공학과 | 21101176 | 김채우 |

## 프로젝트 설명

---

-   개발 동기
    -   평소 주로 하던 게임인 유비소프트(ubisoft) 사의 레인보우 식스 시즈(Rainbow Six Seige), 줄여서 '레식'의 승률, 킬뎃, 랭크와 같은 게임 정보를 게임 스텟 사이트에 직접 접속하지 않고 웹크롤링과 api를 사용하여 게임할 때 주로 사용하는 '디스코드'의 봇을 통해 얻을 수 있도록 함.
-   추후 계획
    -   디스코드 봇은 사이트에 직접 접속하는 것보다는 간편하지만 전체화면 게임의 경우 게임 창을 내려서 사용해야 하기 때문에 게임의 창을 내리지 않고 사용할 수 있도록 '게임 오버레이' 기능을 가진 프로그램을 추후 개발할 예정. 또한 해당 디스코드 봇은 실시간으로 게임 플레이 정보를 얻지 못하므로 실시간으로 정보를 획득할 수 있는 API 활용.

## 프로젝트 기능

---

-   봇 초대 및 기본 사용 방법

    -   디스코드 봇을 서버에 초대

        -   초대 방법
            -   [디스코드 봇 초대 링크](https://discord.com/api/oauth2/authorize?client_id=1050716394792169562&permissions=137439291456&scope=bot)
            -   디스코드에 로그인을 한 후 본인 서버 혹은 봇 초대 권한이 있는 서버에 해당 봇을 초대 가능

    -   봇 명령어 사용 방법
        -   명령어 앞에 접두사 `!`를 붙이거나 멘션(`@R6Helpr`) 뒤에 명령어를 붙여서 사용 가능

-   봇 기본 명령어

    -   `help`
        -   명령어를 카테고리 별로 분류하여 보여줌

-   봇 설정 명령어

    -   `setting`
        -   기본 설정
            -   해당 명령어를 사용한 서버 id와 서버의 채널 id, 기본 명령어 접두사 !를 ./data/guilds.json에 저장
    -   `reset`
        -   설정 초기화
            -   해당 명령어를 사용한 서버의 데이터를 ./data/guilds.json에서 삭제
    -   `prefix` {pre}
        -   명령어 접두사(prefix) 변경 (기본: `!`)
            -   서버마다 별도로 명령어 접두사 설정 가능
            -   일반 문자나 복잡한 특수문자가 아닌 ./constants/prefix.py의 prefix_list에 있는 것만 사용 가능
    -   `load/unload/reload` {\*cogs}
        -   명령어 수정 및 관리 명령어
            -   Cogs 폴더에 정리해둔 명령어 파일들을 관리하는 명령어
            -   해당 명령어들을 통해 봇을 끄지 않고 실행되고 있는 상태로 명령어를 로드, 언로드, 리로드 가능
            -   명령어 뒤에 적은 파일 적용, 파일 이름을 쓰지 않으면 전체 파일 적용
            -   ![image](https://user-images.githubusercontent.com/113341200/206906445-d8e3c784-2f95-4451-b312-74780bb74523.png)


-   유저 관리 명령어

    -   `login`
        -   게임 및 유저 정보를 얻기 위해 이메일, 비밀번호, 닉네임을 봇 DM으로 차례대로 입력하여 유비소프트에 로그인 후 성공적으로 로그인 하면 유저 정보를 ./data/users.json에 저장
        -   비밀번호는 cryptography 모듈을 통해 암호화를 진행하여 저장
    -   `user` {name}
        -   login을 통해 등록한 유저의 정보를 간단하게 확인 가능
    -   `search` {name}
        -   [R6Tracker 사이트](https://r6.tracker.network/) 에서 웹크롤링을 통해 유저를 확인하여 링크를 보냄

-   게임 정보 명령어

    -   `map` {name} {mode} {count}
        -   각 맵을 승률이 높은 순으로 정렬하여 보여줌
        -   mode는 전체, 랭크, 캐주얼 등 게임 모드를 구별함 (default: all)
        -   count는 전체 승률 몇위까지 보여줄 것인지 알려줌 (default: 5)
    -   `rank` {name} {y} {s}
        -   y와 s로 랭크 시즌을 선택하여 해당 시즌 전적 정보를 보여줌
        -   12월 11일 기준 최신 시즌 Y7S4 업데이트 후 해당 시즌은 api 작동이 안되어 이전 시즌인 Y7S3를 기본값으로 함
    -   `operator` {name} {mode} {count} {operator_type}
        -   각 오퍼레이터(캐릭터)를 킬뎃이 높은 순으로 정렬하여 킬뎃, 승률, 플레이 횟수를 보여줌
        -   mode는 전체, 랭크, 캐주얼 등 게임 모드를 구별함 (default: all)
        -   count는 전체 승률 몇위까지 보여줄 것인지 알려줌 (default: 5)
        -   operator_type는 전체, 공격, 방어 오퍼레이터를 결정함 (default: all)

## 프로젝트 사용 예시

## 사용 모듈

-   os
-   pandas
-   numpy
-   pathlib
-   requests
-   beautifulsoup4
-   cryptography
-   discord
-   asyncio
-   siegeapi

## 출처

-   https://www.youtube.com/playlist?list=PLW3GfRiBCHOhfVoiDZpSz8SM_HybXRPzZ
    -   디스코드 봇 구성에 대한 정보
