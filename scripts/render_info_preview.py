import re
from PIL import Image, ImageDraw, ImageFont

def render_info_card_to_png(svg_path, png_path):
    with open(svg_path, 'r', encoding='utf-8') as f:
        svg = f.read()
    
    img = Image.new('RGB', (480, 378), '#0d1117')
    draw = ImageDraw.Draw(img)
    
    try:
        font_main = ImageFont.truetype('consola.ttf', 13)
        font_bold = ImageFont.truetype('consolab.ttf', 13)
        font_title = ImageFont.truetype('consola.ttf', 12)
    except Exception:
        font_main = ImageFont.load_default()
        font_bold = ImageFont.load_default()
        font_title = ImageFont.load_default()
        
    # Draw frame border
    draw.rounded_rectangle([(0, 0), (479, 377)], radius=12, outline='#30363d', width=1)
    # Titlebar line
    draw.line([(0, 30), (480, 30)], fill='#30363d', width=1)
    # Title dots
    colors = ['#ff5f56', '#ffbd2e', '#27c93f']
    for i, col in enumerate(colors):
        cx = 20 + i * 16
        draw.ellipse([(cx-5, 15-5), (cx+5, 15+5)], fill=col)
    
    # Title text
    draw.text((240, 15), "ianuj-yadav@github: ~$ neofetch", fill='#7d8590', font=font_title, anchor='mm')
    
    # Parse text elements from SVG
    # We can match all <text ...> ... </text> or <line ...> in the body
    texts = re.findall(r'<text x="([^"]+)" y="([^"]+)"[^>]*fill="([^"]+)"[^>]*font-size="([^"]+)"(?:[^>]*font-weight="([^"]+)")?[^>]*>(.*?)</text>', svg)
    for x_str, y_str, fill, fsize, fweight, content in texts:
        if 'neofetch' in content:
            continue
        x = float(x_str)
        y = float(y_str)
        
        # Clean tspan if any
        if '<tspan' in content:
            # extract tspan pieces
            pieces = re.findall(r'<tspan fill="([^"]+)">([^<]+)</tspan>', content)
            curr_x = x
            for t_fill, t_text in pieces:
                draw.text((curr_x, y-10), t_text, fill=t_fill, font=font_bold if fweight=='700' else font_main)
                curr_x += len(t_text) * 8
            continue
            
        clean_text = re.sub(r'<[^>]+>', '', content).replace('&#8212;', '—')
        f = font_bold if fweight == '700' else font_main
        draw.text((x, y-10), clean_text, fill=fill, font=f)
        
    # Lines for section dividers
    lines = re.findall(r'<line x1="([^"]+)" y1="([^"]+)" x2="([^"]+)" y2="([^"]+)" stroke="([^"]+)"', svg)
    for x1, y1, x2, y2, stroke in lines:
        if float(y1) == 30.0:
            continue
        draw.line([(float(x1), float(y1)), (float(x2), float(y2))], fill=stroke, width=1)
        
    # Green circles for bullets
    circles = re.findall(r'<circle cx="([^"]+)" cy="([^"]+)" r="([^"]+)" fill="([^"]+)"', svg)
    for cx, cy, r, fill in circles:
        if float(cy) < 30:
            continue
        cx, cy, r = float(cx), float(cy), float(r)
        draw.ellipse([(cx-r, cy-r), (cx+r, cy+r)], fill=fill)
        
    img.save(png_path)
    print(f"Rendered info card preview to {png_path}")

if __name__ == '__main__':
    render_info_card_to_png('info-card.svg', 'info-card-preview.png')
