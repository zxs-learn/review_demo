from fastapi import FastAPI
import os
from pathlib import Path

app = FastAPI(title="FastAPI + uv Demo")

# 数据存储路径（容器内路径，会映射到宿主机）
try:
    DATA_DIR = Path("/app/data")
    DATA_DIR.mkdir(exist_ok=True)  # 确保目录存在
except FileNotFoundError:
    DATA_DIR = Path(os.getcwd()) / "data"
    DATA_DIR.mkdir(exist_ok=True)  # 确保目录存在

@app.get("/")
def read_root():
    return {"message": "FastAPI with uv running successfully!"}

@app.post("/create-file")
def create_file(filename: str, content: str):
    """创建文件并保存到数据目录（测试持久化）"""
    file_path = DATA_DIR / filename
    with open(file_path, "w") as f:
        f.write(content)
    return {"status": "success", "file_path": str(file_path)}

@app.get("/list-files")
def list_files():
    """列出数据目录中的文件"""
    files = [f.name for f in DATA_DIR.glob("*") if f.is_file()]
    return {"files": files}