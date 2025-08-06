FROM nvcr.io/nvidia/pytorch:25.02-py3

# 基础工具
RUN apt-get update && apt-get install -y git curl

# Python packages（按用途整理模块）
RUN pip install --upgrade pip setuptools wheel && \
    pip install \
    # 通用工具
    requests==2.32.3 \
    pandas==2.2.3 \
    matplotlib \
    ipython \
    tqdm \
    packaging \
    protobuf \
    wheel \
    jsonlines==4.0.0 \
    bpe \
    omegaconf \
    hydra-core \
    sentence_transformers \
    datasets \
    accelerate \
    tensorboard \
    boto3 \
    # Flask Web 服务
    Flask==3.1.0 \
    flask_cors==5.0.1 \
    Werkzeug==3.1.3 \
    # NLP 工具
    spacy==3.8.4 \
    nltk==3.9.1 \
    # transformer 模型生态
    transformers==4.53.1 \
    transformers_stream_generator \
    peft \
    optimum \
    bitsandbytes \
    deepspeed==0.17.2 \
    loralib \
    torchmetrics \
    torchdata \
    ray[default]==2.43.0 \
    optree>=0.13.0 \
    einops \
    pynvml>=12.0.0 \
    # OpenAI 接口/对齐类库
    openai>=1.25.1 \
    FlagEmbedding==1.3.4 \
    mistralai \
    anthropic \
    google-generativeai \
    google-cloud-aiplatform \
    ai_researcher \
    magic_pdf==1.2.2 \
    fschat \
    art \
    datasketch \
    isort \
    wandb

# 安装 flash-attn（必须最后，因为它较重）
RUN pip install flash-attn==2.8.0.post2 --no-build-isolation

# 单独安装 openrlhf
RUN pip install openrlhf[vllm]
