import requests
import os

def open_url(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    req = requests.get(url, headers=headers)
    return req

def get_page(url):
    req = open_url(url)
    html = req.text  # 返回顶层网页字符串信息
    a = html.find('current-comment-page') + 23  # 在网页信息中查找页号开始位置
    b = html.find(']', a)  # 确定页号结束位置

    return html[a:b]  # 返回页号字符串

def find_imgs(page_url):
    req = open_url(page_url)
    html = req.text  # 返回具体页号对应的网页信息
    img_addrs = []  # 存储图片地址的列表
    a = html.find('img src=')  # 查找首个图片地址开始的位置

    while a != -1:
        b = html.find('.jpg', a, a + 255)  # 确定图片地址结束位置
        if b != -1:
            img_addrs.append(html[a+9:b+4])
        else:
            b = a + 9
        a = html.find('img src=', b)  # 更新图片开始位置

    return img_addrs

def save_imgs(folder, img_addres):
    for each in img_addres:
        pic_name = each.split('/')[-1]  # 在每个图片地址中，取出最后的名字
        with open(pic_name, 'wb') as f:  # 打开写入名为pic_name的文件
            req = open_url('http:' + each)
            img = req.content  # content返回的是二进制字节流，text返回的是字符串
            f.write(img)


def downloadpic(folder='ooxx', pages=5):
    url = 'http://jandan.net/pic/'  # 获取顶层网址，即服务器文件夹
    page_num = int(get_page(url))  # 根据顶层网址信息，获得当前更新到的页号位置

    os.mkdir('C:\\Users\\Wangqian\\Desktop\\' + folder)  # 文件夹设置
    os.chdir('C:\\Users\\Wangqian\\Desktop\\' + folder)
    # 以页号为例，循环查找每页网址中所有图片的地址，并保存图片
    for i in range(pages):
        page_num -= i
        page_url = url + 'page-' + str(page_num) + '#comments'  # 获得每个页号对应的网址

        img_list = find_imgs(page_url)  # 获得该页号网址中所有图片的地址
        save_imgs(folder, img_list)  # 向文件夹保存页号网址中所有的图片

if __name__ == '__main__':
    downloadpic()
