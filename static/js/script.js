// Basic form validation and interactivity
document.addEventListener('DOMContentLoaded', function() {
    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            let valid = true;
            const inputs = form.querySelectorAll('input[required], select[required]');
            
            inputs.forEach(input => {
                if (!input.value.trim()) {
                    valid = false;
                    highlightError(input);
                } else {
                    removeErrorHighlight(input);
                }
            });
            
            if (!valid) {
                e.preventDefault();
                showNotification('Please fill in all required fields.', 'error');
            }
        });
    });
    
    // Input validation
    const numberInputs = document.querySelectorAll('input[type="number"]');
    numberInputs.forEach(input => {
        input.addEventListener('blur', function() {
            const min = parseFloat(this.min);
            const max = parseFloat(this.max);
            const value = parseFloat(this.value);
            
            if (!isNaN(min) && value < min) {
                this.value = min;
                showNotification(`Value cannot be less than ${min}`, 'warning');
            }
            
            if (!isNaN(max) && value > max) {
                this.value = max;
                showNotification(`Value cannot be greater than ${max}`, 'warning');
            }
        });
    });
    
    // Interactive elements
    const interactiveElements = document.querySelectorAll('.feature-card, .btn');
    interactiveElements.forEach(element => {
        element.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-3px)';
            this.style.boxShadow = '0 6px 12px rgba(0, 0, 0, 0.1)';
        });
        
        element.addEventListener('mouseleave', function() {
            this.style.transform = '';
            this.style.boxShadow = '';
        });
    });
});

function highlightError(element) {
    element.style.borderColor = '#e63946';
    element.style.boxShadow = '0 0 0 3px rgba(230, 57, 70, 0.1)';
}

function removeErrorHighlight(element) {
    element.style.borderColor = '';
    element.style.boxShadow = '';
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'error' ? 'exclamation-circle' : type === 'warning' ? 'exclamation-triangle' : 'info-circle'}"></i>
        <span>${message}</span>
    `;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 5px;
        color: white;
        display: flex;
        align-items: center;
        gap: 10px;
        z-index: 1000;
        transform: translateX(100%);
        transition: transform 0.3s;
    `;
    
    if (type === 'error') {
        notification.style.background = '#e63946';
    } else if (type === 'warning') {
        notification.style.background = '#fca311';
    } else {
        notification.style.background = '#4361ee';
    }
    
    // Add to document
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 10);
    
    // Remove after delay
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// Heart animation control
function setHeartRate(rate) {
    const heart = document.querySelector('.heart');
    const glow = document.querySelector('.heart-glow');
    if (heart) {
        const bpm = Math.max(30, Math.min(200, rate || 72));
        const duration = 60 / bpm; // seconds per beat
        // intensity: faster heart -> slightly stronger contraction up to a cap
        const scale = (bpm < 60) ? 1.12 : ((bpm < 90) ? 1.22 : 1.36);
        // glow scale follows contraction but is a bit larger
        const glowScale = Math.min(2.6, scale * 1.6);

        // set CSS variables so both elements use the same timing and intensity
        heart.style.setProperty('--hr-duration', `${duration}s`);
        heart.style.setProperty('--hr-scale', scale);
        heart.style.setProperty('--hr-glow-scale', glowScale);
        if (glow) {
            glow.style.setProperty('--hr-duration', `${duration}s`);
            glow.style.setProperty('--hr-glow-scale', glowScale);
        }
    }
}

// Initialize interactive elements
function initInteractiveElements() {
    // Add loading state to buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (this.type === 'submit' || this.href) {
                this.classList.add('loading');
                this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
                
                // For demonstration purposes, remove loading state after 2 seconds
                if (!this.href) {
                    setTimeout(() => {
                        this.classList.remove('loading');
                        this.innerHTML = this.getAttribute('data-original-text') || 'Submit';
                    }, 2000);
                }
            }
        });
    });
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', initInteractiveElements);

// Theme toggle
function setDarkMode(enabled) {
    if (enabled) document.body.classList.add('dark-mode');
    else document.body.classList.remove('dark-mode');
}

function toggleTheme() {
    const enabled = document.body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', enabled ? '1' : '0');
}

// Apply theme from storage on load
document.addEventListener('DOMContentLoaded', function() {
    try {
        const stored = localStorage.getItem('darkMode');
        if (stored === '1') setDarkMode(true);
        const btn = document.getElementById('themeToggle');
        if (btn) btn.addEventListener('click', toggleTheme);
    } catch (e) {
        // ignore storage errors
    }
});