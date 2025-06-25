import cv2
import numpy as np
from utils.MyPaddle import ocr_image
# 初始化OCR模型

# 读取图片
img_path = 'assets/image3.png'  # 请替换为你的图片路径
img = cv2.imread(img_path)

# 执行OCR识别
ocr_result = ocr_image(img_path, det=True)

# 获取气泡的颜色判断
def get_bubble_color(crop):
    hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.mean(hsv)[:3]
    return h, s, v


def is_my_message(h, s, v):
    # 调整后的微信绿色范围（经过测试更准确）
    # 注意：HSV中的H范围在OpenCV中是0-180（而不是0-360）
    return 35 < h < 80 and s > 50 and 100 < v < 250
# 遍历OCR结果并提取文本与颜色信息
for group in ocr_result:  # 每个 group 对应一行文本（包含多个 block）
    for i, block in enumerate(group):  # 每个 block 是一个文本框
        box, (text, conf) = block
        x_coords = [int(point[0]) for point in box]
        y_coords = [int(point[1]) for point in box]
        x_min, x_max = min(x_coords), max(x_coords)
        y_min, y_max = min(y_coords), max(y_coords)

        # 添加 padding 防止只裁出文字，包含气泡背景
        pad = 8
        x_min = max(x_min - pad, 0)
        x_max = min(x_max + pad, img.shape[1])
        y_min = max(y_min - pad, 0)
        y_max = min(y_max + pad, img.shape[0])

        # 提取气泡区域
        bubble_crop = img[y_min:y_max, x_min:x_max]
        h, s, v = get_bubble_color(bubble_crop)
        mine = is_my_message(h, s, v)

        # 输出判断结果
        label = '我说的' if mine else '对方说的'
        print(f'{label}: {text}')

        # 可视化（调试时查看气泡标记）
        color = (0, 255, 0) if mine else (255, 0, 0)  # 绿色是“我说的”，红色是“对方说的”
        cv2.rectangle(img, (x_min, y_min), (x_max, y_max), color, 2)
        cv2.putText(img, text, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

# 显示最终的标注结果（可视化调试）
cv2.imshow('Result', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
