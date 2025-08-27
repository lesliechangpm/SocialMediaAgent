// Social Media Agent - Main JavaScript Application
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        setTimeout(() => {
            card.classList.add('fade-in');
        }, index * 100);
    });

    // Auto-refresh rates every 5 minutes on dashboard
    if (window.location.pathname === '/') {
        setInterval(refreshRatesIfNeeded, 300000); // 5 minutes
    }
});

// Global utility functions
const SocialMediaAgent = {
    // API wrapper functions
    async apiRequest(endpoint, options = {}) {
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            },
        };

        const config = { ...defaultOptions, ...options };

        try {
            const response = await fetch(endpoint, config);
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || `HTTP error! status: ${response.status}`);
            }
            
            return data;
        } catch (error) {
            console.error('API Request failed:', error);
            throw error;
        }
    },

    // Generate content
    async generateContent(payload) {
        return this.apiRequest('/api/generate', {
            method: 'POST',
            body: JSON.stringify(payload)
        });
    },

    // Generate variations
    async generateVariations(payload) {
        return this.apiRequest('/api/variations', {
            method: 'POST',
            body: JSON.stringify(payload)
        });
    },

    // Get current rates
    async getCurrentRates() {
        return this.apiRequest('/api/rates');
    },

    // Get audience data
    async getAudiences() {
        return this.apiRequest('/api/audiences');
    },

    // Utility functions
    formatDate(date) {
        return new Date(date).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    },

    formatNumber(num, decimals = 2) {
        return parseFloat(num).toFixed(decimals);
    },

    // Copy to clipboard
    async copyToClipboard(text) {
        try {
            await navigator.clipboard.writeText(text);
            return true;
        } catch (err) {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.focus();
            textArea.select();
            
            try {
                const successful = document.execCommand('copy');
                document.body.removeChild(textArea);
                return successful;
            } catch (err) {
                document.body.removeChild(textArea);
                return false;
            }
        }
    },

    // Show toast notifications
    showToast(message, type = 'success') {
        const toastContainer = this.getOrCreateToastContainer();
        
        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-white bg-${type} border-0`;
        toast.setAttribute('role', 'alert');
        toast.setAttribute('aria-live', 'assertive');
        toast.setAttribute('aria-atomic', 'true');
        
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;
        
        toastContainer.appendChild(toast);
        
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();
        
        // Remove toast after it's hidden
        toast.addEventListener('hidden.bs.toast', () => {
            toast.remove();
        });
    },

    // Get or create toast container
    getOrCreateToastContainer() {
        let container = document.querySelector('.toast-container');
        
        if (!container) {
            container = document.createElement('div');
            container.className = 'toast-container position-fixed top-0 end-0 p-3';
            container.style.zIndex = '9999';
            document.body.appendChild(container);
        }
        
        return container;
    },

    // Loading states
    setLoadingState(element, loading = true) {
        if (loading) {
            element.dataset.originalHtml = element.innerHTML;
            element.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status"></span>Loading...';
            element.disabled = true;
        } else {
            element.innerHTML = element.dataset.originalHtml;
            element.disabled = false;
            delete element.dataset.originalHtml;
        }
    },

    // Form validation
    validateForm(formElement) {
        const inputs = formElement.querySelectorAll('input[required], select[required], textarea[required]');
        let isValid = true;
        
        inputs.forEach(input => {
            if (!input.value.trim()) {
                input.classList.add('is-invalid');
                isValid = false;
            } else {
                input.classList.remove('is-invalid');
            }
        });
        
        return isValid;
    },

    // Local storage helpers
    saveToLocalStorage(key, data) {
        try {
            localStorage.setItem(key, JSON.stringify(data));
            return true;
        } catch (err) {
            console.error('Failed to save to localStorage:', err);
            return false;
        }
    },

    loadFromLocalStorage(key) {
        try {
            const data = localStorage.getItem(key);
            return data ? JSON.parse(data) : null;
        } catch (err) {
            console.error('Failed to load from localStorage:', err);
            return null;
        }
    },

    // Content analysis
    analyzeContent(content) {
        const analysis = {
            characterCount: content.length,
            wordCount: content.split(/\s+/).filter(word => word.length > 0).length,
            hashtagCount: (content.match(/#\w+/g) || []).length,
            mentionCount: (content.match(/@\w+/g) || []).length,
            lineCount: content.split('\n').length,
            readingTime: Math.ceil(content.split(/\s+/).length / 200) // ~200 words per minute
        };
        
        return analysis;
    },

    // Platform-specific validation
    validateForPlatform(content, platform) {
        const limits = {
            instagram: { maxChars: 2200, optimalChars: 350, maxHashtags: 30 },
            facebook: { maxChars: 63206, optimalChars: 500, maxHashtags: 30 },
            linkedin: { maxChars: 3000, optimalChars: 700, maxHashtags: 20 }
        };
        
        const platformLimits = limits[platform] || limits.facebook;
        const analysis = this.analyzeContent(content);
        
        const validation = {
            isValid: true,
            warnings: [],
            errors: []
        };
        
        if (analysis.characterCount > platformLimits.maxChars) {
            validation.isValid = false;
            validation.errors.push(`Content exceeds ${platform} character limit (${analysis.characterCount} > ${platformLimits.maxChars})`);
        } else if (analysis.characterCount > platformLimits.optimalChars) {
            validation.warnings.push(`Content is longer than optimal for ${platform} (${analysis.characterCount} > ${platformLimits.optimalChars})`);
        }
        
        if (analysis.hashtagCount > platformLimits.maxHashtags) {
            validation.isValid = false;
            validation.errors.push(`Too many hashtags for ${platform} (${analysis.hashtagCount} > ${platformLimits.maxHashtags})`);
        }
        
        return validation;
    }
};

// Dashboard-specific functions
function refreshRatesIfNeeded() {
    // Only refresh if rates data is older than 30 minutes
    const ratesTimestamp = localStorage.getItem('rates_timestamp');
    const now = Date.now();
    
    if (!ratesTimestamp || (now - parseInt(ratesTimestamp)) > 1800000) { // 30 minutes
        refreshRates();
    }
}

function refreshRates() {
    SocialMediaAgent.getCurrentRates()
        .then(data => {
            if (data.success) {
                localStorage.setItem('rates_timestamp', Date.now().toString());
                // Update rates display if elements exist
                updateRatesDisplay(data.rates);
                SocialMediaAgent.showToast('Rates updated successfully');
            }
        })
        .catch(error => {
            SocialMediaAgent.showToast('Failed to refresh rates: ' + error.message, 'warning');
        });
}

function updateRatesDisplay(rates) {
    // Update rate display elements if they exist on the page
    const rateElement = document.querySelector('[data-rate-current]');
    const changeElement = document.querySelector('[data-rate-change]');
    const dateElement = document.querySelector('[data-rate-date]');
    
    if (rateElement) rateElement.textContent = SocialMediaAgent.formatNumber(rates.current_rate) + '%';
    if (changeElement) {
        const change = rates.rate_change;
        changeElement.textContent = (change > 0 ? '+' : '') + SocialMediaAgent.formatNumber(change) + '%';
        changeElement.className = change > 0 ? 'text-danger' : change < 0 ? 'text-success' : 'text-secondary';
    }
    if (dateElement) dateElement.textContent = rates.date;
}

// Enhanced copy function with feedback
async function copyContentWithFeedback(content, buttonElement) {
    if (!content) return;
    
    const success = await SocialMediaAgent.copyToClipboard(content);
    
    if (success) {
        const originalText = buttonElement.innerHTML;
        buttonElement.innerHTML = '<i class="fas fa-check me-1"></i>Copied!';
        buttonElement.classList.remove('btn-outline-primary', 'btn-primary');
        buttonElement.classList.add('btn-success');
        
        setTimeout(() => {
            buttonElement.innerHTML = originalText;
            buttonElement.classList.remove('btn-success');
            buttonElement.classList.add('btn-outline-primary');
        }, 2000);
        
        SocialMediaAgent.showToast('Content copied to clipboard!');
    } else {
        SocialMediaAgent.showToast('Failed to copy content', 'danger');
    }
}

// Auto-save functionality for form data
function autoSaveFormData(formId, key) {
    const form = document.getElementById(formId);
    if (!form) return;
    
    // Load saved data
    const savedData = SocialMediaAgent.loadFromLocalStorage(key);
    if (savedData) {
        Object.keys(savedData).forEach(fieldName => {
            const field = form.querySelector(`[name="${fieldName}"]`);
            if (field) {
                field.value = savedData[fieldName];
            }
        });
    }
    
    // Save data on input change
    form.addEventListener('input', function(e) {
        const formData = new FormData(form);
        const data = Object.fromEntries(formData);
        SocialMediaAgent.saveToLocalStorage(key, data);
    });
}

// Real-time content analysis
function setupContentAnalysis(textareaId, analysisContainerId) {
    const textarea = document.getElementById(textareaId);
    const container = document.getElementById(analysisContainerId);
    
    if (!textarea || !container) return;
    
    function updateAnalysis() {
        const content = textarea.value;
        const analysis = SocialMediaAgent.analyzeContent(content);
        
        container.innerHTML = `
            <div class="row text-center">
                <div class="col">
                    <div class="fw-bold">${analysis.characterCount}</div>
                    <small class="text-muted">Characters</small>
                </div>
                <div class="col">
                    <div class="fw-bold">${analysis.wordCount}</div>
                    <small class="text-muted">Words</small>
                </div>
                <div class="col">
                    <div class="fw-bold">${analysis.hashtagCount}</div>
                    <small class="text-muted">Hashtags</small>
                </div>
                <div class="col">
                    <div class="fw-bold">${analysis.readingTime}min</div>
                    <small class="text-muted">Read Time</small>
                </div>
            </div>
        `;
    }
    
    textarea.addEventListener('input', updateAnalysis);
    updateAnalysis(); // Initial analysis
}

// Export functions to global scope for inline event handlers
window.SocialMediaAgent = SocialMediaAgent;
window.copyContentWithFeedback = copyContentWithFeedback;
window.refreshRates = refreshRates;