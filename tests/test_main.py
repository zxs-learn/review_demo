import pytest

from app.main import app, DATA_DIR

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


