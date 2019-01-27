particlesJS.load('particles-js', '/static/configs/particles.json', function () {
    console.log('callback - particles.js config loaded');
});

window.addEventListener('resize', () => {
    document.querySelector("#particles-js").width = `${window.innerWidth}`;
    document.querySelector("#particles-js").height = `${document.querySelector("#wrapper").offsetHeight}`;
});

document.querySelector("#particles-js").style.width = `${window.innerWidth}`;
document.querySelector("#particles-js").style.height = `calc(${document.querySelector("#wrapper").offsetHeight}px - 10px)`;
