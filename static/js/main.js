// Main JavaScript for Front Page

document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for anchor links
    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add colorful particle effect to hero section
    createParticles();

    // Enhanced scroll animations
    const animateOnScroll = () => {
        const elements = document.querySelectorAll('.service-card, .card, .feature-badge');
        elements.forEach(element => {
            const elementTop = element.getBoundingClientRect().top;
            const elementVisible = 150;

            if (elementTop < window.innerHeight - elementVisible) {
                element.style.opacity = '1';
                element.style.transform = 'translateY(0)';
            }
        });
    };

    // Initialize elements for animation
    const elements = document.querySelectorAll('.service-card, .card, .feature-badge');
    elements.forEach(element => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(50px)';
        element.style.transition = 'all 0.6s ease';
    });

    window.addEventListener('scroll', animateOnScroll);
    animateOnScroll(); // Run once on load

    // Enhanced navbar scroll effect
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
                navbar.style.transform = 'translateY(0)';
            } else {
                navbar.classList.remove('scrolled');
            }
        });

        // Hide navbar on scroll down, show on scroll up
        let lastScrollTop = 0;
        window.addEventListener('scroll', function() {
            let scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            if (scrollTop > lastScrollTop && scrollTop > 100) {
                navbar.style.transform = 'translateY(-100%)';
            } else {
                navbar.style.transform = 'translateY(0)';
            }
            lastScrollTop = scrollTop;
        });
    }

    // Fade in animation on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);

    // Observe elements for fade-in animation
    const fadeElements = document.querySelectorAll('.card, .service-card, .feature-icon');
    fadeElements.forEach(el => {
        el.classList.add('fade-in');
        observer.observe(el);
    });

    // Form validation for appointment booking
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Mobile menu close on link click
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (navbarCollapse.classList.contains('show')) {
                const bsCollapse = new bootstrap.Collapse(navbarCollapse);
                bsCollapse.hide();
            }
        });
    });

    // Loading animation for buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            if (this.type === 'submit') {
                const originalText = this.innerHTML;
                this.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Loading...';
                this.disabled = true;
                
                // Re-enable after 3 seconds (adjust as needed)
                setTimeout(() => {
                    this.innerHTML = originalText;
                    this.disabled = false;
                }, 3000);
            }
        });
    });
});

// Particle effect function
function createParticles() {
    const heroSection = document.querySelector('.hero-section');
    if (!heroSection) return;

    const particleCount = 50;

    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.cssText = `
            position: absolute;
            width: ${Math.random() * 4 + 2}px;
            height: ${Math.random() * 4 + 2}px;
            background: ${['#ffd700', '#ff6b6b', '#4ecdc4', '#45b7d1'][Math.floor(Math.random() * 4)]};
            border-radius: 50%;
            left: ${Math.random() * 100}%;
            top: ${Math.random() * 100}%;
            opacity: ${Math.random() * 0.5 + 0.2};
            animation: particleFloat ${Math.random() * 3 + 2}s ease-in-out infinite;
            animation-delay: ${Math.random() * 2}s;
            pointer-events: none;
            z-index: 1;
        `;
        heroSection.appendChild(particle);
    }
}

// Additional CSS for animations and effects
const style = document.createElement('style');
style.textContent = `
    .navbar {
        transition: all 0.3s ease;
    }

    .navbar.scrolled .navbar-brand img {
        height: 35px;
    }

    @keyframes particleFloat {
        0%, 100% {
            transform: translateY(0px) translateX(0px) rotate(0deg);
            opacity: 0.2;
        }
        25% {
            transform: translateY(-20px) translateX(10px) rotate(90deg);
            opacity: 0.5;
        }
        50% {
            transform: translateY(-10px) translateX(-10px) rotate(180deg);
            opacity: 0.8;
        }
        75% {
            transform: translateY(-30px) translateX(5px) rotate(270deg);
            opacity: 0.3;
        }
    }

    .service-card {
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }

    .feature-badge {
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
`;
document.head.appendChild(style);
