# -*- coding: utf-8 -*-
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw, ImageOps
import numpy as np
from io import BytesIO
import base64


def get_file_base64(pic):
    with open(pic, 'rb') as f:  # 以二进制读取图片
        data = f.read()
        encodestr = base64.b64encode(data)  # 得到 byte 编码的数据
        return str(encodestr, 'utf-8')


# gts is an array of tuple which is (int[8], str)
def draw_polygon(img, gts, color='red'):
    draw = ImageDraw.Draw(img)
    for gt in gts:
        coo = gt[0]
        draw.line([tuple((coo[0], coo[1])),
                   tuple((coo[2], coo[3])),
                   tuple((coo[4], coo[5])),
                   tuple((coo[6], coo[7])),
                   tuple((coo[0], coo[1]))], width=1, fill=color)
    return img


# codes from: https://github.com/Leungtamir/Image-Freehand/blob/master/image.py
def hand_draw(input_path, output_path):
    L = np.asarray(Image.open(input_path).convert('L')).astype('float')  # 取得图像灰度

    depth = 10.  # (0-100)
    grad = np.gradient(L)  # 取图像灰度的梯度值
    grad_x, grad_y = grad  # 分别取横纵图像梯度值
    grad_x = grad_x * depth / 100.
    grad_y = grad_y * depth / 100.
    A = np.sqrt(grad_x ** 2 + grad_y ** 2 + 1.)
    uni_x = grad_x / A
    uni_y = grad_y / A
    uni_z = 1. / A

    el = np.pi / 2.2  # 光源的俯视角度，弧度值
    az = np.pi / 4  # 光源的方位角度，弧度值
    dx = np.cos(el) * np.cos(az)  # 光源对x轴的影响
    dy = np.cos(el) * np.sin(az)  # 光源对y轴的影响
    dz = np.sin(el)  # 光源对z轴的影响

    gd = 255 * (dx * uni_x + dy * uni_y + dz * uni_z)  # 光源归一化
    gd = gd.clip(0, 255)  # 避免数据越界，将生成的灰度值裁剪至0-255之间

    im = Image.fromarray(gd.astype('uint8'))  # 重构图像
    im.save(output_path)  # 保存图像


