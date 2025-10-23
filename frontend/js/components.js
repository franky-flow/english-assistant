/**
 * UI Components and Utilities for English Assistant
 */

/**
 * Main UI utility class
 */
class UI {
    /**
     * Show success toast message
     */
    static showSuccess(message) {
        const toast = document.getElementById('success-toast');
        const messageEl = document.getElementById('success-message');
        
        messageEl.textContent = message;
        toast.classList.remove('hidden');
        
        setTimeout(() => {
            toast.classList.add('hidden');
        }, CONFIG.TOAST_DURATION);
    }

    /**
     * Show error modal
     */
    static showError(message, details = null) {
        const modal = document.getElementById('error-modal');
        const messageEl = document.getElementById('error-message');
        
        messageEl.textContent = message;
        modal.classList.remove('hidden');
        
        // Log details to console for debugging
        if (details) {
            console.error('Error details:', details);
        }
    }

    /**
     * Hide error modal
     */
    static hideError() {
        const modal = document.getElementById('error-modal');
        modal.classList.add('hidden');
    }

    /**
     * Show loading screen
     */
    static showLoading() {
        const loading = document.getElementById('loading-screen');
        loading.style.display = 'flex';
    }

    /**
     * Hide loading screen
     */
    static hideLoading() {
        const loading = document.getElementById('loading-screen');
        const app = document.getElementById('app');
        
        loading.style.display = 'none';
        app.style.display = 'flex';
    }

    /**
     * Create loading spinner element
     */
    static createSpinner(size = 'w-6 h-6') {
        const spinner = document.createElement('div');
        spinner.className = `loading-spinner ${size}`;
        return spinner;
    }

    /**
     * Create badge element
     */
    static createBadge(text, type = 'gray') {
        const badge = document.createElement('span');
        badge.className = `badge-${type}`;
        badge.textContent = text;
        return badge;
    }

    /**
     * Create button element
     */
    static createButton(text, type = 'primary', onClick = null) {
        const button = document.createElement('button');
        button.className = `btn-${type}`;
        button.textContent = text;
        
        if (onClick) {
            button.addEventListener('click', onClick);
        }
        
        return button;
    }

    /**
     * Format date for display
     */
    static formatDate(date) {
        if (typeof date === 'string') {
            date = new Date(date);
        }
        
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    }

    /**
     * Truncate text with ellipsis
     */
    static truncateText(text, maxLength = 100) {
        if (text.length <= maxLength) return text;
        return text.substring(0, maxLength) + '...';
    }

    /**
     * Escape HTML to prevent XSS
     */
    static escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    /**
     * Copy text to clipboard
     */
    static async copyToClipboard(text) {
        try {
            await navigator.clipboard.writeText(text);
            UI.showSuccess(CONFIG.SUCCESS_MESSAGES.COPIED);
        } catch (error) {
            console.error('Failed to copy to clipboard:', error);
            UI.showError('Failed to copy to clipboard');
        }
    }

    /**
     * Animate element entrance
     */
    static animateIn(element, animation = 'fade-in') {
        element.classList.add(animation);
        setTimeout(() => {
            element.classList.remove(animation);
        }, 300);
    }
}

/**
 * Input/Response Layout Component
 */
class InputResponseLayout {
    constructor(container, options = {}) {
        this.container = container;
        this.options = {
            placeholder: 'Enter your text here...',
            buttonText: 'Submit',
            showExamples: true,
            showTags: true,
            ...options
        };
        
        this.render();
        this.bindEvents();
    }

