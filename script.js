document.addEventListener('DOMContentLoaded', () => {
    // Scroll reveals
    const reveals = document.querySelectorAll('.fade-in, .fade-in-delay, .fade-in-delay-2');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
            }
        });
    }, { threshold: 0.1 });

    reveals.forEach(reveal => {
        observer.observe(reveal);
    });

    // Product Modal Logic
    const modal = document.getElementById('productModal');
    const modalImg = document.getElementById('modalImg');
    const modalTitle = document.getElementById('modalTitle');
    const modalDesc = document.getElementById('modalDesc');
    const modalPrice = document.getElementById('modalPrice');
    const closeModal = document.querySelector('.close-modal');

    const whatsappBtn = document.getElementById('whatsappBtn');
    const whatsappNumber = "919567040754"; // Replace with actual business number

    document.querySelectorAll('.product-card').forEach(card => {
        card.addEventListener('click', () => {
            const title = card.querySelector('h3').innerText;
            const desc = card.querySelector('p').innerText;
            const price = card.querySelector('.price').innerText;
            const img = card.querySelector('img').src;

            modalTitle.innerText = title;
            modalDesc.innerText = desc + " This is a premium product from Anqah Group, ensuring the highest quality and satisfaction.";
            modalPrice.innerText = price;
            modalImg.src = img;
            modalImg.alt = title;

            // Update WhatsApp link with product details
            const message = `Hello Anqah Group, I am interested in inquiring about "${title}" priced at ${price}. Could you provide more details?`;
            whatsappBtn.onclick = () => {
                const url = `https://wa.me/${whatsappNumber}?text=${encodeURIComponent(message)}`;
                window.open(url, '_blank');
            };

            modal.style.display = 'block';
            document.body.style.overflow = 'hidden';
        });
    });

    closeModal.addEventListener('click', () => {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    });

    window.onclick = (event) => {
        if (event.target == modal) {
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
        }
    };

    // Smooth scroll for nav links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
});
