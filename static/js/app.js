let bar = document.querySelector(".navbar");
//<i class='bx bx-x'></i>

// sidebar open close js code
let menuOpenBtn = document.querySelector(".navbar .bx-menu");
let closeOpenBtn = document.querySelector(".nav-links .bx-x");
let navLinks = document.querySelector(".nav-links");
const logo = document.querySelector('.logo');

menuOpenBtn.addEventListener("click", () => {
    navLinks.style.left="0";
    logo.classList.add('hidden');
});
closeOpenBtn.addEventListener("click", () => {
    navLinks.style.left="-100%";
    logo.classList.remove('hidden');
});

// sidebar sub menu open close js code

let htmlcssArrow = document.querySelector(".htmlcss-arrow");
htmlcssArrow.addEventListener("click" ,() =>{
    navLinks.classList.toggle("show1");
});
// let moreArrow = document.querySelector(".more-arrow");
// moreArrow.addEventListener("click" ,() =>{
//     navLinks.classList.toggle("show2");
// });
// let jsArrow = document.querySelector(".js-arrow");
// jsArrow.addEventListener("click" ,() =>{
//     navLinks.classList.toggle("show3");
// });

// document.addEventListener('DOMContentLoaded', function () {
//     const sidebarLogo = document.querySelector('.sidebar-logo');
//     const logo = document.querySelector('.logo');

//     sidebarLogo.addEventListener('click', function () {
//         logo.classList.add('hidden');
//     });
// });
