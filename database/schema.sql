-- English Assistant Database Schema
-- PostgreSQL schema for history and phrasal verbs

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Main history table for all user interactions
CREATE TABLE history (
    id SERIAL PRIMARY KEY,
    section VARCHAR(50) NOT NULL CHECK (section IN ('vocabulary', 'correction', 'grammar', 'phrasal-verbs')),
    query TEXT NOT NULL,
    result TEXT NOT NULL,
    explanation TEXT,
    examples TEXT[],
    tags TEXT[],
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Phrasal verbs with progress tracking
CREATE TABLE phrasal_verbs (
    id SERIAL PRIMARY KEY,
    verb TEXT NOT NULL UNIQUE,
    definition TEXT NOT NULL,
    examples TEXT[],
    difficulty VARCHAR(20) DEFAULT 'beginner' CHECK (difficulty IN ('beginner', 'intermediate', 'advanced')),
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'in_progress', 'learned')),
    user_progress JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Performance indexes
CREATE INDEX idx_history_section ON history(section);
CREATE INDEX idx_history_created_at ON history(created_at DESC);
CREATE INDEX idx_history_tags ON history USING GIN(tags);
CREATE INDEX idx_history_section_created ON history(section, created_at DESC);

CREATE INDEX idx_phrasal_verbs_difficulty ON phrasal_verbs(difficulty);
CREATE INDEX idx_phrasal_verbs_status ON phrasal_verbs(status);
CREATE INDEX idx_phrasal_verbs_verb ON phrasal_verbs(verb);
CREATE INDEX idx_phrasal_verbs_difficulty_status ON phrasal_verbs(difficulty, status);

-- Full-text search indexes for better search performance
CREATE INDEX idx_history_query_fts ON history USING GIN(to_tsvector('english', query));
CREATE INDEX idx_history_result_fts ON history USING GIN(to_tsvector('english', result));
CREATE INDEX idx_phrasal_verbs_verb_fts ON phrasal_verbs USING GIN(to_tsvector('english', verb));
CREATE INDEX idx_phrasal_verbs_definition_fts ON phrasal_verbs USING GIN(to_tsvector('english', definition));

-- Trigger function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply update triggers
CREATE TRIGGER update_history_updated_at BEFORE UPDATE ON history
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_phrasal_verbs_updated_at BEFORE UPDATE ON phrasal_verbs
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();