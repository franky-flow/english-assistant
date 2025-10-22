-- Database migration script for English Assistant
-- Run this script to set up the complete database

\echo 'Creating English Assistant database schema...'

-- Create the main schema
\i schema.sql

\echo 'Schema created successfully!'

\echo 'Inserting initial data...'

-- Insert initial phrasal verbs and sample data
\i initial_data.sql

\echo 'Initial data inserted successfully!'

\echo 'Database setup complete!'

-- Display summary
SELECT 
    'phrasal_verbs' as table_name,
    COUNT(*) as record_count,
    COUNT(CASE WHEN difficulty = 'beginner' THEN 1 END) as beginner_count,
    COUNT(CASE WHEN difficulty = 'intermediate' THEN 1 END) as intermediate_count,
    COUNT(CASE WHEN difficulty = 'advanced' THEN 1 END) as advanced_count
FROM phrasal_verbs
UNION ALL
SELECT 
    'history' as table_name,
    COUNT(*) as record_count,
    COUNT(CASE WHEN section = 'vocabulary' THEN 1 END) as vocabulary_count,
    COUNT(CASE WHEN section = 'grammar' THEN 1 END) as grammar_count,
    COUNT(CASE WHEN section = 'correction' THEN 1 END) as correction_count
FROM history;