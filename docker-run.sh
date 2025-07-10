#!/bin/bash
# Docker를 사용하여 Manim MCP OpenAPI Proxy 서버 실행

echo "🐳 Docker를 사용하여 Manim MCP OpenAPI Proxy 서버 빌드 및 실행..."

# Docker Compose를 사용하여 서비스 실행
docker-compose up --build -d

echo "✅ 서버가 성공적으로 시작되었습니다!"
echo "🌐 서버 주소: http://localhost:8005"
echo "📋 OpenAPI 스키마: http://localhost:8005/openapi.json"
echo "🩺 헬스 체크: http://localhost:8005/health"
echo ""
echo "📊 로그 확인: docker-compose logs -f"
echo "🛑 서버 중지: docker-compose down"