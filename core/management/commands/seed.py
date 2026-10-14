from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from core.models import Service, Testimonial
from projects.models import Project


def make_mockup(title, subtitle, c1, c2, kind='site'):
    """يولّد صورة SVG بشكل موك أب موقع"""
    if kind == 'store':
        cards = ''.join([
            f'<rect x="{80 + i*220}" y="440" width="190" height="220" rx="12" fill="rgba(255,255,255,0.08)"/>'
            f'<rect x="{80 + i*220}" y="460" width="190" height="120" rx="8" fill="{c1}" opacity="0.5"/>'
            f'<rect x="{95 + i*220}" y="595" width="120" height="12" rx="6" fill="rgba(255,255,255,0.5)"/>'
            f'<rect x="{95 + i*220}" y="615" width="80" height="10" rx="5" fill="rgba(255,255,255,0.3)"/>'
            for i in range(4)
        ])
        body = cards
    elif kind == 'dashboard':
        body = (
            f'<rect x="60" y="420" width="260" height="280" rx="12" fill="rgba(255,255,255,0.08)"/>'
            f'<rect x="340" y="420" width="400" height="130" rx="12" fill="rgba(255,255,255,0.08)"/>'
            f'<rect x="340" y="570" width="400" height="130" rx="12" fill="rgba(255,255,255,0.08)"/>'
            f'<polyline points="370,510 430,470 490,490 550,440 620,460 700,420" '
            f'stroke="{c1}" stroke-width="4" fill="none" stroke-linecap="round"/>'
            f'<circle cx="700" cy="420" r="6" fill="{c2}"/>'
            f'<rect x="90" y="460" width="200" height="14" rx="7" fill="rgba(255,255,255,0.4)"/>'
            f'<rect x="90" y="490" width="160" height="12" rx="6" fill="rgba(255,255,255,0.25)"/>'
            f'<rect x="90" y="520" width="180" height="12" rx="6" fill="rgba(255,255,255,0.25)"/>'
            f'<rect x="90" y="550" width="140" height="12" rx="6" fill="rgba(255,255,255,0.25)"/>'
        )
    elif kind == 'webapp':
        body = (
            f'<rect x="60" y="420" width="200" height="280" rx="12" fill="rgba(255,255,255,0.08)"/>'
            f'<rect x="280" y="420" width="200" height="130" rx="12" fill="{c1}" opacity="0.4"/>'
            f'<rect x="280" y="570" width="200" height="130" rx="12" fill="rgba(255,255,255,0.08)"/>'
            f'<rect x="500" y="420" width="240" height="280" rx="12" fill="rgba(255,255,255,0.08)"/>'
            f'<rect x="80" y="450" width="160" height="12" rx="6" fill="rgba(255,255,255,0.4)"/>'
            f'<rect x="80" y="480" width="120" height="10" rx="5" fill="rgba(255,255,255,0.25)"/>'
            f'<rect x="80" y="505" width="140" height="10" rx="5" fill="rgba(255,255,255,0.25)"/>'
            f'<rect x="80" y="530" width="100" height="10" rx="5" fill="rgba(255,255,255,0.25)"/>'
            f'<circle cx="600" cy="480" r="50" fill="{c2}" opacity="0.6"/>'
            f'<circle cx="600" cy="480" r="30" fill="rgba(255,255,255,0.15)"/>'
            f'<rect x="530" y="570" width="180" height="12" rx="6" fill="rgba(255,255,255,0.4)"/>'
            f'<rect x="530" y="595" width="140" height="10" rx="5" fill="rgba(255,255,255,0.25)"/>'
        )
    elif kind == 'ui':
        body = (
            f'<rect x="150" y="420" width="220" height="400" rx="30" fill="rgba(255,255,255,0.08)" stroke="rgba(255,255,255,0.2)" stroke-width="2"/>'
            f'<rect x="170" y="450" width="180" height="12" rx="6" fill="rgba(255,255,255,0.4)"/>'
            f'<rect x="170" y="480" width="140" height="60" rx="10" fill="{c1}" opacity="0.5"/>'
            f'<rect x="170" y="555" width="180" height="10" rx="5" fill="rgba(255,255,255,0.3)"/>'
            f'<rect x="170" y="575" width="160" height="10" rx="5" fill="rgba(255,255,255,0.3)"/>'
            f'<rect x="170" y="620" width="180" height="80" rx="10" fill="rgba(255,255,255,0.08)"/>'
            f'<rect x="170" y="720" width="180" height="44" rx="22" fill="{c2}"/>'
            f'<rect x="420" y="440" width="230" height="300" rx="20" fill="rgba(255,255,255,0.06)" stroke="rgba(255,255,255,0.15)"/>'
            f'<circle cx="535" cy="530" r="40" fill="{c1}" opacity="0.5"/>'
            f'<rect x="450" y="600" width="170" height="12" rx="6" fill="rgba(255,255,255,0.4)"/>'
            f'<rect x="450" y="625" width="130" height="10" rx="5" fill="rgba(255,255,255,0.25)"/>'
        )
    else:  # website
        body = (
            f'<rect x="60" y="420" width="680" height="200" rx="14" fill="{c1}" opacity="0.35"/>'
            f'<rect x="100" y="470" width="300" height="16" rx="8" fill="rgba(255,255,255,0.6)"/>'
            f'<rect x="100" y="500" width="220" height="12" rx="6" fill="rgba(255,255,255,0.35)"/>'
            f'<rect x="100" y="540" width="120" height="34" rx="17" fill="{c2}"/>'
            f'<rect x="520" y="450" width="180" height="140" rx="10" fill="rgba(255,255,255,0.15)"/>'
            f'<rect x="80" y="650" width="200" height="60" rx="10" fill="rgba(255,255,255,0.08)"/>'
            f'<rect x="300" y="650" width="200" height="60" rx="10" fill="rgba(255,255,255,0.08)"/>'
            f'<rect x="520" y="650" width="200" height="60" rx="10" fill="rgba(255,255,255,0.08)"/>'
        )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="780" viewBox="0 0 800 780">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{c1}"/>
      <stop offset="100%" stop-color="{c2}"/>
    </linearGradient>
    <linearGradient id="bgDark" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0d1424"/>
      <stop offset="100%" stop-color="#131a30"/>
    </linearGradient>
  </defs>

  <!-- خلفية -->
  <rect width="800" height="780" fill="url(#bgDark)"/>

  <!-- شريط المتصفح -->
  <rect x="0" y="0" width="800" height="40" fill="#1a2240"/>
  <circle cx="25" cy="20" r="6" fill="#ff5f57"/>
  <circle cx="45" cy="20" r="6" fill="#febc2e"/>
  <circle cx="65" cy="20" r="6" fill="#28c840"/>
  <rect x="100" y="12" width="500" height="16" rx="8" fill="rgba(255,255,255,0.08)"/>
  <text x="115" y="24" font-family="Arial" font-size="11" fill="rgba(255,255,255,0.5)">{title.lower().replace(' ', '-')}.com</text>

  <!-- هيدر الموقع -->
  <rect x="0" y="40" width="800" height="60" fill="rgba(255,255,255,0.03)"/>
  <circle cx="60" cy="70" r="14" fill="url(#bg)"/>
  <rect x="85" y="64" width="70" height="12" rx="6" fill="rgba(255,255,255,0.5)"/>
  <rect x="420" y="65" width="50" height="10" rx="5" fill="rgba(255,255,255,0.25)"/>
  <rect x="490" y="65" width="50" height="10" rx="5" fill="rgba(255,255,255,0.25)"/>
  <rect x="560" y="65" width="50" height="10" rx="5" fill="rgba(255,255,255,0.25)"/>
  <rect x="630" y="58" width="110" height="26" rx="13" fill="{c2}"/>

  <!-- عنوان المشروع -->
  <text x="60" y="180" font-family="Arial" font-size="42" font-weight="bold" fill="#ffffff">{title}</text>
  <text x="60" y="215" font-family="Arial" font-size="16" fill="rgba(255,255,255,0.55)">{subtitle}</text>
  <rect x="60" y="235" width="70" height="4" rx="2" fill="{c1}"/>

  <!-- محتوى الموقع -->
  {body}

  <!-- تدرج لوني شفاف أسفل -->
  <rect x="0" y="700" width="800" height="80" fill="url(#bgDark)" opacity="0.9"/>
