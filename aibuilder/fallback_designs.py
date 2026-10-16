"""تصميمات احترافية احتياطية"""


def saas_design(prompt):
    return '''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SaaS Platform</title>
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;900&display=swap" rel="stylesheet">
<style>
  body { font-family: 'Tajawal', sans-serif; -webkit-font-smoothing: antialiased; }
  .grid-bg {
    background-image: linear-gradient(rgba(99,102,241,.05) 1px, transparent 1px),
                      linear-gradient(90deg, rgba(99,102,241,.05) 1px, transparent 1px);
    background-size: 60px 60px;
  }
  .glow { box-shadow: 0 0 80px rgba(99,102,241,.3); }
</style>
</head>
<body class="bg-slate-950 text-white">

<!-- Navigation -->
<header class="fixed top-0 inset-x-0 z-50 backdrop-blur-xl bg-slate-950/70 border-b border-white/5">
  <div class="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
    <div class="flex items-center gap-2">
      <div class="w-8 h-8 bg-gradient-to-br from-indigo-500 to-purple-500 rounded-lg"></div>
      <span class="font-black tracking-tight">Nexora</span>
    </div>
    <nav class="hidden md:flex items-center gap-8 text-sm text-slate-400">
      <a href="#" class="hover:text-white transition">المميزات</a>
      <a href="#" class="hover:text-white transition">الأسعار</a>
      <a href="#" class="hover:text-white transition">التوثيق</a>
      <a href="#" class="hover:text-white transition">الشركة</a>
    </nav>
    <div class="flex items-center gap-3">
      <a href="#" class="text-sm text-slate-300 hover:text-white transition">دخول</a>
      <a href="#" class="text-sm bg-white text-slate-900 font-semibold px-4 py-2 rounded-lg hover:bg-slate-200 transition">ابدأ مجاناً</a>
    </div>
  </div>
</header>

<!-- Hero -->
<section class="relative pt-32 pb-24 grid-bg overflow-hidden">
  <div class="absolute top-1/3 left-1/2 -translate-x-1/2 w-[600px] h-[600px] bg-indigo-500/20 rounded-full blur-3xl"></div>
  <div class="relative max-w-4xl mx-auto px-6 text-center">
    <span class="inline-flex items-center gap-2 text-xs font-semibold text-indigo-400 bg-indigo-500/10 border border-indigo-500/20 px-3 py-1.5 rounded-full mb-6">
      <span class="w-1.5 h-1.5 bg-indigo-400 rounded-full"></span>
      جديد — الإصدار 2.0 متوفر الآن
    </span>
    <h1 class="text-5xl md:text-7xl font-black leading-[1.05] tracking-tight mb-6">
      منصة حديثة<br>
      <span class="bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent">لعصر جديد</span>
    </h1>
    <p class="text-lg text-slate-400 max-w-2xl mx-auto mb-10 leading-relaxed">
      ''' + prompt[:180] + '''
    </p>
    <div class="flex gap-4 justify-center">
      <a href="#" class="bg-white text-slate-900 px-6 py-3 rounded-lg font-semibold hover:bg-slate-200 transition">
        ابدأ الآن مجاناً
      </a>
      <a href="#" class="border border-white/10 px-6 py-3 rounded-lg font-semibold hover:bg-white/5 transition">
        مشاهدة العرض ←
      </a>
    </div>
    <p class="text-xs text-slate-500 mt-4">بدون بطاقة ائتمان · إلغاء في أي وقت</p>
  </div>
</section>

<!-- Stats Bar -->
<section class="border-y border-white/5 bg-slate-900/30">
  <div class="max-w-6xl mx-auto px-6 py-12 grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
    <div><p class="text-3xl font-black">10K+</p><p class="text-xs text-slate-500 mt-1">مستخدم نشط</p></div>
    <div><p class="text-3xl font-black">99.9%</p><p class="text-xs text-slate-500 mt-1">وقت التشغيل</p></div>
    <div><p class="text-3xl font-black">50M+</p><p class="text-xs text-slate-500 mt-1">طلب يومي</p></div>
    <div><p class="text-3xl font-black">4.9/5</p><p class="text-xs text-slate-500 mt-1">تقييم العملاء</p></div>
  </div>
</section>

<!-- Features -->
<section class="py-24">
  <div class="max-w-6xl mx-auto px-6">
    <div class="text-center mb-16">
      <h2 class="text-4xl md:text-5xl font-black mb-4">كل ما تحتاجه</h2>
      <p class="text-slate-400 max-w-xl mx-auto">منصة متكاملة بواجهة بسيطة وقدرات احترافية</p>
    </div>
    <div class="grid md:grid-cols-3 gap-6">
      <div class="p-8 rounded-2xl bg-gradient-to-b from-white/5 to-transparent border border-white/5">
        <div class="w-12 h-12 bg-indigo-500/20 rounded-xl flex items-center justify-center mb-6">
          <div class="w-5 h-5 bg-indigo-400 rounded"></div>
        </div>
        <h3 class="text-lg font-bold mb-2">أداء فائق</h3>
        <p class="text-slate-400 text-sm leading-relaxed">بنية حديثة تضمن سرعة استجابة فائقة تحت أي ضغط</p>
      </div>
      <div class="p-8 rounded-2xl bg-gradient-to-b from-white/5 to-transparent border border-white/5">
        <div class="w-12 h-12 bg-purple-500/20 rounded-xl flex items-center justify-center mb-6">
          <div class="w-5 h-5 bg-purple-400 rounded-full"></div>
        </div>
        <h3 class="text-lg font-bold mb-2">أمان متقدم</h3>
        <p class="text-slate-400 text-sm leading-relaxed">تشفير كامل وحماية على مستوى المؤسسات</p>
      </div>
      <div class="p-8 rounded-2xl bg-gradient-to-b from-white/5 to-transparent border border-white/5">
        <div class="w-12 h-12 bg-cyan-500/20 rounded-xl flex items-center justify-center mb-6">
          <div class="w-5 h-5 bg-cyan-400 rounded-lg"></div>
        </div>
        <h3 class="text-lg font-bold mb-2">قابلية التوسع</h3>
        <p class="text-slate-400 text-sm leading-relaxed">توسّع بلا حدود مع نمو أعمالك</p>
      </div>
    </div>
  </div>
</section>

<!-- CTA -->
<section class="py-24 bg-gradient-to-br from-indigo-600 to-purple-700 relative overflow-hidden">
  <div class="absolute inset-0 grid-bg opacity-50"></div>
  <div class="relative max-w-3xl mx-auto px-6 text-center">
    <h2 class="text-4xl md:text-5xl font-black mb-6">جاهز للبدء؟</h2>
    <p class="text-white/80 mb-8 text-lg">انضم لأكثر من 10,000 عميل يستخدمون منصتنا يومياً</p>
    <a href="#" class="inline-block bg-white text-indigo-600 px-8 py-4 rounded-xl font-bold hover:bg-slate-100 transition">
      ابدأ رحلتك الآن
    </a>
  </div>
</section>

<footer class="border-t border-white/5 py-10 text-center">
  <p class="text-sm text-slate-500">© 2026 Nexora. جميع الحقوق محفوظة.</p>
</footer>

</body>
</html>'''


