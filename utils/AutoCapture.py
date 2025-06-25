import pyautogui
import imagehash
from sqlalchemy import false

from utils.MyPaddle import ocr_image, print_ocr_result  # 导入特定函数
import os
from PIL import Image
from utils.SaveToJson import convert_to_chat_json

from paddleocr import PaddleOCR
# def capture_chat_window(prop_region,read = False):
#     last_hash = None
#     screen_width, screen_height = pyautogui.size()
#     # 从字典中提取所需信息
#     left = prop_region.get('x', 0)
#     top = prop_region.get('y', 0)
#     width = prop_region.get('width', 0)
#     height = prop_region.get('height', 0)
#     # 检查区域是否在屏幕范围内
#     if left < 0 or top < 0 or left + width > screen_width or top + height > screen_height:
#         print("所选区域超出屏幕范围，请重新选择。")
#         return
#     try:
#         screenshot = pyautogui.screenshot(region=(left, top, width, height))
#         current_hash = imagehash.average_hash(screenshot)
#
#         if last_hash is None or current_hash != last_hash:
#             print(current_hash)
#             if not os.path.exists("assets"):
#                 os.makedirs("assets")
#             screenshot.save("assets/image1.png")
#             if read:
#                 result = ocr_image("assets/image1.png", det=True)
#                 print_ocr_result(result)
#             last_hash = current_hash
#     except Exception as e:
#         print(f"发生未知错误: {e}")


def capture_chat_window(prop_region, last_hash, read=False):
    screen_width, screen_height = pyautogui.size()
    left = prop_region.get('x', 0)
    top = prop_region.get('y', 0)
    width = prop_region.get('width', 0)
    height = prop_region.get('height', 0)

    if left < 0 or top < 0 or left + width > screen_width or top + height > screen_height:
        print("所选区域超出屏幕范围，请重新选择。")
        return False, last_hash

    try:
        screenshot = pyautogui.screenshot(region=(left, top, width, height))
        current_hash = imagehash.average_hash(screenshot)

        if last_hash is None or current_hash != last_hash:
            print(current_hash)
            if not os.path.exists("assets"):
                os.makedirs("assets")
            screenshot.save("assets/image1.png")
            if read:
                result = ocr_image("assets/image1.png", det=True)
                print_ocr_result(result)
            return True, current_hash
        else :
            print("等待微信聊天信息更新")
    except Exception as e:
        print(f"发生未知错误: {e}")
    return False, last_hash


def extract_chat_Coord(image_path,name = '', det=False, cls=False):
    result = ocr_image("assets/image1.png", det=True)

    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            text = line[1][0]   #获取识别的文本
            if text == name:
                return line[0][0]




def crop_picture(image_path, coord,read = False):
    """
    截取聊天区域：从 coord 开始到图像最右下角，并保存成新图像。

    参数:
        image_path (str): 图片路径（如 "assets/image1.png"）
        coord (tuple): (x, y) 坐标，表示聊天区域左上角（例如用户名坐标）

    返回:
        cropped_image_path (str): 新图像路径
    """
    if not os.path.exists(image_path):
        print(f"图像文件不存在: {image_path}")
        return None

    try:
        image = Image.open(image_path)
        width, height = image.size
        x, y = coord

        if x < 0 or y < 0 or x >= width or y >= height:
            print("坐标超出图像范围")
            return None

        # 裁剪从 (x, y) 到右下角
        cropped = image.crop((x, y, width, height))

        output_path = "assets/image2.png"
        cropped.save(output_path)
        print(f"✅ 聊天区域裁剪完成，保存至: {output_path}")
        if read:
            result = ocr_image(output_path, det=True)
            print_ocr_result(result)


            return output_path
        return True
    except Exception as e:
        print(f"裁剪时发生错误: {e}")
        return  False
