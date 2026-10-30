from fastapi import FastAPI, File, UploadFile, HTTPException
import onnxruntime as ort
import numpy as np
from PIL import Image, ImageOps
import io

app = FastAPI(title="Product Image Embedding Microservice")

# Initialize ONNX Runtime Session using INT8 quantized model
# Thread limits tuned for a 4 vCPU server
session_options = ort.SessionOptions()
session_options.intra_op_num_threads = 2
session_options.inter_op_num_threads = 2
session = ort.InferenceSession("trendyol_v2.1_int8.onnx", session_options, providers=["CPUExecutionProvider"])

input_name = session.get_inputs()[0].name

def preprocess_image_v21(image_bytes: bytes) -> np.ndarray:
    """
    Trendyol v2.1 Exact Preprocessing Pipeline:
    1. Scale keeping aspect ratio (max side 224px)
    2. Pad to square with white (RGB 255)
    3. ImageNet Normalization
    """
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    
    # 1. Scale max side to 224 keeping ratio
    image.thumbnail((224, 224), Image.Resampling.LANCZOS)
    
    # 2. Pad to square with white background (255, 255, 255)
    delta_w = 224 - image.width
    delta_h = 224 - image.height
    padding = (delta_w // 2, delta_h // 2, delta_w - (delta_w // 2), delta_h - (delta_h // 2))
    padded_image = ImageOps.expand(image, padding, fill=(255, 255, 255))
    
    # Ensure exact 224x224
    padded_image = padded_image.resize((224, 224), Image.Resampling.LANCZOS)
    
    # 3. Convert to float array (0.0 to 1.0)
    img_np = np.array(padded_image, dtype=np.float32) / 255.0
    
    # ImageNet Mean & Std
    mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
    std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
    
    # Apply normalization
    img_np = (img_np - mean) / std
    
    # Transpose HWC -> CHW (3, 224, 224)
    img_np = img_np.transpose(2, 0, 1)
    
    # Add Batch dimension (1, 3, 224, 224)
    return np.expand_dims(img_np, axis=0).astype(np.float32)

@app.post("/embed")
async def get_embedding(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")
    
    try:
        image_bytes = await file.read()
        tensor = preprocess_image_v21(image_bytes)
        
        # Run ONNX inference
        outputs = session.run(None, {input_name: tensor})
        embedding_vector = outputs[0][0].tolist()
        
        return {
            "status": "success",
            "dimensions": len(embedding_vector),
            "embedding": embedding_vector
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "ok", "model": "Trendyol-DINOv2.1-INT8"}