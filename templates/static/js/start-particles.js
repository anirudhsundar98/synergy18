particlesJS.load('particles-js', '/static/configs/particles.json', function () {
    console.log('callback - particles.js config loaded');
});

// window.addEventListener('resize', () => {
//     resizeParticlesCanvas();
// });

// function resizeParticlesCanvas() {
//     if (document.querySelector("#particles-js")) {
//         document.querySelector("#particles-js").style.width = `${window.innerWidth}px`;
//         if (document.querySelector("#wrapper").offsetHeight > window.innerHeight) {
//             document.querySelector("#particles-js").style.height = `${document.querySelector("#wrapper").offsetHeight - 10}px`;
//         } else {
//             document.querySelector("#particles-js").style.height = `${window.innerHeight - 10}px`;
//         }
//     }
// }

// resizeParticlesCanvas();