def pic_dealer_example(pic_path, output_path):
    im = Image.open(pic_path)
    # 创建缩略图
    im.thumbnail((128, 128), Image.ANTIALIAS)
    im.save(output_path + "/thumbnail.jpg")
    im = Image.open(pic_path)
    # 剪切图片，四元组分别表示左、上、右、下（以图片左上角为坐标原点）
    # 示例代码剪切了一块 200x200 pixel的区域
    region = im.crop((100, 100, 300, 300))
    region.save(output_path + "/crop.jpg")
    # 图片粘贴，第二个参数含义同上
    region = region.transpose(Image.ROTATE_180)
    im.paste(region, (100, 100, 300, 300))
    im.save(output_path + "/paste.jpg")
    im = Image.open(pic_path)
    # 分离和合并颜色通道
    r, g, b = im.split()
    im2 = Image.merge("RGB", (r, g, b))
    im2.save(output_path + "/merge.jpg")
    # 对图像进行几何变换是一种基本处理，在Pillow中包括resize()和rotate()，如用法如下：
    # 调整图片大小
    out = im.resize((128, 128))
    # 旋转图片，参数为顺时针旋转（degree conter-clockwise）的角度，或者用Image定义好的值
    out = im.rotate(45)
    out = im.transpose(Image.FLIP_LEFT_RIGHT)
    out = im.transpose(Image.FLIP_TOP_BOTTOM)
    out = im.transpose(Image.ROTATE_90)
    out = im.transpose(Image.ROTATE_180)
    out = im.transpose(Image.ROTATE_270)
    out.save(output_path + "/rotate.jpg")
    # 进行颜色空间的变换
    cmyk = im.convert("CMYK")
    cmyk.save(output_path + "/cmyk.jpg")
    gray = im.convert("L")
    gray.save(output_path + "/gray.jpg")
    '''
    图像滤波

    '''
    imgF = Image.open(pic_path)
    # 均值滤波（模糊），图片看起来柔和一些
    imgF.filter(ImageFilter.BLUR).save(output_path + "/blur.jpg")
    # 图片细节效果，没看出什么区别
    imgF.filter(ImageFilter.DETAIL).save(output_path + "/detail.jpg")
    # 轮廓效果
    imgF.filter(ImageFilter.CONTOUR).save(output_path + "/contour.jpg")
    # 边界效果
    imgF.filter(ImageFilter.FIND_EDGES).save(output_path + "/edges.jpg")
    imgF.filter(ImageFilter.EDGE_ENHANCE).save(output_path + "/edge_enhance.jpg")
    # 阈值边界加强
    imgF.filter(ImageFilter.EDGE_ENHANCE_MORE).save(output_path + "/edge_enhance_more.jpg")
    # 浮雕
    imgF.filter(ImageFilter.EMBOSS).save(output_path + "/emboss.jpg")
    # 平滑，柔和效果貌似比均值滤波好些
    imgF.filter(ImageFilter.SMOOTH).save(output_path + "/smooth.jpg")
    # 阈值平滑
    imgF.filter(ImageFilter.SMOOTH_MORE).save(output_path + "/smooth_more.jpg")
    # 锐化
    imgF.filter(ImageFilter.SHARPEN).save(output_path + "/sharpen.jpg")
    '''
    图像增强
    '''
    imgE = Image.open(pic_path)
    # 增强对比度 0.0（solid grey实灰）~1.0（原图）
    imgEH = ImageEnhance.Contrast(imgE)
    imgEH.enhance(1.3).show()
    # 色彩平衡 0.0（黑白）~1.0（原图）
    imgEH = ImageEnhance.Color(imgE)
    imgEH.enhance(0.5).show()
    # 亮度 0.0（黑）~1.0（原图）
    imgEH = ImageEnhance.Brightness(imgE)
    imgEH.enhance(0.5).show()
    # 锐化 0.0（模糊）~1.0（原图）~2.0（尖锐）
    imgEH = ImageEnhance.Sharpness(imgE)
    imgEH.enhance(1.5).show()
    # 图片在α通道添加一层颜色
    im = Image.open(pic_path).convert("RGBA")
    p = Image.new('RGBA', im.size, (0, 128, 128))
    # 新图片=im*0.7+p*0.3
    img = Image.blend(im, p, 0.3)
    img.show()


# 若img.save()报错 cannot write mode RGBA as JPEG
# 则img = Image.open(image_path).convert('RGB')
def image_to_base64(image_path):
    img = Image.open(image_path).convert('RGB')
    output_buffer = BytesIO()
    img.save(output_buffer, format='JPEG')
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data)
    return base64_str


def new_image_base64(image_path):
    with open(image_path, 'rb') as f:  # 以二进制读取图片
        data = f.read()
        encodestr = base64.b64encode(data)  # 得到 byte 编码的数据
    return encodestr


def base64_to_image(base64_str, image_path=None):
    imgdata = base64.b64decode(base64_str)
    image_data = BytesIO(imgdata)
    img = Image.open(image_data)
    if image_path:
        img.save(image_path)
    img.show()


def revert_image(origin_image):
    if origin_image.mode == 'RGBA':
        r, g, b, a = origin_image.split()
        rgb_image = Image.merge('RGB', (r, g, b))
        inverted_image = ImageOps.invert(rgb_image)
        r2, g2, b2 = inverted_image.split()
        final_transparent_image = Image.merge('RGBA', (r2, g2, b2, a))
        return final_transparent_image
    else:
        inverted_image = ImageOps.invert(origin_image)
        return inverted_image


if __name__ == "__main__":
    path = "/Users/thean/Desktop/test-picture/21.png"
    print(image_to_base64(path))

    # im = Image.open("/Users/thean/Pictures/test.jpg")
    # print(im.format, im.size, im.mode, im.n_frames)
    # for index in range(im.n_frames):
    #     if index > 4:
    #         break
    #     print(index)
    #     im.seek(index)
    #     im.show()

    # b64 = image_to_base64(path)
    # base64_to_image(b64, "/Users/thean/Desktop/1.jpg")
