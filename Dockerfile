# Use Ubuntu 22.04 as the base image
FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    python3 \
    && curl -sSL https://storage.googleapis.com/tensorflow-serving-apt/tensorflow-serving.release.pub.gpg | tee /usr/share/keyrings/tensorflow-serving-archive-keyring.gpg > /dev/null && \
    echo "deb [signed-by=/usr/share/keyrings/tensorflow-serving-archive-keyring.gpg] https://storage.googleapis.com/tensorflow-serving-apt stable tensorflow-model-server" | tee /etc/apt/sources.list.d/tensorflow-serving.list && \
    apt-get update && \
    apt-get install -y tensorflow-model-server && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY models/serving /models/serving

ENV MODEL_NAME=deepfake-serving

EXPOSE 8501

CMD tensorflow_model_server --rest_api_port=8501 --model_name=${MODEL_NAME} --model_base_path=/models/serving/
