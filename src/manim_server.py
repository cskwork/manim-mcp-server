from fastapi.responses import FileResponse
from fastapi import FastAPI
import subprocess
import os
import shutil
import base64
import glob
from mcp.server.fastmcp import FastMCP

# FastAPI 앱 (HTTP 모드용)
app = FastAPI(
    title="Manim MCP Server",
    description="A server to render Manim scenes.",
    version="1.0.0",
)

# MCP 서버 (stdio 모드용) - FastMCP 사용
mcp = FastMCP(
    name="Manim MCP Server",
    instructions="A server to render Manim scenes and return generated videos.",
    app=app  # FastAPI 앱을 MCP 서버에 연결
)

# Get Manim executable path from environment variables or assume it's in the system PATH
MANIM_EXECUTABLE = os.getenv("MANIM_EXECUTABLE", "manim")

PROJECT_ROOT = os.getenv("MCP_PROJECT_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE_DIR = os.path.join(PROJECT_ROOT, "media")
os.makedirs(BASE_DIR, exist_ok=True)  # Ensure the media folder exists
VIDEOS_DIR = os.path.join(BASE_DIR, "videos")
os.makedirs(VIDEOS_DIR, exist_ok=True) # Ensure the videos folder exists

# Add a health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for Docker and load balancers"""
    return {"status": "healthy", "service": "manim-mcp-server", "version": "1.0.0"}

# Add a new endpoint to serve videos
@app.get("/videos/{video_name}")
async def get_video(video_name: str):
    video_path = os.path.join(VIDEOS_DIR, video_name)
    if os.path.exists(video_path):
        return FileResponse(video_path)
    return {"error": "File not found"}

@mcp.tool()
def health_check() -> dict:
    """
    Health check endpoint for monitoring server status.
    Returns server health status and basic information.
    """
    return {
        "status": "healthy",
        "service": "manim-mcp-server",
        "version": "1.0.0",
        "timestamp": os.environ.get("HOSTNAME", "unknown")
    }

@mcp.tool()
def execute_manim_code(manim_code: str) -> dict:
    """
    Execute the Manim code and returns the generated video.
    Returns a dictionary with HTML video tag containing base64 encoded video data.
    """
    tmpdir = os.path.join(BASE_DIR, "manim_tmp")
    # Clean up previous temp directory if it exists
    if os.path.exists(tmpdir):
        shutil.rmtree(tmpdir)
    os.makedirs(tmpdir, exist_ok=True)
    script_path = os.path.join(tmpdir, "scene.py")
    
    try:
        with open(script_path, "w") as script_file:
            script_file.write(manim_code)
        
        # Execute Manim with the correct path
        result = subprocess.run(
            [MANIM_EXECUTABLE, "-p", "-ql", script_path], # Using -ql for lower quality and faster rendering
            capture_output=True,
            text=True,
            cwd=tmpdir
        )

        if result.returncode == 0:
            video_files = glob.glob(os.path.join(tmpdir, '**', '*.mp4'), recursive=True)
            
            if video_files:
                video_path = video_files[0]
                video_filename = os.path.basename(video_path)
                
                # Move the video to the public videos directory
                final_video_path = os.path.join(VIDEOS_DIR, video_filename)
                shutil.move(video_path, final_video_path)
                
                # Read video file and encode as base64
                with open(final_video_path, "rb") as video_file:
                    video_data = video_file.read()
                    video_base64 = base64.b64encode(video_data).decode('utf-8')
                
                # Create HTML video tag with data URI
                video_html = f'<video controls><source src="data:video/mp4;base64,{video_base64}"></video>'
                
                # Clean up the temp directory
                shutil.rmtree(tmpdir)

                return {
                    "message": "Execution successful. Video generated.",
                    "video_filename": video_filename,
                    "video_html": video_html,
                    "mime_type": "video/mp4",
                    "size_bytes": len(video_data)
                }
            else:
                # This case might happen if the scene has no animations.
                return {"message": "Execution successful, but no video file was found.", "stderr": result.stderr, "stdout": result.stdout}
        else:
            return {"message": f"Execution failed: {result.stderr}", "stdout": result.stdout}

    except Exception as e:
        return {"message": f"Error during execution: {str(e)}"}
    finally:
        # Ensure cleanup happens even if there are errors
        if os.path.exists(tmpdir):
            shutil.rmtree(tmpdir)


if __name__ == "__main__":
    # mcpo 환경에서 실행될 때는 stdio 전송을 시작해야 함
    # mcpo가 subprocess로 이 스크립트를 실행하고 stdio 통신을 기대함
    import sys
    if len(sys.argv) > 1 and '--standalone' in sys.argv:
        # 독립 실행 모드
        mcp.run()
    else:
        # mcpo 환경에서 기본적으로 stdio 전송 시작
        mcp.run()