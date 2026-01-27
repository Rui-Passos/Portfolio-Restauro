window.onscroll = function() {
    const header = this.document.querySelector("header");
    if (window.pageYOffset > 50) {
        header.style.padding = "10px 50px";
        header.style.background ="rgba(255, 255, 255, 0.95)";
    } else {
        header.style.padding = "20px 50px";
        header.style.background ="white";
    }
};