document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const languageSelect = document.getElementById('language');
    const fileInput = document.getElementById('audio');
    const submitButton = document.querySelector('input[type="submit"]');

    form.style.opacity = '0';
    form.style.transform = 'translateY(20px)';
    setTimeout(() => {
        form.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        form.style.opacity = '1';
        form.style.transform = 'translateY(0)';
    }, 100);
    languageSelect.addEventListener('change', function() {
        this.style.transform = 'scale(1.03)';
        setTimeout(() => this.style.transform = 'scale(1)', 300);
    });
    fileInput.addEventListener('change', function() {
        const fileName = this.files[0].name;
        let fileNameDisplay = this.nextElementSibling;
        if (!fileNameDisplay || !fileNameDisplay.classList.contains('file-name')) {
            fileNameDisplay = document.createElement('div');
            fileNameDisplay.classList.add('file-name');
            this.parentNode.insertBefore(fileNameDisplay, this.nextSibling);
        }
        fileNameDisplay.textContent = `Selected file: ${fileName}`;
        fileNameDisplay.style.opacity = '0';
        fileNameDisplay.style.transform = 'translateY(-10px)';
        setTimeout(() => {
            fileNameDisplay.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
            fileNameDisplay.style.opacity = '1';
            fileNameDisplay.style.transform = 'translateY(0)';
        }, 50);
    });
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        submitButton.value = 'Translating...';
        submitButton.disabled = true;
        submitButton.style.cursor = 'wait';
        submitButton.classList.add('loading');
        setTimeout(() => {
            submitButton.value = 'Translation Complete!';
            submitButton.style.backgroundColor = '#4ecdc4';
            submitButton.classList.remove('loading');
            createStarryBackground();
            setTimeout(() => {
                submitButton.value = 'Translate';
                submitButton.disabled = false;
                submitButton.style.cursor = 'pointer';
                submitButton.style.backgroundColor = '';
                removeStarryBackground();
            }, 2000);
        }, 3000);
    });
    form.addEventListener('mouseenter', function() {
        this.style.transform = 'scale(1.02)';
        this.style.boxShadow = '0 15px 35px rgba(0, 0, 0, 0.3)';
    });

    form.addEventListener('mouseleave', function() {
        this.style.transform = 'scale(1)';
        this.style.boxShadow = '0 10px 30px rgba(0, 0, 0, 0.2)';
    });

    function createStarryBackground() {
        const starContainer = document.createElement('div');
        starContainer.id = 'starry-background';
        starContainer.style.position = 'fixed';
        starContainer.style.top = '0';
        starContainer.style.left = '0';
        starContainer.style.width = '100%';
        starContainer.style.height = '100%';
        starContainer.style.pointerEvents = 'none';
        document.body.appendChild(starContainer);

        for (let i = 0; i < 100; i++) {
            const star = document.createElement('div');
            star.style.position = 'absolute';
            star.style.width = '2px';
            star.style.height = '2px';
            star.style.backgroundColor = 'white';
            star.style.borderRadius = '50%';
            star.style.left = `${Math.random() * 100}%`;
            star.style.top = `${Math.random() * 100}%`;
            star.style.animation = `twinkle ${Math.random() * 2 + 1}s infinite`;
            starContainer.appendChild(star);
        }

        const style = document.createElement('style');
        style.textContent = `
            @keyframes twinkle {
                0% { opacity: 0; }
                50% { opacity: 1; }
                100% { opacity: 0; }
            }
        `;
        document.head.appendChild(style);
    }

    function removeStarryBackground() {
        const starContainer = document.getElementById('starry-background');
        if (starContainer) {
            starContainer.remove();
        }
    }
});