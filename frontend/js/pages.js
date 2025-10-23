/**
 * Page implementations for English Assistant
 */

/**
 * Pages namespace containing all page implementations
 */
const Pages = {
    /**
     * Home page
     */
    home() {
        const content = document.getElementById('page-content');
        content.innerHTML = `
            <div class="max-w-4xl mx-auto">
                <!-- Welcome Section -->
                <div class="text-center mb-12">
                    <h1 class="text-4xl font-bold text-gray-900 mb-4">
                        Welcome to English Assistant
                    </h1>
                    <p class="text-xl text-gray-600 mb-8">
                        AI-powered English learning for Spanish speakers
                    </p>
                    <div class="text-6xl mb-4">📚</div>
                </div>

                <!-- Feature Cards -->
                <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
                    <div class="card hover:shadow-lg transition-shadow cursor-pointer" onclick="window.nav.navigateTo('vocabulary')">
                        <div class="card-body text-center">
                            <div class="text-4xl mb-4">📖</div>
                            <h3 class="text-lg font-semibold mb-2">Vocabulary</h3>
                            <p class="text-gray-600">Get bilingual explanations for words and phrases with examples and context.</p>
                        </div>
                    </div>

                    <div class="card hover:shadow-lg transition-shadow cursor-pointer" onclick="window.nav.navigateTo('correction')">
                        <div class="card-body text-center">
                            <div class="text-4xl mb-4">✏️</div>
                            <h3 class="text-lg font-semibold mb-2">Writing Correction</h3>
                            <p class="text-gray-600">Improve your writing with AI-powered grammar and style corrections.</p>
                        </div>
                    </div>

                    <div class="card hover:shadow-lg transition-shadow cursor-pointer" onclick="window.nav.navigateTo('grammar')">
                        <div class="card-body text-center">
                            <div class="text-4xl mb-4">📝</div>
                            <h3 class="text-lg font-semibold mb-2">Grammar Help</h3>
                            <p class="text-gray-600">Ask grammar questions and get clear explanations with examples.</p>
                        </div>
                    </div>

                    <div class="card hover:shadow-lg transition-shadow cursor-pointer" onclick="window.nav.navigateTo('phrasal-verbs')">
                        <div class="card-body text-center">
                            <div class="text-4xl mb-4">🔗</div>
                            <h3 class="text-lg font-semibold mb-2">Phrasal Verbs</h3>
                            <p class="text-gray-600">Learn phrasal verbs with progress tracking and difficulty levels.</p>
                        </div>
                    </div>

                    <div class="card hover:shadow-lg transition-shadow cursor-pointer" onclick="window.nav.navigateTo('history')">
                        <div class="card-body text-center">
                            <div class="text-4xl mb-4">📚</div>
                            <h3 class="text-lg font-semibold mb-2">Learning History</h3>
                            <p class="text-gray-600">Review your past queries and track your learning progress.</p>
                        </div>
                    </div>

                    <div class="card hover:shadow-lg transition-shadow">
                        <div class="card-body text-center">
                            <div class="text-4xl mb-4">🤖</div>
                            <h3 class="text-lg font-semibold mb-2">AI-Powered</h3>
                            <p class="text-gray-600">All features work offline using advanced AI models on your device.</p>
                        </div>
                    </div>
                </div>

                <!-- Quick Start Section -->
                <div class="card">
                    <div class="card-header">
                        <h2 class="text-xl font-semibold">Quick Start</h2>
                    </div>
                    <div class="card-body">
                        <div class="grid md:grid-cols-2 gap-6">
                            <div>
                                <h3 class="font-semibold mb-2">For Beginners</h3>
                                <ul class="space-y-2 text-gray-600">
                                    <li>• Start with <a href="#vocabulary" class="text-primary-600 hover:underline">Vocabulary</a> to learn new words</li>
                                    <li>• Use <a href="#grammar" class="text-primary-600 hover:underline">Grammar Help</a> for basic rules</li>
                                    <li>• Practice with simple <a href="#phrasal-verbs" class="text-primary-600 hover:underline">Phrasal Verbs</a></li>
                                </ul>
                            </div>
                            <div>
                                <h3 class="font-semibold mb-2">For Advanced Learners</h3>
                                <ul class="space-y-2 text-gray-600">
                                    <li>• Use <a href="#correction" class="text-primary-600 hover:underline">Writing Correction</a> to polish your texts</li>
                                    <li>• Ask complex grammar questions</li>
                                    <li>• Challenge yourself with advanced phrasal verbs</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        UI.animateIn(content, 'fade-in');
    },

    /**
     * Vocabulary page
     */
    vocabulary() {
        const content = document.getElementById('page-content');
        content.innerHTML = `
            <div class="max-w-4xl mx-auto">
                <div class="mb-8">
                    <h1 class="text-3xl font-bold text-gray-900 mb-2">Vocabulary Assistant</h1>
                    <p class="text-gray-600">Get bilingual explanations for English and Spanish words or phrases.</p>
                </div>
                
                <div id="vocabulary-container"></div>
            </div>
        `;

        // Initialize vocabulary layout
        const container = document.getElementById('vocabulary-container');
        new VocabularyLayout(container);
        
        UI.animateIn(content, 'fade-in');
    },

    /**
     * Writing correction page
     */
    correction() {
        const content = document.getElementById('page-content');
        content.innerHTML = `
            <div class="max-w-4xl mx-auto">
                <div class="mb-8">
                    <h1 class="text-3xl font-bold text-gray-900 mb-2">Writing Correction</h1>
                    <p class="text-gray-600">Improve your English writing with AI-powered grammar and style corrections.</p>
                </div>
                
                <div id="correction-container"></div>
            </div>
        `;

        // Initialize correction layout
        const container = document.getElementById('correction-container');
        new CorrectionLayout(container);
        
        UI.animateIn(content, 'fade-in');
    },

    /**
     * Grammar page
     */
    grammar() {
        const content = document.getElementById('page-content');
        content.innerHTML = `
            <div class="max-w-4xl mx-auto">
                <div class="mb-8">
                    <h1 class="text-3xl font-bold text-gray-900 mb-2">Grammar Assistant</h1>
                    <p class="text-gray-600">Ask grammar questions and get clear explanations with examples.</p>
                </div>
                
                <div id="grammar-container"></div>
            </div>
        `;

        // Initialize grammar layout
        const container = document.getElementById('grammar-container');
        new GrammarLayout(container);
        
        UI.animateIn(content, 'fade-in');
    },

    /**
     * Phrasal verbs page
     */
    'phrasal-verbs'() {
        const content = document.getElementById('page-content');
        content.innerHTML = `
            <div class="max-w-6xl mx-auto">
                <div class="mb-8">
                    <h1 class="text-3xl font-bold text-gray-900 mb-2">Phrasal Verbs</h1>
                    <p class="text-gray-600">Learn English phrasal verbs with progress tracking and difficulty levels.</p>
                </div>
                
                <div id="phrasal-verbs-container"></div>
            </div>
        `;

        // Initialize phrasal verbs layout
        const container = document.getElementById('phrasal-verbs-container');
        new PhrasalVerbsLayout(container);
        
        UI.animateIn(content, 'fade-in');
    },

    /**
     * History page
     */
    history() {
        const content = document.getElementById('page-content');
        content.innerHTML = `
            <div class="max-w-6xl mx-auto">
                <div class="mb-8">
                    <h1 class="text-3xl font-bold text-gray-900 mb-2">Learning History</h1>
                    <p class="text-gray-600">Review your past queries and track your learning progress.</p>
                </div>
                
                <div id="history-container"></div>
            </div>
        `;

        // Initialize history layout
        const container = document.getElementById('history-container');
        new HistoryLayout(container);
        
        UI.animateIn(content, 'fade-in');
    }
};

/**
 * Vocabulary-specific layout
 */
class VocabularyLayout extends InputResponseLayout {
    constructor(container) {
        super(container, {
            placeholder: 'Enter a word or phrase in English or Spanish...',
            buttonText: 'Explain',
            showOptions: true
        });
    }

    renderOptions() {
        return `
            <div class="grid grid-cols-2 gap-4">
                <div>
                    <label class="form-label">From Language</label>
                    <select id="source-language" class="select-field">
                        <option value="es">Spanish</option>
                        <option value="en">English</option>
                    </select>
                </div>
                <div>
                    <label class="form-label">To Language</label>
                    <select id="target-language" class="select-field">
                        <option value="en">English</option>
                        <option value="es">Spanish</option>
                    </select>
                </div>
            </div>
        `;
    }

    async processRequest(text) {
        const sourceLanguage = this.container.querySelector('#source-language').value;
        const targetLanguage = this.container.querySelector('#target-language').value;
        
        return await api.explainVocabulary(text, sourceLanguage, targetLanguage);
    }

    displayResult(result) {
        const responseContent = this.container.querySelector('#response-content');
        
        responseContent.innerHTML = `
            <div class="space-y-4">
                <div>
                    <h4 class="font-semibold text-gray-900 mb-2">Translation</h4>
                    <p class="text-lg text-primary-600 font-medium">${UI.escapeHtml(result.data.result)}</p>
                </div>
                
                ${result.data.translations ? `
                    <div>
                        <h4 class="font-semibold text-gray-900 mb-2">All Translations</h4>
                        <div class="bg-gray-50 p-4 rounded-lg">
                            ${Object.entries(result.data.translations).map(([lang, translation]) => 
                                `<div class="mb-2"><strong>${lang.toUpperCase()}:</strong> ${UI.escapeHtml(translation)}</div>`
                            ).join('')}
                        </div>
                    </div>
                ` : ''}
                
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
                
                ${result.data.word_type ? `
                    <div>
                        <h4 class="font-semibold text-gray-900 mb-2">Word Type</h4>
                        <span class="badge-info">${UI.escapeHtml(result.data.word_type)}</span>
                    </div>
                ` : ''}
            </div>
        `;

        UI.animateIn(responseContent, 'slide-up');
    }
}

/**
 * Correction-specific layout
 */
class CorrectionLayout extends InputResponseLayout {
    constructor(container) {
        super(container, {
            placeholder: 'Enter your English text to be corrected...',
            buttonText: 'Correct Text',
            showOptions: true
        });
    }

    renderOptions() {
        return `
            <div>
                <label class="form-label">Correction Level</label>
                <select id="correction-level" class="select-field">
                    <option value="comprehensive">Comprehensive (Grammar + Style)</option>
                    <option value="basic">Basic (Grammar Only)</option>
                </select>
            </div>
        `;
    }

    async processRequest(text) {
        const correctionLevel = this.container.querySelector('#correction-level').value;
        return await api.correctText(text, correctionLevel);
    }

    displayResult(result) {
        const responseContent = this.container.querySelector('#response-content');
        
        responseContent.innerHTML = `
            <div class="space-y-4">
                <div>
                    <h4 class="font-semibold text-gray-900 mb-2">Corrected Text</h4>
                    <div class="bg-green-50 border border-green-200 p-4 rounded-lg">
                        <p class="text-gray-900">${UI.escapeHtml(result.data.corrected_text)}</p>
                    </div>
                </div>
                
                ${result.data.correction_count > 0 ? `
                    <div>
                        <h4 class="font-semibold text-gray-900 mb-2">
                            Corrections Made (${result.data.correction_count})
                        </h4>
                        <div class="space-y-2">
                            ${result.data.corrections.map(correction => `
                                <div class="bg-yellow-50 border border-yellow-200 p-3 rounded-lg">
                                    <div class="flex items-start space-x-2">
                                        <span class="badge-warning">${UI.escapeHtml(correction.error_type)}</span>
                                        <div class="flex-1">
                                            <p class="text-sm">
                                                <span class="line-through text-red-600">${UI.escapeHtml(correction.original)}</span>
                                                →
                                                <span class="text-green-600 font-medium">${UI.escapeHtml(correction.corrected)}</span>
                                            </p>
                                            <p class="text-xs text-gray-600 mt-1">${UI.escapeHtml(correction.rule_explanation)}</p>
                                        </div>
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                ` : `
                    <div class="bg-green-50 border border-green-200 p-4 rounded-lg">
                        <p class="text-green-800">✅ No corrections needed! Your text looks great.</p>
                    </div>
                `}
                
                ${result.data.explanation ? `
                    <div>
                        <h4 class="font-semibold text-gray-900 mb-2">Summary</h4>
                        <p class="text-gray-700">${UI.escapeHtml(result.data.explanation)}</p>
                    </div>
                ` : ''}
            </div>
        `;

        UI.animateIn(responseContent, 'slide-up');
    }
}

/**
 * Grammar-specific layout
 */
class GrammarLayout extends InputResponseLayout {
    constructor(container) {
        super(container, {
            placeholder: 'Ask a grammar question or request word comparison...',
            buttonText: 'Get Explanation',
            showOptions: true
        });
    }

    renderOptions() {
        return `
            <div>
                <label class="form-label">Question Type</label>
                <select id="question-type" class="select-field">
                    <option value="explanation">Grammar Explanation</option>
                    <option value="comparison">Word Comparison</option>
                    <option value="usage">Usage Question</option>
                </select>
            </div>
        `;
    }

    async processRequest(text) {
        const questionType = this.container.querySelector('#question-type').value;
        return await api.explainGrammar(text, questionType);
    }
}

/**
 * Phrasal Verbs layout
 */
class PhrasalVerbsLayout {
    constructor(container) {
        this.container = container;
        this.currentFilters = {};
        this.phrasalVerbs = [];
        
        this.render();
        this.bindEvents();
        this.loadPhrasalVerbs();
    }

    render() {
        this.container.innerHTML = `
            <div class="space-y-6">
                <!-- Filters -->
                <div class="card">
                    <div class="card-body">
                        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                            <div>
                                <label class="form-label">Difficulty</label>
                                <select id="difficulty-filter" class="select-field">
                                    <option value="">All Levels</option>
                                    <option value="beginner">Beginner</option>
                                    <option value="intermediate">Intermediate</option>
                                    <option value="advanced">Advanced</option>
                                </select>
                            </div>
                            <div>
                                <label class="form-label">Status</label>
                                <select id="status-filter" class="select-field">
                                    <option value="">All Status</option>
                                    <option value="pending">Pending</option>
                                    <option value="in_progress">In Progress</option>
                                    <option value="learned">Learned</option>
                                </select>
                            </div>
                            <div>
                                <label class="form-label">Search</label>
                                <input type="text" id="search-filter" class="input-field" placeholder="Search phrasal verbs...">
                            </div>
                            <div class="flex items-end">
                                <button id="clear-filters" class="btn-secondary w-full">Clear Filters</button>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Phrasal Verbs List -->
                <div id="phrasal-verbs-list">
                    <div class="text-center py-8">
                        <div class="loading-spinner w-8 h-8 mx-auto mb-4"></div>
                        <p class="text-gray-600">Loading phrasal verbs...</p>
                    </div>
                </div>
            </div>
        `;
    }

    bindEvents() {
        const difficultyFilter = this.container.querySelector('#difficulty-filter');
        const statusFilter = this.container.querySelector('#status-filter');
        const searchFilter = this.container.querySelector('#search-filter');
        const clearFilters = this.container.querySelector('#clear-filters');

        // Filter change handlers
        difficultyFilter.addEventListener('change', () => this.applyFilters());
        statusFilter.addEventListener('change', () => this.applyFilters());
        
        // Debounced search
        searchFilter.addEventListener('input', 
            APIUtils.debounce(() => this.applyFilters(), 300)
        );

        // Clear filters
        clearFilters.addEventListener('click', () => {
            difficultyFilter.value = '';
            statusFilter.value = '';
            searchFilter.value = '';
            this.applyFilters();
        });
    }

    async loadPhrasalVerbs() {
        try {
            const result = await api.getPhrasalVerbs(this.currentFilters);
            this.phrasalVerbs = result.data;
            this.renderPhrasalVerbs();
        } catch (error) {
            console.error('Failed to load phrasal verbs:', error);
            this.renderError();
        }
    }

    applyFilters() {
        const difficulty = this.container.querySelector('#difficulty-filter').value;
        const status = this.container.querySelector('#status-filter').value;
        const search = this.container.querySelector('#search-filter').value;

        this.currentFilters = {};
        if (difficulty) this.currentFilters.difficulty = difficulty;
        if (status) this.currentFilters.status = status;
        if (search) this.currentFilters.search = search;

        this.loadPhrasalVerbs();
    }

    renderPhrasalVerbs() {
        const listContainer = this.container.querySelector('#phrasal-verbs-list');
        
        if (this.phrasalVerbs.length === 0) {
            listContainer.innerHTML = `
                <div class="text-center py-8">
                    <p class="text-gray-600">No phrasal verbs found matching your criteria.</p>
                </div>
            `;
            return;
        }

        listContainer.innerHTML = `
            <div class="grid gap-4">
                ${this.phrasalVerbs.map(verb => this.renderPhrasalVerbCard(verb)).join('')}
            </div>
        `;
    }

    renderPhrasalVerbCard(verb) {
        const statusConfig = CONFIG.PHRASAL_VERB_STATUS[verb.status];
        const difficultyConfig = CONFIG.DIFFICULTY_LEVELS[verb.difficulty];

        return `
            <div class="card">
                <div class="card-body">
                    <div class="flex justify-between items-start mb-3">
                        <h3 class="text-lg font-semibold text-gray-900">${UI.escapeHtml(verb.verb)}</h3>
                        <div class="flex space-x-2">
                            <span class="badge-${difficultyConfig.color}">${difficultyConfig.icon} ${difficultyConfig.label}</span>
                            <span class="badge-${statusConfig.color}">${statusConfig.icon} ${statusConfig.label}</span>
                        </div>
                    </div>
                    
                    <p class="text-gray-700 mb-3">${UI.escapeHtml(verb.definition)}</p>
                    
                    ${verb.examples && verb.examples.length > 0 ? `
                        <div class="mb-4">
                            <h4 class="font-medium text-gray-900 mb-2">Examples:</h4>
                            <ul class="list-disc list-inside space-y-1 text-sm text-gray-600">
                                ${verb.examples.map(example => 
                                    `<li>${UI.escapeHtml(example)}</li>`
                                ).join('')}
                            </ul>
                        </div>
                    ` : ''}
                    
                    <div class="flex justify-between items-center">
                        <div class="text-sm text-gray-500">
                            Progress: ${Math.round(verb.progress.mastery_level * 100)}%
                        </div>
                        <div class="space-x-2">
                            ${verb.status !== 'learned' ? `
                                <button class="btn-primary btn-sm" onclick="Pages.updatePhrasalVerbStatus(${verb.id}, 'learned')">
                                    Mark as Learned
                                </button>
                            ` : ''}
                            ${verb.status === 'pending' ? `
                                <button class="btn-secondary btn-sm" onclick="Pages.updatePhrasalVerbStatus(${verb.id}, 'in_progress')">
                                    Start Learning
                                </button>
                            ` : ''}
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    renderError() {
        const listContainer = this.container.querySelector('#phrasal-verbs-list');
        listContainer.innerHTML = `
            <div class="text-center py-8">
                <p class="text-red-600">Failed to load phrasal verbs. Please try again.</p>
                <button class="btn-primary mt-4" onclick="this.loadPhrasalVerbs()">Retry</button>
            </div>
        `;
    }
}

/**
 * History layout
 */
class HistoryLayout {
    constructor(container) {
        this.container = container;
        this.currentFilters = {};
        this.historyEntries = [];
        
        this.render();
        this.bindEvents();
        this.loadHistory();
    }

    render() {
        this.container.innerHTML = `
            <div class="space-y-6">
                <!-- Filters -->
                <div class="card">
                    <div class="card-body">
                        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                            <div>
                                <label class="form-label">Section</label>
                                <select id="section-filter" class="select-field">
                                    <option value="">All Sections</option>
                                    <option value="vocabulary">Vocabulary</option>
                                    <option value="correction">Writing Correction</option>
                                    <option value="grammar">Grammar</option>
                                    <option value="phrasal_verbs">Phrasal Verbs</option>
                                </select>
                            </div>
                            <div>
                                <label class="form-label">Search</label>
                                <input type="text" id="search-filter" class="input-field" placeholder="Search history...">
                            </div>
                            <div class="flex items-end">
                                <button id="clear-history" class="btn-danger w-full">Clear All History</button>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- History List -->
                <div id="history-list">
                    <div class="text-center py-8">
                        <div class="loading-spinner w-8 h-8 mx-auto mb-4"></div>
                        <p class="text-gray-600">Loading history...</p>
                    </div>
                </div>
            </div>
        `;
    }

    bindEvents() {
        const sectionFilter = this.container.querySelector('#section-filter');
        const searchFilter = this.container.querySelector('#search-filter');
        const clearHistory = this.container.querySelector('#clear-history');

        sectionFilter.addEventListener('change', () => this.applyFilters());
        searchFilter.addEventListener('input', 
            APIUtils.debounce(() => this.applyFilters(), 300)
        );

        clearHistory.addEventListener('click', () => this.clearAllHistory());
    }

    async loadHistory() {
        try {
            const result = await api.getHistory(this.currentFilters);
            this.historyEntries = result.data.entries;
            this.renderHistory();
        } catch (error) {
            console.error('Failed to load history:', error);
            this.renderError();
        }
    }

    applyFilters() {
        const section = this.container.querySelector('#section-filter').value;
        const search = this.container.querySelector('#search-filter').value;

        this.currentFilters = {};
        if (section) this.currentFilters.section = section;
        if (search) this.currentFilters.search = search;

        this.loadHistory();
    }

    renderHistory() {
        const listContainer = this.container.querySelector('#history-list');
        
        if (this.historyEntries.length === 0) {
            listContainer.innerHTML = `
                <div class="text-center py-8">
                    <p class="text-gray-600">No history entries found.</p>
                </div>
            `;
            return;
        }

        listContainer.innerHTML = `
            <div class="space-y-4">
                ${this.historyEntries.map(entry => this.renderHistoryCard(entry)).join('')}
            </div>
        `;
    }

    renderHistoryCard(entry) {
        return `
            <div class="card">
                <div class="card-body">
                    <div class="flex justify-between items-start mb-3">
                        <div>
                            <span class="badge-info">${UI.escapeHtml(entry.section)}</span>
                            <span class="text-sm text-gray-500 ml-2">${UI.formatDate(entry.created_at)}</span>
                        </div>
                        <button class="btn-danger btn-sm" onclick="Pages.deleteHistoryEntry(${entry.id})">
                            Delete
                        </button>
                    </div>
                    
                    <div class="mb-3">
                        <h4 class="font-medium text-gray-900 mb-1">Query:</h4>
                        <p class="text-gray-700">${UI.escapeHtml(UI.truncateText(entry.query, 200))}</p>
                    </div>
                    
                    <div class="mb-3">
                        <h4 class="font-medium text-gray-900 mb-1">Result:</h4>
                        <p class="text-gray-700">${UI.escapeHtml(UI.truncateText(entry.result, 200))}</p>
                    </div>
                    
                    ${entry.tags && entry.tags.length > 0 ? `
                        <div class="flex flex-wrap gap-2">
                            ${entry.tags.map(tag => 
                                `<span class="badge-gray">${UI.escapeHtml(tag)}</span>`
                            ).join('')}
                        </div>
                    ` : ''}
                </div>
            </div>
        `;
    }

    renderError() {
        const listContainer = this.container.querySelector('#history-list');
        listContainer.innerHTML = `
            <div class="text-center py-8">
                <p class="text-red-600">Failed to load history. Please try again.</p>
                <button class="btn-primary mt-4" onclick="this.loadHistory()">Retry</button>
            </div>
        `;
    }

    async clearAllHistory() {
        if (confirm('Are you sure you want to clear all history? This action cannot be undone.')) {
            try {
                await api.clearHistory(null, true);
                UI.showSuccess('History cleared successfully');
                this.loadHistory();
            } catch (error) {
                console.error('Failed to clear history:', error);
            }
        }
    }
}

// Helper functions for page interactions
Pages.updatePhrasalVerbStatus = async function(id, status) {
    try {
        await api.updatePhrasalVerbProgress(id, status);
        UI.showSuccess('Status updated successfully');
        // Reload the current page to reflect changes
        if (window.nav.getCurrentPage() === 'phrasal-verbs') {
            Pages['phrasal-verbs']();
        }
    } catch (error) {
        console.error('Failed to update status:', error);
    }
};

Pages.deleteHistoryEntry = async function(id) {
    if (confirm('Are you sure you want to delete this history entry?')) {
        try {
            await api.deleteHistoryEntry(id);
            UI.showSuccess('History entry deleted');
            // Reload the current page to reflect changes
            if (window.nav.getCurrentPage() === 'history') {
                Pages.history();
            }
        } catch (error) {
            console.error('Failed to delete history entry:', error);
        }
    }
};

// Make Pages globally available
window.Pages = Pages;