(() => {
  const dialog = document.querySelector('dialog');
  const pictures = [...document.querySelectorAll('.photo-button')];
  if (!dialog || !pictures.length) return;
  let active = 0, opener = null, hideTimer, keyboardMode = false;

  function showControls() {
    clearTimeout(hideTimer);
    dialog.classList.remove('is-idle');
    if (dialog.open && !keyboardMode) {
      hideTimer = setTimeout(() => dialog.classList.add('is-idle'), 2000);
    }
  }

  function showPhoto(index) {
    active = (index + pictures.length) % pictures.length;
    const source = pictures[active].querySelector('img');
    const image = dialog.querySelector('.lightbox-content img');
    image.src = source.src;
    image.alt = source.alt;
    dialog.querySelector('.lightbox-count').textContent = (active + 1) + ' / ' + pictures.length;
    showControls();
  }

  pictures.forEach((button, index) => button.addEventListener('click', event => {
    opener = button;
    keyboardMode = event.detail === 0;
    showPhoto(index);
    dialog.showModal();
    document.body.style.overflow = 'hidden';
    showControls();
  }));
  dialog.querySelector('.lightbox-close').addEventListener('click', () => dialog.close());
  dialog.querySelector('.prev').addEventListener('click', () => showPhoto(active - 1));
  dialog.querySelector('.next').addEventListener('click', () => showPhoto(active + 1));
  dialog.addEventListener('click', () => { if (dialog.open) showControls(); });
  dialog.addEventListener('pointerdown', () => {
    keyboardMode = false;
    clearTimeout(hideTimer);
  }, {passive: true});
  for (const event of ['pointerup', 'pointercancel']) {
    dialog.addEventListener(event, () => {
      if (dialog.open && !dialog.classList.contains('is-idle')) showControls();
    }, {passive: true});
  }
  dialog.addEventListener('pointermove', event => {
    if (event.pointerType === 'mouse') showControls();
  }, {passive: true});
  dialog.addEventListener('keydown', event => {
    keyboardMode = true;
    showControls();
    if (event.key === 'ArrowRight') showPhoto(active + 1);
    if (event.key === 'ArrowLeft') showPhoto(active - 1);
  });
  dialog.addEventListener('close', () => {
    clearTimeout(hideTimer);
    dialog.classList.remove('is-idle');
    document.body.style.overflow = '';
    opener?.focus();
  });
})();
