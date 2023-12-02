var toggleButton = document.getElementById('toggleSlider'),
    slide = document.querySelector('.slide');

toggleButton.addEventListener('click', toggleSlider, false);

function toggleSlider() {
  if (slide.classList.contains('slide-up')) {
    slide.classList.remove('slide-up');
  } else {
    slide.classList.add('slide-up');
  }
}

setTimeout(transition, 4000);

function transition() {
  toggleButton.click();
}