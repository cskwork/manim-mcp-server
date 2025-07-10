#!/bin/bash
# Manim MCP Server를 OpenAPI Proxy로 실행하는 스크립트

# 스크립트 디렉터리 설정
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 가상환경 활성화
source venv/bin/activate

# 환경 변수 설정
export MANIM_EXECUTABLE="manim"
export MCP_PROJECT_ROOT="$SCRIPT_DIR"

# OpenAPI proxy 서버 실행
echo "🚀 Manim MCP Server를 OpenAPI Proxy로 실행 중..."
echo "🌐 서버 주소: http://localhost:8005"
echo "📋 OpenAPI 스키마: http://localhost:8005/openapi.json"
echo "🩺 헬스 체크: http://localhost:8005/health"
echo ""

# mcpo를 사용하여 OpenAPI proxy 서버 실행
mcpo \
  --host 0.0.0.0 \
  --port 8005 \
  --cors-allow-origins "*" \
  -- python src/manim_server.py
