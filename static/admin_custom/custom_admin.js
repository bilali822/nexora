/* NEXORA ADMIN — LIGHT JS */
(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {

    // ========== 1. Command Palette (Ctrl+K) ==========
    var palette = document.createElement('div');
    palette.id = 'nexora-command-palette';
    palette.innerHTML = '' +
      '<div class="nx-palette-overlay"></div>' +
      '<div class="nx-palette-modal">' +
        '<div class="nx-palette-header">' +
          '<i class="fas fa-search"></i>' +
          '<input type="text" id="nx-palette-input" placeholder="ابحث أو انتقل... (Esc لإغلاق)" autocomplete="off">' +
          '<kbd>Esc</kbd>' +
        '</div>' +
        '<div class="nx-palette-results" id="nx-palette-results">' +
          '<div class="nx-palette-section-title">وصول سريع</div>' +
          '<a href="/admin/requests_app/projectrequest/" class="nx-palette-item" data-keywords="طلبات مشاريع">' +
            '<i class="fas fa-inbox"></i><div><strong>طلبات المشاريع</strong><small>عرض وإدارة</small></div></a>' +
          '<a href="/admin/projects/project/" class="nx-palette-item" data-keywords="مشاريع أعمال">' +
            '<i class="fas fa-briefcase"></i><div><strong>المشاريع</strong><small>إدارة الأعمال</small></div></a>' +
          '<a href="/admin/core/service/" class="nx-palette-item" data-keywords="خدمات">' +
            '<i class="fas fa-concierge-bell"></i><div><strong>الخدمات</strong></div></a>' +
          '<a href="/admin/core/blogpost/" class="nx-palette-item" data-keywords="مقالات مدونة">' +
            '<i class="fas fa-newspaper"></i><div><strong>المدونة</strong></div></a>' +
          '<a href="/admin/core/sitesettings/" class="nx-palette-item" data-keywords="إعدادات موقع">' +
            '<i class="fas fa-cog"></i><div><strong>إعدادات الموقع</strong></div></a>' +
          '<a href="/admin/core/contactmessage/" class="nx-palette-item" data-keywords="رسائل تواصل">' +
            '<i class="fas fa-envelope"></i><div><strong>رسائل التواصل</strong></div></a>' +
          '<a href="/admin/auth/user/" class="nx-palette-item" data-keywords="مستخدمين">' +
            '<i class="fas fa-users"></i><div><strong>المستخدمون</strong></div></a>' +
          '<a href="/" target="_blank" class="nx-palette-item" data-keywords="الموقع">' +
            '<i class="fas fa-external-link-alt"></i><div><strong>عرض الموقع</strong></div></a>' +
        '</div>' +
        '<div class="nx-palette-footer">' +
          '<span><kbd>↑</kbd><kbd>↓</kbd> تنقل</span>' +
          '<span><kbd>Enter</kbd> اختيار</span>' +
          '<span><kbd>Ctrl</kbd>+<kbd>K</kbd> فتح</span>' +
        '</div>' +
      '</div>';
    document.body.appendChild(palette);

    var overlay = palette.querySelector('.nx-palette-overlay');
    var input = document.getElementById('nx-palette-input');
    var items = palette.querySelectorAll('.nx-palette-item');
    var idx = 0;

    function openPalette() {
      palette.classList.add('nx-palette-open');
      setTimeout(function () { input.focus(); }, 50);
      idx = 0;
      updateSel();
    }
    function closePalette() {
      palette.classList.remove('nx-palette-open');
      input.value = '';
      items.forEach(function (r) { r.style.display = ''; });
    }
    function updateSel() {
      var vis = Array.prototype.filter.call(items, function (r) { return r.style.display !== 'none'; });
      vis.forEach(function (r, i) { r.classList.toggle('nx-palette-selected', i === idx); });
    }

    document.addEventListener('keydown', function (e) {
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        openPalette();
      }
      if (e.key === 'Escape' && palette.classList.contains('nx-palette-open')) {
        closePalette();
      }
    });

    overlay.addEventListener('click', closePalette);

    input.addEventListener('input', function () {
      var q = this.value.toLowerCase().trim();
      idx = 0;
      items.forEach(function (r) {
        var t = (r.textContent + ' ' + (r.dataset.keywords || '')).toLowerCase();
        r.style.display = t.indexOf(q) !== -1 ? '' : 'none';
      });
      updateSel();
    });

    input.addEventListener('keydown', function (e) {
      var vis = Array.prototype.filter.call(items, function (r) { return r.style.display !== 'none'; });
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        idx = (idx + 1) % vis.length;
        updateSel();
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        idx = (idx - 1 + vis.length) % vis.length;
        updateSel();
      } else if (e.key === 'Enter') {
        e.preventDefault();
        var sel = vis[idx];
        if (sel) {
          if (sel.target === '_blank') window.open(sel.href, '_blank');
          else window.location.href = sel.href;
        }
      }
    });

    // ========== 2. أزرار الهيدر: زر Palette + إشعارات ==========
    var navbarNav = document.querySelector('.navbar-nav.ml-auto') || document.querySelector('.navbar-nav.ms-auto');
    if (navbarNav) {
      // Palette trigger
      var paletteBtn = document.createElement('li');
      paletteBtn.className = 'nav-item';
      var paletteLink = document.createElement('a');
      paletteLink.className = 'nav-link';
      paletteLink.href = '#';
      paletteLink.title = 'Ctrl+K للبحث السريع';
      paletteLink.innerHTML = '<i class="fas fa-search"></i>';
      paletteLink.addEventListener('click', function (e) {
        e.preventDefault();
        openPalette();
      });
      paletteBtn.appendChild(paletteLink);
      navbarNav.insertBefore(paletteBtn, navbarNav.firstChild);

      // Notifications
      var notifBtn = document.createElement('li');
      notifBtn.className = 'nav-item';
      var notifLink = document.createElement('a');
      notifLink.className = 'nav-link';
      notifLink.href = '/admin/requests_app/projectrequest/?status__exact=new';
      notifLink.title = 'الطلبات الجديدة';
      notifLink.innerHTML = '<i class="fas fa-bell"></i><span class="nx-notif-dot"></span>';
      notifBtn.appendChild(notifLink);
      navbarNav.appendChild(notifBtn);
    }

    // ========== 3. Active state للسايدبار ==========
    // نحسن تفاعل الروابط — بدون animations ثقيلة
    var sidebarLinks = document.querySelectorAll('.sidebar .nav-link');
    sidebarLinks.forEach(function (link) {
      link.addEventListener('click', function () {
        // اترك Django يشتغل طبيعي
      });
    });

  });
})();
