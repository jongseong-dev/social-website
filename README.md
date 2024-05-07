# blog-site

- "예제로 배우는 Django 4" 책을 보고 만든 예제 Repo

<!-- TOC -->
* [blog-site](#blog-site)
* [프로젝트 시작하기](#프로젝트-시작하기)
  * [필요한 요소 세팅 및 Django App 실행하기](#필요한-요소-세팅-및-django-app-실행하기)
    * [1. 패키지 설치](#1-패키지-설치)
    * [2. DB 설치 후 migration](#2-db-설치-후-migration)
    * [3. Django 실행하기](#3-django-실행하기)
    * [4. Django test 실행하기](#4-django-test-실행하기)
  * [번외. docker-compose로 실행하기](#번외-docker-compose로-실행하기)
    * [1. docker-compose 서비스 실행](#1-docker-compose-서비스-실행)
    * [2. docker-compose 서비스 종료](#2-docker-compose-서비스-종료)
  * [환경변수](#환경변수)
    * [Django Config](#django-config)
    * [DB](#db)
    * [EMAIL](#email)
* [프로젝트의 기능 소개](#프로젝트의-기능-소개)
<!-- TOC -->
<!-- TOC -->

# 프로젝트 시작하기

## 필요한 요소 세팅 및 Django App 실행하기

- 들어가기에 앞서 `poetry`와 `docker`를 설치해주세요.
    - poetry 설치 방법: https://python-poetry.org/docs/#installation
    - docker 설치 방법: https://docs.docker.com/engine/install/

- DJANGO_SETTING_MODULE 설정하기
    - 현재 개발환경에서는 `config.settings.local`을 사용하고 있습니다.
    - 따라서 명령마다 --settings 옵션을 넣기 불편하다면 **DJANGO_SETTING_MODULE**을 `config.settings.local`로 환경변수로 설정해주세요.

### 1. 패키지 설치

- poetry를 통해 패키지를 설치합니다.

  ```bash
  poetry install
  ```

- 가상환경이 활성화 되었다면 `pre-commit`을 설치합니다.

  ```bash
  pre-commit install
  ```

### 2. DB 설치 후 migration

- django를 띄우기 위해 db를 설치합니다.
  ```bash
  docker-compose up -d db
  ```

- 해당 db가 무사히 실행되었다면, migration을 실행합니다.
- 이떄 주의할 점은 project 위치는 webapp 이므로 `webapp`으로 이동 후 실행합니다.
  ```bash 
  python manage.py migrate --settings=config.settings.local
  ```

### 3. Django 실행하기

- migration이 완료되었다면, django를 실행합니다.

  ```bash
  python manage.py runserver --settings=config.settings.local
  ```

### 4. Django test 실행하기

- test는 아래와 같이 실행합니다.

- Linux, MacOS
  ```bash
  pytest
  ```

- 만약 test 가 제대로 실행되지 않는다면 pytest의 실행 위치가 `webapp` 디렉토리인지 확인해주세요.

## 번외. docker-compose로 실행하기

- 만약 docker-compose를 통해 Django를 실행시키고 싶다면 steps를 따라주세요.

### 1. docker-compose 서비스 실행

- docker compose 를 통해 db와 test, was를 실행합니다.

  ```bash
  docker-compose up --build -d db
  docker-compose up --build web 
  docker-compose up --build test_web 
  ```

### 2. docker-compose 서비스 종료

- 확인했다면 docker-compose에 떠있는 container를 종료시킵니다.

  ```bash
  docker-compose down
  ```

## 환경변수

- 기본값이 없는 경우 **직접 지정해야 합니다.**

### Django Config

| 변수명                    | 기본값            | 비고                                                      |
|------------------------|----------------|---------------------------------------------------------| 
| DJANGO_SETTINGS_MODULE | 없음             |                                                         |
| SECRET_KEY             | 94n7fx27pd-... | local 환경과 test 환경에서는 기본값을 사용하지만 <br/> prod에서는 주입해야 합니다. |

### DB

| 변수명         | 기본값       |
|-------------|-----------|
| DB_NAME     | postgres  |
| DB_USER     | postgres  |
| DB_PASSWORD | postgres  |
| DB_HOST     | localhost |
| DB_PORT     | 5432      |

### EMAIL

| 변수명                 | 기본값                   |
|---------------------|-----------------------|
| EMAIL_HOST_PASSWORD | 없음                    |
| EMAIL_HOST          | smtp.gmail.com        |
| EMAIL_HOST_USER     | dlwhdtjd098@gmail.com |
| EMAIL_PORT          | 587                   |
| EMAIL_USE_TLS       | True                  |

# 프로젝트의 기능 소개

## 사용자 인증 시스템

### Middleware
- AuthenticationMiddleware
  - 세션을 사용해서 사용자와 요청(request)를 연결한다. 
- SessionMiddleware
  - 요청 간에 현재 세션을 처리한다. 

### Django의 인증뷰

- Django는 인증을 처리하기 위해 다음과 같은 클래스 기반 뷰를 제공한다.
  - LoginView
    - 로그인 폼을 처리하고 사용자를 로그인시킨다.
  - LogoutView
    - 사용자를 로그아웃 시킨다.
  - PaswordChangeView
    - 사용자의 비밀번호를 변경한다.
  - PasswordChangeDoneView
    - 성공적인 패스워드 변경 후 사용자가 리디렉션되는 뷰
  - PasswordResetView
    - 사용자의 비밀번호를 재설정한다.
    - 토큰으로 일회용 링크를 생성해서 사용자의 이메일 계정으로 보낸다.
  - PasswordResetDoneView
    - 사용자에게 패스워드 재설정 링크가 포함된 이메일이 전송되었음을 알린다.
  - PasswordResetConfirmView
    - 사용자가 새로운 패스워드를 설정할 수 있다.
  - PasswordResetCompleteView
    - 사용자가 패스워드를 성공적으로 재설정한 후 리디렉션되는 성공 뷰이다.
    
- `templates/registration`는 Django 인증 뷰에서 인증 템플릿이 있을 것으로 예상하는 기본 경로이다.

## 사용자 등록
- 사용자 계정을 등록할 수 있다.

## 사용자 정보 수정
- 사용자 정보를 수정할 수 있다.
- 정보가 수정되면 메시지 프레임워크를 통해 메시지를 받을 수 있다.

## 메시지 프레임워크를 통한 알림 표시
- Django에는 사용자에게 일회성 알림을 표시할 수 있는 내장 메시지 프레임워크가 있다.
- 메시지 프레임워크는 사용자에게 메시지를 추가하는 간단한 방법을 제공
- 메시지들은 기본적으로 쿠키에 저장되며 사용자의 다음 요청 시에 표시되고 삭제된다.
- 메서드 정리
  - success(): 작업이 성공했을 때 표시할 성공 메시지를 만들 때 사용
  - info(): 정보성 메시지를 표시할 때 사용
  - warning(): 경고성 메시지를 표시할 때 사용
  - error(): 작업이 실패했거나 오류가 발생했을 때 사용
  - debug(): 프로덕션 환경에서는 제거해야 하거나 무시되는 디버그 메시지를 만들 때 사용

## 커스텀 인증 백엔드 구축하기
- 기본 `ModelBackend`는 django.contrib.auth의 User 모델을 사용해서 데이터베이스에 사용자를 인증한다.
- 이는 대부분의 웹 프로젝트에 적합하지만, 커스텀 백엔드를 만들어 LDAP 디렉토리 또는 기타 시스템과 같은 다른 사용자를 인증할 수 있다.
- django.contrib.auth의 authenticate() 함수가 사용될 때마다 Django는 AUTHENTICATION_BACKENDS 설정에 지정된 백엔드를 순회하며 사용자를 인증한다.
- 커스텀 인증 백엔드는 아래의 두 가지 메서드를 모두 구현하는 클래스를 작성하여 구현한다.
  - authenticate(): request 객체 및 사용자 자격 증명을 매개 변수로 사용한다. 자격 증명이 유효하면 user 객체를 반호나하고 그렇지 않으면 None을 반환
  - get_user(): 사용자 ID를 매개 변수로 취해서 user 객체를 반환해야 한다. 