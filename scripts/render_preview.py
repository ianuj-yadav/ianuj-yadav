import re
from PIL import Image, ImageDraw, ImageFont

def render_svg_to_png(svg_path, png_path):
    with open(svg_path, 'r', encoding='utf-8') as f:
        svg = f.read()
    
    # Extract all text rows
    lines = re.findall(r'<text xml:space="preserve"[^>]*>(.*?)</text>', svg)
    
    # Canvas size 840 x 875
    img = Image.new('RGB', (840, 875), '#0d1117')
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype('consola.ttf', 13)
    except Exception:
        font = ImageFont.load_default()
        
    y = 45
    for line in lines:
        clean_line = line.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&').replace('&#8212;', '—')
        draw.text((20, y), clean_line, fill='#c9d1d9', font=font)
        y += 15
        
    img.save(png_path)
    print(f"Rendered preview PNG to {png_path}")

if __name__ == '__main__':
    render_svg_to_png('avi-ascii.svg', 'avi-ascii-preview.png')
