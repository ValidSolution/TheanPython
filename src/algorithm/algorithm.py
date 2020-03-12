import hashlib


def get_md5(bytes_arr):
    md = hashlib.md5()
    md.update(bytes_arr)
    return md.hexdigest()


def iou2(position1, position2):
    p1_x1 = position1[0]
    p1_y1 = position1[1]
    p1_x2 = position1[2]
    p1_y2 = position1[3]

    p2_x1 = position2[0]
    p2_y1 = position2[1]
    p2_x2 = position2[2]
    p2_y2 = position2[3]

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


# return the minimum 2^n which is not less than the given num
def get_init_size(num):
    if num <= 1:
        return 1
    num -= 1
    num |= num >> 1
    num |= num >> 2
    num |= num >> 4
    num |= num >> 8
    num |= num >> 16
    num += 1
    return num


if __name__ == "__main__":
    print(get_init_size(123664))