</svg>'''
    return ContentFile(svg.encode('utf-8'))


class Command(BaseCommand):
    help = 'يضيف بيانات تجريبية للموقع'

    def handle(self, *args, **kwargs):
        Service.objects.all().delete()
        Testimonial.objects.all().delete()
        Project.objects.all().delete()

        # ===== الخدمات =====
        services = [
            ('مواقع تعريفية', 'مواقع سريعة ومتجاوبة تعرّف عن نشاطك التجاري بشكل احترافي.', 'fa-globe', 1),
            ('تطبيقات ويب', 'تطبيقات ويب حديثة بـ Django و React مع لوحات تحكم كاملة.', 'fa-code', 2),
            ('متاجر إلكترونية', 'متاجر إلكترونية متكاملة مع سلة شراء، دفع إلكتروني، وإدارة منتجات.', 'fa-shopping-cart', 3),
            ('لوحات تحكم', 'لوحات تحكم إدارية بتصميم عصري وتقارير وإحصائيات مباشرة.', 'fa-chart-line', 4),
            ('تصميم UI/UX', 'تصميم واجهات مستخدم جذابة وتجربة استخدام سلسة.', 'fa-paint-brush', 5),
            ('APIs وتكامل', 'بناء REST APIs وربط الأنظمة والخدمات الخارجية.', 'fa-plug', 6),
        ]
        for title, desc, icon, order in services:
            Service.objects.create(title=title, description=desc, icon=icon, order=order)
        self.stdout.write(self.style.SUCCESS(f'✅ {len(services)} خدمة'))

        # ===== المشاريع =====
        projects_data = [
            {
                'title': 'متجر أزياء إلكتروني',
                'slug': 'fashion-store',
                'category': 'store',
                'subtitle': 'Modern Fashion E-Commerce Store',
                'short_description': 'متجر إلكتروني كامل لبيع الملابس مع سلة ودفع إلكتروني.',
                'description': 'متجر إلكتروني متكامل يتضمن صفحة منتجات، سلة شراء، دفع إلكتروني، لوحة تحكم لإدارة المنتجات والطلبات، وإشعارات فورية.',
                'tech_stack': 'Django, PostgreSQL, Stripe, Tailwind',
                'is_featured': True,
                'color': ('#5B8CFF', '#8B5CF6'),
                'kind': 'store',
            },
            {
                'title': 'منصة تعليمية أونلاين',
                'slug': 'edu-platform',
                'category': 'webapp',
                'subtitle': 'Online Learning Platform',
                'short_description': 'منصة تعليمية فيها دورات، دروس فيديو، واختبارات.',
                'description': 'منصة تعليمية كاملة تتيح للمدرّبين رفع الدورات، وللطلاب التسجيل والمتابعة، مع نظام دفع، شهادات، ولوحة تحكم.',
                'tech_stack': 'Django, React, Redis, AWS S3',
                'is_featured': True,
                'color': ('#10B981', '#059669'),
                'kind': 'webapp',
            },
            {
                'title': 'لوحة تحكم لوجستية',
                'slug': 'logistics-dashboard',
                'category': 'dashboard',
                'subtitle': 'Logistics Analytics Dashboard',
                'short_description': 'لوحة تحكم لتتبع الشحنات والسائقين بشكل مباشر.',
                'description': 'لوحة تحكم إدارية متقدمة لتتبع الشحنات، إدارة السائقين، تقارير مباشرة، وخرائط تفاعلية.',
                'tech_stack': 'Django, Chart.js, Leaflet, PostgreSQL',
                'is_featured': True,
                'color': ('#F59E0B', '#EF4444'),
                'kind': 'dashboard',
            },
            {
                'title': 'موقع شركة عقارية',
                'slug': 'real-estate',
                'category': 'website',
                'subtitle': 'Real Estate Agency Website',
                'short_description': 'موقع تعريفي لشركة عقارية مع عرض العقارات.',
                'description': 'موقع تعريفي احترافي لشركة عقارية، مع عرض العقارات، فلترة متقدمة، ونموذج تواصل.',
                'tech_stack': 'Django, HTMX, Tailwind',
                'is_featured': True,
                'color': ('#0EA5E9', '#6366F1'),
                'kind': 'website',
            },
            {
                'title': 'تطبيق إدارة المهام',
                'slug': 'task-manager',
                'category': 'webapp',
                'subtitle': 'Team Task Management App',
                'short_description': 'تطبيق ويب لإدارة المهام مع فرق العمل والمشاريع.',
                'description': 'تطبيق ويب لإدارة المهام والفرق، بتصميم بسيط وعصري، يتضمن Kanban Board، إشعارات، وتقارير.',
                'tech_stack': 'Django, Alpine.js, WebSocket',
                'is_featured': True,
                'color': ('#8B5CF6', '#EC4899'),
                'kind': 'webapp',
            },
            {
                'title': 'تطبيق مصرفي',
                'slug': 'banking-app',
                'category': 'ui',
                'subtitle': 'Modern Banking Mobile UI',
                'short_description': 'تصميم UI/UX لتطبيق مصرفي حديث.',
                'description': 'تصميم واجهات كامل لتطبيق مصرفي، يتضمن شاشات تسجيل دخول، تحويلات، محفظة، وإحصائيات.',
                'tech_stack': 'Figma, Design System, Prototyping',
                'is_featured': True,
                'color': ('#1E293B', '#64748B'),
                'kind': 'ui',
            },
        ]

        for p in projects_data:
            project = Project(
                title=p['title'],
                slug=p['slug'],
                category=p['category'],
                short_description=p['short_description'],
                description=p['description'],
                tech_stack=p['tech_stack'],
                is_featured=p['is_featured'],
            )
            project.cover.save(
                f"{p['slug']}.svg",
                make_mockup(p['title'], p['subtitle'], p['color'][0], p['color'][1], p['kind']),
                save=False,
            )
            project.save()

        self.stdout.write(self.style.SUCCESS(f'✅ {len(projects_data)} مشروع'))

        # ===== آراء العملاء =====
        testimonials = [
            ('أحمد خالد', 'صاحب متجر', 'شغل احترافي وسريع، الموقع صار جاهز بأقل من شهر والنتيجة فوق التوقعات.'),
            ('سارة محمد', 'مدربة أونلاين', 'منصة التعليم اللي سووها لي سهلة جدًا وبتشتغل بسلاسة، وأهم شي الدعم بعد التسليم.'),
            ('شركة النور', 'قطاع لوجستي', 'لوحة التحكم وفّرت علينا وقت كبير، والتقارير المباشرة ساعدتنا نتخذ قرارات أسرع.'),
            ('كرم حسن', 'مؤسس Startup', 'تعامل راقي، التزام بالمواعيد، وأفكار إبداعية بالتصميم. أنصح فيهم بقوة.'),
        ]
        for name, role, msg in testimonials:
            Testimonial.objects.create(name=name, role=role, message=msg)
        self.stdout.write(self.style.SUCCESS(f'✅ {len(testimonials)} رأي عميل'))

        self.stdout.write(self.style.SUCCESS('\n🎉 تم إضافة البيانات بنجاح!'))
