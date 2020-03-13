from PIL import Image, ImageDraw, ImageFont


def draw_single_rectangle(img, rectangle, color='red'):
    draw = ImageDraw.Draw(img)
    draw.line([tuple((rectangle[0], rectangle[1])),
               tuple((rectangle[2], rectangle[3])),
               tuple((rectangle[4], rectangle[5])),
               tuple((rectangle[6], rectangle[7])),
               tuple((rectangle[0], rectangle[1]))], width=2, fill=color)


def draw_detect_reg(img_path, gts, color='red'):
    img = Image.open(img_path)
    font_path = "/Users/thean/Library/Fonts/msyh.ttf"
    canvas = Image.new('RGB', (img.size[0]*2, img.size[1]), (255, 255, 255))
    canvas.paste(img, (0, 0, img.size[0], img.size[1]))
    draw = ImageDraw.Draw(canvas)
    for index in range(len(gts)):
        rectangle = gts[index][0]
        content = gts[index][1]
        draw.line([tuple((rectangle[0], rectangle[1])),
                   tuple((rectangle[2], rectangle[3])),
                   tuple((rectangle[4], rectangle[5])),
                   tuple((rectangle[6], rectangle[7])),
                   tuple((rectangle[0], rectangle[1]))], width=2, fill=color)

        # 微软雅黑比普通字体大一些，这里手动减去两个像素，其他字体可以不减或适当调整
        area_height = min(rectangle[5] - rectangle[1], rectangle[7] - rectangle[3]) - 2
        fontsize = 18  # 预计比从1开始快一些
        font = ImageFont.truetype(font_path, fontsize)
        while font.getsize('我')[0] < area_height:
            fontsize += 1
            font = ImageFont.truetype(font_path, fontsize)
        while font.getsize('我')[0] > area_height:
            fontsize -= 1
            font = ImageFont.truetype(font_path, fontsize)
        draw.text((rectangle[0] + img.size[0], rectangle[1]), text=content, fill=(64, 64, 64), font=font)
    return canvas


def parse_gt_file(path):
    gt_res = []
    with open(path, "r") as file:
        while True:
            line = file.readline()
            if not line:
                break
            arr = line.split(",")
            coo = arr[:8]
            content = ",".join(arr[8:])
            pair = ([int(i) for i in coo], content)
            gt_res.append(pair)
    return gt_res


# gt struct: [([8], str), ([8], str)...]
# file line: x1,y1,x2,y2,x3,y3,x4,y4,content
def write_gt_to_file(gt, file_path):
    with open(file_path, "w") as file:
        for index in range(len(gt)):
            ele = gt[index]
            coo = ",".join([str(e) for e in ele[0]])
            content = ele[1]
            file.write("%s,%s\n" % (coo, content))


if __name__ == "__main__":
    image = "/Users/thean/Desktop/tmp/entire_pic.png"
    gt_file = "/Users/thean/Desktop/tmp/1.txt"
    gt = parse_gt_file(gt_file)
    res = draw_detect_reg(image, gt)
    res.show()
