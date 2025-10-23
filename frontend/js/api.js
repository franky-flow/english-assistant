/**
 * API Client for English Assistant
 * Handles all HTTP requests to the backend API
 */

class APIClient {
    constructor() {
        this.baseURL = CONFIG.API_BASE_URL;
        this.timeout = CONFIG.API_TIMEOUT;
        this.cache = new Map();
        this.requestQueue = new Map();
    }

    /**
     * Make HTTP request with error handling and caching
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const cacheKey = this._getCacheKey(url, options);
        
        // Check cache for GET requests
        if (options.method === 'GET' && this.cache.has(cacheKey)) {
            const cached = this.cache.get(cacheKey);
            if (Date.now() - cached.timestamp < 300000) { // 5 minutes cache
                return cached.data;
            }
        }
        
        // Prevent duplicate requests
        if (this.requestQueue.has(cacheKey)) {
            return this.requestQueue.get(cacheKey);
        }
        
        const requestPromise = this._makeRequest(url, options);
        this.requestQueue.set(cacheKey, requestPromise);
        
        try {
            const result = await requestPromise;
            
            // Cache successful GET requests
            if (options.method === 'GET' && result.success) {
                this.cache.set(cacheKey, {
                    data: result,
                    timestamp: Date.now()
                });
            }
            
            return result;
        } finally {
            this.requestQueue.delete(cacheKey);
        }
    }

    /**
     * Make the actual HTTP request
     */
    async _makeRequest(url, options) {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), this.timeout);
        
        try {
            const response = await fetch(url, {
                method: options.method || 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                body: options.body ? JSON.stringify(options.body) : undefined,
                signal: controller.signal,
                ...options
            });
            
            clearTimeout(timeoutId);
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new APIError(
                    data.message || `HTTP ${response.status}`,
                    response.status,
                    data
                );
            }
            
            return { success: true, data };
            
        } catch (error) {
            clearTimeout(timeoutId);
            
            if (error.name === 'AbortError') {
                throw new APIError(CONFIG.ERROR_MESSAGES.TIMEOUT, 408);
            }
            
            if (error instanceof APIError) {
                throw error;
            }
            
            // Network or other errors
            throw new APIError(
                CONFIG.ERROR_MESSAGES.NETWORK_ERROR,
                0,
                { originalError: error.message }
            );
        }
    }

    /**
     * Generate cache key for request
     */
    _getCacheKey(url, options) {
        const method = options.method || 'GET';
        const body = options.body ? JSON.stringify(options.body) : '';
        return `${method}:${url}:${body}`;
    }

    /**
     * Clear cache
     */
    clearCache(pattern = null) {
        if (pattern) {
            for (const key of this.cache.keys()) {
                if (key.includes(pattern)) {
                    this.cache.delete(key);
                }
            }
        } else {
            this.cache.clear();
        }
    }

    // Vocabulary API
    async explainVocabulary(query, sourceLanguage = 'es', targetLanguage = 'en') {
        return this.request(CONFIG.ENDPOINTS.VOCABULARY, {
            method: 'POST',
            body: {
                query,
                source_language: sourceLanguage,
                target_language: targetLanguage
            }
        });
    }

    // Correction API
    async correctText(text, correctionLevel = 'comprehensive') {
        return this.request(CONFIG.ENDPOINTS.CORRECTION, {
            method: 'POST',
            body: {
                text,
                correction_level: correctionLevel
            }
        });
    }

    // Grammar API
    async explainGrammar(question, questionType = 'explanation') {
        return this.request(CONFIG.ENDPOINTS.GRAMMAR, {
            method: 'POST',
            body: {
                question,
                question_type: questionType
            }
        });
    }

    // Phrasal Verbs API
    async getPhrasalVerbs(filters = {}) {
        const params = new URLSearchParams();
        
        Object.entries(filters).forEach(([key, value]) => {
            if (value !== null && value !== undefined && value !== '') {
                params.append(key, value);
            }
        });
        
        const queryString = params.toString();
        const endpoint = queryString ? 
            `${CONFIG.ENDPOINTS.PHRASAL_VERBS}?${queryString}` : 
            CONFIG.ENDPOINTS.PHRASAL_VERBS;
            
        return this.request(endpoint, { method: 'GET' });
    }

    async getPhrasalVerbById(id) {
        return this.request(`${CONFIG.ENDPOINTS.PHRASAL_VERBS}/${id}`, {
            method: 'GET'
        });
    }

    async updatePhrasalVerbProgress(id, status, progress = null) {
        return this.request(`${CONFIG.ENDPOINTS.PHRASAL_VERBS}/${id}/progress`, {
            method: 'PUT',
            body: {
                status,
                progress
            }
        });
    }

    async getPhrasalVerbRecommendations(limit = 5) {
        return this.request(`${CONFIG.ENDPOINTS.PHRASAL_VERBS}/recommendations/practice?limit=${limit}`, {
            method: 'GET'
        });
    }

    async searchPhrasalVerbs(query) {
        return this.request(`${CONFIG.ENDPOINTS.PHRASAL_VERBS}/search/${encodeURIComponent(query)}`, {
            method: 'GET'
        });
    }

    // History API
    async getHistory(filters = {}) {
        const params = new URLSearchParams();
        
        Object.entries(filters).forEach(([key, value]) => {
            if (value !== null && value !== undefined && value !== '') {
                if (Array.isArray(value)) {
                    value.forEach(v => params.append(key, v));
                } else {
                    params.append(key, value);
                }
            }
        });
        
        const queryString = params.toString();
        const endpoint = queryString ? 
            `${CONFIG.ENDPOINTS.HISTORY}?${queryString}` : 
            CONFIG.ENDPOINTS.HISTORY;
            
        return this.request(endpoint, { method: 'GET' });
    }

    async getHistoryEntry(id) {
        return this.request(`${CONFIG.ENDPOINTS.HISTORY}/${id}`, {
            method: 'GET'
        });
    }

    async deleteHistoryEntry(id) {
        return this.request(`${CONFIG.ENDPOINTS.HISTORY}/${id}`, {
            method: 'DELETE'
        });
    }

    async clearHistory(section = null, confirm = false) {
        const params = new URLSearchParams();
        if (section) params.append('section', section);
        if (confirm) params.append('confirm', 'true');
        
        const queryString = params.toString();
        const endpoint = queryString ? 
            `${CONFIG.ENDPOINTS.HISTORY}?${queryString}` : 
            CONFIG.ENDPOINTS.HISTORY;
            
        return this.request(endpoint, { method: 'DELETE' });
    }

    // Health Check
    async healthCheck() {
        // Health endpoint is at root level, not under /api
        const url = 'http://localhost:8000/health';
        try {
            const response = await fetch(url);
            const data = await response.json();
            if (response.ok) {
                return { success: true, data };
            } else {
                throw new APIError(data.message || `HTTP ${response.status}`, response.status, data);
            }
        } catch (error) {
            throw new APIError(CONFIG.ERROR_MESSAGES.NETWORK_ERROR, 0, { originalError: error.message });
        }
    }
}