def agency_design(prompt):
    return '''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Creative Agency</title>
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&display=swap" rel="stylesheet">
<style>
  body { font-family: 'Tajawal', sans-serif; }
  .marquee { animation: marquee 30s linear infinite; }
  @keyframes marquee { from { transform: translateX(0); } to { transform: translateX(-50%); } }
</style>
</head>
<body class="bg-neutral-50 text-neutral-900">

<!-- Nav -->
<header class="fixed top-0 inset-x-0 z-50 bg-neutral-50/80 backdrop-blur-md border-b border-neutral-200">
  <div class="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
    <span class="text-2xl font-black tracking-tighter">STUDIO<span class="text-orange-500">.</span></span>
    <nav class="hidden md:flex items-center gap-10 text-sm font-medium">
      <a href="#">الأعمال</a>
      <a href="#">الخدمات</a>
      <a href="#">الاستوديو</a>
      <a href="#">تواصل</a>
    </nav>
    <a href="#" class="text-sm bg-neutral-900 text-white px-5 py-2.5 rounded-full font-medium">لنبدأ مشروعك</a>
  </div>
</header>

<!-- Hero -->
<section class="pt-40 pb-32 px-6">
  <div class="max-w-7xl mx-auto">
    <h1 class="text-6xl md:text-9xl font-black leading-[0.95] tracking-tighter mb-12">
      نصنع<br>
      <span class="text-orange-500">أفكار</span><br>
      تُحدث فرقاً
    </h1>
    <div class="grid md:grid-cols-2 gap-12 items-end">
      <p class="text-xl text-neutral-600 leading-relaxed max-w-lg">
        ''' + prompt[:200] + '''
      </p>
      <div class="flex gap-4 md:justify-end">
        <a href="#" class="bg-neutral-900 text-white px-8 py-4 rounded-full font-semibold hover:bg-neutral-700 transition">
          ابدأ المشروع
        </a>
        <a href="#" class="border border-neutral-300 px-8 py-4 rounded-full font-semibold hover:bg-neutral-100 transition">
          مشاهدة الأعمال
        </a>
      </div>
    </div>
  </div>
</section>

<!-- Marquee -->
<section class="py-6 border-y border-neutral-200 overflow-hidden">
  <div class="flex whitespace-nowrap">
    <div class="marquee flex gap-16 px-8 text-3xl md:text-5xl font-black tracking-tighter">
      <span>BRANDING</span><span class="text-orange-500">✦</span>
      <span>DIGITAL</span><span class="text-orange-500">✦</span>
      <span>MOTION</span><span class="text-orange-500">✦</span>
      <span>STRATEGY</span><span class="text-orange-500">✦</span>
      <span>BRANDING</span><span class="text-orange-500">✦</span>
      <span>DIGITAL</span><span class="text-orange-500">✦</span>
      <span>MOTION</span><span class="text-orange-500">✦</span>
      <span>STRATEGY</span><span class="text-orange-500">✦</span>
    </div>
  </div>
</section>

<!-- Work -->
<section class="py-32 px-6">
  <div class="max-w-7xl mx-auto">
    <div class="flex justify-between items-end mb-16">
      <h2 class="text-5xl font-black tracking-tighter">أعمال مختارة</h2>
      <a href="#" class="text-sm font-medium border-b-2 border-neutral-900 pb-1">جميع الأعمال →</a>
    </div>
    <div class="grid md:grid-cols-2 gap-8">
      <div class="group cursor-pointer">
        <div class="aspect-[4/3] bg-gradient-to-br from-neutral-800 to-neutral-600 rounded-2xl mb-4 overflow-hidden"></div>
        <h3 class="text-xl font-bold">هوية بصرية · شركة تقنية</h3>
        <p class="text-sm text-neutral-500 mt-1">2026 · Branding</p>
      </div>
      <div class="group cursor-pointer">
        <div class="aspect-[4/3] bg-gradient-to-br from-orange-400 to-orange-600 rounded-2xl mb-4 overflow-hidden"></div>
        <h3 class="text-xl font-bold">موقع تفاعلي · متحف فني</h3>
        <p class="text-sm text-neutral-500 mt-1">2026 · Web Design</p>
      </div>
    </div>
  </div>
</section>

<!-- CTA -->
<section class="py-32 px-6 bg-neutral-900 text-white">
  <div class="max-w-4xl mx-auto text-center">
    <h2 class="text-5xl md:text-7xl font-black tracking-tighter mb-8">
      عندك فكرة؟
    </h2>
    <p class="text-neutral-400 text-xl mb-12">لنحوّلها إلى شيء استثنائي</p>
    <a href="#" class="inline-block bg-orange-500 text-white px-10 py-5 rounded-full font-bold text-lg hover:bg-orange-400 transition">
      تواصل معنا
    </a>
  </div>
</section>

<footer class="py-8 px-6 text-center text-sm text-neutral-500 border-t border-neutral-200">
  <p>© 2026 Studio. جميع الحقوق محفوظة.</p>
</footer>

</body>
</html>'''


