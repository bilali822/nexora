from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import os

OUT = Path.home() / 'nexora' / 'media' / 'projects' / 'covers'
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1280, 900

def load_font(size, bold=False):
    candidates = [
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
    ]
    for p in candidates:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def browser_bar(draw):
    draw.rectangle([0, 0, W, 50], fill='#1e2235')
    draw.ellipse([20, 18, 36, 34], fill='#ff5f57')
    draw.ellipse([46, 18, 62, 34], fill='#febc2e')
    draw.ellipse([72, 18, 88, 34], fill='#28c840')
    draw.rounded_rectangle([110, 12, W-20, 38], 13, fill='#2a3355')
    draw.text((130, 18), 'your-site.com', fill='#6b7a9e', font=load_font(14))

def make_fashion():
    img = Image.new('RGB', (W, H), '#ffffff')
    d = ImageDraw.Draw(img)

    # Nav
    d.rectangle([0, 50, W, 120], fill='#ffffff')
    d.line([0, 120, W, 120], fill='#eee', width=1)
    d.text((60, 76), 'VOGUE.', fill='#111', font=load_font(24, bold=True))
    for i, m in enumerate(['New In', 'Women', 'Men', 'Sale']):
        d.text((520 + i*130, 82), m, fill='#666', font=load_font(15))
    d.rounded_rectangle([1140, 70, 1220, 105], 18, fill='#111')
    d.text((1155, 79), 'Cart', fill='#fff', font=load_font(14, bold=True))

    # Hero left
    for y in range(120, 620):
        t = (y-120)/500
        r = int(245 + (237-245)*t); g = int(243 + (233-243)*t); b = int(255 + (254-255)*t)
        d.line([0, y, W//2, y], fill=(r, g, b))
    d.text((60, 220), 'Summer', fill='#111', font=load_font(58, bold=True))
    d.text((60, 285), 'Collection', fill='#8B5CF6', font=load_font(58, bold=True))
    d.text((60, 350), '2026', fill='#111', font=load_font(58, bold=True))
    d.text((60, 450), 'Discover the new arrivals with premium', fill='#666', font=load_font(16))
    d.text((60, 472), 'fabrics and modern cuts.', fill='#666', font=load_font(16))
    d.rounded_rectangle([60, 520, 220, 565], 22, fill='#111')
    d.text((82, 533), 'Shop Now →', fill='#fff', font=load_font(15, bold=True))

    # Hero right (purple gradient)
    for y in range(120, 620):
        t = (y-120)/500
        r = int(196 + (167-196)*t); g = int(181 + (139-181)*t); b = int(253 + (250-253)*t)
        d.line([W//2, y, W, y], fill=(r, g, b))
    d.rounded_rectangle([820, 220, 1080, 560], 130, fill=(255, 255, 255, 80))

    # Products
    px = 60
    for i in range(4):
        x = px + i*300
        d.rounded_rectangle([x, 660, x+280, 870], 16, fill='#f8f8f8')
        d.rounded_rectangle([x, 660, x+280, 800], 16, fill='#e0e7ff')
        d.rounded_rectangle([x+40, 680, x+240, 780], 50, fill='#c7d2fe')
        d.text((x+16, 810), '★★★★★', fill='#fbbf24', font=load_font(12))
        d.text((x+16, 828), f'Product {i+1}', fill='#111', font=load_font(14, bold=True))
        d.text((x+16, 848), f'${39 + i*30}', fill='#8B5CF6', font=load_font(15, bold=True))

    browser_bar(d)
    img.save(OUT / 'fashion-store.png')
    print('✅ fashion-store.png')

def make_dashboard():
    img = Image.new('RGB', (W, H), '#0f1524')
    d = ImageDraw.Draw(img)

    # Sidebar
    d.rectangle([0, 50, 240, H], fill='#0a0f1c')
    d.text((30, 80), 'Nexora.', fill='#fff', font=load_font(22, bold=True))
    for i, item in enumerate(['Dashboard', 'Orders', 'Drivers', 'Routes', 'Reports', 'Settings']):
        y = 150 + i*50
        if i == 0:
            d.rounded_rectangle([20, y-10, 220, y+30], 8, fill='#1a2240')
        d.ellipse([30, y, 46, y+16], fill='#8B5CF6' if i == 0 else '#3a4466')
        d.text((60, y+2), item, fill='#fff' if i == 0 else '#8892aa', font=load_font(14))

    # Topbar
    d.rectangle([240, 50, W, 110], fill='#0a0f1c')
    d.text((280, 74), 'Dashboard Overview', fill='#fff', font=load_font(20, bold=True))
    d.ellipse([1180, 68, 1210, 98], fill='#8B5CF6')

    # KPI cards
    for i, (label, val, col) in enumerate([
        ('Total Shipments', '12,458', '#5B8CFF'),
        ('In Transit', '342', '#F59E0B'),
        ('Delivered', '11,890', '#10B981'),
    ]):
        x = 280 + i*320
        d.rounded_rectangle([x, 140, x+290, 250], 14, fill='#131a30')
        d.text((x+20, 160), label, fill='#8892aa', font=load_font(13))
        d.text((x+20, 185), val, fill='#fff', font=load_font(32, bold=True))
        d.rounded_rectangle([x+20, 232, x+80, 240], 4, fill=col)

    # Chart card
    d.rounded_rectangle([280, 280, 740, 620], 14, fill='#131a30')
    d.text((300, 300), 'Delivery Analytics', fill='#fff', font=load_font(16, bold=True))
    pts = [(320, 560), (390, 500), (460, 520), (530, 460), (600, 490), (670, 400), (720, 380)]
    for i in range(len(pts)-1):
        d.line([pts[i], pts[i+1]], fill='#5B8CFF', width=3)
    for p in pts:
        d.ellipse([p[0]-4, p[1]-4, p[0]+4, p[1]+4], fill='#8B5CF6')
    # Grid lines
    for y in range(360, 620, 60):
        d.line([300, y, 720, y], fill='#1e2540', width=1)

    # Pie-ish card
    d.rounded_rectangle([770, 280, 1230, 620], 14, fill='#131a30')
    d.text((790, 300), 'Shipment Status', fill='#fff', font=load_font(16, bold=True))
    d.ellipse([820, 360, 1060, 600], outline='#1e2540', width=30)
    d.arc([820, 360, 1060, 600], -90, 40, fill='#5B8CFF', width=30)
    d.arc([820, 360, 1060, 600], 40, 180, fill='#10B981', width=30)
    d.arc([820, 360, 1060, 600], 180, 270, fill='#F59E0B', width=30)
    for i, (label, col) in enumerate([('Delivered', '#10B981'), ('In Transit', '#F59E0B'), ('Pending', '#5B8CFF')]):
        y = 400 + i*30
        d.rounded_rectangle([1090, y, 1105, y+15], 3, fill=col)
        d.text((1115, y), label, fill='#8892aa', font=load_font(12))

    # Bottom cards
    for i in range(3):
        x = 280 + i*320
        d.rounded_rectangle([x, 650, x+290, 860], 14, fill='#131a30')
        d.text((x+20, 670), f'Driver #{i+1}', fill='#fff', font=load_font(14, bold=True))
        d.ellipse([x+20, 700, x+60, 740], fill='#8B5CF6')
        d.text((x+75, 705), f'Route {chr(65+i)}', fill='#8892aa', font=load_font(12))
        d.text((x+75, 722), '98% on time', fill='#10B981', font=load_font(12))
        d.rounded_rectangle([x+20, 760, x+270, 780], 4, fill='#1e2540')
        d.rounded_rectangle([x+20, 760, x+20+180, 780], 4, fill='#10B981')

    browser_bar(d)
    img.save(OUT / 'logistics-dashboard.png')
    print('✅ logistics-dashboard.png')

def make_edu():
    img = Image.new('RGB', (W, H), '#ffffff')
    d = ImageDraw.Draw(img)

    # Nav
    d.rectangle([0, 50, W, 110], fill='#ffffff')
    d.line([0, 110, W, 110], fill='#eee')
    d.text((60, 72), 'EDU.', fill='#10B981', font=load_font(24, bold=True))
    for i, m in enumerate(['Courses', 'Teachers', 'Pricing', 'About']):
        d.text((520 + i*120, 78), m, fill='#666', font=load_font(15))
    d.rounded_rectangle([1140, 68, 1220, 100], 16, fill='#10B981')
    d.text((1158, 75), 'Sign In', fill='#fff', font=load_font(13, bold=True))

    # Hero
    d.rectangle([0, 110, W, 560], fill='#f0fdf4')
    d.text((60, 200), 'Learn From The', fill='#111', font=load_font(50, bold=True))
    d.text((60, 260), 'Best Teachers', fill='#10B981', font=load_font(50, bold=True))
    d.text((60, 340), 'Access 500+ courses with lifetime updates.', fill='#555', font=load_font(16))
    d.rounded_rectangle([60, 400, 220, 445], 22, fill='#10B981')
    d.text((85, 413), 'Start Learning', fill='#fff', font=load_font(15, bold=True))
    d.rounded_rectangle([240, 400, 380, 445], 22, outline='#10B981', width=2)
    d.text((270, 413), 'View Courses', fill='#10B981', font=load_font(15, bold=True))

    # Hero image
    d.rounded_rectangle([720, 170, 1220, 500], 20, fill='#10B981')
    d.rounded_rectangle([760, 200, 1180, 470], 15, fill='#ffffff')
    d.ellipse([900, 260, 1040, 400], fill='#d1fae5')
    d.text((920, 340), '▶', fill='#10B981', font=load_font(60, bold=True))

    # Courses
    d.text((60, 610), 'Popular Courses', fill='#111', font=load_font(24, bold=True))
    for i in range(4):
        x = 60 + i*300
        d.rounded_rectangle([x, 660, x+280, 870], 14, fill='#f8fafc')
        colors = ['#10B981', '#5B8CFF', '#F59E0B', '#8B5CF6']
        d.rounded_rectangle([x, 660, x+280, 770], 14, fill=colors[i])
        d.text((x+20, 785), f'Course {i+1}', fill='#111', font=load_font(14, bold=True))
        d.text((x+20, 808), '$49.99', fill=colors[i], font=load_font(15, bold=True))
        d.text((x+20, 835), '★★★★★ (245)', fill='#fbbf24', font=load_font(11))

    browser_bar(d)
    img.save(OUT / 'edu-platform.png')
    print('✅ edu-platform.png')

def make_realestate():
    img = Image.new('RGB', (W, H), '#ffffff')
    d = ImageDraw.Draw(img)

    d.rectangle([0, 50, W, 110], fill='#ffffff')
    d.text((60, 72), 'ESTATE.', fill='#0EA5E9', font=load_font(24, bold=True))
    for i, m in enumerate(['Buy', 'Rent', 'Sell', 'Agents']):
        d.text((520 + i*120, 78), m, fill='#666', font=load_font(15))
    d.rounded_rectangle([1140, 68, 1220, 100], 16, fill='#0EA5E9')
    d.text((1160, 75), 'Contact', fill='#fff', font=load_font(13, bold=True))

    # Hero with bg
    d.rectangle([0, 110, W, 520], fill='#0EA5E9')
    for y in range(110, 520):
        t = (y-110)/410
        r = int(14 + (99-14)*t); g = int(165 + (102-165)*t); b = int(233 + (241-233)*t)
        d.line([0, y, W, y], fill=(r, g, b))
    d.text((60, 220), 'Find Your', fill='#fff', font=load_font(56, bold=True))
    d.text((60, 285), 'Dream Home', fill='#fff', font=load_font(56, bold=True))
    d.text((60, 370), 'Browse 10,000+ properties across the country.', fill='#e0f2fe', font=load_font(16))

    # Search bar
    d.rounded_rectangle([60, 420, 900, 490], 35, fill='#ffffff')
    d.text((90, 445), '📍 Location', fill='#888', font=load_font(14))
    d.line([300, 435, 300, 475], fill='#ddd', width=1)
    d.text((330, 445), '🏠 Type', fill='#888', font=load_font(14))
    d.line([540, 435, 540, 475], fill='#ddd', width=1)
    d.text((570, 445), '💰 Price', fill='#888', font=load_font(14))
    d.rounded_rectangle([740, 432, 880, 478], 23, fill='#0EA5E9')
    d.text((775, 445), 'Search', fill='#fff', font=load_font(15, bold=True))

    # Properties
    d.text((60, 570), 'Featured Properties', fill='#111', font=load_font(24, bold=True))
    for i in range(3):
        x = 60 + i*400
        d.rounded_rectangle([x, 620, x+370, 870], 14, fill='#f8fafc')
        d.rounded_rectangle([x, 620, x+370, 760], 14, fill='#e0f2fe')
        d.rounded_rectangle([x+20, 640, x+120, 740], 8, fill='#bae6fd')
        d.text((x+20, 780), f'Modern Villa {i+1}', fill='#111', font=load_font(15, bold=True))
        d.text((x+20, 805), '📍 Downtown', fill='#888', font=load_font(12))
        d.text((x+20, 830), f'${250 + i*100},000', fill='#0EA5E9', font=load_font(16, bold=True))

    browser_bar(d)
    img.save(OUT / 'real-estate.png')
    print('✅ real-estate.png')

def make_taskapp():
    img = Image.new('RGB', (W, H), '#f8fafc')
    d = ImageDraw.Draw(img)

    d.rectangle([0, 50, 220, H], fill='#1e1b4b')
    d.text((30, 80), 'TASKY.', fill='#fff', font=load_font(22, bold=True))
    for i, item in enumerate(['Board', 'My Tasks', 'Team', 'Calendar', 'Reports']):
        y = 150 + i*50
        if i == 0:
            d.rounded_rectangle([15, y-10, 205, y+30], 8, fill='#312e81')
        d.text((35, y+2), item, fill='#fff' if i == 0 else '#a5b4fc', font=load_font(14))

    d.rectangle([220, 50, W, 120], fill='#ffffff')
    d.line([220, 120, W, 120], fill='#e5e7eb')
    d.text((260, 76), 'My Board', fill='#111', font=load_font(20, bold=True))
    for i, (l, c) in enumerate([('All', '#8B5CF6'), ('Active', '#aaa'), ('Done', '#aaa')]):
        x = 500 + i*90
        if i == 0:
            d.rounded_rectangle([x, 78, x+70, 105], 13, fill='#8B5CF6')
            d.text((x+22, 84), l, fill='#fff', font=load_font(13))
        else:
            d.text((x+15, 84), l, fill='#888', font=load_font(13))
    d.rounded_rectangle([1150, 72, 1230, 108], 18, fill='#8B5CF6')
    d.text((1165, 80), '+ New', fill='#fff', font=load_font(13, bold=True))

    # Kanban columns
    cols = [('To Do', '#8B5CF6', 4), ('In Progress', '#F59E0B', 3), ('Done', '#10B981', 2)]
    for ci, (title, col, n) in enumerate(cols):
        x = 260 + ci*330
        d.rounded_rectangle([x, 150, x+300, 870], 14, fill='#eef2f7')
        d.rounded_rectangle([x+15, 165, x+165, 195], 15, fill=col)
        d.text((x+30, 172), title, fill='#fff', font=load_font(13, bold=True))
        d.text((x+240, 172), f'{n}', fill='#555', font=load_font(14, bold=True))

        for i in range(n):
            y = 215 + i*140
            d.rounded_rectangle([x+15, y, x+285, y+120], 10, fill='#ffffff')
            d.rounded_rectangle([x+30, y+15, x+120, y+35], 10, fill=col)
            d.text((x+40, y+20), 'Feature', fill='#fff', font=load_font(11))
            d.text((x+30, y+50), f'Task #{i+1}', fill='#111', font=load_font(14, bold=True))
            d.text((x+30, y+75), 'Landing page design', fill='#888', font=load_font(12))
            for j in range(3):
                d.ellipse([x+30+j*22, y+95, x+45+j*22, y+110], fill=['#8B5CF6','#F59E0B','#10B981'][j])

    browser_bar(d)
    img.save(OUT / 'task-manager.png')
    print('✅ task-manager.png')

def make_banking():
    img = Image.new('RGB', (W, H), '#0b1020')
    d = ImageDraw.Draw(img)

    # Left info
    d.text((80, 180), 'Modern Banking', fill='#fff', font=load_font(48, bold=True))
    d.text((80, 245), 'Redefined.', fill='#8B5CF6', font=load_font(48, bold=True))
    d.text((80, 330), 'Design system for a next-gen', fill='#8892aa', font=load_font(16))
    d.text((80, 355), 'mobile banking experience.', fill='#8892aa', font=load_font(16))

    for i, (label, val) in enumerate([('Users', '50K+'), ('Rating', '4.9★'), ('Countries', '12')]):
        x = 80 + i*160
        d.text((x, 450), val, fill='#fff', font=load_font(28, bold=True))
        d.text((x, 490), label, fill='#8892aa', font=load_font(13))

    # Phone 1
    d.rounded_rectangle([720, 130, 990, 800], 40, fill='#1a2240', outline='#2a3355', width=3)
    d.rounded_rectangle([735, 145, 975, 785], 30, fill='#0d1424')
    d.ellipse([840, 155, 870, 170], fill='#0a0f1c')

    # Screen 1 content
    d.text((760, 200), 'Good morning', fill='#8892aa', font=load_font(12))
    d.text((760, 220), 'Sarah 👋', fill='#fff', font=load_font(20, bold=True))

    d.rounded_rectangle([755, 270, 955, 410], 20, fill='#8B5CF6')
    d.text((775, 290), 'Total Balance', fill='#e9d5ff', font=load_font(12))
    d.text((775, 315), '$24,890.00', fill='#fff', font=load_font(28, bold=True))
    d.text((775, 370), '•••• 4521', fill='#e9d5ff', font=load_font(13))

    d.text((760, 440), 'Quick Actions', fill='#fff', font=load_font(13, bold=True))
    for i, label in enumerate(['Send', 'Request', 'Top up']):
        x = 755 + i*70
        d.rounded_rectangle([x, 470, x+58, 528], 14, fill='#1e2540')
        d.ellipse([x+18, 485, x+40, 507], fill='#8B5CF6')
        d.text((x+8, 535), label, fill='#8892aa', font=load_font(10))

    for i in range(3):
        y = 580 + i*65
        d.rounded_rectangle([755, y, 955, y+55], 12, fill='#131a30')
        d.ellipse([765, y+12, 795, y+42], fill=['#10B981','#F59E0B','#5B8CFF'][i])
        d.text((805, y+12), ['Netflix','Spotify','Uber'][i], fill='#fff', font=load_font(12))
        d.text((805, y+32), 'Subscription', fill='#8892aa', font=load_font(10))
        d.text((910, y+20), ['-$15','-$10','-$24'][i], fill='#ff6b6b', font=load_font(12, bold=True))

    # Phone 2 (smaller, behind)
    d.rounded_rectangle([1030, 220, 1230, 720], 30, fill='#1a2240', outline='#2a3355', width=2)
    d.rounded_rectangle([1042, 232, 1218, 708], 22, fill='#0d1424')
    d.text((1060, 270), 'Statistics', fill='#fff', font=load_font(14, bold=True))
    for i in range(12):
        x = 1060 + i*13
        h = [40, 60, 30, 80, 50, 90, 45, 70, 55, 85, 35, 65][i]
        d.rounded_rectangle([x, 500-h, x+8, 500], 3, fill='#8B5CF6' if i % 3 == 0 else '#3a4466')
    d.text((1060, 540), 'This Month', fill='#8892aa', font=load_font(11))
    d.text((1060, 560), '+$2,450', fill='#10B981', font=load_font(18, bold=True))

    browser_bar(d)
    img.save(OUT / 'banking-app.png')
    print('✅ banking-app.png')


if __name__ == '__main__':
    make_fashion()
    make_dashboard()
    make_edu()
    make_realestate()
    make_taskapp()
    make_banking()
    print(f'\n🎉 كل الصور محفوظة في: {OUT}')
