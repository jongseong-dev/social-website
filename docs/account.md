<!-- TOC -->
  * [사용자 인증 시스템](#사용자-인증-시스템)
    * [Middleware](#middleware)
    * [Django의 인증뷰](#django의-인증뷰)
  * [사용자 등록](#사용자-등록)
  * [사용자 정보 수정](#사용자-정보-수정)
  * [메시지 프레임워크를 통한 알림 표시](#메시지-프레임워크를-통한-알림-표시)
  * [커스텀 인증 백엔드 구축하기](#커스텀-인증-백엔드-구축하기)
  * [소셜 인증하기](#소셜-인증하기)
    * [개발환경에서 localhost 리다이렉션 하기](#개발환경에서-localhost-리다이렉션-하기)
    * [소셜 인증을 위한 HTTPS 연결 방법](#소셜-인증을-위한-https-연결-방법)
    * [X를 사용한 인증](#x를-사용한-인증)
    * [google을 사용한 인증](#google을-사용한-인증)
    * [소셜 인증으로 등록한 사용자 프로필 생성하기](#소셜-인증으로-등록한-사용자-프로필-생성하기)
<!-- TOC -->


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

## 소셜 인증하기
- Facebook, Google, Twitter를 사용한 인증
  - OAuth 2.0 사용
    - OAuth 2.0은 웹 사이트 또는 애플리케이션이 사용자를 대신해서 다른 웹 앱에서 호스팅하는 리소스에 액세스할 수 있도록 설계된 표준이다. 
    - https://github.com/python-social-auth/social-app-django
  - SSO를 사용하기

### 개발환경에서 localhost 리다이렉션 하기
- 여러 소셜 서비스는 인증에 성공한 후 사용자를 127.0.0.1 또는 localhost로 리디렉션하는 것을 허용하지 않는다.
- URL 리디렉션을 위한 도메인 이름을 기대한다.
- 로컬시스템에서는 도메인 설정을 위해 hosts를 수정하자.

```shell
# linux 또는 macOs 에서는 hosts 위치: /etc/hosts
# windows 에서는 C:\Windows\System32\drivers\etc\hosts

...
127.0.0.1 mysite.com
```
- 해당 설정을 한 뒤 Django에서 ALLOWED_HOSTS에 mysite.com을 추가하자.

### 소셜 인증을 위한 HTTPS 연결 방법
- 사용할 소셜 인증 방법 중 일부는 HTTPS 연결이 필요하다.
- Django 개발 서버는 정식 서비스 용도가 아니기 떄문에 HTTPS를 통해 사이트를 제공할 수 없다.
- Django 확장 패키지의 RunServerPlus 확장을 통한 소셜 인증 테스트를 하자
  - 단 RunServerPlus는 개발 서버를 실행할 때만 사용해야 한다.
  ```shell
  poetry add django-extensions --group dev
  poetry add werkzeug --group dev
  poetry add pyOpenSSL --group dev 
  ```
  - 위의 패키지를 설치 한 뒤, 다음과 같이 실행하자.
  ```shell
  python manage.py runserver_plus --cert-file cert.crt
  ```
  
### X를 사용한 인증
- https://developer.twitter.com/ 에서 개발자 계정을 만든 뒤 app을 등록한다.

### google을 사용한 인증
- https://console.cloud.google.com/ 에서 프로젝트를 만든 뒤, OAuth 2.0 클라이언트 ID를 만든다.

### 소셜 인증으로 등록한 사용자 프로필 생성하기

- 사용자가 소셜 인증을 사용해서 인증할 때 해당 소셜 프로필과 연결된 기존 사용자가 없으면 새 사용자 객체가 생성된다.
- 파이썬 소셜 인증은 인증 흐름 중에 실행되는 일련의 함수 집합으로 이뤄진 파이프라인을 사용한다.
- 파이프라인은 특정 순서로 실행된다.
- 이 함수들은 사용자 세부 정보 조회, 데이터베이스에 소셜 프로필 생성, 기존 사용자에 연결 또는 새로운 프로필 생성을 처리한다.
- 현재 소셜 인증을 통해 신규 사용자가 생성되면 Profile 객체가 생성되지 않는다. 
- 새로운 사용자가 생성될 때 자동으로 데이터베이스에 Profile 객체가 생성되도록 파이프라인에 새로운 단계를 추가할 예정