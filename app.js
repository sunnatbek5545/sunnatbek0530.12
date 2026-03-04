document.addEventListener('DOMContentLoaded', () => {
    // Backend'dan darslarni olish
    fetch('/api/lessons')
        .then(response => response.json())
        .then(data => {
            console.log("Darslar yuklandi:", data);
            // Bu yerda darslarni dinamik ravishda sahifaga qo'shish mumkin
        });

    // Menyu tugmasi bosilganda rang o'zgarishi
    const navLinks = document.querySelectorAll('.nav-links li a');
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            navLinks.forEach(l => l.style.color = 'white');
            link.style.color = '#00d2ff';
        });
    });
});