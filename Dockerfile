# ============================================================================
# 奇玥验证引擎 - 多阶段构建（镜像瘦身 + 依赖层缓存）
# 阶段1: 依赖锁定层（可复用缓存，减少 CI 时间）
# 阶段2: 运行层（仅含运行时产物）
# ============================================================================
FROM python:3.14.6-slim AS deps

WORKDIR /app

# 复制依赖锁定文件（利用 Docker 层缓存）
COPY requirements.txt /app/requirements.txt

# 锁定核心依赖版本（与 requirements.txt 一致）
RUN pip install --no-cache-dir -r /app/requirements.txt

# 复制实验代码与数据
COPY . /app

# ============================================================================
# 运行阶段
# ============================================================================
FROM python:3.14.6-slim AS runtime

WORKDIR /app

# 设置全局随机种子（用于复现实验，构建期可覆盖）
ARG SEED=0x612
ENV SEED=${SEED}

# 从依赖层复制已安装包，避免重复安装
COPY --from=deps /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=deps /usr/local/bin /usr/local/bin

# 复制实验代码（不含数据包，数据按需挂载，避免镜像膨胀）
COPY run_all.py /app/run_all.py 2>/dev/null || true
COPY configs/ /app/configs/ 2>/dev/null || true
COPY docs/ /app/docs/ 2>/dev/null || true
COPY data/ /app/data/ 2>/dev/null || true

# 非 root 运行（纵深防御）
RUN useradd --create-home --shell /bin/bash imager && \
    chown -R imager:imager /app
USER imager

CMD ["python", "run_all.py"]
