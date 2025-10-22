-- Initial phrasal verbs data for English Assistant
-- Common phrasal verbs with difficulty levels and examples

INSERT INTO phrasal_verbs (verb, definition, examples, difficulty, status) VALUES
-- Beginner level phrasal verbs
('get up', 'To rise from bed or a sitting position', ARRAY['I get up at 7 AM every day.', 'Please get up from the chair.'], 'beginner', 'pending'),
('sit down', 'To take a seat', ARRAY['Please sit down and relax.', 'She sat down at the table.'], 'beginner', 'pending'),
('turn on', 'To start or activate something', ARRAY['Turn on the lights, please.', 'Can you turn on the TV?'], 'beginner', 'pending'),
('turn off', 'To stop or deactivate something', ARRAY['Turn off the computer before leaving.', 'Don''t forget to turn off the lights.'], 'beginner', 'pending'),
('look for', 'To search for something', ARRAY['I''m looking for my keys.', 'She is looking for a new job.'], 'beginner', 'pending'),
('pick up', 'To lift or collect something', ARRAY['Pick up your toys from the floor.', 'I''ll pick you up at 6 PM.'], 'beginner', 'pending'),
('put on', 'To wear or place clothing on body', ARRAY['Put on your jacket, it''s cold.', 'She put on her favorite dress.'], 'beginner', 'pending'),
('take off', 'To remove clothing or depart', ARRAY['Take off your shoes before entering.', 'The plane will take off soon.'], 'beginner', 'pending'),
('wake up', 'To stop sleeping', ARRAY['I wake up early every morning.', 'The noise woke me up.'], 'beginner', 'pending'),
('come back', 'To return', ARRAY['Come back soon!', 'He came back from vacation yesterday.'], 'beginner', 'pending'),

-- Intermediate level phrasal verbs
('give up', 'To stop trying or surrender', ARRAY['Don''t give up on your dreams.', 'He gave up smoking last year.'], 'intermediate', 'pending'),
('look after', 'To take care of someone or something', ARRAY['Can you look after my cat while I''m away?', 'She looks after her elderly parents.'], 'intermediate', 'pending'),
('run out of', 'To have no more of something', ARRAY['We ran out of milk.', 'I''m running out of time.'], 'intermediate', 'pending'),
('get along', 'To have a good relationship', ARRAY['Do you get along with your coworkers?', 'They get along very well.'], 'intermediate', 'pending'),
('break down', 'To stop working or collapse emotionally', ARRAY['My car broke down on the highway.', 'She broke down and started crying.'], 'intermediate', 'pending'),
('figure out', 'To understand or solve', ARRAY['I can''t figure out this math problem.', 'Did you figure out what went wrong?'], 'intermediate', 'pending'),
('put off', 'To postpone or delay', ARRAY['Don''t put off your homework.', 'The meeting was put off until next week.'], 'intermediate', 'pending'),
('bring up', 'To mention a topic or raise a child', ARRAY['Don''t bring up that subject again.', 'She brought up three children alone.'], 'intermediate', 'pending'),
('call off', 'To cancel', ARRAY['They called off the wedding.', 'The game was called off due to rain.'], 'intermediate', 'pending'),
('catch up', 'To reach the same level or get updated', ARRAY['I need to catch up on my reading.', 'Let''s catch up over coffee.'], 'intermediate', 'pending'),

-- Advanced level phrasal verbs
('come across', 'To find by chance or seem to be', ARRAY['I came across an old photo yesterday.', 'She comes across as very confident.'], 'advanced', 'pending'),
('get over', 'To recover from illness or disappointment', ARRAY['It took him months to get over the breakup.', 'I''m getting over a cold.'], 'advanced', 'pending'),
('look down on', 'To consider someone inferior', ARRAY['Don''t look down on people less fortunate.', 'He looks down on anyone without a degree.'], 'advanced', 'pending'),
('put up with', 'To tolerate or endure', ARRAY['I can''t put up with this noise anymore.', 'She puts up with a lot from her boss.'], 'advanced', 'pending'),
('live up to', 'To meet expectations', ARRAY['The movie didn''t live up to the hype.', 'He always lives up to his promises.'], 'advanced', 'pending'),
('cut down on', 'To reduce the amount of something', ARRAY['I''m trying to cut down on sugar.', 'We need to cut down on expenses.'], 'advanced', 'pending'),
('go through', 'To experience or examine carefully', ARRAY['She''s going through a difficult time.', 'Let''s go through the contract together.'], 'advanced', 'pending'),
('stand up for', 'To defend or support', ARRAY['You should stand up for your beliefs.', 'She always stands up for her friends.'], 'advanced', 'pending'),
('keep up with', 'To stay at the same level or pace', ARRAY['It''s hard to keep up with technology.', 'Can you keep up with the class?'], 'advanced', 'pending'),
('fall through', 'To fail to happen or be completed', ARRAY['Our vacation plans fell through.', 'The business deal fell through at the last minute.'], 'advanced', 'pending');

-- Add some sample history entries for testing
INSERT INTO history (section, query, result, explanation, examples, tags) VALUES
('vocabulary', 'hello', 'hola', 'A common greeting used when meeting someone', ARRAY['Hello, how are you?', 'Hello there!'], ARRAY['greeting', 'basic']),
('vocabulary', 'beautiful', 'hermoso/hermosa', 'Adjective describing something pleasing to look at', ARRAY['She is beautiful.', 'What a beautiful day!'], ARRAY['adjective', 'description']),
('grammar', 'present simple vs present continuous', 'Present simple is used for habits and facts, present continuous for actions happening now', 'Present simple: I work every day. Present continuous: I am working now.', ARRAY['I eat breakfast every morning.', 'I am eating breakfast right now.'], ARRAY['grammar', 'tenses']),
('correction', 'I am go to school', 'I am going to school', 'Use present continuous form "going" not base form "go"', ARRAY['I am going to the store.', 'She is going home.'], ARRAY['grammar', 'present-continuous']);