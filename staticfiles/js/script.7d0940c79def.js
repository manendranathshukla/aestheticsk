$(document).ready(function () {
  simpleCarousel($(".simple-carousel"), 3000);
});

function simpleCarousel(carousel, intervalTime = 3000) {
  var slideCount = $(carousel).find("ul li.slide").length;
  var activeSlide = 0;

  function showSlide() {
    $(carousel)
      .find("ul li.slide")
      .each(function (index) {
        if (index == activeSlide) {
          $(this).fadeIn();
        } else {
          $(this).fadeOut();
        }
      });
  }

  setInterval(function () {
    moveRight();
  }, intervalTime);

  function moveLeft() {
    activeSlide -= 1;
    if (activeSlide < 0) {
      activeSlide = slideCount - 1;
    }
    showSlide();
  }

  function moveRight() {
    activeSlide += 1;
    if (activeSlide >= slideCount) {
      activeSlide = 0;
    }
    showSlide();
  }

  $(carousel)
    .find("a.control_prev")
    .click(function () {
      moveLeft();
    });

  $(carousel)
    .find("a.control_next")
    .click(function () {
      moveRight();
    });
}
