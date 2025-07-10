@echo off
REM Manim MCP Server를 OpenAPI Proxy로 실행하는 스크립트 (Windows용)

REM 현재 디렉터리 설정
cd /d "%~dp0"

REM 가상환경 활성화
call venv\Scripts\activate

REM 환경 변수 설정
set MANIM_EXECUTABLE=manim
set MCP_PROJECT_ROOT=%~dp0

REM OpenAPI proxy 서버 실행
echo 🚀 Manim MCP Server를 OpenAPI Proxy로 실행 중...
echo 🌐 서버 주소: http://localhost:8005
echo 📋 OpenAPI 스키마: http://localhost:8005/openapi.json
echo 🩺 헬스 체크: http://localhost:8005/health
echo.

REM mcpo를 사용하여 OpenAPI proxy 서버 실행
mcpo --host 0.0.0.0 --port 8005 --cors-allow-origins "*" -- python src/manim_server.py

pause