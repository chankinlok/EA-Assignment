const composer = document.querySelector('#compose-dialog');

document.querySelectorAll('[data-open-composer]').forEach((button) => {
  button.addEventListener('click', () => composer.showModal());
});

document.querySelector('[data-close-composer]')?.addEventListener('click', () => composer.close());

composer?.addEventListener('click', (event) => {
  if (event.target === composer) composer.close();
});

document.addEventListener('keydown', (event) => {
  if (event.key === '/' && !['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName)) {
    event.preventDefault();
    document.querySelector('#site-search')?.focus();
  }
});

if (new URLSearchParams(location.search).get('compose') === '1') {
  composer?.showModal();
}