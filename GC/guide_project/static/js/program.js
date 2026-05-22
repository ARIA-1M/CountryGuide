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

/* Управление лимитом при создании */
document.addEventListener('DOMContentLoaded', function() {
    const startDate = document.getElementById('id_start_date');
    const endDate = document.getElementById('id_end_date');
    const amount = document.getElementById('id_amount');
    const dailyLimit = document.getElementById('id_daily_limit');
    const budgetInfo = document.getElementById('budgetInfo');
    
    function calculateDays() {
        if (startDate.value && endDate.value) {
            const start = new Date(startDate.value);
            const end = new Date(endDate.value);
            const days = Math.ceil((end - start) / (1000 * 60 * 60 * 24));
            return days > 0 ? days : 0;
        }
        return 0;
    }
    
    function updateBudgetInfo() {
        const days = calculateDays();
        const totalBudget = parseFloat(amount.value) || 0;
        const daily = parseFloat(dailyLimit.value) || 0;
        
        if (days > 0 && totalBudget > 0) {
            const recommendedDaily = totalBudget / days;
            let message = `<strong>Прогноз:</strong><br>
                Дней поездки: ${days}<br>
                Рекомендуемый лимит на день: ${recommendedDaily.toFixed(2)}<br>`;
            
            if (daily > 0) {
                if (daily > recommendedDaily) {
                    message += `<span class="text-warning"> Ваш лимит выше рекомендуемого </span>`;
                } else if (daily < recommendedDaily) {
                    message += `<span class="text-danger"> Ваш лимит ниже рекомендуемого </span>`;
                } else {
                    message += `<span class="text-success"> Ваш лимит оптимален</span>`;
                }
            }
            
            budgetInfo.innerHTML = message;
            budgetInfo.style.display = 'block';
        } else {
            budgetInfo.style.display = 'none';
        }
    }
    
    startDate.addEventListener('change', updateBudgetInfo);
    endDate.addEventListener('change', updateBudgetInfo);
    amount.addEventListener('input', updateBudgetInfo);
    dailyLimit.addEventListener('input', updateBudgetInfo);
});