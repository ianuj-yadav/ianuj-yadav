import re, html
from PIL import Image, ImageDraw, ImageFont

def render_heatmap_to_png(svg_path, png_path):
    with open(svg_path, 'r', encoding='utf-8') as f:
        svg = f.read()
    
    # Extract dimensions from svg tag: width="850" height="230" roughly
    w_match = re.search(r'width="(\d+)"', svg)
    h_match = re.search(r'height="(\d+)"', svg)
    w = int(w_match.group(1)) if w_match else 850
    h = int(h_match.group(1)) if h_match else 230
    
    img = Image.new('RGB', (w, h), '#0a0e14')
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype('consola.ttf', 11)
        font_bold = ImageFont.truetype('consolab.ttf', 12)
    except Exception:
        font = ImageFont.load_default()
        font_bold = ImageFont.load_default()
        
    # Draw frame border
    draw.rounded_rectangle([(0, 0), (w-1, h-1)], radius=12, outline='#1f6feb', width=1)
    # Titlebar line
    draw.line([(0, 30), (w, 30)], fill='#1f6feb', width=1)
    # Title dots
    colors = ['#ff5f56', '#ffbd2e', '#27c93f']
    for i, col in enumerate(colors):
        cx = 22 + i * 16
        draw.ellipse([(cx-5, 15-5), (cx+5, 15+5)], fill=col)
    
    # Title text
    draw.text((w/2, 15), "ianuj-yadav@github: ~/contributions --graph", fill='#7d8590', font=font, anchor='mm')
    
    # Draw rects
    rects = re.findall(r'<rect[^>]*x="([^"]+)" y="([^"]+)" width="([^"]+)" height="([^"]+)" rx="([^"]+)" fill="([^"]+)"', svg)
    for x, y, rw, rh, rx, fill in rects:
        if float(y) == 0.5 or float(y) == 0:
            continue
        x, y, rw, rh = float(x), float(y), float(rw), float(rh)
        draw.rounded_rectangle([(x, y), (x+rw, y+rh)], radius=float(rx), fill=fill)
        
    # Draw texts
    texts = re.findall(r'<text[^>]*x="([^"]+)" y="([^"]+)"[^>]*fill="([^"]+)"[^>]*font-size="([^"]+)"(?:[^>]*text-anchor="([^"]+)")?[^>]*>(.*?)</text>', svg)
    for x_str, y_str, fill, fsize, anchor, content in texts:
        if '--graph' in content:
            continue
        x = float(x_str)
        y = float(y_str)
        
        # Unescape and clean tspan
        content = html.unescape(content)
        if '<tspan' in content:
            # strip tspan tags but keep text
            clean = re.sub(r'<[^>]+>', '', content)
            draw.text((x, y-10), clean, fill=fill, font=font_bold if 'font-weight="700"' in content else font, anchor='rm' if anchor=='end' else 'la')
        else:
            clean = re.sub(r'<[^>]+>', '', content)
            draw.text((x, y-10), clean, fill=fill, font=font, anchor='rm' if anchor=='end' else 'la')
            
    img.save(png_path)
    print(f"Rendered heatmap preview to {png_path}")

if __name__ == '__main__':
    render_heatmap_to_png('contrib-heatmap.svg', 'contrib-heatmap-preview.png')
