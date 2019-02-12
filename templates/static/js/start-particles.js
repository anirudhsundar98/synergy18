particlesJS.load('particles-js', '/static/configs/particles.json', function () {
    console.log('callback - particles.js config loaded');
});

window.addEventListener('resize', () => {
    document.querySelector("#particles-js").style.width = `${window.innerWidth}px`;
    document.querySelector("#particles-js").style.height = `${window.innerHeight - 10}px`;
});

document.querySelector("#particles-js").style.width = `${window.innerWidth}px`;
document.querySelector("#particles-js").style.height = `${window.innerHeight - 10}px`;
