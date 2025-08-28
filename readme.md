# Next-Gen-Parsing-Serve

# setup
pip install --no-cache-dir -r requirements.txt


# 调用示例
curl -X POST http://localhost:8000/v1/run \
  -H "Content-Type: application/json" \
  -d '{
    "usecase": "document_qa",
    "data": {
      "image": "/9j/4AAQSkZJR...",  // base64 编码的图像或PDF
      "content_type": "image/png",
      "question": "合同总金额是多少？"
    }
  }'



ray stop
ray start --head --dashboard-port=8265
serve start --http-host 0.0.0.0 --http-port 8101
serve deploy F:/PythonProjects/VLM-Parser-VLM-Serve/config/ray_serve_config.yaml
serve status


http://127.0.0.1:8265/
http://localhost:8101/docs


