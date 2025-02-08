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