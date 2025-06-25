import json
import cv2

from utils.MyPaddle import ocr_image


def get_bubble_color(crop):
    hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.mean(hsv)[:3]
    return h, s, v

def is_my_message(h, s, v):
    return 60 < h < 100 and s > 40 and v > 100

def assign_roles_by_color(ocr_result, img_path, chat_json_path):
    print(ocr_result)
    # 加载图片
    img = cv2.imread(img_path)
    if img is None:
        print("❌ 图片加载失败！")
        return

    # 加载原始JSON聊天内容（无角色信息）
    with open(chat_json_path, 'r', encoding='utf-8') as f:
        chat_data = json.load(f)

    message_index = 0  # 用于匹配chat_data里的每条消息

    for group in ocr_result:
        for i, block in enumerate(group):
            if message_index >= len(chat_data):
                break  # 已处理完所有消息

            if len(block) != 2 or not isinstance(block[1], tuple):
                continue

            box, (text, conf) = block
            if conf < 0.9 or not text.strip():
                continue

            # 计算位置
            x_coords = [int(point[0]) for point in box]
            y_coords = [int(point[1]) for point in box]
            x_min, x_max = max(min(x_coords) - 8, 0), min(max(x_coords) + 8, img.shape[1])
            y_min, y_max = max(min(y_coords) - 8, 0), min(max(y_coords) + 8, img.shape[0])

            bubble_crop = img[y_min:y_max, x_min:x_max]
            h, s, v = get_bubble_color(bubble_crop)
            mine = is_my_message(h, s, v)

            role = "我" if mine else "对方"
            chat_data[message_index]["role"] = role
            message_index += 1

    # 重新保存 JSON（带角色）
    with open(chat_json_path, 'w', encoding='utf-8') as f:
        json.dump(chat_data, f, ensure_ascii=False, indent=2)

    print(f"✅ 已更新角色信息，共处理 {message_index} 条消息")

if __name__ == '__main__':
    img_path = '/Users/skater/PycharmProjects/PaddlePaddle/assets/image2.png'  # 请替换为你的图片路径

    result = ocr_image(img_path, det=True)

    assign_roles_by_color(result, img_path, 'assets/MorganLeGouar.json')