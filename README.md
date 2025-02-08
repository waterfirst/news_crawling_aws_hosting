안녕하세요! 뉴스 크롤러를 구축하고 AWS S3를 사용하여 결과를 호스팅하는 전체 과정을 단계별로 정리한 매뉴얼을 제공해드리겠습니다. 이 매뉴얼을 따라 하시면 Python과 VS Code 설치부터 AWS 설정, Python 스크립트 작성 및 실행, 비용 관리까지 모든 과정을 원활하게 완료하실 수 있습니다.

https://my-news-report-bucket-unique123.s3.ap-northeast-2.amazonaws.com/news_report.html

## 목차

1. [필요한 도구 및 사전 준비](#1-필요한-도구-및-사전-준비)
2. [Python 설치](#2-python-설치)
3. [VS Code 설치 및 설정](#3-vs-code-설치-및-설정)
4. [AWS 계정 생성 및 IAM 사용자 설정](#4-aws-계정-생성-및-iam-사용자-설정)
5. [AWS CLI 설치 및 구성](#5-aws-cli-설치-및-구성)
6. [AWS S3 버킷 생성 및 설정](#6-aws-s3-버킷-생성-및-설정)
7. [Python 스크립트 작성 및 `boto3` 설치](#7-python-스크립트-작성-및-boto3-설치)
8. [Python 스크립트 실행 및 S3 업로드](#8-python-스크립트-실행-및-s3-업로드)
9. [S3 버킷 Lifecycle 정책 설정](#9-s3-버킷-lifecycle-정책-설정)
10. [IAM 권한 최소화 및 보안 설정](#10-iam-권한-최소화-및-보안-설정)
11. [비용 모니터링 및 관리](#11-비용-모니터링-및-관리)
12. [자동화 및 스케줄링 설정 (선택 사항)](#12-자동화-및-스케줄링-설정-선택-사항)
13. [최종 확인 및 테스트](#13-최종-확인-및-테스트)
14. [문제 해결](#14-문제-해결)

---

## 1. 필요한 도구 및 사전 준비

### 필수 도구

- **AWS 계정**: [AWS 계정 생성](https://aws.amazon.com/ko/) (이미 보유 중인 경우 이 단계를 건너뛰세요)
- **Python**: 최신 버전 설치
- **Visual Studio Code (VS Code)**: 코드 편집기
- **AWS CLI**: AWS 서비스와 상호작용하기 위한 명령줄 도구
- **Git (선택 사항)**: 버전 관리

### 사전 준비

- **인터넷 연결**
- **AWS 자격 증명 (Access Key ID 및 Secret Access Key)**: IAM 사용자 생성 시 발급

---

## 2. Python 설치

1. **Python 다운로드**
   - [Python 공식 웹사이트](https://www.python.org/downloads/)로 이동하여 최신 버전을 다운로드합니다.
   - Windows 사용자는 `Windows x86-64 executable installer`를 다운로드합니다.

2. **Python 설치**
   - 다운로드한 설치 파일을 실행합니다.
   - **Important:** 설치 화면 하단의 **"Add Python to PATH"** 옵션을 체크합니다.
   - **Install Now**를 클릭하여 기본 설정으로 설치를 진행합니다.

3. **설치 확인**
   - **명령 프롬프트** 또는 **PowerShell**을 열고 다음 명령어를 입력합니다:
     ```bash
     python --version
     ```
     - Python 버전 정보가 출력되면 정상 설치된 것입니다.

---

## 3. VS Code 설치 및 설정

1. **VS Code 다운로드**
   - [Visual Studio Code 공식 웹사이트](https://code.visualstudio.com/)로 이동하여 운영체제에 맞는 설치 파일을 다운로드합니다.

2. **VS Code 설치**
   - 다운로드한 설치 파일을 실행하고 화면 지침에 따라 설치를 완료합니다.

3. **필수 확장 프로그램 설치**
   - **VS Code**를 열고 **Extensions** 탭 (`Ctrl+Shift+X`)으로 이동합니다.
   - 다음 확장 프로그램을 검색하여 설치합니다:
     - **Python**: Python 코드 작성 및 디버깅 지원
     - **AWS Toolkit for Visual Studio Code**: AWS 서비스와의 통합
     - **Remote - SSH** (선택 사항): 원격 서버 작업 시 유용

---

## 4. AWS 계정 생성 및 IAM 사용자 설정

### 4.1. AWS 계정 생성

1. [AWS 계정 생성 페이지](https://portal.aws.amazon.com/billing/signup)로 이동합니다.
2. 이메일 주소, 강력한 비밀번호 등을 입력하여 계정을 생성합니다.

### 4.2. IAM 사용자 생성 및 권한 설정

1. **AWS Management Console**에 로그인한 후, **IAM (Identity and Access Management)** 서비스로 이동합니다.
2. **Users** 메뉴에서 **Add user**를 클릭합니다.
3. **User name**을 입력하고 **Programmatic access**를 선택합니다.
4. **Permissions** 단계에서 **Attach existing policies directly**를 선택하고 다음 정책을 추가합니다:
   - **AmazonS3FullAccess** (필요한 경우, 최소 권한 원칙에 따라 정책을 조정할 수 있습니다)
5. **Tags** 및 **Review** 단계를 거쳐 **Create user**를 완료합니다.
6. **Access Key ID**와 **Secret Access Key**를 안전하게 저장합니다. (나중에 AWS CLI 구성 시 필요)

---

## 5. AWS CLI 설치 및 구성

### 5.1. AWS CLI 설치

#### Windows 사용자

1. [AWS CLI 설치 페이지](https://docs.aws.amazon.com/ko_kr/cli/latest/userguide/getting-started-install.html)로 이동합니다.
2. **Windows MSI Installer** (`AWSCLIV2.msi`)를 다운로드합니다.
3. 다운로드한 MSI 파일을 실행하여 설치를 완료합니다.

#### 설치 확인

1. **명령 프롬프트** 또는 **PowerShell**을 열고 다음 명령어를 입력합니다:
   ```bash
   aws --version
   ```
   - 예시 출력:
     ```
     aws-cli/2.12.0 Python/3.8.8 Windows/10 exe/AMD64 prompt/off
     ```

### 5.2. AWS CLI 구성

1. **명령 프롬프트** 또는 **PowerShell**에서 다음 명령어를 실행합니다:
   ```bash
   aws configure
   ```
2. 프롬프트에 따라 다음 정보를 입력합니다:
   - **AWS Access Key ID**: 생성한 IAM 사용자의 Access Key ID
   - **AWS Secret Access Key**: 생성한 IAM 사용자의 Secret Access Key
   - **Default region name**: 예: `ap-northeast-2` (서울)
   - **Default output format**: `json`

   ```plaintext
   AWS Access Key ID [None]: YOUR_ACCESS_KEY_ID
   AWS Secret Access Key [None]: YOUR_SECRET_ACCESS_KEY
   Default region name [None]: ap-northeast-2
   Default output format [None]: json
   ```

3. 설정 확인:
   ```bash
   aws configure list
   ```
   - 입력한 정보가 올바르게 표시되는지 확인합니다.

---

## 6. AWS S3 버킷 생성 및 설정

### 6.1. S3 버킷 생성

1. **AWS Management Console**에서 **S3** 서비스를 선택합니다.
2. **Create bucket** 버튼을 클릭합니다.
3. **Bucket name**: 고유한 버킷 이름 입력 (예: `my-news-report-bucket-unique123`)
4. **Region**: `ap-northeast-2` 등을 선택합니다.
5. **버킷 설정**:
   - **더 많은 옵션 표시**를 클릭하여 추가 설정을 확인합니다.
   - **Block all public access**: S3 버킷을 공개적으로 접근 가능하게 설정하려면 해당 옵션을 해제합니다.
6. **Create bucket**을 클릭하여 버킷을 생성합니다.

### 6.2. S3 버킷 권한 설정

1. 생성한 S3 버킷을 클릭합니다.
2. **Permissions** 탭으로 이동합니다.
3. **Bucket Policy** 섹션에서 **Edit**를 클릭하고 다음 JSON 정책을 추가합니다:
   
   ```json
   {
       "Version": "2012-10-17",
       "Statement": [
           {
               "Sid": "PublicReadGetObject",
               "Effect": "Allow",
               "Principal": "*",
               "Action": "s3:GetObject",
               "Resource": "arn:aws:s3:::my-news-report-bucket-unique123/*"
           }
       ]
   }
   ```
   
   - **주의:** `my-news-report-bucket-unique123`을 실제 버킷 이름으로 변경하세요.
4. **Save changes**를 클릭하여 정책을 저장합니다.

### 6.3. Object Ownership 설정

1. **Permissions** 탭에서 **Object Ownership** 섹션으로 이동합니다.
2. **Object Ownership**를 **Bucket owner enforced**로 설정합니다.
   - 이 설정은 ACL을 비활성화하고 모든 객체 소유권을 버킷 소유자에게 부여합니다.
3. **Save changes**를 클릭하여 설정을 저장합니다.

### 6.4. 정적 웹사이트 호스팅 설정

1. **Permissions** 탭에서 **Properties** 섹션으로 이동합니다.
2. **Static website hosting**을 클릭합니다.
3. **Enable**을 선택하고 **Index document**에 `news_report.html`을 입력합니다.
4. **Save changes**를 클릭하여 설정을 완료합니다.
5. **Static website endpoint**를 복사하여 웹사이트 URL로 사용할 수 있습니다.

---

## 7. Python 스크립트 작성 및 `boto3` 설치

### 7.1. `boto3` 라이브러리 설치

1. **명령 프롬프트** 또는 **PowerShell**에서 다음 명령어를 실행하여 `boto3`를 설치합니다:
   ```bash
   pip install boto3
   ```

### 7.2. Python 스크립트 작성

1. **VS Code**에서 새로운 Python 파일(`crawler.py`)을 생성합니다.
2. 아래의 코드를 `crawler.py`에 복사하여 붙여넣습니다.

```python
import requests
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader
import datetime
import os
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

def get_news(keyword, category='general'):
    if category == 'politics':
        url = f'https://search.naver.com/search.naver?where=news&query={keyword}&sm=tab_pge&sort=1&field=1&category=100'  # 카테고리 코드 예시
    elif category == 'economy':
        url = f'https://search.naver.com/search.naver?where=news&query={keyword}&sm=tab_pge&sort=1&field=1&category=101'  # 카테고리 코드 예시
    else:
        url = f'https://search.naver.com/search.naver?where=news&query={keyword}&sm=tab_pge&sort=1'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f'Failed to retrieve news for {keyword} in {category}')
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    articles = []

    # 네이버 뉴스의 HTML 구조에 맞게 수정 필요
    news_items = soup.select('div.news_area')  # 네이버 뉴스의 뉴스 항목 선택자
    for item in news_items:
        title = item.select_one('a.news_tit').get_text()
        link = item.select_one('a.news_tit')['href']
        summary = item.select_one('div.news_dsc').get_text() if item.select_one('div.news_dsc') else '요약 정보 없음'

        articles.append({
            'title': title,
            'link': link,
            'summary': summary
        })

    return articles

def generate_html_report(all_news, template_file='report_template.html', output_dir='reports'):
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template(template_file)
    html_content = template.render(all_news=all_news)
    
    # 현재 날짜와 시간을 기반으로 파일명 생성
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f'{timestamp}_news_report.html'
    
    # 출력 디렉토리가 존재하지 않으면 생성
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    output_path = os.path.join(output_dir, output_file)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f'{output_path}이(가) 생성되었습니다.')
    
    return output_path

def upload_to_s3(file_path, bucket_name):
    s3_client = boto3.client('s3')
    filename = os.path.basename(file_path)
    fixed_filename = 'news_report.html'  # 고정된 파일명
    
    try:
        # 1. 고유한 파일명으로 업로드
        s3_client.upload_file(
            file_path,
            bucket_name,
            filename,
            ExtraArgs={'ContentType': 'text/html'}
        )
        print(f'S3 버킷 {bucket_name}에 {filename}이(가) 업로드되었습니다.')
        
        # 2. 고정된 이름으로 업로드 (최신 보고서로 덮어쓰기)
        s3_client.upload_file(
            file_path,
            bucket_name,
            fixed_filename,
            ExtraArgs={'ContentType': 'text/html'}
        )
        print(f'S3 버킷 {bucket_name}에 {fixed_filename}이(가) 업로드되었습니다.')
        
        # S3 객체 URL 생성
        region = s3_client.get_bucket_location(Bucket=bucket_name)['LocationConstraint']
        if region is None:
            region = 'us-east-1'
        s3_url = f'https://{bucket_name}.s3-{region}.amazonaws.com/{fixed_filename}'
        print(f'접근 URL: {s3_url}')
    except FileNotFoundError:
        print(f'파일을 찾을 수 없습니다: {file_path}')
    except NoCredentialsError:
        print('AWS 자격 증명을 찾을 수 없습니다.')
    except PartialCredentialsError:
        print('부분적인 AWS 자격 증명이 제공되었습니다.')
    except Exception as e:
        print(f'파일 업로드 중 오류 발생: {e}')

if __name__ == '__main__':
    keywords = ['정치', '경제', '기술', '스포츠']
    all_news = {}

    for keyword in keywords:
        if keyword in ['정치', '경제']:
            news = get_news(keyword, category=keyword)
        else:
            news = get_news(keyword)
        all_news[keyword] = news

    # HTML 보고서 생성
    report_path = generate_html_report(all_news)

    # S3 버킷 이름 설정
    bucket_name = 'my-news-report-bucket-unique123'  # 실제 버킷 이름으로 변경

    # S3에 파일 업로드
    upload_to_s3(report_path, bucket_name)
```

### 7.3. HTML 템플릿 작성

1. **VS Code**에서 **`report_template.html`** 파일을 생성합니다.
2. 아래의 간단한 HTML 템플릿을 작성합니다. 필요에 따라 디자인을 수정할 수 있습니다.

```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>뉴스 보고서</title>
</head>
<body>
    <h1>뉴스 보고서 - {{ all_news.keys() | list | join(', ') }}</h1>
    {% for category, articles in all_news.items() %}
        <h2>{{ category }}</h2>
        <ul>
            {% for article in articles %}
                <li>
                    <a href="{{ article.link }}" target="_blank">{{ article.title }}</a><br>
                    {{ article.summary }}
                </li>
            {% endfor %}
        </ul>
    {% endfor %}
</body>
</html>
```

---

## 8. Python 스크립트 실행 및 S3 업로드

### 8.1. Python 스크립트 실행

1. **VS Code**에서 열려 있는 프로젝트 폴더 내에서 **터미널**을 엽니다 (`Ctrl + `).
2. 다음 명령어를 입력하여 스크립트를 실행합니다:
   ```bash
   python crawler.py
   ```
3. 스크립트 실행 결과:
   - `reports/` 디렉토리에 **날짜-시간이 포함된 HTML 파일**이 생성됩니다.
   - 동일한 보고서가 **고정된 이름**(`news_report.html`)으로 S3 버킷에 업로드됩니다.
   - 고정된 URL을 통해 최신 보고서를 접근할 수 있습니다.

### 8.2. 웹사이트 확인

1. 웹 브라우저에서 다음 URL을 열어 보고서가 제대로 표시되는지 확인합니다:
   ```
   https://my-news-report-bucket-unique123.s3.ap-northeast-2.amazonaws.com/news_report.html
   ```
2. 최신 보고서가 정상적으로 렌더링되는지 확인합니다.

---

## 9. S3 버킷 Lifecycle 정책 설정

### 9.1. Lifecycle 규칙 설정하기

1. **AWS Management Console**에서 **S3** 서비스를 선택합니다.
2. 해당 버킷(`my-news-report-bucket-unique123`)을 클릭합니다.
3. 상단의 **관리** 탭을 선택한 후, **Lifecycle 규칙** 섹션으로 이동합니다.
4. **Add lifecycle rule** 버튼을 클릭합니다.
5. **Rule name**: `DeleteOldReports` 등 의미 있는 이름 입력
6. **Scope 지정**:
   - **이 규칙을 모든 객체에 적용**할지 특정 접두사에만 적용할지를 선택합니다.
   - 예를 들어, `reports/` 폴더에만 적용하려면 **Limit the scope of this rule using one or more filters**을 선택하고 **Prefix**에 `reports/`를 입력합니다.
7. **Lifecycle rule actions** 설정:
   - **Expiration** 섹션에서 **현재 날짜로부터 **30**일 후에 객체 삭제**를 선택합니다.
8. **Review**를 클릭하고, 설정을 확인한 후 **Create rule**을 클릭하여 규칙을 생성합니다.

### 9.2. Lifecycle 정책 JSON 예시

만약 JSON으로 설정하려면 다음과 같은 형식을 사용할 수 있습니다:

```json
{
    "Rules": [
        {
            "ID": "DeleteOldReports",
            "Prefix": "reports/",
            "Status": "Enabled",
            "Expiration": {
                "Days": 30
            }
        }
    ]
}
```

1. **Lifecycle 규칙** 편집 화면에서 **JSON** 탭을 선택합니다.
2. 위의 JSON을 복사하여 붙여넣고 **Save**를 클릭합니다.

---

## 10. IAM 권한 최소화 및 보안 설정

### 10.1. 최소 권한 원칙 적용

가능한 최소한의 권한만을 IAM 사용자에게 부여하여 보안을 강화합니다.

#### 최소 권한 정책 예시

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject"
            ],
            "Resource": "arn:aws:s3:::my-news-report-bucket-unique123/*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetBucketLocation"
            ],
            "Resource": "arn:aws:s3:::my-news-report-bucket-unique123"
        }
    ]
}
```

1. **IAM 관리 콘솔**로 이동합니다.
2. 해당 사용자를 선택하거나 **New user**를 생성합니다.
3. **Permissions**에서 **Attach existing policies directly**을 선택하고, **Create policy**를 클릭합니다.
4. **JSON** 탭에서 위의 정책을 붙여넣습니다.
5. **Review policy**를 클릭하고, 정책 이름을 지정한 후 **Create policy**를 클릭합니다.
6. 생성한 정책을 사용자에게 할당합니다.

### 10.2. 자격 증명 안전하게 관리

- **환경 변수 사용**: 자격 증명을 코드에 하드코딩하지 않고 환경 변수나 AWS CLI 설정 파일을 통해 관리합니다.
- **`.gitignore` 설정**: 자격 증명 파일이나 민감한 정보를 포함한 파일을 Git 버전 관리에서 제외합니다.

   `.gitignore` 파일에 다음을 추가합니다:
   ```
   .env
   credentials
   ```

---

## 11. 비용 모니터링 및 관리

### 11.1. AWS Cost Explorer 사용

1. **AWS Management Console**에서 **Billing** 대시보드로 이동합니다.
2. **Cost Explorer**를 활성화합니다.
3. **Cost Explorer**에서 **Usage Reports**를 설정하여 S3 사용량과 비용을 추적합니다.
4. **필터링**을 통해 S3 관련 비용을 확인하고, 추세를 모니터링합니다.

### 11.2. S3 Storage Metrics 확인

1. **AWS Management Console**에서 **S3** 서비스를 선택합니다.
2. 해당 버킷을 선택하고, **Metrics** 탭으로 이동합니다.
3. **Storage Metrics**를 확인하여 스토리지 사용량을 모니터링합니다.
4. 필요한 경우 **CloudWatch**와 연동하여 알림을 설정할 수 있습니다.

### 11.3. 추가 비용 절감 방안

- **더 저렴한 스토리지 클래스 사용**: 필요에 따라 객체를 더 저렴한 스토리지 클래스로 전환할 수 있습니다. 예를 들어, Standard-IA 또는 Glacier 클래스로 전환하여 비용을 절감할 수 있습니다.
- **객체 압축**: HTML 파일이 큰 경우, Gzip 등의 압축 방식을 사용하여 파일 크기를 줄일 수 있습니다.

---

## 12. 자동화 및 스케줄링 설정 (선택 사항)

정기적으로 스크립트를 실행하여 최신 보고서를 자동으로 생성하고 업로드하려면 스케줄링을 설정할 수 있습니다.

### 12.1. Windows 작업 스케줄러 설정

1. **작업 스케줄러**를 엽니다:
   - **시작 메뉴**에서 "작업 스케줄러"를 검색하여 실행합니다.
2. **작업 만들기**를 클릭합니다.
3. **일반 탭**:
   - **이름**: `뉴스 보고서 업로드`
4. **트리거 탭**:
   - **새로 만들기**를 클릭하고, 실행 주기를 설정합니다 (예: 매일 오전 9시).
5. **동작 탭**:
   - **새로 만들기**를 클릭하고, 다음을 입력합니다:
     - **프로그램/스크립트**: `python`
     - **인수 추가**: `C:\path\to\your\crawler.py` (스크립트 경로로 변경)
6. **조건 및 설정 탭**에서 필요한 추가 설정을 구성합니다.
7. **확인**을 클릭하여 작업을 생성합니다.

### 12.2. Linux/macOS에서 크론 작업 설정

1. 터미널을 엽니다.
2. 크론 편집기를 엽니다:
   ```bash
   crontab -e
   ```
3. 다음 라인을 추가하여 매일 오전 9시에 스크립트를 실행하도록 설정합니다:
   ```plaintext
   0 9 * * * /usr/bin/python3 /path/to/your/crawler.py
   ```
4. **저장** 후 종료합니다.

---

## 13. 최종 확인 및 테스트

### 13.1. Python 스크립트 실행

1. **VS Code**에서 `crawler.py` 파일이 열려 있는지 확인합니다.
2. **터미널**을 열고 다음 명령어를 실행합니다:
   ```bash
   python crawler.py
   ```
3. 스크립트 출력 확인:
   ```plaintext
   reports\20250208_111442_news_report.html이(가) 생성되었습니다.
   S3 버킷 my-news-report-bucket-unique123에 20250208_111442_news_report.html이(가) 업로드되었습니다.
   S3 버킷 my-news-report-bucket-unique123에 news_report.html이(가) 업로드되었습니다.
   접근 URL: https://my-news-report-bucket-unique123.s3.ap-northeast-2.amazonaws.com/news_report.html
   ```

### 13.2. 웹사이트 테스트

1. 웹 브라우저에서 **접근 URL**을 열어 최신 뉴스 보고서가 정상적으로 표시되는지 확인합니다.
2. `news_report.html`를 항상 최신 파일로 보여주는지 확인합니다.

### 13.3. Lifecycle 정책 동작 확인

1. **reports/** 폴더 내의 오래된 파일이 자동으로 삭제되는지 확인합니다.
2. 설정한 일수(예: 30일) 이후에 파일이 삭제되는지 모니터링합니다.

---

## 14. 문제 해결

### 14.1. AWS CLI 인식 안 됨 (`aws : 'aws' 용어가 cmdlet ...`)

- **원인**: AWS CLI가 설치되지 않았거나 PATH 환경 변수에 추가되지 않음
- **해결 방법**:
  1. AWS CLI가 설치되었는지 확인합니다:
     ```bash
     aws --version
     ```
  2. 설치되지 않았다면 [AWS CLI 설치](#5-aws-cli-설치-및-구성) 단계를 따라 설치합니다.
  3. 설치 후 **명령 프롬프트** 또는 **PowerShell**을 재시작합니다.

### 14.2. S3 업로드 시 `AccessControlListNotSupported` 오류 발생

- **원인**: S3 버킷이 ACL 사용을 허용하지 않음 (`Bucket owner enforced` 설정)
- **해결 방법**:
  1. Python 스크립트에서 `ExtraArgs={'ACL': 'public-read'}`를 제거합니다.
  2. S3 버킷 정책을 통해 공개 읽기 권한을 설정했는지 확인합니다.
  3. `Content-Type`을 `text/html`로 설정하여 브라우저가 HTML 파일을 올바르게 렌더링하도록 합니다.

### 14.3. `news_report.html`이 다운로드되고 렌더링되지 않음

- **원인**: `Content-Type`이 올바르게 설정되지 않음
- **해결 방법**:
  1. Python 스크립트에서 `ExtraArgs={'ContentType': 'text/html'}`을 설정했는지 확인합니다.
  2. S3 콘솔에서 업로드된 객체의 메타데이터를 확인하여 `Content-Type`이 `text/html`로 설정되어 있는지 확인합니다.
  3. 필요시, 스크립트를 다시 실행하여 파일을 재업로드합니다.

### 14.4. S3 버킷 비용이 과도하게 증가함

- **원인**: 고유한 파일명이 계속해서 업로드되어 버킷 내 객체 수가 증가
- **해결 방법**:
  1. Python 스크립트를 수정하여 고유한 파일명으로 업로드하지 않고, 고정된 이름으로만 업로드하도록 변경합니다.
  2. Lifecycle 정책을 설정하여 일정 기간 이후 객체를 자동으로 삭제하도록 설정합니다.

---

## 결론

이 매뉴얼을 따라 Python 기반의 뉴스 크롤러를 구축하고, AWS S3를 통해 자동으로 결과를 생성 및 호스팅하는 과정을 완료하셨습니다. 이를 통해 최신 뉴스 보고서를 익주일마다 자동으로 생성하고, 웹사이트를 통해 쉽게 접근할 수 있습니다. 추가적으로, 비용 관리를 위해 S3 Lifecycle 정책과 IAM 권한을 적절히 설정하였습니다.

추가적인 도움이 필요하시거나 다른 질문이 있으시면 언제든지 문의해 주세요. 성공적인 프로젝트 진행을 기원합니다!
