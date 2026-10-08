'use strict';
const input = document.querySelector('#search');
const track = document.querySelector('#track');
const categories = [...document.querySelectorAll('.category')];
const status = document.querySelector('#status');
function filter() {
  const query = input.value.trim().toLocaleLowerCase();
  let count = 0;
  let visibleCategories = 0;
  for (const category of categories) {
    const eligible = track.value === 'all' || category.dataset.track === track.value;
    const titleMatch = category.querySelector('h2').textContent.toLocaleLowerCase().includes(query);
    let matches = 0;
    for (const term of category.querySelectorAll('.term')) {
      const visible = eligible && (titleMatch || term.textContent.toLocaleLowerCase().includes(query));
      term.hidden = !visible;
      if (visible) matches++;
    }
    category.hidden = matches === 0;
    if (matches) visibleCategories++;
    count += matches;
  }
  status.textContent = `${count.toLocaleString()} concept listings in ${visibleCategories} categories`;
  document.querySelector('#empty').hidden = count !== 0;
  for (const link of document.querySelectorAll('nav a')) {
    link.parentElement.hidden = document.querySelector(link.getAttribute('href')).hidden;
  }
}
input.addEventListener('input', filter);
track.addEventListener('change', filter);
document.querySelector('#reset').addEventListener('click', () => {
  input.value = '';
  track.value = 'all';
  filter();
  input.focus();
});
filter();
