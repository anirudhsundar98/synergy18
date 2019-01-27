function load() {
    setTimeout(() => {
        document.querySelector("#preloader-container").style.opacity = 0;
        setTimeout(() => {
            document.querySelectorAll(".outer-img-container").forEach(div => {
                div.style.opacity = 1;
            });
        }, 1000);
        setTimeout(() => {
            document.querySelector("#preloader-container").style.display = "none";
        }, 2000);
    }, 2000);
}
