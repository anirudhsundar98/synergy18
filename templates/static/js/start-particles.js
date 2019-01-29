particlesJS.load('particles-js', '/static/configs/particles.json', function () {
    console.log('callback - particles.js config loaded');
});

window.addEventListener('resize', () => {
    document.querySelector("#particles-js").width = `${window.innerWidth}px`;
    document.querySelector("#particles-js").height = `${document.querySelector("#wrapper").offsetHeight - 10}px)`;
});

document.querySelector("#particles-js").style.width = `${window.innerWidth}px`;
document.querySelector("#particles-js").style.height = `${document.querySelector("#wrapper").offsetHeight - 10}px`;
console.log(document.querySelector("#particles-js").style.width, document.querySelector("#particles-js").style.height)
console.log(document.querySelector("#wrapper").offsetHeight - 10)
