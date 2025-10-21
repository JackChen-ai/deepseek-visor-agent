"""
Simple inference test - Create a test image with text and verify OCR works
"""

from PIL import Image, ImageDraw, ImageFont
import tempfile
import os
from pathlib import Path

from deepseek_visor_agent import VisionDocumentTool


def create_invoice_test_image():
    """Create a simple invoice-like test image"""

    # Create a white image
    img = Image.new('RGB', (800, 600), color='white')
    draw = ImageDraw.Draw(img)

    # Try to use a default font, fall back to default if not available
    try:
        font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
        font_normal = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 18)
        font_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 14)
    except:
        font_large = ImageFont.load_default()
        font_normal = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Draw invoice content
    y_pos = 50

    # Header
    draw.text((50, y_pos), "INVOICE", fill='black', font=font_large)
    y_pos += 60

    # Invoice details
    draw.text((50, y_pos), "Invoice Number: INV-2024-001", fill='black', font=font_normal)
    y_pos += 30
    draw.text((50, y_pos), "Date: 2024-01-15", fill='black', font=font_normal)
    y_pos += 30
    draw.text((50, y_pos), "Vendor: Acme Corporation", fill='black', font=font_normal)
    y_pos += 50

    # Line items
    draw.text((50, y_pos), "Description", fill='black', font=font_small)
    draw.text((400, y_pos), "Quantity", fill='black', font=font_small)
    draw.text((550, y_pos), "Price", fill='black', font=font_small)
    y_pos += 30

    draw.line([(50, y_pos), (750, y_pos)], fill='black', width=1)
    y_pos += 10

    draw.text((50, y_pos), "Product A", fill='black', font=font_small)
    draw.text((400, y_pos), "2", fill='black', font=font_small)
    draw.text((550, y_pos), "$50.00", fill='black', font=font_small)
    y_pos += 25

    draw.text((50, y_pos), "Product B", fill='black', font=font_small)
    draw.text((400, y_pos), "1", fill='black', font=font_small)
    draw.text((550, y_pos), "$99.00", fill='black', font=font_small)
    y_pos += 35

    draw.line([(50, y_pos), (750, y_pos)], fill='black', width=1)
    y_pos += 10

    # Total
    draw.text((400, y_pos), "Total:", fill='black', font=font_normal)
    draw.text((550, y_pos), "$199.00", fill='black', font=font_normal)

    return img


def main():
    print("=" * 60)
    print("简单推理测试")
    print("=" * 60)

    # Create test image
    print("\n1. 创建测试发票图片...")
    img = create_invoice_test_image()

    # Save to temp file
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
        img.save(tmp.name)
        test_image_path = tmp.name

    print(f"   测试图片保存至: {test_image_path}")

    # Initialize tool
    print("\n2. 初始化 VisionDocumentTool...")
    print("   (使用 CPU + tiny 模式以节省资源)")
    tool = VisionDocumentTool(inference_mode="tiny", device="cpu")

    # Run inference
    print("\n3. 运行 OCR 推理...")
    try:
        result = tool.run(test_image_path)

        print("\n✅ 推理成功完成！")
        print("\n" + "=" * 60)
        print("OCR 结果")
        print("=" * 60)
        print("\nMarkdown 输出:")
        print(result["markdown"])

        print("\n提取的字段:")
        if result.get("fields"):
            for key, value in result["fields"].items():
                print(f"  - {key}: {value}")
        else:
            print("  (未提取到结构化字段)")

        print(f"\n文档类型: {result.get('document_type', 'unknown')}")
        print(f"置信度: {result.get('confidence', 'N/A')}")

        print("\n元数据:")
        if result.get("metadata"):
            for key, value in result["metadata"].items():
                print(f"  - {key}: {value}")

    except Exception as e:
        print(f"\n❌ 推理失败: {e}")
        import traceback
        traceback.print_exc()

    finally:
        # Cleanup
        if os.path.exists(test_image_path):
            os.unlink(test_image_path)
            print(f"\n清理临时文件: {test_image_path}")

    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)


if __name__ == "__main__":
    main()