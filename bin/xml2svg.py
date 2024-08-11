import glob
import subprocess
from xml.etree import ElementTree as ET

# wd=input('输出宽度(像素,不输入则使用原始宽度):')
# if wd=='':
#     wd=0

def runsub(*args):
    simpresult = subprocess.run([arg for arg in args])
    # print(simpresult)
    # return simpresult

def convertSvgToPng():
    runsub('python', 'svg2png.py')

def convertXmlToSvg(input):
    # 读取 XML 文件内容
    with open(input, 'r', encoding='utf-8') as file:
        xml_content = file.read()
    # 解析 XML 内容
    root = ET.fromstring(xml_content)
    # 从 XML 中读取属性
    width = root.get('{http://schemas.android.com/apk/res/android}width', '2000dp')[:-2]
    height = root.get('{http://schemas.android.com/apk/res/android}height', '2000dp')[:-2]
    viewport_width = root.get('{http://schemas.android.com/apk/res/android}viewportWidth', '2000.0')
    viewport_height = root.get('{http://schemas.android.com/apk/res/android}viewportHeight', '2000.0')

    # if wd!='':
    #     x=int(wd)/int(float(width))
    #     width=int(wd)
    #     height=int(x*int(float(height)))
    #     # viewport_width=x*float(viewport_width)
    #     # viewport_height=x*float(viewport_height)
    #     # viewport_width=width
    #     # viewport_height=height

    # 创建 SVG 文件头
    svg_header = f'''<svg id="vector" xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {viewport_width} {viewport_height}">\n'''
    svg_footer = '</svg>'
    svg_paths = []
    # 处理每个 path 元素
    for i, path in enumerate(root.findall('.//path')):
        cl = path.get('{http://schemas.android.com/apk/res/android}fillColor', '#000000')
        path_data = path.get('{http://schemas.android.com/apk/res/android}pathData', '')
        stroke_width = path.get('{http://schemas.android.com/apk/res/android}strokeWidth', '1.0')
        fill_type = path.get('{http://schemas.android.com/apk/res/android}fillType', 'evenodd')

        if len(cl)==9:
            fill_color=cl[0]+cl[3:]+cl[1:3]
        else:
            fill_color=cl
        # 处理颜色格式（Android 颜色格式与 SVG 颜色格式兼容）
        svg_path = f'<path fill="{fill_color}" d="{path_data}" stroke-width="{stroke_width}" fill-rule="{fill_type}" id="path_{i}"/>\n'
        svg_paths.append(svg_path)

    # 生成 SVG 内容
    svg_content = svg_header + ''.join(svg_paths) + svg_footer

    fname=xml_file.split('\\')[-1][:-4]
    # 写入 SVG 文件
    with open(f'../svg/{fname}.svg', 'w') as f:
        f.write(svg_content)



xml_files = glob.glob(r'..\xml\*.xml')
for xml_file in xml_files:
    try:
        convertXmlToSvg(xml_file)
        print(f'success: {xml_file}')
    except:
        print(f'error: {xml_file}')

input('是否生成png,直接回车继续:')

convertSvgToPng()