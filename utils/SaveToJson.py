import json
import re
import cv2


# 获取气泡的颜色判断
def get_bubble_color(crop):
    hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.mean(hsv)[:3]
    return h, s, v

def is_my_message(h, s, v):
    # 调整后的微信绿色范围（经过测试更准确）
    # 注意：HSV中的H范围在OpenCV中是0-180（而不是0-360）
    return 35 < h < 80 and s > 50 and 100 < v < 250

def sanitize_filename(name):
    return re.sub( r'[\\/:*?"<>|]', "_", name)

# def convert_to_chat_json(ocr_result, output_dir='assets'):
#     messages = []
#     filename_text = "chat"
#
#     for group in ocr_result:
#         for i, block in enumerate(group):
#             if len(block) != 2:
#                 continue
#
#             _, text_data = block
#             if not isinstance(text_data, tuple) or len(text_data) != 2:
#                 continue
#
#             text, confidence = text_data
#             print(_)
#             if not isinstance(text, str) or confidence < 0.9:
#                 continue
#
#
#             text = text.strip()
#             if not text:
#                 continue
#
#             if len(messages) == 0:
#                 filename_text = sanitize_filename(text)
#
#             messages.append({
#                 "text": text
#             })
#
#     output_path = f"{output_dir}/{filename_text}.json"
#     with open(output_path, "w", encoding="utf-8") as f:
#         json.dump(messages, f, ensure_ascii=False, indent=2)
#
#     print(f"✅ 成功保存到: {output_path}，共 {len(messages)} 条")
#     return messages


def convert_to_chat_json(ocr_result, img_path, output_dir='assets'):
    messages = []
    filename_text = "chat"

    # 加载图片
    img = cv2.imread(img_path)
    if img is None:
        print("❌ 图片加载失败！")
        return

    message_index = 0

    for group in ocr_result:
        for i, block in enumerate(group):
            if len(block) != 2:
                continue

            _, text_data = block
            if not isinstance(text_data, tuple) or len(text_data) != 2:
                continue

            text, confidence = text_data
            if not isinstance(text, str) or confidence < 0.9:
                continue

            text = text.strip()
            if not text:
                continue

            if len(messages) == 0:
                filename_text = sanitize_filename(text)

            if len(block) == 2 and isinstance(block[1], tuple):
                box, (text, conf) = block
                if conf >= 0.9 and text.strip():
                    # 计算位置
                    x_coords = [int(point[0]) for point in box]
                    y_coords = [int(point[1]) for point in box]
                    x_min, x_max = max(min(x_coords) - 8, 0), min(max(x_coords) + 8, img.shape[1])
                    y_min, y_max = max(min(y_coords) - 8, 0), min(max(y_coords) + 8, img.shape[0])

                    bubble_crop = img[y_min:y_max, x_min:x_max]
                    h, s, v = get_bubble_color(bubble_crop)
                    mine = is_my_message(h, s, v)

                    role = "我" if mine else "对方"
                else:
                    role = None
            else:
                role = None

            messages.append({
                "text": text,
                "role": role
            })
            message_index += 1

    output_path = f"{output_dir}/{filename_text}.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

    print(f"✅ 成功保存到: {output_path}，共处理 {message_index} 条消息")
    return messages



