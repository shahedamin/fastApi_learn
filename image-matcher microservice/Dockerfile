FROM python:3.10-slim 
WORKDIR /app 
RUN pip install --no-cache-dir fastapi uvicorn onnxruntime pillow numpy python-multipart 
COPY main.py /app/main.py 
COPY trendyol_v2.1_int8.onnx /app/trendyol_v2.1_int8.onnx 
EXPOSE 8080 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"] 
