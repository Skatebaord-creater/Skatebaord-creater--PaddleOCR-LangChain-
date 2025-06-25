import subprocess
import time
import tempfile

def get_wechat_window_rect(timeout=30, check_interval=1):
    script_template = '''
on getValueOrZero(val)
    if val is missing value then
        return 0
    else
        return val
    end if
end getValueOrZero

tell application "System Events"
    set appRunning to exists (application processes whose name is "WeChat")
    if appRunning then
        set appProcesses to application processes whose name is "WeChat"
        if (count of windows of item 1 of appProcesses) > 0 then
            tell item 1 of appProcesses
                set isFront to frontmost as string
                set windowPosition to position of first window
                set windowSize to size of first window
                set x to my getValueOrZero(item 1 of windowPosition) as string
                set y to my getValueOrZero(item 2 of windowPosition) as string
                set w to my getValueOrZero(item 1 of windowSize) as string
                set h to my getValueOrZero(item 2 of windowSize) as string
                return isFront & "," & x & "," & y & "," & w & "," & h
            end tell
        else
            return "not_found"
        end if
    else
        return "not_found"
    end if
end tell

'''

    start_time = time.time()

    # 写入临时 AppleScript 文件
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.applescript', delete=False) as temp_script:
        temp_script.write(script_template)
        temp_script_path = temp_script.name

    while time.time() - start_time < timeout:
        try:
            result = subprocess.run(
                ['osascript', temp_script_path],
                capture_output=True,
                text=True,
                check=True
            )

            output = result.stdout.strip()

            if output != "not_found":
                parts = output.split(',')
                if len(parts) >= 5:
                    is_front = parts[0].strip().lower() == "true"
                    x, y, width, height = map(int, map(str.strip, parts[1:5]))
                    return {
                        "x": x,
                        "y": y,
                        "width": width,
                        "height": height,
                        "is_front": is_front,
                        "timestamp": time.time()
                    }
                else:
                    print(f"[WARN] 返回格式不完整: {parts}")

        except subprocess.CalledProcessError as e:
            print(f"执行AppleScript出错: {e}")
        except ValueError as e:
            print(f"解析坐标出错: {e}")
        except Exception as e:
            print(f"未知错误: {e}")

        time.sleep(check_interval)

    print(f"等待微信窗口超时({timeout}秒)")
    return None
