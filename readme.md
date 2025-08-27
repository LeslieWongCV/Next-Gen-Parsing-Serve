# Next-Gen-Parsing-Serve

# setup
pip install --no-cache-dir -r requirements.txt


# 启动 Ray Head
ray start --head --port=6379

# 运行服务
serve run main:app

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

