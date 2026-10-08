'use strict';
document.addEventListener('keydown', (event) => {
  if (!(event.ctrlKey || event.metaKey) || event.altKey || event.key.toLowerCase() !== 'k') return;
  const toggle = document.querySelector('[data-md-toggle="search"]');
  const query = document.querySelector('[data-md-component="search-query"]');
  if (!toggle || !query) return;
  event.preventDefault();
  toggle.checked = true;
  query.focus();
});
