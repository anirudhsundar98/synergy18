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
        startNotifs();
    }, 2000);
}

function startNotifs() {
    let notifs = [
        "Registrations are open for all events",
        "A fee of ₹200 will be collected on registration",
        "If a college has more than 15 participants...",
        "...that college's participants get a total discount of 10%",
        "Accomodation will be provided",
        "We are accepting abstracts for Paper presentation",
        "Certificates will be provided for all events and workshops"
    ];
    let pointer = 0;
    document.querySelector("#notifs").innerHTML = notifs[pointer];
    setInterval(() => {
        pointer = (pointer === notifs.length - 1) ? 0 : pointer + 1;
        document.querySelector("#notifs").style.opacity = 0;
        setTimeout(() => {
            document.querySelector("#notifs").innerHTML = notifs[pointer];
            document.querySelector("#notifs").style.opacity = 1;
        }, 750);
    }, 3500);
}
