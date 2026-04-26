# Portfolio

백엔드 개발자 개인 포트폴리오 사이트입니다.

## 빠른 시작

```bash
# 빌드 & 실행
docker compose up -d

# 브라우저에서 열기
open http://localhost:3000
```

## 내용 수정

`index.html` 파일에서 아래 placeholder를 찾아 교체하세요:

| Placeholder         | 설명               |
|---------------------|--------------------|
| `YOUR_NAME`         | 이름               |
| `your@email.com`    | 이메일             |
| `YOUR_GITHUB`       | GitHub 아이디      |
| `YOUR_LINKEDIN`     | LinkedIn 아이디    |
| `Company Name`      | 회사명             |
| `20XX`              | 연도               |
| `Project Name`      | 프로젝트명         |

## 명령어

```bash
docker compose up -d        # 백그라운드 실행
docker compose down         # 중지
docker compose up --build   # 수정 후 재빌드
docker compose logs -f      # 로그 확인
```

## 구조

```
portfolio/
├── index.html          # 포트폴리오 단일 페이지
├── nginx.conf          # Nginx 설정
├── Dockerfile          # Docker 이미지 빌드
├── docker-compose.yml  # 서비스 실행 설정
└── README.md
```
