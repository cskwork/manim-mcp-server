# Manim MCP Server OpenAPI Proxy Dockerfile

FROM python:3.11-slim

# 시스템 패키지 업데이트 및 필요한 의존성 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    libcairo2-dev \
    libpango1.0-dev \
    libgdk-pixbuf2.0-dev \
    libffi-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# 작업 디렉터리 설정
WORKDIR /app

# Python 의존성 파일 복사
COPY requirements.txt .

# mcpo 설치를 위한 추가 의존성 설치
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir mcpo

# 소스 코드 복사
COPY src/ ./src/

# 환경 변수 설정
ENV MANIM_EXECUTABLE=manim
ENV MCP_PROJECT_ROOT=/app
ENV PYTHONPATH=/app

# 포트 노출
EXPOSE 8005

# 볼륨 마운트 포인트
VOLUME ["/app/media"]

# 헬스 체크
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8005/health || exit 1

# OpenAPI proxy 서버 실행
CMD ["mcpo", "--host", "0.0.0.0", "--port", "8005", "--cors-allow-origins", "*", "--", "python", "src/manim_server.py"]