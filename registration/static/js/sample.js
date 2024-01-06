 
    let text = new SplitType('#text');
    let characters = document.querySelectorAll('.char');

    for(i=0; i<characters.length; i++){
        characters[i].classList.add('translate-y-full')
    }
    gsap.to('.char',{
        y: 0,
        stagger: 0.05,
        delay:0.5,
        duration: 1,
    })

 let sections = document.querySelectorAll('.section');

 window.onscroll = () => {
    sections.forEach(sec => {
        let top = window.scrollY;
        let offset = sec.offsetTop - 275;
        let height = sec.offsetHeight;

        if (top >= offset && top < offset + height){
            sec.classList.add('show-animate');
        }
        // if want to use repeating animation on scroll, use this
        else {
            sec.classList.remove('show-animate');
        }
    })
 }

var container = document.getElementById('container');
console.log("container");

const mobileMenuButton = document.querySelector('.mobile-menu-button');
const mobileView = document.getElementById('mobileView');

mobileMenuButton.addEventListener('click', function() {
    console.log('click');
  mobileView.classList.toggle('hidden');
});
