FROM python:3.11-slim AS builder

# --- 网络兼容性修复 ---
RUN echo "precedence ::ffff:0:0/96 100" >> /etc/gai.conf

RUN apt-get update && apt-get install -y --no-install-recommends \
curl gcc libssl-dev pkg-config \
&& rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

# 使用官方 PyPI（更稳定）
ENV PIP_INDEX_URL="https://pypi.org/simple"

RUN uv --version

WORKDIR /app
COPY pyproject.toml uv.lock ./

# 创建虚拟环境
RUN uv venv /app/venv

# 设置国内 PyPI 源（可选）
ENV UV_PYPI_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple

# 在虚拟环境中安装依赖
RUN uv pip install -p /app/venv .

FROM python:3.11-slim
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser
ENV PATH="/app/venv/bin:${PATH}" PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
WORKDIR /app
COPY --from=builder /app/venv /app/venv
COPY . .
USER appuser
EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]