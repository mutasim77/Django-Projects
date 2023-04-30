let slideIndex = 0;

function showSlides() {
    let slides = document.getElementsByClassName("mySlides");

    if (slides.length < 1) return

    for (let i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }

    slideIndex++;

    if (slideIndex > slides.length) {
        slideIndex = 1
    }

    slides[slideIndex - 1].style.display = "block";

    setTimeout(showSlides, 3000);
}

showSlides();



//! Fetch the Data from API FOR QUOTE
async function getQuotes(url) {
    const res = await fetch(url);
    const quotes = await res.json();
    show(quotes);
}

getQuotes("https://type.fit/api/quotes");

let counter = 0;
function show(quotes) {
    let arr = quotes;
    const button = document.querySelector('.quotes button');
    if (!button) return;

    button.addEventListener('click', () => {
        counter++;
        document.querySelector('.quotes q').textContent = arr[counter].text;
    })
}



//! Burget Menu;

const menuToggle = document.querySelector('#menu > i');
const dropLeftMenu = document.querySelector('.drop-left-menu');

menuToggle.addEventListener('click', () => {
    if (menuToggle.classList.contains('fa-xmark')) {
        closeMenu();
    } else {
        showMenu();
    }
});

function showMenu() {
    dropLeftMenu.classList.add('active');
    menuToggle.classList.remove('fa-bars');
    menuToggle.classList.add('fa-xmark');
}

function closeMenu() {
    dropLeftMenu.classList.remove('active');
    menuToggle.classList.remove('fa-xmark');
    menuToggle.classList.add('fa-bars');
}

document.addEventListener('scroll', () => {
    if (window.scrollY > 165) {
        closeMenu();
    }
})