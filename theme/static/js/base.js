// Flash message handling
document.addEventListener('DOMContentLoaded', () => {
    // Close flash messages on close button click
    document.querySelectorAll('.close-btn').forEach(btn => {
        // Prevent multiple event listeners by checking if already added
        if (!btn.dataset.listenerAdded) {
            btn.dataset.listenerAdded = 'true';
            btn.addEventListener('click', () => {
                const message = btn.closest('.flash-message');
                message.style.transition = 'opacity 0.3s ease';
                message.style.opacity = '0';
                setTimeout(() => {
                    message.style.display = 'none';
                }, 300); // Match transition duration
            });
        }
    });

    // Auto-close flash messages after 3 seconds
    document.querySelectorAll('.flash-message').forEach(msg => {
        setTimeout(() => {
            msg.style.transition = 'opacity 0.3s ease';
            msg.style.opacity = '0';
            setTimeout(() => {
                msg.style.display = 'none';
            }, 300); // Match transition duration
        }, 3000); // Auto-close after 3 seconds
    });
});





// Swiper slider
document.addEventListener("DOMContentLoaded", function () {
    const swiper = new Swiper('.swiper', {
        loop: true,
        autoplay: {
            delay: 3000,
            disableOnInteraction: false,
        },
        pagination: {
            el: '.swiper-pagination',
            clickable: true,
        },
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
    });
});



// AOS animations
document.addEventListener("DOMContentLoaded", function () {
    AOS.init({
        once: false,  // Ensures animation happens every time an element enters the viewport
        duration: 1000, // Adjust animation duration as needed
        offset: 100, // Adjust how early animation starts when scrolling
    });

    // Listen for scroll and refresh AOS when elements come into view
    window.addEventListener("scroll", function () {
        AOS.refresh();
    });
});



// Dynamic Navbar Styling Based on Scroll Position
document.addEventListener('DOMContentLoaded', () => {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;

    // List of all hero/banner sections that should trigger white navbar
    const heroSections = document.querySelectorAll('.heroSwiper, .STATS, .CTA');

    if (heroSections.length === 0) return;

    const observer = new IntersectionObserver((entries) => {
        // Check if ANY of the hero sections is visible
        const isHeroVisible = entries.some(entry => entry.isIntersecting);

        if (isHeroVisible) {
            // User is at the top (hero visible) → Solid white navbar
            navbar.classList.remove('bg-transparent', 'bg-white/10', 'backdrop-blur-md');
            navbar.classList.add('bg-white', 'shadow-lg');

            document.querySelectorAll('.nav-link').forEach(link => {
                link.classList.remove('text-white');
                link.classList.add('text-neutral-800');
            });

        } else {
            // Scrolled past hero → Glassy transparent navbar
            navbar.classList.remove('bg-white', 'shadow-lg');
            navbar.classList.add('bg-white/10', 'backdrop-blur-md');

            document.querySelectorAll('.nav-link').forEach(link => {
                link.classList.remove('text-neutral-800');
                link.classList.add('text-white');
            });


        }
    }, {
        threshold: 0.1,
        rootMargin: '-80px 0px 0px 0px' // Adjust based on your navbar height
    });

    // Observe ALL hero sections
    heroSections.forEach(section => observer.observe(section));
});