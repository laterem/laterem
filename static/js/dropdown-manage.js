var toggler = document.getElementsByClassName("dropdown-toggle");
var i;

for (i = 0; i < toggler.length; i++) {
    toggler[i].addEventListener("click", function() {
        this.parentElement.querySelector(".dropdown-content").classList.toggle("active");
    });
}