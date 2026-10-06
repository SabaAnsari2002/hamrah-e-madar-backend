(() => {
  const root = document.documentElement;
  const body = document.body;
  const themeButton = document.querySelector('[data-theme-toggle]');
  const sidebar = document.querySelector('[data-sidebar]');
  const openButtons = document.querySelectorAll('[data-sidebar-open]');
  const closeButtons = document.querySelectorAll('[data-sidebar-close]');

  const savedTheme = localStorage.getItem('hamrah-cms-theme');
  const preferredDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  root.dataset.theme = savedTheme || (preferredDark ? 'dark' : 'light');

  themeButton?.addEventListener('click', () => {
    const next = root.dataset.theme === 'dark' ? 'light' : 'dark';
    root.dataset.theme = next;
    localStorage.setItem('hamrah-cms-theme', next);
  });

  const openSidebar = () => body.classList.add('sidebar-open');
  const closeSidebar = () => body.classList.remove('sidebar-open');

  openButtons.forEach((button) => button.addEventListener('click', openSidebar));
  closeButtons.forEach((button) => button.addEventListener('click', closeSidebar));

  window.addEventListener('resize', () => {
    if (window.innerWidth > 1040) closeSidebar();
  });
})();
