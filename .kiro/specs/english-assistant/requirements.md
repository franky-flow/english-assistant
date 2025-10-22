# Requirements Document

## Introduction

The English Assistant is a local web application designed to help Spanish speakers improve their English skills through vocabulary explanations, writing correction, grammar concepts, and phrasal verb learning. The system operates entirely offline using HuggingFace models and LangGraph agents, with all user data and history stored locally in PostgreSQL.

## Glossary

- **English Assistant System**: The complete web application including frontend, backend, and database components
- **LangGraph Agent**: A specialized AI agent that handles specific functionality using offline language models
- **Vocabulary Agent**: Agent responsible for explaining words and sentences using bilingual translation models
- **Correction Agent**: Agent that corrects English text and provides grammar improvement explanations
- **Grammar Agent**: Agent that answers grammar questions and provides word comparisons
- **Phrasal Verb Agent**: Agent that manages phrasal verb data, difficulty levels, and user progress tracking
- **History Panel**: User interface component that displays past queries with search, edit, and open functionality
- **HuggingFace Model**: Pre-trained language model that operates offline without external API requirements
- **PostgreSQL Database**: Local database that stores all user queries, corrections, and learning progress

## Requirements

### Requirement 1

**User Story:** As a Spanish speaker learning English, I want to get vocabulary explanations for words and sentences, so that I can understand their meaning and usage in context.

#### Acceptance Criteria

1. WHEN a user submits a word or sentence to the vocabulary endpoint, THE English Assistant System SHALL provide a bilingual explanation using offline translation models
2. THE English Assistant System SHALL return vocabulary explanations that include the query, result, explanation, examples, and relevant tags
3. THE English Assistant System SHALL store all vocabulary queries and explanations in the PostgreSQL Database for future reference
4. THE English Assistant System SHALL display vocabulary explanations in a clear input-response layout on the frontend
5. THE English Assistant System SHALL operate entirely offline without requiring external API keys or internet connectivity

### Requirement 2

**User Story:** As a Spanish speaker practicing English writing, I want my text to be corrected with explanations, so that I can learn from my mistakes and improve my grammar.

#### Acceptance Criteria

1. WHEN a user submits English text for correction, THE English Assistant System SHALL identify and correct grammar errors using offline correction models
2. THE English Assistant System SHALL provide detailed explanations for each correction made to help users understand the grammar rules
3. THE English Assistant System SHALL store all writing corrections and explanations in the PostgreSQL Database
4. THE English Assistant System SHALL display corrections with clear before-and-after comparisons in the user interface
5. THE English Assistant System SHALL use CPU-friendly models that do not require GPU acceleration

### Requirement 3

**User Story:** As an English learner, I want to ask grammar questions and compare words, so that I can understand grammar rules and word usage differences.

#### Acceptance Criteria

1. WHEN a user submits a grammar question, THE English Assistant System SHALL provide clear explanations of grammar rules using the Grammar Agent
2. WHEN a user requests word comparisons, THE English Assistant System SHALL explain the differences between similar words with examples
3. THE English Assistant System SHALL store all grammar queries and explanations in the PostgreSQL Database
4. THE English Assistant System SHALL present grammar explanations in an easy-to-understand format
5. THE English Assistant System SHALL tag grammar responses appropriately for categorization and search

### Requirement 4

**User Story:** As an English learner, I want to learn phrasal verbs with difficulty tracking, so that I can systematically improve my understanding of English phrasal verbs.

#### Acceptance Criteria

1. THE English Assistant System SHALL provide a comprehensive list of phrasal verbs with difficulty levels and usage examples
2. THE English Assistant System SHALL allow users to track their progress on phrasal verbs with statuses: Pending, In Progress, and Learned
3. THE English Assistant System SHALL provide sortable and filterable table views for phrasal verbs by difficulty, status, or alphabetical order
4. THE English Assistant System SHALL display phrasal verbs with appropriate badges indicating status and difficulty level
5. THE English Assistant System SHALL store phrasal verb progress data in the PostgreSQL Database for persistence

### Requirement 5

**User Story:** As an English learner, I want to access my learning history across all sections, so that I can review past queries, corrections, and track my progress over time.

#### Acceptance Criteria

1. THE English Assistant System SHALL maintain a searchable history of all user queries across vocabulary, correction, grammar, and phrasal verb sections
2. THE English Assistant System SHALL allow users to edit and reopen historical queries for further learning
3. THE English Assistant System SHALL provide search functionality within the history panel to find specific past interactions
4. THE English Assistant System SHALL persist all user data between sessions using local storage and database caching
5. THE English Assistant System SHALL organize history entries with timestamps, sections, and relevant tags for easy navigation

### Requirement 6

**User Story:** As a user, I want a responsive and intuitive interface, so that I can easily access all learning features on any device.

#### Acceptance Criteria

1. THE English Assistant System SHALL provide a single-page application with minimalist responsive design using TailwindCSS
2. THE English Assistant System SHALL include dedicated pages for Home, Vocabulary, Writing Correction, Grammar & Concepts, Phrasal Verbs, and History
3. THE English Assistant System SHALL maintain consistent input-response layout patterns across all sections
4. THE English Assistant System SHALL be deployable as static files served by Nginx
5. THE English Assistant System SHALL provide smooth navigation between different learning sections without page reloads