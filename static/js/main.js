/* ================================================================
   NEXORA — Main JavaScript
   ================================================================ */

(function () {
  'use strict';

  // ============ 1. Loading Screen ============
  var loader = document.getElementById('nx-loader');
  if (loader) {
    window.addEventListener('load', function () {
      setTimeout(function () { loader.classList.add('hidden'); }, 300);
    });
    // Fallback: hide after 3s max
    setTimeout(function () { loader.classList.add('hidden'); }, 3000);
  }

  // ============ 3. Mobile Menu ============
  var menuBtn = document.getElementById('menuToggle');
  var navLinks = document.querySelector('.nav-links');
  if (menuBtn && navLinks) {
    menuBtn.addEventListener('click', function () {
      navLinks.classList.toggle('open');
    });
  }

  // ============ 4. Scroll Top ============
  var scrollTop = document.getElementById('scrollTop');
  window.addEventListener('scroll', function () {
    if (scrollTop) scrollTop.classList.toggle('show', window.scrollY > 400);
  }, { passive: true });

  if (scrollTop) {
    scrollTop.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // ============ 5. Reading Progress Bar ============
  var progress = document.getElementById('nx-progress');
  if (progress) {
    window.addEventListener('scroll', function () {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      var pct = h > 0 ? (window.scrollY / h) * 100 : 0;
      progress.style.width = pct + '%';
    }, { passive: true });
  }

  // ============ 6. Animate on Scroll ============
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) {
        e.target.classList.add('in');
        io.unobserve(e.target);
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.animate').forEach(function (el) { io.observe(el); });

  // ============ 7. Counter Animation ============
  var counters = document.querySelectorAll('.stat-value[data-target]');
  var co = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting && !e.target.dataset.done) {
        e.target.dataset.done = '1';
        var txt = e.target.dataset.target;
        var num = parseInt(txt.replace(/\D/g, ''));
        var suffix = txt.replace(/\d/g, '');
        if (!num) return;
        var cur = 0;
        var step = Math.ceil(num / 40);
        var t = setInterval(function () {
          cur += step;
          if (cur >= num) { cur = num; clearInterval(t); }
          e.target.textContent = cur + suffix;
        }, 30);
      }
    });
  }, { threshold: 0.5 });
  counters.forEach(function (c) { co.observe(c); });

  // ============ 8. Custom Cursor ============
  if (window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
    var cursor = document.createElement('div');
    cursor.className = 'nx-cursor';
    var dot = document.createElement('div');
    dot.className = 'nx-cursor-dot';
    document.body.appendChild(cursor);
    document.body.appendChild(dot);

    var cx = 0, cy = 0, tx = 0, ty = 0;

    document.addEventListener('mousemove', function (e) {
      tx = e.clientX;
      ty = e.clientY;
      dot.style.left = tx + 'px';
      dot.style.top = ty + 'px';
      cursor.classList.add('active');
      dot.classList.add('active');
    });

    function loop() {
      cx += (tx - cx) * 0.15;
      cy += (ty - cy) * 0.15;
      cursor.style.left = cx + 'px';
      cursor.style.top = cy + 'px';
      requestAnimationFrame(loop);
    }
    loop();

    document.querySelectorAll('a, button, .card, .project-card, .blog-card, .faq-item summary').forEach(function (el) {
      el.addEventListener('mouseenter', function () { cursor.classList.add('hover'); });
      el.addEventListener('mouseleave', function () { cursor.classList.remove('hover'); });
    });

    document.addEventListener('mouseleave', function () {
      cursor.classList.remove('active');
      dot.classList.remove('active');
    });
  }

  // ============ 9. Sticky CTA ============
  var stickyCta = document.getElementById('stickyCta');
  if (stickyCta) {
    window.addEventListener('scroll', function () {
      stickyCta.classList.toggle('show', window.scrollY > 800);
    }, { passive: true });
  }

  // ============ 10. Social Proof Popup ============
  var socialProof = document.getElementById('socialProof');
  if (socialProof) {
    var names = ['أحمد من بيروت', 'سارة من دبي', 'كرم من طرابلس', 'منى من الرياض', 'علي من عمّان', 'ليلى من القاهرة'];
    var actions = ['طلب موقع جديد', 'طلب تطبيق ويب', 'حجز استشارة', 'اطلع على الباقات'];
    var currentSP = 0;

    function showSP() {
      var name = names[Math.floor(Math.random() * names.length)];
      var action = actions[Math.floor(Math.random() * actions.length)];
      var min = Math.floor(Math.random() * 25) + 2;
      socialProof.querySelector('.sp-content').innerHTML =
        '<strong>' + name + '</strong> ' + action +
        '<small>قبل ' + min + ' دقيقة</small>';
      socialProof.querySelector('.sp-avatar').textContent = name.charAt(0);
      socialProof.classList.add('show');
      setTimeout(function () {
        socialProof.classList.remove('show');
      }, 6000);
    }

    setTimeout(function () {
      showSP();
      setInterval(showSP, 45000);
    }, 12000);
  }

  // ============ 11. Exit Intent Popup ============
  var exitModal = document.getElementById('exitIntentModal');
  if (exitModal && !sessionStorage.getItem('exitShown')) {
    document.addEventListener('mouseleave', function (e) {
      if (e.clientY < 10 && !sessionStorage.getItem('exitShown')) {
        exitModal.classList.add('show');
        sessionStorage.setItem('exitShown', '1');
      }
    });

    // كل أزرار الإغلاق
    var closeBtns = exitModal.querySelectorAll('.exit-close');
    closeBtns.forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        e.stopPropagation();
        exitModal.classList.remove('show');
        sessionStorage.setItem('exitShown', '1');
      });
    });
    exitModal.addEventListener('click', function (e) {
      if (e.target === exitModal) exitModal.classList.remove('show');
    });
  }

  // ============ 12. Typewriter ============
  var typeEl = document.getElementById('nx-typewriter');
  if (typeEl) {
    var words = (typeEl.dataset.words || '').split(',').filter(Boolean);
    if (words.length) {
      var wi = 0, ci = 0, deleting = false;
      function type() {
        var word = words[wi];
        if (!deleting) {
          typeEl.textContent = word.substring(0, ci + 1);
          ci++;
          if (ci === word.length) {
            deleting = true;
            setTimeout(type, 1800);
            return;
          }
        } else {
          typeEl.textContent = word.substring(0, ci - 1);
          ci--;
          if (ci === 0) {
            deleting = false;
            wi = (wi + 1) % words.length;
          }
        }
        setTimeout(type, deleting ? 40 : 90);
      }
      type();
    }
  }

  // ============ 13. Countdown Timer ============
  var countdown = document.getElementById('nx-countdown');
  if (countdown) {
    var end = new Date();
    end.setDate(end.getDate() + 3);
    end.setHours(23, 59, 59);

    function tick() {
      var now = new Date();
      var diff = end - now;
      if (diff <= 0) { diff = 0; }
      var days = Math.floor(diff / 86400000);
      var hours = Math.floor((diff % 86400000) / 3600000);
      var minutes = Math.floor((diff % 3600000) / 60000);
      var seconds = Math.floor((diff % 60000) / 1000);
      countdown.querySelector('[data-unit="days"] .cd-num').textContent = String(days).padStart(2, '0');
      countdown.querySelector('[data-unit="hours"] .cd-num').textContent = String(hours).padStart(2, '0');
      countdown.querySelector('[data-unit="minutes"] .cd-num').textContent = String(minutes).padStart(2, '0');
      countdown.querySelector('[data-unit="seconds"] .cd-num').textContent = String(seconds).padStart(2, '0');
    }
    tick();
    setInterval(tick, 1000);
  }

  // ============ 14. Price Calculator ============
  var calc = document.getElementById('nx-calculator');
  if (calc) {
    var basePrices = { website: 49, webapp: 99, store: 99, dashboard: 79, ui: 19 };
    var pagesInput = calc.querySelector('#calcPages');
    var typeInput = calc.querySelector('#calcType');
    var options = calc.querySelectorAll('.calc-option input[type="checkbox"]');
    var totalEl = calc.querySelector('.calc-total .value');
    var pagesLabel = calc.querySelector('#calcPagesLabel');

    function updateCalc() {
      var type = typeInput.value;
      var pages = parseInt(pagesInput.value);
      pagesLabel.textContent = pages;
      var total = basePrices[type] + (pages - 1) * 5;
      options.forEach(function (opt) {
        if (opt.checked) total += parseInt(opt.dataset.price);
      });
      totalEl.textContent = '$' + total.toLocaleString();
    }

    pagesInput.addEventListener('input', updateCalc);
    typeInput.addEventListener('change', updateCalc);
    options.forEach(function (opt) {
      opt.addEventListener('change', function () {
        this.closest('.calc-option').classList.toggle('selected', this.checked);
        updateCalc();
      });
    });

    updateCalc();
  }

  // ============ 15. Lightbox ============
  var lightbox = document.getElementById('nx-lightbox');
  if (lightbox) {
    document.querySelectorAll('.gallery img, .project-detail-img').forEach(function (img) {
      img.addEventListener('click', function () {
        lightbox.querySelector('img').src = this.src;
        lightbox.classList.add('show');
      });
    });

    lightbox.addEventListener('click', function () {
      lightbox.classList.remove('show');
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') lightbox.classList.remove('show');
    });
  }

  // ============ 16. Smooth Scroll for Anchors ============
  document.querySelectorAll('a[href^="#"]:not([href="#"])').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var id = this.getAttribute('href');
      var target = document.querySelector(id);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // ============ 17. Auto-dismiss alerts ============
  document.querySelectorAll('.alert').forEach(function (a) {
    setTimeout(function () {
      a.style.transition = 'opacity 0.5s, transform 0.5s';
      a.style.opacity = '0';
      a.style.transform = 'translateY(-10px)';
      setTimeout(function () { a.remove(); }, 500);
    }, 6000);
  });

  // ============ 18. Lazy load images ============
  if ('loading' in HTMLImageElement.prototype) {
    document.querySelectorAll('img:not([loading])').forEach(function (img) {
      img.loading = 'lazy';
    });
  }

})();