def portfolio_design(prompt):
    return '''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Portfolio</title>
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&display=swap" rel="stylesheet">
<style>body{font-family:'Tajawal',sans-serif;}</style>
</head>
<body class="bg-stone-50 text-stone-900">

<nav class="max-w-5xl mx-auto px-6 py-8 flex justify-between items-center">
  <span class="font-bold">أحمد خالد</span>
  <div class="flex gap-6 text-sm">
    <a href="#">أعمالي</a>
    <a href="#">عني</a>
    <a href="#">تواصل</a>
  </div>
</nav>

<section class="max-w-5xl mx-auto px-6 py-20">
  <p class="text-sm uppercase tracking-widest text-stone-500 mb-4">مصمم واجهات · مطور ويب</p>
  <h1 class="text-5xl md:text-7xl font-black leading-tight tracking-tight mb-8">
    أصنع تجارب<br>رقمية أنيقة
  </h1>
  <p class="text-lg text-stone-600 max-w-xl leading-relaxed">
    ''' + prompt[:180] + '''
  </p>
</section>

<section class="max-w-5xl mx-auto px-6 pb-20">
  <div class="grid md:grid-cols-2 gap-6">
    <div class="aspect-square bg-stone-200 rounded-2xl"></div>
    <div class="aspect-square bg-stone-300 rounded-2xl"></div>
    <div class="aspect-square bg-stone-400 rounded-2xl"></div>
    <div class="aspect-square bg-stone-200 rounded-2xl"></div>
  </div>
</section>

<footer class="max-w-5xl mx-auto px-6 py-12 border-t border-stone-200 text-sm text-stone-500">
  <p>© 2026 · صُنع بشغف</p>
</footer>

</body>
</html>'''


