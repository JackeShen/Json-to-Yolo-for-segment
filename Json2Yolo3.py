import os
import json

def convert_to_polygon_format(json_folder, txt_folder, label_map):
    """将JSON文件转换为多边形标注格式"""
    if not os.path.exists(txt_folder):
        os.makedirs(txt_folder)

    for json_file in os.listdir(json_folder):
        if json_file.endswith('.json'):
            json_path = os.path.join(json_folder, json_file)
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            image_width = data['imageWidth']
            image_height = data['imageHeight']

            yolo_data = []
            for shape in data['shapes']:
                label = shape['label']
                points = shape['points']

                # 归一化坐标点
                norm_points = [(x / image_width, y / image_height) for (x, y) in points]

                # 将点格式化为YOLO多边形格式
                formatted_points = "".join(f" {x:.6f} {y:.6f}" for (x, y) in norm_points)

                # 获取类别ID
                class_id = label_map.get(label, -1)
                if class_id == -1:
                    print(f"警告：标签'{label}'没有在label_map中找到，跳过此对象。")
                    continue

                # 生成多边形标注字符串
                yolo_data.append(f"{class_id}{formatted_points}")

            # 保存为TXT文件
            txt_file = os.path.join(txt_folder, os.path.splitext(json_file)[0] + '.txt')
            with open(txt_file, 'w', encoding='utf-8') as f:
                f.write("\n".join(yolo_data))

            print(f"转换完成：{json_file} -> {os.path.basename(txt_file)}")

# 用于映射标签到类别ID
label_map = {
    "Cable": 0,
    "tower_lattice": 1,
    "tower_wooden": 2,
    "cable": 3,
    "void": 4,
    "tower_tucohy": 5
    # 添加更多标签映射...
}

# JSON文件所在文件夹路径
json_folder = 'D:/SHD/annotations/'

# 转换后的多边形标注文件保存路径
txt_folder = 'D:/SHD/json2yolo2/'

# 执行转换
convert_to_polygon_format(json_folder, txt_folder, label_map)