    render() {
        this.container.innerHTML = `
            <div class="space-y-6">
                <!-- Input Section -->
                <div class="card">
                    <div class="card-body">
                        <form id="input-form" class="space-y-4">
                            <div>
                                <label class="form-label">Input</label>
                                <textarea 
                                    id="input-text" 
                                    class="textarea-field" 
                                    placeholder="${this.options.placeholder}"
                                    required
                                ></textarea>
                                <div class="form-help">
                                    Enter your text and click submit to get AI-powered assistance.
                                </div>
                            </div>
                            
                            ${this.options.showOptions ? this.renderOptions() : ''}
                            
                            <div class="flex justify-between items-center">
                                <div class="text-sm text-gray-500">
                                    <span id="char-count">0</span> characters
                                </div>
                                <button type="submit" class="btn-primary" id="submit-btn">
                                    ${this.options.buttonText}
                                </button>
                            </div>
                        </form>
                    </div>
                </div>

                <!-- Loading State -->
                <div id="loading-state" class="hidden">
                    <div class="card">
                        <div class="card-body text-center py-8">
                            <div class="loading-spinner w-8 h-8 mx-auto mb-4"></div>
                            <p class="text-gray-600">Processing your request<span class="loading-dots"></span></p>
                        </div>
                    </div>
                </div>

                <!-- Response Section -->
                <div id="response-section" class="hidden">
                    <div class="card">
                        <div class="card-header">
                            <div class="flex justify-between items-center">
                                <h3 class="text-lg font-semibold">Result</h3>
                                <button id="copy-result" class="btn-secondary btn-sm">
                                    📋 Copy
                                </button>
                            </div>
                        </div>
                        <div class="card-body">
                            <div id="response-content"></div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    renderOptions() {
        // Override in subclasses for specific options
        return '';
    }

    bindEvents() {
        const form = this.container.querySelector('#input-form');
        const inputText = this.container.querySelector('#input-text');
        const charCount = this.container.querySelector('#char-count');
        const submitBtn = this.container.querySelector('#submit-btn');
        const copyBtn = this.container.querySelector('#copy-result');

        // Character count
        inputText.addEventListener('input', () => {
            charCount.textContent = inputText.value.length;
        });

        // Form submission
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            await this.handleSubmit();
        });

        // Copy result
        if (copyBtn) {
            copyBtn.addEventListener('click', () => {
                const responseContent = this.container.querySelector('#response-content');
                if (responseContent) {
                    UI.copyToClipboard(responseContent.textContent);
                }
            });
        }
    }

    async handleSubmit() {
        const inputText = this.container.querySelector('#input-text');
        const loadingState = this.container.querySelector('#loading-state');
        const responseSection = this.container.querySelector('#response-section');
        const submitBtn = this.container.querySelector('#submit-btn');

        if (!inputText.value.trim()) {
            UI.showError('Please enter some text');
            return;
        }

        // Show loading state
        loadingState.classList.remove('hidden');
        responseSection.classList.add('hidden');
        submitBtn.disabled = true;

        try {
            const result = await this.processRequest(inputText.value.trim());
            this.displayResult(result);
            responseSection.classList.remove('hidden');
        } catch (error) {
            console.error('Request failed:', error);
        } finally {
            loadingState.classList.add('hidden');
            submitBtn.disabled = false;
        }
    }

    async processRequest(text) {
        // Override in subclasses
        throw new Error('processRequest must be implemented by subclass');
    }

    displayResult(result) {
        const responseContent = this.container.querySelector('#response-content');
        
        responseContent.innerHTML = `
            <div class="space-y-4">
                <div>
                    <h4 class="font-semibold text-gray-900 mb-2">Result</h4>
                    <p class="text-gray-700">${UI.escapeHtml(result.data.result)}</p>
                </div>
                
                ${result.data.explanation ? `
                    <div>
                        <h4 class="font-semibold text-gray-900 mb-2">Explanation</h4>
                        <p class="text-gray-700">${UI.escapeHtml(result.data.explanation)}</p>
                    </div>
                ` : ''}
                
                ${result.data.examples && result.data.examples.length > 0 ? `
                    <div>
                        <h4 class="font-semibold text-gray-900 mb-2">Examples</h4>
                        <ul class="list-disc list-inside space-y-1 text-gray-700">
                            ${result.data.examples.map(example => 
                                `<li>${UI.escapeHtml(example)}</li>`
                            ).join('')}
                        </ul>
                    </div>
                ` : ''}
                
                ${result.data.tags && result.data.tags.length > 0 ? `
                    <div>
                        <h4 class="font-semibold text-gray-900 mb-2">Tags</h4>
                        <div class="flex flex-wrap gap-2">
                            ${result.data.tags.map(tag => 
                                `<span class="badge-info">${UI.escapeHtml(tag)}</span>`
                            ).join('')}
                        </div>
                    </div>
                ` : ''}
            </div>
        `;

        UI.animateIn(responseContent, 'slide-up');
    }

    clear() {
        const inputText = this.container.querySelector('#input-text');
        const responseSection = this.container.querySelector('#response-section');
        const charCount = this.container.querySelector('#char-count');

        inputText.value = '';
        charCount.textContent = '0';
        responseSection.classList.add('hidden');
    }
}

/**
 * Navigation Manager
 */
class Navigation {
    constructor() {
        this.currentPage = 'home';
        this.bindEvents();
    }

    bindEvents() {
        // Desktop navigation
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const page = link.dataset.page;
                this.navigateTo(page);
            });
        });

        // Mobile navigation
        const mobileNavLinks = document.querySelectorAll('.mobile-nav-link');
        mobileNavLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const page = link.dataset.page;
                this.navigateTo(page);
                this.closeMobileMenu();
            });
        });

        // Mobile menu toggle
        const mobileMenuBtn = document.getElementById('mobile-menu-btn');
        const mobileNav = document.getElementById('mobile-nav');
        
        mobileMenuBtn.addEventListener('click', () => {
            mobileNav.classList.toggle('hidden');
        });

        // Error modal close
        const errorModalClose = document.getElementById('error-modal-close');
        errorModalClose.addEventListener('click', () => {
            UI.hideError();
        });
    }

    navigateTo(page) {
        if (this.currentPage === page) return;

        // Update active states
        this.updateActiveStates(page);
        
        // Load page content
        if (window.Pages && window.Pages[page]) {
            window.Pages[page]();
        }

        this.currentPage = page;
        
        // Update URL hash
        window.location.hash = page;
    }

    updateActiveStates(page) {
        // Desktop navigation
        document.querySelectorAll('.nav-link').forEach(link => {
            if (link.dataset.page === page) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });

        // Mobile navigation
        document.querySelectorAll('.mobile-nav-link').forEach(link => {
            if (link.dataset.page === page) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });
    }

    closeMobileMenu() {
        const mobileNav = document.getElementById('mobile-nav');
        mobileNav.classList.add('hidden');
    }

    getCurrentPage() {
        return this.currentPage;
    }
}

// Make components globally available
window.UI = UI;
window.InputResponseLayout = InputResponseLayout;
window.Navigation = Navigation;