def restaurant_design(prompt):
    return '''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Restaurant</title>
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&family=Playfair+Display:wght@700;900&display=swap" rel="stylesheet">
<style>
  body { font-family: 'Tajawal', sans-serif; }
  .serif { font-family: 'Playfair Display', serif; }
</style>
</head>
<body class="bg-amber-50 text-stone-900">

<nav class="px-8 py-6 flex justify-between items-center border-b border-stone-200">
  <span class="serif text-2xl font-bold">Maison</span>
  <div class="hidden md:flex gap-8 text-sm">
    <a href="#">القائمة</a>
    <a href="#">عننا</a>
    <a href="#">حجز</a>
    <a href="#">تواصل</a>
  </div>
  <a href="#" class="text-sm bg-stone-900 text-white px-5 py-2 rounded-full">احجز طاولة</a>
</nav>

<section class="px-8 py-24 md:py-32 max-w-6xl mx-auto text-center">
  <p class="text-xs uppercase tracking-[0.3em] text-amber-700 mb-6">مطبخ متوسطي · منذ 2018</p>
  <h1 class="serif text-6xl md:text-8xl font-bold leading-tight mb-8">
    نكهات<br>لا تُنسى
  </h1>
  <p class="text-lg text-stone-600 max-w-2xl mx-auto leading-relaxed mb-10">
    ''' + prompt[:180] + '''
  </p>
  <a href="#" class="inline-block bg-stone-900 text-white px-10 py-4 rounded-full font-semibold hover:bg-stone-700 transition">
    استعرض القائمة
  </a>
</section>

<section class="px-8 py-16 max-w-6xl mx-auto">
  <div class="grid md:grid-cols-3 gap-6">
    <div class="bg-white p-8 rounded-2xl border border-stone-200">
      <p class="text-xs uppercase tracking-widest text-amber-700 mb-3">المقبلات</p>
      <h3 class="serif text-2xl mb-3">طبق الشيف</h3>
      <p class="text-sm text-stone-600">مكونات موسمية طازجة</p>
    </div>
    <div class="bg-white p-8 rounded-2xl border border-stone-200">
      <p class="text-xs uppercase tracking-widest text-amber-700 mb-3">الأطباق الرئيسية</p>
      <h3 class="serif text-2xl mb-3">تخصصاتنا</h3>
      <p class="text-sm text-stone-600">وصفات تقليدية بلمسة عصرية</p>
    </div>
    <div class="bg-white p-8 rounded-2xl border border-stone-200">
      <p class="text-xs uppercase tracking-widest text-amber-700 mb-3">الحلويات</p>
      <h3 class="serif text-2xl mb-3">لمسة أخيرة</h3>
      <p class="text-sm text-stone-600">حلويات شرقية وغربية</p>
    </div>
  </div>
</section>

<footer class="px-8 py-12 text-center text-sm text-stone-500 border-t border-stone-200">
  <p>© 2026 Maison. جميع الحقوق محفوظة.</p>
</footer>

</body>
</html>'''
