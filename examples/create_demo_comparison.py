"""
生成 Reddit/Twitter 用的效果对比图

用法:
    python examples/create_demo_comparison.py --image path/to/invoice.jpg --output demo_comparison.png
"""

import argparse
from PIL import Image, ImageDraw, ImageFont
import json
from pathlib import Path


def create_sample_invoice_image(output_path: str = "sample_invoice.png"):
    """创建一个简单的示例发票图片（用于演示）"""
    # 创建白色背景
    width, height = 800, 600
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)

    # 使用系统默认字体
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 32)
        header_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
        body_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 18)
    except:
        title_font = ImageFont.load_default()
        header_font = ImageFont.load_default()
        body_font = ImageFont.load_default()

    # 绘制发票内容
    y_offset = 40

    # 标题
    draw.text((50, y_offset), "INVOICE", font=title_font, fill='black')
    y_offset += 60

    # 发票信息
    draw.text((50, y_offset), "Invoice #: INV-2024-001", font=body_font, fill='black')
    y_offset += 30
    draw.text((50, y_offset), "Date: January 15, 2024", font=body_font, fill='black')
    y_offset += 40

    # 供应商信息
    draw.text((50, y_offset), "From:", font=header_font, fill='black')
    y_offset += 35
    draw.text((50, y_offset), "Acme Corporation", font=body_font, fill='black')
    y_offset += 25
    draw.text((50, y_offset), "123 Business St", font=body_font, fill='black')
    y_offset += 25
    draw.text((50, y_offset), "New York, NY 10001", font=body_font, fill='black')
    y_offset += 50

    # 客户信息
    draw.text((50, y_offset), "Bill To:", font=header_font, fill='black')
    y_offset += 35
    draw.text((50, y_offset), "Client Company LLC", font=body_font, fill='black')
    y_offset += 60

    # 项目表格
    draw.text((50, y_offset), "Description", font=header_font, fill='black')
    draw.text((450, y_offset), "Amount", font=header_font, fill='black')
    y_offset += 35

    draw.line([(50, y_offset), (750, y_offset)], fill='black', width=2)
    y_offset += 20

    draw.text((50, y_offset), "Professional Services", font=body_font, fill='black')
    draw.text((450, y_offset), "$150.00", font=body_font, fill='black')
    y_offset += 30

    draw.text((50, y_offset), "Consulting Fee", font=body_font, fill='black')
    draw.text((450, y_offset), "$49.00", font=body_font, fill='black')
    y_offset += 40

    draw.line([(50, y_offset), (750, y_offset)], fill='black', width=1)
    y_offset += 20

    # 总计 - 修复重叠问题
    draw.text((50, y_offset), "Total Amount Due:", font=header_font, fill='black')
    draw.text((500, y_offset), "$199.00", font=header_font, fill='black')

    img.save(output_path)
    print(f"✅ 示例发票已保存到: {output_path}")
    return output_path


