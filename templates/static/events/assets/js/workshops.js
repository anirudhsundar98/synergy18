let handlePromoClick = ( () => {
    let state = "show";

    return (div) => {
        div.innerHTML = `(Click here to ${state} workshops promo)`;
        state = (state == "show") ? "hide" : "show";
    }
})();
