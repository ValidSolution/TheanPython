import hashlib


def get_md5(bytes_arr):
    md = hashlib.md5()
    md.update(bytes_arr)
    return md.hexdigest()


def iou2(position1, position2):
    p1_x1 = position1.top_left.x
    p1_y1 = position1.top_left.y
    p1_x2 = position1.bottom_right.x
    p1_y2 = position1.bottom_right.y

    p2_x1 = position2.top_left.x
    p2_y1 = position2.top_left.y
    p2_x2 = position2.bottom_right.x
    p2_y2 = position2.bottom_right.y

    start_x = max(p1_x1, p2_x1)
    start_y = max(p1_y1, p2_y1)
    end_x = min(p1_x2, p2_x2)
    end_y = min(p1_y2, p2_y2)

    if start_x > end_x or start_y > end_y:
        ratio = 0
    else:
        intersection_area = (end_x - start_x) * (end_y - start_y)
        area1 = (p1_x2 - p1_x1) * (p1_y2 - p1_y1)
        area2 = (p2_x2 - p2_x1) * (p2_y2 - p2_y1)
        ratio = intersection_area / (area1 + area2 - intersection_area)
    return round(ratio, 2)
