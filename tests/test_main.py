import pytest
from fastapi.testclient import TestClient
from app.main import app, DATA_DIR

client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_data_dir():
    """每个测试前清理数据目录"""
    # 清理已有文件
    for f in DATA_DIR.glob("*"):
        if f.is_file():
            f.unlink()
    yield
    # 测试后再次清理
    for f in DATA_DIR.glob("*"):
        if f.is_file():
            f.unlink()


def test_read_root():
    """测试根路径返回正确的消息"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "FastAPI with uv running successfully!"}


def test_create_file():
    """测试创建文件接口"""
    response = client.post("/create-file?filename=test.txt&content=hello%20world")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "test.txt" in data["file_path"]

    # 验证文件确实被创建
    file_path = DATA_DIR / "test.txt"
    assert file_path.exists()
    assert file_path.read_text() == "hello world"


def test_list_files_empty():
    """测试空目录时列出文件返回空列表"""
    response = client.get("/list-files")
    assert response.status_code == 200
    assert response.json() == {"files": []}


def test_list_files_with_content():
    """测试创建文件后正确列出文件"""
    # 创建两个文件
    client.post("/create-file?filename=file1.txt&content=content1")
    client.post("/create-file?filename=file2.txt&content=content2")

    response = client.get("/list-files")
    assert response.status_code == 200
    data = response.json()
    assert len(data["files"]) == 2
    assert "file1.txt" in data["files"]
    assert "file2.txt" in data["files"]


def test_create_file_overwrite():
    """测试重复创建同名文件会覆盖"""
    # 创建文件
    client.post("/create-file?filename=overwrite.txt&content=old")
    # 覆盖文件
    client.post("/create-file?filename=overwrite.txt&content=new")

    file_path = DATA_DIR / "overwrite.txt"
    assert file_path.read_text() == "new"
