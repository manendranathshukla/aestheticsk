function prev() {
  document.getElementById("slider-container").scrollLeft -= 270;
}

function next() {
  document.getElementById("slider-container").scrollLeft += 270;
}

$(".slide img").on("click", function () {
  $(this).toggleClass("zoomed");
  $(".overlay").toggleClass("active");
});

function prev2() {
  document.getElementById("slider-container2").scrollLeft -= 270;
}

function next2() {
  document.getElementById("slider-container2").scrollLeft += 270;
}

$(".slide2 img").on("click", function () {
  $(this).toggleClass("zoomed");
  $(".overlay").toggleClass("active");
});
