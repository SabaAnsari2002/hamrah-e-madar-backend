(() => {
  'use strict';

  function initNavFilter() {
    const input = document.getElementById('nav-filter');
    if (!input) return;
    const rows = [...document.querySelectorAll('.hamrah-nav-model-row')];
    const groups = [...document.querySelectorAll('.hamrah-nav-group')];
    const apply = () => {
      const q = input.value.trim().toLowerCase();
      rows.forEach(row => {
        const label = (row.dataset.navLabel || row.textContent || '').toLowerCase();
        row.hidden = q && !label.includes(q);
      });
      groups.forEach(group => {
        const visible = [...group.querySelectorAll('.hamrah-nav-model-row')].some(row => !row.hidden);
        group.hidden = !!q && !visible;
      });
    };
    input.addEventListener('input', apply);
    input.addEventListener('keydown', e => {
      if (e.key === 'Escape') { input.value = ''; apply(); input.blur(); }
    });
  }

  function ensureSidebarOpenOnDesktop() {
    const main = document.getElementById('main');
    const sidebar = document.getElementById('nav-sidebar');
    if (!main || !sidebar) return;
    if (window.matchMedia('(min-width: 901px)').matches) {
      main.classList.add('shifted');
      sidebar.setAttribute('aria-expanded', 'true');
      localStorage.setItem('django.admin.navSidebarIsOpen', 'true');
    }
  }

  function markScrolledHeader() {
    const header = document.getElementById('header');
    if (!header) return;
    const update = () => header.classList.toggle('is-scrolled', window.scrollY > 6);
    update();
    window.addEventListener('scroll', update, { passive: true });
  }

  document.addEventListener('DOMContentLoaded', () => {
    initNavFilter();
    ensureSidebarOpenOnDesktop();
    markScrolledHeader();
  });
})();
