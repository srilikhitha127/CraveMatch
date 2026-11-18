document.addEventListener('DOMContentLoaded', () => {
  const cuisineSelect = document.querySelector('select[name="cuisine"]');
  document.querySelectorAll('.cuisine-tile').forEach(tile => {
    tile.addEventListener('click', () => {
      const cuisine = tile.dataset.cuisine;
      document.querySelectorAll('.cuisine-tile').forEach(t => t.classList.remove('selected'));
      tile.classList.add('selected');
      if (cuisineSelect && cuisine !== 'All') {
        const option = [...cuisineSelect.options].find(o => o.value.toLowerCase() === cuisine.toLowerCase());
        if (option) cuisineSelect.value = option.value;
        else cuisineSelect.value = 'Any';
      } else if (cuisineSelect) cuisineSelect.value = 'Any';
      document.querySelector('.search-panel').scrollIntoView({behavior:'smooth', block:'center'});
    });
  });
  document.querySelectorAll('.heart-btn').forEach(btn => btn.addEventListener('click', () => {
    btn.classList.toggle('saved'); btn.textContent = btn.classList.contains('saved') ? '♥' : '♡';
  }));
  const sort = document.getElementById('sort-select');
  const grid = document.getElementById('restaurant-grid');
  if (sort && grid) sort.addEventListener('change', () => {
    const cards = [...grid.querySelectorAll('.restaurant-card')];
    cards.sort((a,b) => {
      if (sort.value === 'rating') return Number(b.dataset.rating) - Number(a.dataset.rating);
      if (sort.value === 'name') return a.dataset.name.localeCompare(b.dataset.name);
      return Number(b.dataset.match) - Number(a.dataset.match);
    }); cards.forEach(card => grid.appendChild(card));
  });
  const modal = document.getElementById('match-modal');
  const closeModal = () => { modal.classList.remove('open'); modal.setAttribute('aria-hidden','true'); };
  document.querySelectorAll('.view-btn').forEach(btn => btn.addEventListener('click', () => {
    document.getElementById('modal-name').textContent = btn.dataset.name;
    document.getElementById('modal-cuisine').textContent = btn.dataset.cuisines;
    document.getElementById('modal-match').textContent = `${btn.dataset.match}%`;
    document.getElementById('modal-rating').textContent = `★ ${Number(btn.dataset.rating).toFixed(1)}`;
    document.getElementById('modal-location').textContent = `⌖ ${btn.dataset.locality || btn.dataset.city}`;
    modal.classList.add('open'); modal.setAttribute('aria-hidden','false');
  }));
  modal.querySelector('.modal-close').addEventListener('click', closeModal);
  modal.querySelector('.modal-backdrop').addEventListener('click', closeModal);
  modal.querySelector('.modal-done').addEventListener('click', closeModal);
  document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });
  const menu = document.querySelector('.mobile-menu');
  menu?.addEventListener('click', () => {
    const nav = document.querySelector('.main-nav');
    const shown = nav.style.display === 'flex';
    nav.style.display = shown ? 'none' : 'flex';
    nav.style.position = 'absolute'; nav.style.top = '63px'; nav.style.left = '0'; nav.style.right = '0';
    nav.style.padding = '14px'; nav.style.background = '#fff'; nav.style.flexDirection = 'column'; nav.style.boxShadow = '0 12px 20px #173b2618';
  });
});
