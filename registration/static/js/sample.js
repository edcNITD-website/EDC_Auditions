
var container = document.getElementById('container');
console.log("container");

const mobileMenuButton = document.querySelector('.mobile-menu-button');
const mobileView = document.getElementById('mobileView');

mobileMenuButton.addEventListener('click', function() {
    console.log('click');
  mobileView.classList.toggle('hidden');
});
