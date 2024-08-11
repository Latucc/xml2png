import glob
# import sys

import cairosvg

# owidth = int(sys.argv[1])
# owidth=0
wd=input('输出宽度(像素,不输入则使用原始宽度):')
if wd=='':
    wd=0
owidth=int(wd)

def convert_svg_to_png(svg_file_path, png_file_path):
    if owidth == 0:
        cairosvg.svg2png(url=svg_file_path, write_to=png_file_path)
    else:
        cairosvg.svg2png(url=svg_file_path, write_to=png_file_path, output_width=owidth)


svg_files = glob.glob(r'..\svg\*.svg')
for svg_file in svg_files:
    fname = svg_file.split('\\')[-1][:-4]
    png_file_path = f'../png/{fname}.png'
    try:
        convert_svg_to_png(svg_file, png_file_path)
        print(f'success: {svg_file}')
    except:
        print(f'error: {svg_file}')