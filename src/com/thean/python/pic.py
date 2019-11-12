from PIL import Image
from PIL import ImageFilter
from PIL import ImageEnhance
import numpy as np


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

if __name__ == "__main__":
    hand_draw("/path/to/your/pic.jpg", "/path/to/save/this/pic.jpg")
