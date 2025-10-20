# Dify Integration Guide

This guide shows how to integrate DeepSeek Visor Agent with Dify as a custom tool.

## Method 1: Using REST API

### Step 1: Start the API Server

Create a simple API wrapper:

```python
# api_server.py
from fastapi import FastAPI, File, UploadFile
from deepseek_visor_agent import VisionDocumentTool
import uvicorn

app = FastAPI()
tool = VisionDocumentTool()

@app.post("/api/ocr")
async def process_document(
    file: UploadFile = File(...),
    document_type: str = "auto"
):
    """Process uploaded document"""
    # Save uploaded file temporarily
    temp_path = f"/tmp/{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    # Process with OCR
    result = tool.run(temp_path, document_type=document_type)

    return result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

Run the server:

```bash
pip install fastapi uvicorn[standard]
python api_server.py
```

### Step 2: Configure in Dify

1. Go to **Tools** → **Custom Tools**
2. Add new **HTTP Request** tool
3. Configure:
   - **Name**: DeepSeek OCR
   - **Method**: POST
   - **URL**: `http://localhost:8000/api/ocr`
   - **Body Type**: Form Data
   - **Parameters**:
     - `file` (File) - Required
     - `document_type` (String) - Optional (default: "auto")

4. Test the tool with a sample image

### Step 3: Use in Workflow

In your Dify workflow:

1. Add **File Upload** node
2. Add **DeepSeek OCR** tool node
3. Connect file upload output to OCR input
4. Use OCR output in subsequent nodes

Example output schema:

```json
{
  "markdown": "# Invoice\n\nDate: 2024-01-15\n...",
  "fields": {
    "total": "$199.00",
    "date": "2024-01-15",
    "vendor": "Acme Corp"
  },
  "document_type": "invoice",
  "confidence": 0.95
}
```

## Method 2: Python Code Node (Advanced)

If you have Python code node access in Dify:

```python
from deepseek_visor_agent import VisionDocumentTool

def main(image_path: str) -> dict:
    tool = VisionDocumentTool()
    result = tool.run(image_path)
    return result
```

## Method 3: Deploy as Microservice

For production deployments:

1. **Containerize the API**:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY api_server.py .

EXPOSE 8000

CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8000"]
```

2. **Deploy to cloud** (Render, Fly.io, Railway)

3. **Use public URL in Dify**:
   - `https://your-app.onrender.com/api/ocr`

## Example Workflows

### Invoice Processing Workflow

```
1. File Upload Node
   ↓
2. DeepSeek OCR Tool (document_type: "invoice")
   ↓
3. Condition Node (check if total > $1000)
   ↓
4. LLM Node (generate summary)
   ↓
5. Email/Webhook Output
```

### Document Classification Workflow

```
1. File Upload Node
   ↓
2. DeepSeek OCR Tool (document_type: "auto")
   ↓
3. Switch Node (based on document_type)
   ├─→ Invoice → Invoice Processing
   ├─→ Contract → Contract Review
   └─→ Other → Manual Review
```

## Tips

1. **Pre-process images** for better accuracy:
   - Convert to high-resolution PNG
   - Crop to document boundaries
   - Adjust brightness/contrast

2. **Cache results** to avoid re-processing:
   ```python
   import hashlib
   import pickle

   def cached_ocr(image_path: str):
       # Generate hash of image
       with open(image_path, 'rb') as f:
           file_hash = hashlib.md5(f.read()).hexdigest()

       cache_file = f"/tmp/ocr_cache_{file_hash}.pkl"

       if os.path.exists(cache_file):
           with open(cache_file, 'rb') as f:
               return pickle.load(f)

       result = tool.run(image_path)

       with open(cache_file, 'wb') as f:
           pickle.dump(result, f)

       return result
   ```

3. **Error handling**:
   ```python
   try:
       result = tool.run(image_path)
   except Exception as e:
       return {
           "error": str(e),
           "markdown": "",
           "fields": {}
       }
   ```

## Troubleshooting

### Issue: "Module not found"
- Make sure `deepseek-visor-agent` is installed in the environment where the API runs

### Issue: "Out of memory"
- Reduce image size before processing
- Use `device="cpu"` mode: `VisionDocumentTool(device="cpu")`

### Issue: "Slow inference"
- Use GPU if available
- Consider deploying on GPU-enabled cloud instance

## Support

For more help:
- GitHub Issues: https://github.com/visor-agent/deepseek-visor-agent/issues
- Email: hello@visor-agent.com
