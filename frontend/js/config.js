/**
 * Configuration for English Assistant Frontend
 */

const CONFIG = {
    // API Configuration
    API_BASE_URL: 'http://localhost:8000/api',
    API_TIMEOUT: 30000, // 30 seconds
    
    // Application Settings
    APP_NAME: 'English Assistant',
    VERSION: '1.0.0',
    
    // UI Settings
    ITEMS_PER_PAGE: 20,
    DEBOUNCE_DELAY: 300,
    TOAST_DURATION: 3000,
    
    // Local Storage Keys
    STORAGE_KEYS: {
        THEME: 'ea_theme',
        LANGUAGE: 'ea_language',
        CACHE_PREFIX: 'ea_cache_',
        HISTORY_CACHE: 'ea_history_cache',
        SETTINGS: 'ea_settings'
    },
    
    // API Endpoints
    ENDPOINTS: {
        VOCABULARY: '/vocabulary',
        CORRECTION: '/correction',
        GRAMMAR: '/grammar',
        PHRASAL_VERBS: '/phrasal-verbs',
        HISTORY: '/history',
        HEALTH: '/health'
    },
    
    // Status and Difficulty Mappings
    PHRASAL_VERB_STATUS: {
        'pending': { label: 'Pending', color: 'gray', icon: '⏳' },
        'in_progress': { label: 'In Progress', color: 'yellow', icon: '📚' },
        'learned': { label: 'Learned', color: 'green', icon: '✅' }
    },
    
    DIFFICULTY_LEVELS: {
        'beginner': { label: 'Beginner', color: 'green', icon: '🟢' },
        'intermediate': { label: 'Intermediate', color: 'yellow', icon: '🟡' },
        'advanced': { label: 'Advanced', color: 'red', icon: '🔴' }
    },
    
    // Error Messages
    ERROR_MESSAGES: {
        NETWORK_ERROR: 'Network error. Please check your connection.',
        SERVER_ERROR: 'Server error. Please try again later.',
        VALIDATION_ERROR: 'Please check your input and try again.',
        NOT_FOUND: 'The requested resource was not found.',
        TIMEOUT: 'Request timed out. Please try again.',
        UNKNOWN: 'An unexpected error occurred.'
    },
    
    // Success Messages
    SUCCESS_MESSAGES: {
        SAVED: 'Successfully saved!',
        UPDATED: 'Successfully updated!',
        DELETED: 'Successfully deleted!',
        COPIED: 'Copied to clipboard!'
    }
};

// Make config globally available
window.CONFIG = CONFIG;