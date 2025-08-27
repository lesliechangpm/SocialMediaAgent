// Advanced UX Interactions - Enhanced User Experience Features

class SocialMediaAgentUX {
    constructor() {
        this.init();
        this.bindEvents();
        this.setupNotifications();
    }

    init() {
        console.log('🎨 Advanced UX Interactions initialized');
        this.addAccessibilityFeatures();
        this.setupProgressiveDisclosure();
        this.initializeTooltips();
    }

    // =============================================================================
    // ENHANCED USER FEEDBACK
    // =============================================================================

    bindEvents() {
        // Enhanced button interactions
        this.setupButtonFeedback();
        
        // Form enhancements
        this.setupFormInteractions();
        
        // Card interactions
        this.setupCardInteractions();
        
        // Keyboard shortcuts
        this.setupKeyboardShortcuts();
    }

    setupButtonFeedback() {
        document.querySelectorAll('.btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.createRippleEffect(e);
                this.addClickFeedback(btn);
            });
        });
    }

    createRippleEffect(e) {
        const button = e.currentTarget;
        const ripple = document.createElement('span');
        const rect = button.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;

        ripple.style.cssText = `
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.6);
            transform: scale(0);
            animation: ripple 0.6s linear;
            left: ${x}px;
            top: ${y}px;
            width: ${size}px;
            height: ${size}px;
        `;

        button.appendChild(ripple);
        setTimeout(() => ripple.remove(), 600);
    }

    addClickFeedback(btn) {
        btn.style.transform = 'scale(0.95)';
        setTimeout(() => {
            btn.style.transform = '';
        }, 150);
    }

    // =============================================================================
    // FORM ENHANCEMENTS
    // =============================================================================

    setupFormInteractions() {
        // Real-time character count
        this.setupCharacterCount();
        
        // Smart form validation
        this.setupSmartValidation();
        
        // Auto-save functionality
        this.setupAutoSave();
    }

    setupCharacterCount() {
        const textInputs = document.querySelectorAll('textarea, input[type="text"]');
        
        textInputs.forEach(input => {
            if (input.dataset.characterCount === 'true') {
                const maxLength = input.getAttribute('maxlength') || 280;
                this.addCharacterCounter(input, maxLength);
            }
        });
    }

    addCharacterCounter(input, maxLength) {
        const counter = document.createElement('div');
        counter.className = 'character-counter mt-2';
        counter.innerHTML = `
            <div class="d-flex justify-content-between align-items-center">
                <small class="text-muted">Characters: <span class="count">0</span>/${maxLength}</small>
                <div class="character-count">
                    <div class="character-count-fill" style="width: 0%"></div>
                </div>
            </div>
        `;

        input.parentNode.insertBefore(counter, input.nextSibling);

        input.addEventListener('input', () => {
            const count = input.value.length;
            const percentage = (count / maxLength) * 100;
            
            counter.querySelector('.count').textContent = count;
            counter.querySelector('.character-count-fill').style.width = `${percentage}%`;
            
            // Color feedback
            if (percentage > 90) {
                counter.querySelector('.character-count').style.background = 'linear-gradient(90deg, #dc3545 0%, #dc3545 100%)';
            } else if (percentage > 70) {
                counter.querySelector('.character-count').style.background = 'linear-gradient(90deg, #28a745 0%, #ffc107 70%, #dc3545 90%)';
            } else {
                counter.querySelector('.character-count').style.background = 'linear-gradient(90deg, #28a745 0%, #ffc107 70%, #dc3545 90%)';
            }
        });
    }

    setupSmartValidation() {
        const forms = document.querySelectorAll('form');
        
        forms.forEach(form => {
            const inputs = form.querySelectorAll('input, textarea, select');
            
            inputs.forEach(input => {
                input.addEventListener('blur', () => this.validateField(input));
                input.addEventListener('input', () => this.clearValidation(input));
            });
        });
    }

    validateField(field) {
        const value = field.value.trim();
        let isValid = true;
        let message = '';

        // Custom validation rules
        if (field.hasAttribute('required') && !value) {
            isValid = false;
            message = 'This field is required';
        } else if (field.type === 'email' && value && !this.isValidEmail(value)) {
            isValid = false;
            message = 'Please enter a valid email address';
        }

        this.showValidationFeedback(field, isValid, message);
    }

    isValidEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }

    showValidationFeedback(field, isValid, message) {
        this.clearValidation(field);

        if (!isValid) {
            field.classList.add('is-invalid');
            const feedback = document.createElement('div');
            feedback.className = 'invalid-feedback';
            feedback.textContent = message;
            field.parentNode.appendChild(feedback);
        } else if (field.value.trim()) {
            field.classList.add('is-valid');
        }
    }

    clearValidation(field) {
        field.classList.remove('is-invalid', 'is-valid');
        const feedback = field.parentNode.querySelector('.invalid-feedback');
        if (feedback) feedback.remove();
    }

    setupAutoSave() {
        const forms = document.querySelectorAll('form[data-autosave]');
        
        forms.forEach(form => {
            const formId = form.id || 'unnamed-form';
            
            // Load saved data
            this.loadSavedFormData(form, formId);
            
            // Save on input
            form.addEventListener('input', () => {
                this.saveFormData(form, formId);
                this.showAutoSaveIndicator();
            });
        });
    }

    saveFormData(form, formId) {
        const formData = new FormData(form);
        const data = Object.fromEntries(formData);
        localStorage.setItem(`autosave_${formId}`, JSON.stringify(data));
    }

    loadSavedFormData(form, formId) {
        const saved = localStorage.getItem(`autosave_${formId}`);
        if (saved) {
            const data = JSON.parse(saved);
            Object.entries(data).forEach(([name, value]) => {
                const field = form.querySelector(`[name="${name}"]`);
                if (field) field.value = value;
            });
        }
    }

    showAutoSaveIndicator() {
        this.showToast('Draft saved automatically', 'success', 2000);
    }

    // =============================================================================
    // CARD INTERACTIONS
    // =============================================================================

    setupCardInteractions() {
        document.querySelectorAll('.status-card').forEach(card => {
            card.addEventListener('click', () => {
                this.animateCardClick(card);
                this.handleCardAction(card);
            });
        });
    }

    animateCardClick(card) {
        card.style.transform = 'scale(0.95)';
        setTimeout(() => {
            card.style.transform = '';
        }, 200);
    }

    handleCardAction(card) {
        const cardTitle = card.querySelector('h5, h6').textContent.trim();
        
        switch (cardTitle) {
            case 'AI Engine':
                this.showAIEngineDetails();
                break;
            case 'Rate Data':
                this.refreshRates();
                break;
            case 'Profile':
                window.location.href = '/settings';
                break;
            default:
                console.log(`Clicked on: ${cardTitle}`);
        }
    }

    showAIEngineDetails() {
        this.showToast('AI Engine is running Claude Sonnet 4', 'info', 3000);
    }

    // =============================================================================
    // PROGRESSIVE DISCLOSURE
    // =============================================================================

    setupProgressiveDisclosure() {
        // Advanced options toggles
        this.createAdvancedToggles();
        
        // Collapsible sections
        this.setupCollapsibleSections();
    }

    createAdvancedToggles() {
        const forms = document.querySelectorAll('form');
        
        forms.forEach(form => {
            const advancedFields = form.querySelectorAll('[data-advanced]');
            
            if (advancedFields.length > 0) {
                this.addAdvancedToggle(form, advancedFields);
            }
        });
    }

    addAdvancedToggle(form, fields) {
        const toggle = document.createElement('button');
        toggle.type = 'button';
        toggle.className = 'advanced-toggle btn btn-sm btn-outline-secondary mb-3';
        toggle.innerHTML = '<i class="fas fa-chevron-down me-2"></i>Advanced Options';

        const container = document.createElement('div');
        container.className = 'collapsible';
        
        fields.forEach(field => {
            container.appendChild(field.closest('.mb-3') || field);
        });

        form.insertBefore(toggle, form.querySelector('.d-grid, button[type="submit"]'));
        form.insertBefore(container, form.querySelector('.d-grid, button[type="submit"]'));

        toggle.addEventListener('click', () => {
            container.classList.toggle('active');
            toggle.classList.toggle('active');
            
            const icon = toggle.querySelector('i');
            if (container.classList.contains('active')) {
                toggle.innerHTML = '<i class="fas fa-chevron-up me-2"></i>Hide Advanced Options';
            } else {
                toggle.innerHTML = '<i class="fas fa-chevron-down me-2"></i>Advanced Options';
            }
        });
    }

    setupCollapsibleSections() {
        document.querySelectorAll('[data-toggle="collapse"]').forEach(trigger => {
            trigger.addEventListener('click', (e) => {
                e.preventDefault();
                const target = document.querySelector(trigger.dataset.target);
                if (target) {
                    target.classList.toggle('active');
                }
            });
        });
    }

    // =============================================================================
    // ACCESSIBILITY FEATURES
    // =============================================================================

    addAccessibilityFeatures() {
        this.addSkipLink();
        this.enhanceFocusManagement();
        this.addAriaLabels();
    }

    addSkipLink() {
        const skipLink = document.createElement('a');
        skipLink.href = '#main-content';
        skipLink.className = 'skip-link';
        skipLink.textContent = 'Skip to main content';
        document.body.insertBefore(skipLink, document.body.firstChild);
    }

    enhanceFocusManagement() {
        // Trap focus in modals
        document.querySelectorAll('.modal').forEach(modal => {
            modal.addEventListener('shown.bs.modal', () => {
                const firstFocusable = modal.querySelector('input, button, textarea, select, a[href]');
                if (firstFocusable) firstFocusable.focus();
            });
        });
    }

    addAriaLabels() {
        // Add aria-labels to interactive elements without labels
        document.querySelectorAll('button:not([aria-label]):not([aria-labelledby])').forEach(btn => {
            const text = btn.textContent.trim() || btn.title || 'Button';
            btn.setAttribute('aria-label', text);
        });
    }

    // =============================================================================
    // KEYBOARD SHORTCUTS
    // =============================================================================

    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ctrl/Cmd + G for generate
            if ((e.ctrlKey || e.metaKey) && e.key === 'g') {
                e.preventDefault();
                const generateBtn = document.querySelector('button[type="submit"], .btn-primary');
                if (generateBtn) generateBtn.click();
                this.showToast('Keyboard shortcut: Generate (Ctrl+G)', 'info', 2000);
            }

            // Ctrl/Cmd + S for save
            if ((e.ctrlKey || e.metaKey) && e.key === 's') {
                e.preventDefault();
                const saveBtn = document.querySelector('#saveBtn');
                if (saveBtn && !saveBtn.disabled) saveBtn.click();
            }

            // Escape to close modals
            if (e.key === 'Escape') {
                const openModal = document.querySelector('.modal.show');
                if (openModal) {
                    const modal = bootstrap.Modal.getInstance(openModal);
                    if (modal) modal.hide();
                }
            }
        });
    }

    // =============================================================================
    // TOOLTIP SYSTEM
    // =============================================================================

    initializeTooltips() {
        // Add tooltips to elements with data-tooltip attribute
        document.querySelectorAll('[data-tooltip]').forEach(element => {
            element.classList.add('tooltip-container');
        });

        // Initialize Bootstrap tooltips
        const tooltipElements = document.querySelectorAll('[data-bs-toggle="tooltip"]');
        tooltipElements.forEach(element => {
            new bootstrap.Tooltip(element);
        });
    }

    // =============================================================================
    // NOTIFICATION SYSTEM
    // =============================================================================

    setupNotifications() {
        // Create toast container if it doesn't exist
        if (!document.querySelector('.toast-container')) {
            const container = document.createElement('div');
            container.className = 'toast-container';
            document.body.appendChild(container);
        }
    }

    showToast(message, type = 'info', duration = 3000) {
        const container = document.querySelector('.toast-container');
        const toast = document.createElement('div');
        toast.className = `toast toast-${type} show`;
        toast.setAttribute('role', 'alert');
        toast.innerHTML = `
            <div class="toast-body">
                <i class="fas fa-${this.getToastIcon(type)} me-2"></i>
                ${message}
                <button type="button" class="btn-close ms-auto" data-bs-dismiss="toast"></button>
            </div>
        `;

        container.appendChild(toast);

        // Auto-hide
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, duration);

        // Manual close
        const closeBtn = toast.querySelector('.btn-close');
        closeBtn.addEventListener('click', () => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        });
    }

    getToastIcon(type) {
        const icons = {
            success: 'check-circle',
            error: 'exclamation-circle',
            warning: 'exclamation-triangle',
            info: 'info-circle'
        };
        return icons[type] || 'info-circle';
    }

    // =============================================================================
    // UTILITY METHODS
    // =============================================================================

    refreshRates() {
        this.showToast('Refreshing mortgage rates...', 'info', 2000);
        // Trigger rate refresh if function exists
        if (window.refreshRates) {
            window.refreshRates();
        }
    }

    // Performance optimization: Debounce function
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    // Check if user prefers reduced motion
    respectsReducedMotion() {
        return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.socialMediaAgentUX = new SocialMediaAgentUX();
});

// Add CSS for ripple effect animation
const style = document.createElement('style');
style.textContent = `
    @keyframes ripple {
        to {
            transform: scale(2);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);