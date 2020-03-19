import hashlib
import numpy


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


def find_lcseque(s1, s2):
    # 生成字符串长度加1的0矩阵，m用来保存对应位置匹配的结果
    m = [[0 for x in range(len(s2) + 1)] for y in range(len(s1) + 1)]
    # d用来记录转移方向
    d = [[None for x in range(len(s2) + 1)] for y in range(len(s1) + 1)]

    for p1 in range(len(s1)):
        for p2 in range(len(s2)):
            if s1[p1] == s2[p2]:  # 字符匹配成功，则该位置的值为左上方的值加1
                m[p1 + 1][p2 + 1] = m[p1][p2] + 1
                d[p1 + 1][p2 + 1] = 'ok'
            elif m[p1 + 1][p2] > m[p1][p2 + 1]:  # 左值大于上值，则该位置的值为左值，并标记回溯时的方向
                m[p1 + 1][p2 + 1] = m[p1 + 1][p2]
                d[p1 + 1][p2 + 1] = 'left'
            else:  # 上值大于左值，则该位置的值为上值，并标记方向up
                m[p1 + 1][p2 + 1] = m[p1][p2 + 1]
                d[p1 + 1][p2 + 1] = 'up'
    (p1, p2) = (len(s1), len(s2))
    numpy.array(d)
    s = []
    while m[p1][p2]:  # 不为None时
        c = d[p1][p2]
        if c == 'ok':  # 匹配成功，插入该字符，并向左上角找下一个
            s.append(s1[p1 - 1])
            p1 -= 1
            p2 -= 1
        if c == 'left':  # 根据标记，向左找下一个
            p2 -= 1
        if c == 'up':  # 根据标记，向上找下一个
            p1 -= 1
    s.reverse()
    return ''.join(s)


if __name__ == "__main__":
    print(get_init_size(123664))
