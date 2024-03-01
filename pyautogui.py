from pydoc import importfile


import win32api
import win32con
import time

def test_click(x, y):
    win32api.SetCursorPos((x, y))

    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    time.sleep(2)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x - 100, y, 0, 0)


# test_click(1012, 704)
# for i in range(5):
#     # test_click(990, 980)
#     print(i)




def simulate_mouse_drag(start_x, start_y, end_x, end_y):
    # 获取鼠标当前位置
    x, y = win32api.GetCursorPos()
    # 移动鼠标到目标位置
    win32api.SetCursorPos((980, 700))
    # 模拟鼠标按下操作
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 980, 700, 0, 0)
    

    # 等待一段时间，让鼠标停留在目标位置
    # time.sleep(1)
    # 移动鼠标到目标位置
    win32api.SetCursorPos((980, 600))

    # 模拟鼠标释放操作
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 980, 600, 0, 0)

# 示例用法
start_pos = (1012, 704)
end_pos = (1112, 704)

# for i in range(1000):
#     # test_click(990, 980)
#     simulate_mouse_drag(start_pos[0], start_pos[1], end_pos[0], end_pos[1])
#     print(i)