/**
 * Custom API Error class
 */
class APIError extends Error {
    constructor(message, status = 0, details = null) {
        super(message);
        this.name = 'APIError';
        this.status = status;
        this.details = details;
    }

    getDisplayMessage() {
        switch (this.status) {
            case 400:
                return CONFIG.ERROR_MESSAGES.VALIDATION_ERROR;
            case 404:
                return CONFIG.ERROR_MESSAGES.NOT_FOUND;
            case 408:
                return CONFIG.ERROR_MESSAGES.TIMEOUT;
            case 500:
                return CONFIG.ERROR_MESSAGES.SERVER_ERROR;
            default:
                return this.message || CONFIG.ERROR_MESSAGES.UNKNOWN;
        }
    }
}

/**
 * Utility functions for API handling
 */
const APIUtils = {
    /**
     * Handle API response with loading state
     */
    async handleRequest(apiCall, loadingElement = null) {
        if (loadingElement) {
            loadingElement.classList.add('loading');
        }
        
        try {
            const result = await apiCall();
            return result;
        } catch (error) {
            console.error('API Request failed:', error);
            
            if (error instanceof APIError) {
                UI.showError(error.getDisplayMessage());
            } else {
                UI.showError(CONFIG.ERROR_MESSAGES.UNKNOWN);
            }
            
            throw error;
        } finally {
            if (loadingElement) {
                loadingElement.classList.remove('loading');
            }
        }
    },

    /**
     * Debounce function for search inputs
     */
    debounce(func, delay = CONFIG.DEBOUNCE_DELAY) {
        let timeoutId;
        return function (...args) {
            clearTimeout(timeoutId);
            timeoutId = setTimeout(() => func.apply(this, args), delay);
        };
    },

    /**
     * Format error for display
     */
    formatError(error) {
        if (error instanceof APIError) {
            return {
                message: error.getDisplayMessage(),
                details: error.details
            };
        }
        
        return {
            message: CONFIG.ERROR_MESSAGES.UNKNOWN,
            details: { originalError: error.message }
        };
    }
};

// Create global API client instance
window.api = new APIClient();
window.APIError = APIError;
window.APIUtils = APIUtils;