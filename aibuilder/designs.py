"""قوالب تصميم احترافية جاهزة"""

TEMPLATES = {
    'saas': {
        'name': 'SaaS / منتج رقمي',
        'description': 'لمنتجات SaaS، أدوات، منصات',
        'prompt': 'landing page for SaaS product with pricing tiers, features grid, hero with dashboard mockup, testimonials, dark modern theme like Linear or Vercel',
    },
    'agency': {
        'name': 'وكالة / استوديو',
        'description': 'لوكالات التسويق، التصميم، التطوير',
        'prompt': 'creative agency landing page with bold typography, portfolio grid, services, case studies, minimal editorial design like Awwwards winners',
    },
    'ecommerce': {
        'name': 'متجر إلكتروني',
        'description': 'لمتاجر الأزياء، الإلكترونيات، إلخ',
        'prompt': 'modern e-commerce store landing with product showcase, categories, featured items, clean minimal design like Apple Store',
    },
    'restaurant': {
        'name': 'مطعم / كافيه',
        'description': 'للمطاعم، الكافيهات، الحلويات',
        'prompt': 'elegant restaurant landing with hero food image, menu section, reservation form, testimonials, warm luxury design like Michelin star restaurants',
    },
    'portfolio': {
        'name': 'بورتفوليو شخصي',
        'description': 'للمصممين، المصورين، المطورين',
        'prompt': 'minimal personal portfolio with large typography, project grid, about section, contact, editorial style like designer portfolios on Behance',
    },
    'startup': {
        'name': 'Startup / شركة ناشئة',
        'description': 'للشركات الناشئة والتقنية',
        'prompt': 'startup landing page with product demo, investors logos, roadmap, team section, modern gradient accents like Stripe or Notion',
    },
    'blog': {
        'name': 'مدونة / مجلة',
        'description': 'للمدونات والمجلات الإلكترونية',
        'prompt': 'magazine blog with featured article, category filters, author profiles, newsletter signup, editorial typography like Medium or The Verge',
    },
    'corporate': {
        'name': 'شركة / مؤسسة',
        'description': 'للشركات والمؤسسات الرسمية',
        'prompt': 'corporate business landing with services, statistics, clients, team, professional clean design like McKinsey or Deloitte',
    },
    'fitness': {
        'name': 'لياقة / رياضة',
        'description': 'للجيم، المدربين، الرياضة',
        'prompt': 'fitness gym landing with energetic hero, classes schedule, trainers, membership pricing, bold athletic design',
    },
    'realestate': {
        'name': 'عقارات',
        'description': 'للشركات العقارية والمشاريع',
        'prompt': 'luxury real estate landing with property showcase, search filters, agent profiles, elegant sophisticated design',
    },
    'education': {
        'name': 'تعليم / كورسات',
        'description': 'للمنصات التعليمية',
        'prompt': 'online education platform with courses, instructors, student testimonials, modern friendly design like Coursera',
    },
    'medical': {
        'name': 'طبي / عيادة',
        'description': 'للعيادات والمراكز الطبية',
        'prompt': 'medical clinic landing with services, doctors, appointments, trust badges, clean professional healthcare design',
    },
}


def get_template_prompt(template_key, user_description=''):
    """يولّد prompt كامل بناءً على القالب"""
    tpl = TEMPLATES.get(template_key, {})
    base = tpl.get('prompt', 'modern professional website')
    if user_description:
        return f"{base}. Extra requirements: {user_description}"
    return base
