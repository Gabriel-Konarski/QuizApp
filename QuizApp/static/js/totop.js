document.querySelector('#back-to-top').addEventListener('click', (event) => {
  event.preventDefault();
  window.scroll({
    top: 0,
    behavior: 'smooth'
  });
});