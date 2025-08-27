import os

def create_project_structure(structure: str, base_path: str = "."):
    lines = structure.strip().splitlines()
    stack = []  # 存储当前层级的目录路径

    for line in lines:
        line = line.rstrip()  # 去除右边空白

        # 跳过仅是结构符号的空节点行（如 "│" 或 "│   └── ..." 中的中间线）
        if not line.strip():
            continue

        # 判断是否为有效节点（以 ├── 或 └── 开头）
        if '├──' not in line and '└──' not in line:
            continue

        # 提取名称部分
        indent = len(line) - len(line.lstrip('│ ├└─'))  # 精确计算缩进级别
        name = line[indent:].split(" ")[0]  # 忽略注释部分

        level = indent // 4  # 每级缩进为 4 字符

        # 根据当前缩进层级调整栈
        stack = stack[:level]

        current_path = os.path.join(base_path, *stack, name)

        if name.endswith("/"):  # 是目录
            os.makedirs(current_path, exist_ok=True)
            stack.append(name.rstrip('/'))
        else:
            with open(current_path, 'a', encoding='utf-8') as f:
                pass  # 创建空文件

# 示例调用：
project_tree = """
vlm_gateway/
├── __init__.py
├── main.py                  # Ray Serve 入口，定义 deployment
├── config/
│   ├── __init__.py
│   └── prompts.yaml         # 不同 usecase 的 prompt 模板
│   └── settings.py          # 通用配置（图像大小、超时等）
│
├── usecases/
│   ├── __init__.py
│   ├── document_qa.py       # 每个 usecase 一个模块
│   ├── image_caption.py
│   ├── table_extraction.py
│   └── base.py              # BaseUsecase 抽象类
│
├── processors/
│   ├── __init__.py
│   ├── image_processor.py   # 图像缩放、反转检测、PDF转图像
│   ├── prompt_builder.py    # 根据 usecase 构建 prompt
│   └── response_parser.py   # 后处理 VLM 输出
│
├── clients/
│   └── vlm_client.py        # 封装对后端 VLM API 的调用（重试、鉴权等）
│
├── utils/
│   └── helpers.py           # 工具函数（如生成 request_id）
│
└── serve_deployment.py      # Ray Serve Deployment 定义（可合并到 main.py）
"""

create_project_structure(project_tree, base_path=r"F:\PythonProjects\VLM-Parser-VLM-Serve")