def create_comparison_image(
    invoice_image_path: str,
    extracted_data: dict,
    output_path: str = "demo_comparison.png"
):
    """
    创建效果对比图: 左边发票原图，右边提取结果

    Args:
        invoice_image_path: 发票图片路径
        extracted_data: 提取的数据字典
        output_path: 输出图片路径
    """
    # 加载发票图片
    invoice_img = Image.open(invoice_image_path)

    # 创建画布 (左边发票 + 右边结果)
    canvas_width = invoice_img.width * 2 + 60  # 20px padding + 40px gap
    canvas_height = max(invoice_img.height, 600) + 40

    canvas = Image.new('RGB', (canvas_width, canvas_height), color='#f5f5f5')

    # 粘贴发票图片（左边）
    canvas.paste(invoice_img, (20, 20))

    # 绘制右边的提取结果
    draw = ImageDraw.Draw(canvas)

    # 使用系统字体
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 28)
        key_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 20)
        value_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
        code_font = ImageFont.truetype("/System/Library/Fonts/Courier New.ttf", 16)
    except:
        title_font = ImageFont.load_default()
        key_font = ImageFont.load_default()
        value_font = ImageFont.load_default()
        code_font = ImageFont.load_default()

    # 右边区域起始位置
    right_x = invoice_img.width + 60
    y_offset = 40

    # 标题
    draw.text((right_x, y_offset), "Extracted Data ✨", font=title_font, fill='#2c3e50')
    y_offset += 50

    # 绘制箭头
    arrow_x = invoice_img.width + 30
    arrow_y = canvas_height // 2
    draw.polygon([
        (arrow_x, arrow_y - 20),
        (arrow_x + 20, arrow_y),
        (arrow_x, arrow_y + 20)
    ], fill='#3498db')

    # 提取的字段
    fields = extracted_data.get('fields', {})

    # 绘制每个字段
    for field_name, field_value in fields.items():
        # 字段名称
        draw.text((right_x, y_offset), f"{field_name.replace('_', ' ').title()}:",
                  font=key_font, fill='#7f8c8d')
        y_offset += 30

        # 字段值 (带背景框)
        value_text = str(field_value)

        # 绘制背景框
        bbox = draw.textbbox((right_x, y_offset), value_text, font=value_font)
        padding = 10
        draw.rectangle([
            (bbox[0] - padding, bbox[1] - padding),
            (bbox[2] + padding, bbox[3] + padding)
        ], fill='#ecf0f1', outline='#3498db', width=2)

        # 绘制文字
        draw.text((right_x, y_offset), value_text, font=value_font, fill='#2c3e50')
        y_offset += 50

    # 添加代码示例
    y_offset += 20
    draw.text((right_x, y_offset), "Code used:", font=key_font, fill='#7f8c8d')
    y_offset += 35

    code_lines = [
        "tool = VisionDocumentTool()",
        "result = tool.run('invoice.jpg')",
        "print(result['fields'])"
    ]

    for line in code_lines:
        draw.text((right_x, y_offset), line, font=code_font, fill='#2c3e50')
        y_offset += 22

    # 保存
    canvas.save(output_path)
    print(f"✅ 效果对比图已保存到: {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(description='生成 DeepSeek Visor Agent 演示对比图')
    parser.add_argument('--image', type=str, help='发票图片路径（如果不提供，会生成示例发票）')
    parser.add_argument('--output', type=str, default='demo_comparison.png', help='输出图片路径')
    parser.add_argument('--create-sample', action='store_true', help='仅创建示例发票')

    args = parser.parse_args()

    # 如果只需要创建示例发票
    if args.create_sample:
        create_sample_invoice_image("sample_invoice.png")
        return

    # 如果没有提供图片，先创建示例发票
    if not args.image:
        print("📝 未提供发票图片，创建示例发票...")
        invoice_path = create_sample_invoice_image("sample_invoice.png")
    else:
        invoice_path = args.image

    # 模拟提取的数据（实际使用时应该运行真实的 OCR）
    extracted_data = {
        "fields": {
            "invoice_number": "INV-2024-001",
            "date": "2024-01-15",
            "vendor": "Acme Corporation",
            "total": "$199.00"
        },
        "document_type": "invoice",
        "confidence": 0.95
    }

    # 如果提供了真实图片，可以尝试运行真实的 OCR
    if args.image and Path(args.image).exists():
        try:
            print("🔄 运行 DeepSeek-OCR 提取数据...")
            from deepseek_visor_agent import VisionDocumentTool

            tool = VisionDocumentTool()
            result = tool.run(args.image, document_type="invoice")
            extracted_data = result
            print(f"✅ 提取完成! 置信度: {result.get('confidence', 'N/A')}")
        except Exception as e:
            print(f"⚠️ 无法运行 OCR (使用模拟数据): {e}")

    # 创建对比图
    create_comparison_image(invoice_path, extracted_data, args.output)

    print(f"\n🎉 完成! 你可以在 Reddit/Twitter 帖子中使用 {args.output}")


if __name__ == "__main__":
    main()
