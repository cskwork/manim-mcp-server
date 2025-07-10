#!/usr/bin/env python3
"""
Manim MCP OpenAPI Proxy 테스트 스크립트
"""

import requests
import json
import time
import sys
from typing import Dict, Any

# 서버 설정
SERVER_URL = "http://localhost:8005"
TEST_TIMEOUT = 30

def test_health_check():
    """헬스 체크 테스트"""
    print("🩺 헬스 체크 테스트...")
    try:
        response = requests.get(f"{SERVER_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ 헬스 체크 통과")
            return True
        else:
            print(f"❌ 헬스 체크 실패: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 헬스 체크 에러: {e}")
        return False

def test_openapi_schema():
    """OpenAPI 스키마 테스트"""
    print("📋 OpenAPI 스키마 테스트...")
    try:
        response = requests.get(f"{SERVER_URL}/openapi.json", timeout=10)
        if response.status_code == 200:
            schema = response.json()
            print("✅ OpenAPI 스키마 로드 성공")
            print(f"📊 서버 제목: {schema.get('info', {}).get('title', 'Unknown')}")
            print(f"📊 서버 버전: {schema.get('info', {}).get('version', 'Unknown')}")
            
            # 사용 가능한 엔드포인트 출력
            paths = schema.get('paths', {})
            print(f"📊 사용 가능한 엔드포인트: {len(paths)}개")
            for path in paths.keys():
                print(f"  - {path}")
            
            return True
        else:
            print(f"❌ OpenAPI 스키마 로드 실패: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ OpenAPI 스키마 에러: {e}")
        return False

def test_execute_manim_code():
    """Manim 코드 실행 테스트"""
    print("🎬 Manim 코드 실행 테스트...")
    
    # 간단한 Manim 테스트 코드
    test_code = '''
from manim import *

class TestScene(Scene):
    def construct(self):
        text = Text("Hello, MCP OpenAPI!")
        self.play(Write(text))
        self.wait()
'''
    
    try:
        response = requests.post(
            f"{SERVER_URL}/execute_manim_code",
            json={"manim_code": test_code},
            timeout=TEST_TIMEOUT
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Manim 코드 실행 성공")
            print(f"📊 결과: {result}")
            return True
        else:
            print(f"❌ Manim 코드 실행 실패: {response.status_code}")
            print(f"📊 에러 내용: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Manim 코드 실행 에러: {e}")
        return False

def test_cleanup_temp_dir():
    """임시 디렉터리 정리 테스트"""
    print("🧹 임시 디렉터리 정리 테스트...")
    
    test_dir = "/tmp/test_manim_cleanup"
    
    try:
        response = requests.post(
            f"{SERVER_URL}/cleanup_manim_temp_dir",
            json={"directory": test_dir},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 임시 디렉터리 정리 테스트 성공")
            print(f"📊 결과: {result}")
            return True
        else:
            print(f"❌ 임시 디렉터리 정리 실패: {response.status_code}")
            print(f"📊 에러 내용: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 임시 디렉터리 정리 에러: {e}")
        return False

def wait_for_server():
    """서버 시작 대기"""
    print("⏳ 서버 시작 대기 중...")
    for i in range(30):
        try:
            response = requests.get(f"{SERVER_URL}/health", timeout=2)
            if response.status_code == 200:
                print("✅ 서버 준비 완료")
                return True
        except:
            pass
        time.sleep(1)
        print(f"  대기 중... ({i+1}/30)")
    
    print("❌ 서버 시작 대기 시간 초과")
    return False

def main():
    """메인 테스트 함수"""
    print("🚀 Manim MCP OpenAPI Proxy 테스트 시작")
    print("=" * 50)
    
    # 서버 시작 대기
    if not wait_for_server():
        print("❌ 서버가 시작되지 않아 테스트를 중단합니다.")
        sys.exit(1)
    
    # 테스트 실행
    tests = [
        ("헬스 체크", test_health_check),
        ("OpenAPI 스키마", test_openapi_schema),
        ("Manim 코드 실행", test_execute_manim_code),
        ("임시 디렉터리 정리", test_cleanup_temp_dir)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name} 테스트 실행...")
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ {test_name} 테스트 예외 발생: {e}")
            failed += 1
    
    # 결과 출력
    print("\n" + "=" * 50)
    print(f"📊 테스트 결과: {passed}개 통과, {failed}개 실패")
    
    if failed == 0:
        print("🎉 모든 테스트가 성공했습니다!")
        sys.exit(0)
    else:
        print(f"❌ {failed}개의 테스트가 실패했습니다.")
        sys.exit(1)

if __name__ == "__main__":
    main()