// ============ Hide scroll-top when sticky CTA is visible ============
(function () {
  var stickyCta = document.getElementById('stickyCta');
  var scrollTopBtn = document.getElementById('scrollTop');
  if (!stickyCta || !scrollTopBtn) return;

  var observer = new MutationObserver(function () {
    if (stickyCta.classList.contains('show')) {
      document.body.classList.add('sticky-cta-active');
    } else {
      document.body.classList.remove('sticky-cta-active');
    }
  });

  observer.observe(stickyCta, { attributes: true, attributeFilter: ['class'] });
})();

// ============ Exit Intent NO button ============
document.addEventListener('DOMContentLoaded', function () {
  var noBtn = document.getElementById('exitNoBtn');
  if (noBtn) {
    noBtn.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();
      var modal = document.getElementById('exitIntentModal');
      if (modal) modal.classList.remove('show');
      sessionStorage.setItem('exitShown', '1');
    });
  }
});

/* ================================================================
   USER MENU — Dropdown (standalone, resilient)
   ================================================================ */
(function () {
  'use strict';

  function initUserMenu() {
    var btn = document.getElementById('userMenuBtn');
    var dropdown = document.getElementById('userMenuDropdown');

    if (!btn || !dropdown) return;

    // منع تسجيل مستمعين متعددين
    if (btn.dataset.menuInit === '1') return;
    btn.dataset.menuInit = '1';

    btn.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();
      var isOpen = dropdown.classList.toggle('show');
      var wrapper = btn.closest('.user-menu');
      if (wrapper) wrapper.classList.toggle('is-open', isOpen);
    });

    document.addEventListener('click', function (e) {
      if (!btn.contains(e.target) && !dropdown.contains(e.target)) {
        dropdown.classList.remove('show');
        var wrapper = btn.closest('.user-menu');
        if (wrapper) wrapper.classList.remove('is-open');
      }
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        dropdown.classList.remove('show');
        var wrapper = btn.closest('.user-menu');
        if (wrapper) wrapper.classList.remove('is-open');
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initUserMenu);
  } else {
    initUserMenu();
  }
})();
