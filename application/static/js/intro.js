window.onload = function () {
  const hasSeenIntro = localStorage.getItem("hasSeenIntro");
  var toggleButton = document.getElementById("toggleSlider");
  var slide = document.querySelector(".slide");

  toggleButton.addEventListener("click", toggleSlider, false);

  function toggleSlider() {
    if (slide.classList.contains("slide-up")) {
      slide.classList.remove("slide-up");
    } else {
      slide.classList.add("slide-up");

      toggleButton.removeEventListener("click", toggleSlider, false);
      localStorage.setItem("hasSeenIntro", true);
    }
  }

  function transition() {
    toggleButton.click();
  }

  if (hasSeenIntro) {
    toggleButton.style.display = "none";
    slide.style.display = "none";
  } else if (window.innerWidth < 800) {
    toggleButton.style.display = "none";
    slide.style.display = "none";
  } else {
    setTimeout(transition, 4000);
  }
};
