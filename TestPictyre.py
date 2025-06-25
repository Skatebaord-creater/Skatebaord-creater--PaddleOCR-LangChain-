from utils.AutoCapture import extract_chat_Coord
from utils.LLM import generate_next_response1
from utils.MyPaddle import ocr_image
from utils.SaveToJson import convert_to_chat_json

name = 'MorganLeGouar'

output_path = "assets/image2.png"
result = ocr_image(output_path, det=True)
convert_to_chat_json(result, 'assets/image2.png')
generate_next_response1(f'assets/{name}.json')