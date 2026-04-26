FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
RUN useradd -m appuser
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . .

RUN pip install kaggle --no-cache-dir && \
    mkdir -p noshow_iq/data && \
    kaggle datasets download -d joniarroba/noshowappointments -p noshow_iq/data --unzip && \
    python -c "
from noshow_iq.preprocess import load_and_clean, get_features_and_target
from noshow_iq.model import train
df = load_and_clean('noshow_iq/data/KaggleV2-May-2016.csv')
X, y = get_features_and_target(df)
train(X, y)
print('Model trained!')
" && \
    rm -rf noshow_iq/data

RUN chown -R appuser:appuser /app
USER appuser
EXPOSE 7860
CMD ["uvicorn", "noshow_iq.api:app", "--host", "0.0.0.0", "--port", "7860"]