# 微信聊天记录GPT微调工具

该工具旨在将微信聊天记录转换为适合用于训练ChatGPT模型的微调数据，训练出一个能够模仿你自己说话风格的AI模型。

## 功能特性

- **数据转换**：将微信导出的文本聊天记录转换为ChatGPT微调所需的JSONL格式。
- **自动上传**：集成OpenAI API，自动上传训练数据。
- **微调任务管理**：一键启动并跟踪模型微调状态，训练出专属对话模型。


## 依赖环境安装

使用以下命令安装所需Python库：

```bash
pip install -r requirements.txt
```

`requirements.txt` 示例内容：

```
openai
tkinter
```

## 如何使用

1. 克隆本项目到本地：

```bash
git clone https://github.com/StarChen4/wechat-gpt-finetune.git
```

2. 进入项目目录并运行程序：

```bash
cd wechat-gpt-finetune
python app.py
```

## 使用步骤

1. 在程序界面选择你导出的微信聊天记录（.txt文件）。
2. 输入你的OpenAI API密钥（注意保密）。
3. 点击转换按钮，生成JSONL数据文件。
4. 上传文件到OpenAI。
5. 启动微调任务并实时监控进度。

## 注意事项

- 请保护好你的OpenAI API密钥，避免泄露。
- 训练和使用API进行对话会产生费用，请酌情使用。
- 该项目在开发初期，存在BUG和功能不完善尽请见谅。
- 该项目仅用于学习和研究，请勿用于商业或不正当用途。

## 开源许可

本项目基于MIT许可协议开源。详情请参阅 [LICENSE](LICENSE)。

## 贡献代码

欢迎提交pull request以改进和扩展本项目。

