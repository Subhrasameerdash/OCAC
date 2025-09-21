// todo.js - minimal client-side behaviors for UX
document.addEventListener('DOMContentLoaded', function() {
  const inputs = document.querySelectorAll('input');
  inputs.forEach(i => {
    i.addEventListener('focus', () => { i.style.outline='2px solid rgba(255,255,255,0.06)'; });
    i.addEventListener('blur', () => { i.style.outline='none'; });
  });
});
