# main.py
from sqlalchemy import false

from utils.MyPaddle import ocr_image, print_ocr_result  # 导入特定函数
from utils.AutoCapture import capture_chat_window,extract_chat_Coord,crop_picture
from utils.select_region import get_wechat_window_rect
from utils.LLM import generate_next_response1
from utils.SaveToJson import convert_to_chat_json

import os
import pyautogui
import time

if __name__ == "__main__":
    name = 'Sivyy'
    last_hash = None  # 通过HashImage来判断图像是否重复

    while True:
        try:
            # {'x': 93, 'y': 143, 'width': 830, 'height': 654, 'is_front': True, 'timestamp': 1744630484.294406}
            region = get_wechat_window_rect()
            if region["is_front"]:
                 # ✅ 只有在微信窗口在最前面时才执行
                # print(f"Selected region: {region}")
                 # 获取当前微信框
                is_different,last_hash = capture_chat_window(region,last_hash)
                print(last_hash)
                if is_different:

                     # 只获取聊天框 去除侧边栏 获取名字的的坐标
                    NameCoord = extract_chat_Coord("assets/image1.png", name)

                    is_crop_success = crop_picture("assets/image1.png", NameCoord)

                    if  is_crop_success:

                        output_path = "assets/image2.png"
                        result = ocr_image(output_path, det=True)
                        convert_to_chat_json(result,'assets/image2.png')
                        generate_next_response1(f'assets/{name}.json')

            else:
                print("未能获取到微信聊天框区域，等待下次检查...")






        except KeyboardInterrupt:
            print("程序被手动中断。")
            break

        except Exception as e:
            print(f"发生未知错误: {e}")