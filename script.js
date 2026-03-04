document.addEventListener('DOMContentLoaded', function() {
    // Navigatsiya almashinuvi
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            navLinks.forEach(l => l.classList.remove('active'));
            this.classList.add('active');

            const tab = this.dataset.tab;
            console.log("Yuklanmoqda: " + tab);
            // Bu yerda dinamik ravishda content-area ni o'zgartirish mumkin
        });
    });

    // Chart.js - Analitika grafigi
    const ctx = document.getElementById('revenueChart');
    if(ctx) {
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Dush', 'Sesh', 'Chor', 'Pay', 'Jum', 'Shan', 'Yak'],
                datasets: [{
                    label: 'Haftalik Savdo',
                    data: [12, 19, 15, 25, 22, 30, 28],
                    borderColor: '#38bdf8',
                    tension: 0.4,
                    fill: true,
                    backgroundColor: 'rgba(56, 189, 248, 0.1)'
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { display: false } }
            }
        });
    }

    // Saqlash tugmasi
    document.getElementById('saveProductBtn')?.addEventListener('click', function() {
        Swal.fire({
            title: 'Muvaffaqiyatli!',
            text: 'Mahsulot bazaga qo\'shildi',
            icon: 'success',
            confirmButtonColor: '#38bdf8'
        });
        bootstrap.Modal.getInstance(document.getElementById('productModal')).hide();
    });
});