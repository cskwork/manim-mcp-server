# Manim MCP OpenAPI Proxy

Manim MCP Server를 OpenAPI 호환 REST API로 변환하여 사용할 수 있는 프록시 서버입니다.

## 🚀 빠른 시작

### 1. 개발 환경 실행

```bash
# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
pip install mcpo

# 개발 서버 실행
./run_openapi_proxy.sh
```

### 2. 프로덕션 환경 실행

```bash
# 프로덕션 모드로 실행
./run_openapi_proxy_prod.sh
```

### 3. Docker 환경 실행

```bash
# Docker Compose를 사용한 실행
./docker-run.sh

# 또는 직접 실행
docker-compose up --build -d
```

## 🌐 API 엔드포인트

서버 실행 후 다음 URL에서 API를 사용할 수 있습니다:

- **서버 주소**: http://localhost:8005
- **OpenAPI 스키마**: http://localhost:8005/openapi.json
- **헬스 체크**: http://localhost:8005/health
- **API 문서**: http://localhost:8005/docs (자동 생성)

## 🔧 사용 가능한 API

### 1. Manim 코드 실행

```http
POST /execute_manim_code
Content-Type: application/json

{
  "manim_code": "from manim import *\n\nclass TestScene(Scene):\n    def construct(self):\n        text = Text('Hello, World!')\n        self.play(Write(text))\n        self.wait()"
}
```

### 2. 임시 디렉터리 정리

```http
POST /cleanup_manim_temp_dir
Content-Type: application/json

{
  "directory": "/path/to/temp/directory"
}
```

## 📋 테스트 실행

```bash
# 서버 시작 후 별도 터미널에서 테스트 실행
./run_tests.sh

# 또는 Python으로 직접 실행
python test_openapi_proxy.py
```

## 🛠️ 구성 옵션

### 환경 변수

- `MANIM_EXECUTABLE`: Manim 실행 파일 경로 (기본값: "manim")
- `MCP_PROJECT_ROOT`: 프로젝트 루트 디렉터리
- `MCPO_API_KEY`: API 키 (선택사항)

### 포트 변경

스크립트 파일에서 `--port 8005`를 원하는 포트로 변경하세요.

## 📁 생성된 파일

### 실행 스크립트
- `run_openapi_proxy.sh` - 개발용 실행 스크립트 (Linux/Mac)
- `run_openapi_proxy_prod.sh` - 프로덕션용 실행 스크립트 (Linux/Mac)
- `run_openapi_proxy.bat` - Windows용 실행 스크립트

### Docker 설정
- `Dockerfile` - Docker 이미지 빌드 설정
- `docker-compose.yml` - Docker Compose 설정
- `docker-run.sh` - Docker 실행 스크립트

### 테스트 파일
- `test_openapi_proxy.py` - API 테스트 스크립트
- `run_tests.sh` - 테스트 실행 스크립트

## 🔗 Open WebUI 통합

Open WebUI와 통합하려면:

1. OpenAPI proxy 서버 실행
2. Open WebUI 설정에서 다음 URL 추가:
   - OpenAPI URL: `http://localhost:8005/openapi.json`

## 🐛 문제 해결

### 서버 시작 오류
```bash
# 포트 충돌 확인
lsof -i :8005

# 프로세스 종료
kill -9 <PID>
```

### 의존성 문제
```bash
# 가상환경 재생성
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install mcpo
```

### Docker 문제
```bash
# 컨테이너 정리
docker-compose down
docker system prune -f

# 이미지 재빌드
docker-compose build --no-cache
```

## 📊 성능 최적화

### 프로덕션 설정
- `--workers 4`: 워커 프로세스 수 조정
- `--log-level WARNING`: 로그 레벨 조정
- `--reload` 제거: 자동 리로드 비활성화

### 리소스 제한
```yaml
# docker-compose.yml에 추가
deploy:
  resources:
    limits:
      cpus: '2'
      memory: 4G
```

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 🤝 기여

1. 이 저장소를 포크하세요
2. 새로운 기능 브랜치를 생성하세요
3. 변경사항을 커밋하세요
4. 브랜치에 푸시하세요
5. Pull Request를 생성하세요

## 📞 지원

문제가 발생하거나 질문이 있으시면 GitHub Issues에 문의해주세요.

---

**다음 단계**: 
1. 서버 실행 및 테스트 진행
2. Open WebUI 통합 테스트
3. 추가 기능 구현 (인증, 로깅, 모니터링 등)
4. 성능 최적화 및 스케일링