/* Слайдер */
document.addEventListener('DOMContentLoaded', function() {
    let slides = document.querySelectorAll('.slide');
    let currentSlide = 0;

    function showSlide(index) {
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

//Функция для управления бюджетом
document.addEventListener('DOMContentLoaded', function() {
    console.log("Вошел в функцию для бюджета");
    // Получаем элементов стнаницы
    const totalBudgetEl = document.getElementById('totalBudget');// общий бюджет
    const spentAmountEl = document.getElementById('spentAmount');// расход
    const remainingAmountEl = document.getElementById('remainingAmount');//остаток
    const expenseInput = document.getElementById('expenseAmount');// поле расхода
    const includeTaxCheck = document.getElementById('includeTax');// налог
    const taxAmountField = document.getElementById('taxAmountField');
    const amountWithTaxSpan = document.getElementById('amountWithTax');// поле сумма с налогом
    const rubAmountInput = document.getElementById('rubAmount');// итоговая сумма
    const applyBtn = document.getElementById('applyExpenseBtn');// кнопка расхода
    const completeTripBtn = document.getElementById('completeTripBtn');// завершить поездку
    const taxRateSpan = document.getElementById('taxRate');
    const tripIdInput = document.getElementById('tripId');
    const currencyCodeSpan = document.getElementById('currencyCode');
    console.log("код валюты страны " + currencyCodeSpan.innerText);
    
    // Переменные для хранения данных
    let totalBudget = parseFloat(totalBudgetEl?.getAttribute('data-value') || 0);
    let currentSpent = parseFloat(spentAmountEl?.getAttribute('data-value') || 0);
    let taxRate = parseFloat(taxRateSpan?.textContent || 0);
    let currencyCode = currencyCodeSpan?.textContent || 'RUB';
    console.log("код валюты страны " + currencyCode);
    let exchangeRate = 90;
    
    // Функция обновления цвета остатка
    function updateRemainingColor(remaining) {
        console.log("обновил цвет остатка");
        const remainingSpan = document.getElementById('remainingAmount');
        if (!remainingSpan) return;
        
        if (remaining < totalBudget * 0.2) {
            remainingSpan.style.color = '#dc3545';
            remainingSpan.className = 'stat-value remaining-critical';
        } else if (remaining < totalBudget * 0.5) {
            remainingSpan.style.color = '#ffc107';
            remainingSpan.className = 'stat-value remaining-moderate';
        } else {
            remainingSpan.style.color = '#28a745';
            remainingSpan.className = 'stat-value remaining-good';
        }
    }
    
    // Получение курса валюты
    async function getExchangeRate() {
        console.log("вошел в функцию расчета курса валют");
        if (currencyCode === 'RUB') {
            exchangeRate = 1;
            return;
        }
        
        try {
            const response = await fetch(`https://open.er-api.com/v6/latest/${currencyCode}`);
            const data = await response.json();
            exchangeRate = data.rates.RUB;
            console.log(`Курс 1 ${currencyCode} = ${exchangeRate} RUB`);
            
        } catch (error) {
            console.error('Ошибка получения курса:', error);
            exchangeRate = 90;
        }
    }
    
    // Расчёт суммы с налогом и в рублях
    function calculateRub() {
        let amount = parseFloat(expenseInput?.value) || 0;
        let includeTax = includeTaxCheck?.checked || false;
        
        if (includeTax && taxAmountField && amountWithTaxSpan) {
            let withTax = amount * (1 + taxRate / 100);
            amountWithTaxSpan.value = withTax.toFixed(2) + ' ' + currencyCode;
            taxAmountField.style.display = 'block';
            amount = withTax;
        } else if (taxAmountField) {
            taxAmountField.style.display = 'none';
        }
        
        let rubAmount = amount * exchangeRate;
        if (rubAmountInput) rubAmountInput.value = rubAmount.toFixed(2) + ' ₽';
        if (applyBtn) applyBtn.disabled = !amount;
    }
    
    // Добавление расхода
    async function addExpense() {
        let rubAmount = parseFloat(rubAmountInput?.value) || 0;
        let localAmount = parseFloat(expenseInput?.value) || 0;
        let includeTax = includeTaxCheck?.checked || false;
        let tripId = tripIdInput?.value;
        
        if (rubAmount <= 0) return;
        
        let newSpent = currentSpent + rubAmount;
        
        if (newSpent > totalBudget) {
            if (!confirm(' Внимание! Расход превышает бюджет! Продолжить?')) return;
        }
        
        try {
            // ИСПРАВЛЕНО: правильный URL и передача trip_id в теле
            const response = await fetch(`/api/add-expense/${tripId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken()
                },
                body: JSON.stringify({
                    trip_id: tripId,
                    amount_local: localAmount,
                    amount_rub: rubAmount,
                    include_tax: includeTax
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                currentSpent = data.new_spent;
                let remaining = totalBudget - currentSpent;
                
                if (spentAmountEl) spentAmountEl.textContent = currentSpent.toFixed(2) + ' ₽';
                if (remainingAmountEl) remainingAmountEl.textContent = remaining.toFixed(2) + ' ₽';
                
                updateRemainingColor(remaining);
                
                // Очистка формы
                if (expenseInput) expenseInput.value = '';
                if (rubAmountInput) rubAmountInput.value = '';
                if (applyBtn) applyBtn.disabled = true;
                if (taxAmountField) taxAmountField.style.display = 'none';
                if (includeTaxCheck) includeTaxCheck.checked = false;
                
                alert(`Расход ${rubAmount.toFixed(2)} ₽ добавлен!`);
            } else {
                alert('Ошибка: ' + data.error);
            }
        } catch (error) {
            console.error('Ошибка:', error);
            alert('Ошибка при добавлении расхода');
        }
    }
    
    // Завершение поездки
    async function completeTrip() {
        let tripId = tripIdInput?.value;
        
        if (!confirm('Завершить поездку?')) return;
        
        try {
            // ИСПРАВЛЕНО: правильный URL и передача trip_id в теле
            const response = await fetch(`/api/complete-trip/${tripId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken()
                },
                body: JSON.stringify({
                    trip_id: tripId
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                alert('Поездка завершена!');
                window.location.href = '/';
            } else {
                alert('Ошибка: ' + data.error);
            }
        } catch (error) {
            console.error('Ошибка:', error);
            alert('Ошибка при завершении поездки');
        }
    }
    
    // Получение CSRF-токена
    function getCsrfToken() {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, 10) === 'csrftoken=') {
                    cookieValue = decodeURIComponent(cookie.substring(10));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    // Применение обработчиков
    if (expenseInput) expenseInput.addEventListener('input', calculateRub);
    if (includeTaxCheck) includeTaxCheck.addEventListener('change', calculateRub);
    if (applyBtn) applyBtn.addEventListener('click', addExpense);
    if (completeTripBtn) completeTripBtn.addEventListener('click', completeTrip);
    
    // Инициализация
    getExchangeRate().then(() => {
        calculateRub();
        updateRemainingColor(totalBudget - currentSpent);
    });
});