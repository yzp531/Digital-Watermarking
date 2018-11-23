import numpy.core._methods
import numpy.lib.format
from PIL import Image
import time
import numpy as np
import functools
import sys

def embedding_info(picname, savename, text):
    text += '#%#' #作为结束标记
    try:
        im = np.array(Image.open(picname))
    except:
        print("无法获得该图像，请检查文件名")
        time.sleep(3)
        sys.exit()
        
    rows, columns, colors = im.shape
    embed = []
    for c in text:
        bin_sign = (bin(ord(c))[2:]).zfill(16)
        for i in range(16):
            embed.append(int(bin_sign[i]))
    
    count = 0
    for row in range(rows):
        for col in range(columns):
            for color in range(colors):
                if count < len(embed):
                    im[row][col][color] = im[row][col][color] //2 * 2 + embed[count]
                    count += 1

    Image.fromarray(im).save(savename)

def extract_info(picname):
    try:
        im = np.array(Image.open(picname))
    except:
        print("无法获得该图像，请检查文件名")
        time.sleep(2)
        sys.exit()

    rows, columns, colors = im.shape
    text = ""
    extract = np.array([], dtype = int)

    count = 0
    for row in range(rows):
        for col in range(columns):
            for color in range(colors):
                extract = np.append(extract, im[row][col][color] % 2)
                count += 1
                if count % 16 == 0:
                    bcode = functools.reduce(lambda x, y: str(x) + str(y), extract)
                    cur_char = chr(int(bcode, 2))
                    text += cur_char
                    if cur_char == '#' and text[-3:] == '#%#':
                        return text[:-3]
                    extract = np.array([], dtype=int)
            
def check_user():
    user_pass = {}
    username = input("你的名字首字母缩写（大写）：")
    password = input("你的生日（年月日 8位）：")
    if username not in user_pass or user_pass[username] != password:
        print("非合法用户，请联系作者")
        time.sleep(2)
        sys.exit()


def check_pic_format(picname):
    if picname[-4:] != '.png':
        print("图片格式非 png， 请重新输入")
        time.sleep(2)
        sys.exit()

def main():
    # check_user()
    print("欢迎使用图像文字嵌入程序, author：suzh")
    choose = input("选择你的功能: 1.图像加密  2.图像解密\n")
    if choose == '1':
        picname = input("请输入原图像名称(.png) ")
        check_pic_format(picname)
        text = input("输入你加密的内容： ")
        savename = 'After.png'
        embedding_info(picname, savename, text)
        print("已完成图像加密，生成文件 After.png")
        input("按下回车键退出程序")
    elif choose == '2':
        picname = input("请输入原图像名称(.png) ")
        check_pic_format(picname)
        text = extract_info(picname)
        print("由图片中提取的信息： ", text)
        input("按下回车键退出程序")
    else:
        print("参数错误")
        time.sleep(2)
        sys.exit()

if __name__ == '__main__':
    main()