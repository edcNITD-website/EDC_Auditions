// gsap.registerPlugin(ScrollTrigger, ScrollSmoother);

// create the scrollSmoother before your scrollTriggers
// ScrollSmoother.create({
//   smooth: 1, // how long (in seconds) it takes to "catch up" to the native scroll position
//   effects: true, // looks for data-speed and data-lag attributes on elements
//   smoothTouch: 0.1, // much shorter smoothing time on touch devices (default is NO smoothing on touch devices)
// });
let text = new SplitType('#text');
// let aud = new SplitType('#audition');

var pointer = document.getElementById('pointer');

var py = 0;
window.addEventListener('mousemove', (e) => {
  // // Get mouse pointer coordinates
  // const mouseX = ;
  py = e.clientY;


  // // Update CSS variables
  // pointer.style.setProperty('--mouseX', `${mouseX}px`);
  // pointer.style.setProperty('--mouseY', `${mouseY}px`);

  // // // Update pointer position
  // // pointer.style.left = `${mouseX}px`;
  // // pointer.style.top = `${mouseY}px`;

  pointer.animate({
    left: `${e.clientX}px`,
    top: `${e.clientY + window.scrollY}px`
  }, {
    duration: 500,
    fill: "forwards"
  });
});

document.addEventListener('scroll', (e) => {
  // Get scroll position
  // let scrollY = window.scrollY;

  // // Update CSS variable for scroll position
  // pointer.style.setProperty('--scrollY', `${scrollY}px`);
  // console.log(`${py + window.scrollY}px`);

  pointer.animate({
    top: `${py + window.scrollY}px`,
  }, {
    duration: 500,
    fill: "forwards"
  });
});

var tl = gsap.timeline();

let loader = document.getElementById("preloader");

window.addEventListener("load", () => {
  setTimeout(() => {
    loader.style.display = "none";
  }, 3000);

  tl.to('#preloader', {
    y: -1000,
    delay: 1,
    duration: 1
  })

  tl.from('.bg.poster .image', {
    rotate: 60,
    x: 300,
    opacity: 0,
    delay: .2,
    duration: 1
  })

  tl.from('.char', {
    y: 50,
    opacity: 0,
    stagger: 0.1,
    delay: .2,
    duration: .25,
  })

  tl.from('#audition', {
    y: 30,
    opacity: 0,
    delay: .2,
    duration: .5,
  })

  tl.from('header button', {
    x: 20,
    opacity: 0,
    delay: 0,
    duration: .1
  })

  tl.to('header button', {
    x: 0,
    opacity: 1,
    delay: 0,
    duration: .3
  })

  tl.from('.desc p', {
    x: -100,
    opacity: 0,
    delay: 0,
    duration: .2
  })
});

// gsap.from('#Content', {
//   scrollTrigger: {
//     trigger: '#Content',
//     start: "top 60%",
//     end: "bottom 45%",
//     toggleActions: "play none none reverse",
//     scrub: 1,
//     toggleClass: "hide"
//   }
// })

// gsap.from('#WebD', {
//   scrollTrigger: {
//     trigger: '#WebD',
//     start: "top 60%",
//     end: "bottom 45%",
//     toggleActions: "play none none reverse",
//     scrub: 1,
//     toggleClass: "hide"
//   }
// })

// gsap.from('#Video', {
//   scrollTrigger: {
//     trigger: '#Video',
//     start: "top 60%",
//     end: "bottom 45%",
//     toggleActions: "play none none reverse",
//     scrub: 1,
//     toggleClass: "hide"
//   }
// })

// gsap.from('#GD', {
//   scrollTrigger: {
//     trigger: '#GD',
//     start: "top 60%",
//     end: "bottom 45%",
//     toggleActions: "play none none reverse",
//     scrub: 1,
//     toggleClass: "hide"
//   }
// })

const mobileMenuButton = document.querySelector('.mobile-menu-button');
const mobileView = document.getElementById('mobileView');

mobileMenuButton.addEventListener('click', function () {
  console.log('click');
  mobileView.classList.toggle('hidden');
});
