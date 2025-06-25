from paddleocr import PaddleOCR


def ocr_image(image_path, det=False, cls=False):
    """
    使用 PaddleOCR 识别图片中的文字

    参数:
        image_path (str): 图片路径
        det (bool): 是否启用文字检测（默认为 False）
        cls (bool): 是否启用方向分类（默认为 False）
        lang: 语言模型（None表示默认中英文混合）
    返回:
        list: 识别结果列表
    """
    ocr_engine = PaddleOCR()
    result = ocr_engine.ocr(image_path, det=det, cls=cls)
    return result


def print_ocr_result(result):
    """打印 OCR 识别结果"""
    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            text = line[1][0]  # 获取识别的文本
            print(f"文本: {text}")
            print(f"位置: {line[0]}")
