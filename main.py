import win32gui
import win32ui
import win32con
import numpy as np
import cv2
from PIL import Image


def capture_screen_fixed_v3(x, y, width, height):
    """
    截取屏幕的指定区域并确保颜色正确显示。
    :param x: 截取区域左上角的 x 坐标
    :param y: 截取区域左上角的 y 坐标
    :param width: 截取区域的宽度
    :param height: 截取区域的高度
    :return: 截取的屏幕内容 (numpy array)
    """
    # 获取桌面窗口的设备上下文
    hdesktop = win32gui.GetDesktopWindow()
    desktop_dc = win32gui.GetWindowDC(hdesktop)
    img_dc = win32ui.CreateDCFromHandle(desktop_dc)
    mem_dc = img_dc.CreateCompatibleDC()

    # 创建位图对象
    screenshot = win32ui.CreateBitmap()
    screenshot.CreateCompatibleBitmap(img_dc, width, height)
    mem_dc.SelectObject(screenshot)

    # 从屏幕的指定位置开始复制内容
    mem_dc.BitBlt((0, 0), (width, height), img_dc, (x, y), win32con.SRCCOPY)

    # 获取位图信息并转换为 numpy 格式
    bmpinfo = screenshot.GetInfo()
    bmpstr = screenshot.GetBitmapBits(True)
    img = np.frombuffer(bmpstr, dtype='uint8')
    img.shape = (bmpinfo['bmHeight'], bmpinfo['bmWidth'], 4)  # BGRA 格式

    # 释放资源
    mem_dc.DeleteDC()
    win32gui.ReleaseDC(hdesktop, desktop_dc)
    win32gui.DeleteObject(screenshot.GetHandle())

    # 删除 Alpha 通道，保留 BGR 顺序
    return img[..., :3]


if __name__ == "__main__":
    # 定义截取区域
    x, y, width, height = 100, 100, 800, 600

    # 截取屏幕内容
    screen_img = capture_screen_fixed_v3(x, y, width, height)

    # 使用 OpenCV 正确显示
    cv2.imshow("Captured Screen", screen_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



