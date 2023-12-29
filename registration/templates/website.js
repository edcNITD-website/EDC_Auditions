const mobileMenuButton = document.querySelector('.mobile-menu-button');
const mobileView = document.getElementById('mobileView');

mobileMenuButton.addEventListener('click', function() {
  mobileView.classList.toggle('hidden');
});