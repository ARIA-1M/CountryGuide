/* Слайдер */
document.addEventListener('DOMContentLoaded', function() {
    let slides = document.querySelectorAll('.slide');
    console.log(slides);
    let currentSlide = 0;

    function showSlide(index) {
        console.log('JS зашел!');
        slides.forEach(slide => slide.classList.remove('active'));
        
        if (index >= slides.length) currentSlide = 0;
        else if (index < 0) currentSlide = slides.length - 1;
        else currentSlide = index;
        
        slides[currentSlide].classList.add('active');
    }

     setInterval(() => {
        showSlide(currentSlide + 1);
    }, 3000);

});