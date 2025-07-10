#!/bin/bash
# OpenAPI Proxy 테스트 실행 스크립트

# 스크립트 디렉터리 설정
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 가상환경 활성화
source venv/bin/activate

# requests 라이브러리 설치 (테스트에 필요)
pip install requests

echo "🧪 Manim MCP OpenAPI Proxy 테스트 실행"
echo "=" * 50

# 테스트 실행
python test_openapi_proxy.py