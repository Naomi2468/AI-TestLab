import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing")

client = genai.Client(api_key=api_key)

# 读取 Pytest 测试日志
log_path = Path("reports/test_output.txt")
test_log = log_path.read_text(encoding="utf-8")

# 给 AI 的分析任务
prompt = f"""
You are an experienced Python API testing engineer.

Analyze the following Pytest test results.

Please explain:
1. Which test failed?
2. What caused the failure?
3. Is this likely an API bug or an incorrect test expectation?
4. How should the developer investigate and fix it?

Do not invent missing evidence.
If the cause is uncertain, say so.

Pytest log:
{test_log}
"""

# 调用 Gemini
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

analysis = response.text

# 保存 AI 分析报告
report_path = Path("reports/ai_analysis.md")
report_path.write_text(
    analysis or "No analysis returned.",
    encoding="utf-8"
)

print("AI analysis saved to:", report_path)
print(analysis)