import platform
import os

def configure_local_environment():
    print("Gesturify Local Environment Setup")
    print("-" * 30)
    
    os_name = platform.system().lower()
    arch = platform.machine().lower()

    print(f"> Detected OS: {os_name.capitalize()}")
    print(f"> Detected Architecture: {arch}")

    # --- THE PRODUCTION BASELINE ---
    tf_package = "tensorflow-cpu"
    cv2_package = "opencv-python-headless"
    tool_override = ""

    # --- APPLY LOCAL HARDWARE TWEAKS ---
    if os_name == "windows":
        print("\\ Configuring for Windows Local Dev...")
        tf_package = "tensorflow-intel"
        cv2_package = "opencv-python" # Needs UI for webcam testing
        tool_override = """
[tool.uv]
override-dependencies = [
    "tensorflow-io-gcs-filesystem==0.31.0"
]"""

    elif os_name == "darwin": 
        cv2_package = "opencv-python"
        if arch == "arm64":
            print("\\ Configuring for Mac (Apple Silicon) Local Dev...")
            tf_package = "tensorflow-macos"
        else:
            print("\\ Configuring for Mac (Intel) Local Dev...")
            tf_package = "tensorflow"

    elif os_name == "linux":
        print("\\ Configuring for Linux Local Dev...")
        tf_package = "tensorflow"
        cv2_package = "opencv-python"
        
    else:
        print("XX Unknown OS, keeping server defaults...")

    # --- BUILD THE FILE ---
    base_toml = f"""[project]
name = "gesturify"
version = "0.1.0"
description = "AI Sign Language Recognition App"
readme = "README.md"
requires-python = ">=3.10,<3.11"
dependencies = [
    "fastapi==0.135.2",
    "uvicorn==0.42.0",
    "websockets==16.0",
    "python-multipart==0.0.22",
    "keras==2.12.0",
    "mediapipe==0.10.5",
    "numpy==1.23.5",
    "{cv2_package}==4.7.0.72",
    "pandas==1.5.3",
    "protobuf==3.20.3",
    "{tf_package}==2.12.0",
]
"""
    final_toml = base_toml + tool_override

    # Prevent cache conflicts by clearing the lockfile
    if os.path.exists("uv.lock"):
        os.remove("uv.lock")
        print("\\ Cleared old uv.lock file.")

    with open("pyproject.toml", "w") as f:
        f.write(final_toml)

    print("-" * 30)
    print("< Successfully configured pyproject.toml for local development!")
    print("< Next step: Run 'uv sync' in your terminal.")

if __name__ == "__main__":
    configure_local_environment()