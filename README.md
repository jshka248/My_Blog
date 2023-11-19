# 목표 

- Django를 통해 블로그를 만드는 걸 목표

---
# 기술스택

- Django
- Python


- Bootstrap
- Javascript
- Html5


- Visual Studio Code

---

# 프로젝트 구조
```sh
my_blog
│
│  db.sqlite3
│  manage.py
│  requirements.txt
│  
├─accounts
│  │  admin.py
│  │  apps.py
│  │  forms.py
│  │  models.py
│  │  tests.py
│  │  urls.py
│  │  views.py
│  │  __init__.py
│  │  
│  ├─migrations
│  │  │  0001_initial.py
│  │  │  __init__.py
│  │  │  
│  │  └─__pycache__
│  │          0001_initial.cpython-311.pyc
│  │          __init__.cpython-311.pyc
│  │          
│  └─__pycache__
│          
├─blog
│  │  admin.py
│  │  apps.py
│  │  forms.py
│  │  models.py
│  │  tests.py
│  │  urls.py
│  │  views.py
│  │  __init__.py
│  │  
│  ├─migrations
│  │  │  0001_initial.py
│  │  │  0002_comment_content.py
│  │  │  0003_post_tag.py
│  │  │  0004_remove_post_tag_alter_tag_name.py
│  │  │  __init__.py
│  │  │  
│  │  └─__pycache__
│  │          
│  └─__pycache__
│          
├─blogbase
│  │  asgi.py
│  │  settings.py
│  │  urls.py
│  │  wsgi.py
│  │  __init__.py
│  │  
│  └─__pycache__
│          
├─locale
│  ├─en
│  │  └─LC_MESSAGES
│  │          django.mo
│  │          django.po
│  │          
│  └─ko
│      └─LC_MESSAGES
│              django.mo
│              django.po
│              
├─logs
│      bloglog
│      
├─main
│  │  admin.py
│  │  apps.py
│  │  models.py
│  │  tests.py
│  │  urls.py
│  │  views.py
│  │  
│  └─migrations
│    │  __init__.py
│    └─__pycache__
│            └─__init__.cpython-311.pyc
│          
├─media
│  └─blog
│      ├─files               
│      └─images
│                          
├─static
│  ├─assets
│  │      error.jpg
│  │      favicon.ico
│  │      home-bg.jpg
│  │      
│  ├─css
│  │      styles.css
│  │      
│  └─js
│          scripts.js
│          
└─templates
    │  400.html
    │  403.html
    │  404.html
    │  500.html
    │  base.html
    │  
    ├─accounts
    │      change_password.html
    │      form.html
    │      profile.html
    │      user_delete.html
    │      
    ├─blog
    │      form.html
    │      post_confirm_delete.html
    │      post_detail.html
    │      post_list.html
    │      
    └─main
            index.html
```

# ERD 구조


---

# Url 구조

|app: main |views 함수 이름|html 파일이름|
|:--------|:------------|:---------|
|''       |index         |index.html |

|app: accounts |views 함수 이름|html 파일이름   |
|:------------|:------------|:------------|
|'signup/'     |signup        |form.html|
|'login/'      |login         |form.html|
|'logout/'     |logout        |
|'profile/'    |profile       |profile.html  |
|'change_password/'|change_password|change_password.html|
|'delete/'|user_delete|user_delete.html|

|app: blog  |views 함수 이름  |html 파일이름   |
|:-------------|:--------------|:------------|
|''|post_list|post_list.html|
|'new/'|post_new|form.html|
|'<int: pk>/'|post_detail|post_detail.html|
|'<int: pk>/edit/'|postedit|form.html|
|'<int: pk>/delete/'|post_delete|post_confirm_delete.html|
|'<int: pk>/comment/new/'|comment_new|form.html|
|'<int: post_pk>/comment/<int: comment_pk>/edit/'|comment_edit|form.html|
|'<int: post_pk>/comment/<int: comment_pk>/delete/'|comment_delete|post_confirm_delete.html|
|'<int: post_pk>/comment/<int: comment_pk>/reply/'|comment_reply|form.html|
|'<int: post_pk>/comment/<int: comment_pk>/reply/<int: reply_pk>/edit/'|reply_edit|form.html|
|'<int: post_pk>/comment/<int: comment_pk>/reply/<int: reply_pk>/delete/'|reply_delete|post_confirm_delete.html|

---

# 요구 기능 구현

## 블로그


---

## 검색 (태그, 제목)


---

## 영한 변환 (I18N)


setting.py
```
LANGUAGE_CODE = 'ko-kr'

# 번역할 언어 추가
LANGUAGES = [
    ('en', 'English'),
    ('ko', 'Korean'),
]

USE_I18N = True # <-  True 인지 확인


# 번역될 .po 파일 저장소
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# 추가
'django.middleware.locale.LocaleMiddleware',

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware', # <--- 이곳에 추가함 (꼭 이곳에 추가)
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

MY_BLOG 폴더 안에서 locale 폴더 생성
```
mkdir locale
```


터미널에서
```
django-admin makemessages -l en
django-admin makemessages -l ko
```

입력하여 django.po 파일생성 후 

변역될 부분 
예시로 
```
#: .\templates\base.html:21 .\templates\base.html:39
msgid "블로그"
msgstr "블로그" <- 이곳에 번역 될 언어로 작성
```
입력 후 터미널에서
```
django-admin compilemessages
```
입력하여 django.mo파일이 생성되면 완료

---

## 비밀번호 수정 및 회원탈퇴


---

## 댓글과 대댓글 (생성, 수정, 삭제)


---

## 게시물 수정 삭제


---

## 삭제된 페이지 오류 페이지 


---
# 로그 코드

```
# log 기록 남기는 코드 
DEBUG = True  # <- True와 False일때 밑의 LOGGING 코드에서 'filters': ['require_debug_true'],에서 True를 Fales 로 수정 해줘야 한다. (수정될 부분은 * 로 표기)

ALLOWED_HOSTS = ['*']

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[{server_time}] {message}',
            'style': '{',
        },
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_false'], # *
            'class': 'logging.StreamHandler',
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
        'mail_admins': {
            'level': 'INFO',
            'filters': ['require_debug_false'], # *
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'file': {
            'level': 'INFO',
            'encoding': 'utf-8',
            'filters': ['require_debug_false'], # *
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs/bloglog', # log파일 경로와 저장될 파일명
            'maxBytes': 1024*1024*1,  # 용량 1 MB
            'backupCount': 25, # 파일갯수 (25개 넘어가면 기존파일이 지워지고 새로 생성)
            'formatter': 'standard',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'mail_admins', 'file'],
            'level': 'INFO',
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        },
        'my': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
    }
}

# 'level' 은 DEBUG < INFO < WARNING < ERROR < CRITICAL 순 입니다.
```

MY_BLOG 폴더 
```
mkdir logs 
```
폴더 생성 하면 완료

---





