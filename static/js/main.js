// Tabs (profile)
document.addEventListener('click', (e) => {
  const tab = e.target.closest('.tab');
  if (!tab) return;
  const target = tab.dataset.tab;
  if (!target) return;
  document.querySelectorAll('.tab').forEach(t => t.classList.toggle('active', t === tab));
  document.querySelectorAll('.tab-panel').forEach(p => {
    p.style.display = p.dataset.panel === target ? 'block' : 'none';
  });
  if (history.replaceState) history.replaceState(null, '', '#' + target);
});

document.addEventListener('DOMContentLoaded', () => {
  // Activate tab from hash
  const hash = window.location.hash.replace('#', '');
  if (hash) {
    const tab = document.querySelector(`.tab[data-tab="${hash}"]`);
    if (tab) tab.click();
  } else {
    const first = document.querySelector('.tab');
    if (first) first.click();
  }

  // Sport choice toggle
  document.querySelectorAll('.choice input[type=checkbox]').forEach(cb => {
    const update = () => cb.closest('.choice').classList.toggle('active', cb.checked);
    update();
    cb.addEventListener('change', update);
  });

  // Click on choice card toggles checkbox
  document.querySelectorAll('.choice').forEach(c => {
    c.addEventListener('click', (e) => {
      if (e.target.tagName === 'INPUT') return;
      const cb = c.querySelector('input[type=checkbox]');
      if (cb) { cb.checked = !cb.checked; cb.dispatchEvent(new Event('change')); }
    });
  });

  // Steps progress
  document.querySelectorAll('.progress[data-pct]').forEach(p => {
    const pct = Math.min(100, Math.max(0, parseFloat(p.dataset.pct) || 0));
    const bar = p.querySelector('span');
    if (bar) requestAnimationFrame(() => { bar.style.width = pct + '%'; });
  });
});
