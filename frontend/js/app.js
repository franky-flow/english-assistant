/**
 * Main Application Entry Point for English Assistant
 */

class EnglishAssistantApp {
    constructor() {
        this.nav = null;
        this.isInitialized = false;
    }

    /**
     * Initialize the application
     */
    async init() {
        try {
            console.log('🚀 Initializing English Assistant...');
            
            // Show loading screen
            UI.showLoading();
            
            // Initialize navigation
            this.nav = new Navigation();
            window.nav = this.nav; // Make globally available
            
            // Check API connection
            await this.checkAPIConnection();
            
            // Load initial page
            this.loadInitialPage();
            
            // Set up global event listeners
            this.setupGlobalEvents();
            
            // Hide loading screen
            setTimeout(() => {
                UI.hideLoading();
                this.isInitialized = true;
                console.log('✅ English Assistant initialized successfully');
            }, 1000);
            
        } catch (error) {
            console.error('❌ Failed to initialize English Assistant:', error);
            this.handleInitializationError(error);
        }
    }

    /**
     * Check API connection and update status
     */
    async checkAPIConnection() {
        const statusElement = document.getElementById('connection-status');
        
        try {
            await api.healthCheck();
            
            statusElement.innerHTML = `
                <div class="w-2 h-2 bg-green-400 rounded-full mr-2"></div>
                Connected
            `;
            statusElement.className = 'flex items-center text-green-600';
            
        } catch (error) {
            console.warn('API connection failed:', error);
            
            statusElement.innerHTML = `
                <div class="w-2 h-2 bg-red-400 rounded-full mr-2"></div>
                Disconnected
            `;
            statusElement.className = 'flex items-center text-red-600';
            
            // Show warning but don't block initialization
            setTimeout(() => {
                UI.showError('API connection failed. Some features may not work properly.');
            }, 2000);
        }
    }

    /**
     * Load initial page based on URL hash or default to home
     */
    loadInitialPage() {
        const hash = window.location.hash.substring(1);
        const page = hash && Pages[hash] ? hash : 'home';
        
        this.nav.navigateTo(page);
    }

    /**
     * Set up global event listeners
     */
    setupGlobalEvents() {
        // Handle browser back/forward
        window.addEventListener('hashchange', () => {
            if (this.isInitialized) {
                const hash = window.location.hash.substring(1);
                const page = hash && Pages[hash] ? hash : 'home';
                this.nav.navigateTo(page);
            }
        });

        // Handle keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            // Ctrl/Cmd + K for search (future feature)
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                // Focus search input if available
                const searchInput = document.querySelector('input[type="text"]');
                if (searchInput) {
                    searchInput.focus();
                }
            }
            
            // Escape to close modals
            if (e.key === 'Escape') {
                UI.hideError();
            }
        });

        // Handle online/offline status
        window.addEventListener('online', () => {
            UI.showSuccess('Connection restored');
            this.checkAPIConnection();
        });

        window.addEventListener('offline', () => {
            UI.showError('Connection lost. Working in offline mode.');
        });

        // Handle visibility change (tab switching)
        document.addEventListener('visibilitychange', () => {
            if (!document.hidden && this.isInitialized) {
                // Refresh connection status when tab becomes visible
                this.checkAPIConnection();
            }
        });

        // Prevent form submissions from refreshing the page
        document.addEventListener('submit', (e) => {
            e.preventDefault();
        });

        // Handle clicks on external links
        document.addEventListener('click', (e) => {
            const link = e.target.closest('a[href^="http"]');
            if (link) {
                e.preventDefault();
                window.open(link.href, '_blank', 'noopener,noreferrer');
            }
        });
    }

    /**
     * Handle initialization errors
     */
    handleInitializationError(error) {
        UI.hideLoading();
        
        const app = document.getElementById('app');
        app.style.display = 'flex';
        
        const content = document.getElementById('page-content');
        content.innerHTML = `
            <div class="max-w-2xl mx-auto text-center py-12">
                <div class="text-6xl mb-6">⚠️</div>
                <h1 class="text-3xl font-bold text-gray-900 mb-4">
                    Initialization Failed
                </h1>
                <p class="text-gray-600 mb-8">
                    English Assistant failed to initialize properly. This might be due to:
                </p>
                <ul class="text-left text-gray-600 mb-8 space-y-2">
                    <li>• API server is not running</li>
                    <li>• Network connectivity issues</li>
                    <li>• Browser compatibility problems</li>
                </ul>
                <div class="space-x-4">
                    <button onclick="location.reload()" class="btn-primary">
                        Retry
                    </button>
                    <button onclick="app.initOfflineMode()" class="btn-secondary">
                        Continue Offline
                    </button>
                </div>
                <div class="mt-8 p-4 bg-gray-100 rounded-lg text-left">
                    <h3 class="font-semibold mb-2">Error Details:</h3>
                    <pre class="text-sm text-gray-700">${error.message}</pre>
                </div>
            </div>
        `;
    }

    /**
     * Initialize offline mode (limited functionality)
     */
    initOfflineMode() {
        console.log('🔄 Initializing offline mode...');
        
        // Initialize navigation
        this.nav = new Navigation();
        window.nav = this.nav;
        
        // Load home page with offline notice
        const content = document.getElementById('page-content');
        content.innerHTML = `
            <div class="max-w-4xl mx-auto">
                <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-8">
                    <div class="flex items-center">
                        <div class="text-yellow-400 mr-3">⚠️</div>
                        <div>
                            <h3 class="font-semibold text-yellow-800">Offline Mode</h3>
                            <p class="text-yellow-700">Limited functionality available. API features are disabled.</p>
                        </div>
                    </div>
                </div>
                
                <div class="text-center">
                    <h1 class="text-4xl font-bold text-gray-900 mb-4">
                        English Assistant
                    </h1>
                    <p class="text-xl text-gray-600 mb-8">
                        Currently running in offline mode
                    </p>
                    <div class="text-6xl mb-8">📚</div>
                    
                    <div class="bg-white rounded-lg shadow-md p-6">
                        <h2 class="text-xl font-semibold mb-4">Available in Offline Mode:</h2>
                        <ul class="text-gray-600 space-y-2">
                            <li>• Browse the interface</li>
                            <li>• View cached content (if any)</li>
                            <li>• Access help documentation</li>
                        </ul>
                        
                        <div class="mt-6">
                            <button onclick="location.reload()" class="btn-primary">
                                Try to Reconnect
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        this.isInitialized = true;
        UI.showSuccess('Offline mode initialized');
    }

    /**
     * Get application status
     */
    getStatus() {
        return {
            initialized: this.isInitialized,
            currentPage: this.nav ? this.nav.getCurrentPage() : null,
            version: CONFIG.VERSION
        };
    }
}

/**
 * Initialize application when DOM is ready
 */
document.addEventListener('DOMContentLoaded', () => {
    // Create global app instance
    window.app = new EnglishAssistantApp();
    
    // Initialize the application
    window.app.init();
});

/**
 * Handle unhandled promise rejections
 */
window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason);
    
    // Show user-friendly error for API-related rejections
    if (event.reason instanceof APIError) {
        UI.showError(event.reason.getDisplayMessage());
    }
    
    // Prevent the default browser error handling
    event.preventDefault();
});

/**
 * Handle global errors
 */
window.addEventListener('error', (event) => {
    console.error('Global error:', event.error);
    
    // Show generic error message
    UI.showError('An unexpected error occurred. Please refresh the page.');
});

console.log('📚 English Assistant loaded successfully');