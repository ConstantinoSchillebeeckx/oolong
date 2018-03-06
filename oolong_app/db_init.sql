INSERT INTO activity (name, description, icon) VALUES 
('Drink','Drinking some liquids.','fa-beer'),
('Eat','Eating some food.','fa-utensils'),
('Sleep','Sleeping event.','fa-moon'),
('Medication','Taking medication.','fa-pills'),
('Sex','Having sex, either with someone or masturbating.','fa-heart'),
('Note','Generic note.','fa-sticky-note'),
('Bathroom','Using the bathroom.','fa-bath'),
('Exercise','Any type of physical activity.','fa-football-ball'),
('Relax','A general catch-all for a relaxing or social event.','fa-hand-peace'),
('Daily','Daily metric recording','fa-signal');

INSERT INTO public.auth_user
(password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) VALUES
('pbkdf2_sha256$36000$usemzdFnEivt$Wpb4Z2zJq/YUrg8FFN+y/qzB20pDeJfqg2CE24ey5nc=', NULL, true, 'constantino', 'Constantino', 'Schillebeeckx', 'titou@gmail.com', true, true, '2018-02-26 17:12:31.240'),
('pbkdf2_sha256$36000$wLBJNgE16iS4$1NFzUVoGAmIq6phn61H0LDbeJrcZHSOLbxfzpiivkwc=', '2018-02-27 16:42:57.534', false, 'meow', 'meow', 'meow', 'meow@gmail.com', false, true, '2018-02-27 16:42:57.449');

INSERT INTO questionnaire (name, description, form_header) VALUES 
('GAD-7','Generalized Anxiety Disorder 7 (GAD-7) is a self-reported questionnaire for screening and severity measuring of generalized anxiety disorder (GAD).','Over the last <b>2 weeks</b>, how often have you been bothered by the following problems?'),
('PHQ-9','The PHQ-9 is a 9-question instrument given to patients in a primary care setting to screen for the presence and severity of depression.','Over the last <b>2 weeks</b>, how often have you been bothered by any of the following problems?'),
('Happiness','My own custom daily questionnaire for happiness.','For each of the following emotions, respond with how strongly you agree or disgree with the statement: <b>Today</b> I felt ...'),
('Anxiety','My own custom daily questionnaire for anxiety.','For each of the following emotions, respond with how strongly you agree or disgree with the statement: <b>Today</b> I felt ...'),
('Depression','My own custom daily questionnaire for depression.','For each of the following emotions, respond with how strongly you agree or disgree with the statement: <b>Today</b> I felt ...'),
('Summary', 'Questionnaire to get a single, summarizing stat for each affect.','On a score from 1 to 10, 10 being the strongest feeling, rate how you felt <b>today</b> for each of the feelings:');

INSERT INTO question (question, questionnaire_id) VALUES
('Feeling nervous, anxious or on edge','GAD-7'),
('Not being able to stop or control worrying','GAD-7'),
('Worrying too much about different things','GAD-7'),
('Trouble relaxing','GAD-7'),
('Being so restless that it is hard to sit still','GAD-7'),
('Becoming easily annoyed or irritable','GAD-7'),
('Feeling afraid as if something awful might happen','GAD-7'),
('Little interest or pleasure in doing things','PHQ-9'),
('Feeling down, depressed, or hopeless','PHQ-9'),
('Trouble falling or staying asleep, or sleeping too much','PHQ-9'),
('Feeling tired or having little energy','PHQ-9'),
('Poor appetite or overeating','PHQ-9'),
('Feeling bad about yourself — or that you are a failure or have let yourself or your family down','PHQ-9'),
('Trouble concentrating on things, such as reading the newspaper or watching television','PHQ-9'),
('Moving or speaking so slowly that other people could have noticed? Or the opposite — being so fidgety or restless that you have been moving around a lot more than usual ','PHQ-9'),
('Thoughts that you would be better off dead or of hurting yourself in some way','PHQ-9'),
('hopeful','Happiness'),
('cheerful','Happiness'),
('enthusiastic','Happiness'),
('interested, engaged and stimulated','Happiness'),
('I liked myself','Happiness'),
('satisfied','Happiness'),
('tranquil','Happiness'),
('purposeful / meaningful','Happiness'),
('my life was worth living','Happiness'),
('uneasy / nervous / tense','Anxiety'),
('stressed','Anxiety'),
('overwhelmed','Anxiety'),
('ruminative / can''t concentrate','Anxiety'),
('impending doom','Anxiety'),
('nervous when my normal routine was disturbed','Anxiety'),
('that various situations made me worry','Anxiety'),
('I had difficulty calming down','Anxiety'),
('I had sudden feelings of panic','Anxiety'),
('hopeless','Depression'),
('sad','Depression'),
('tired','Depression'),
('discouraged','Depression'),
('low self-esteem / worthless','Depression'),
('guilt','Depression'),
('lonely','Depression'),
('like a failure','Depression'),
('like hurting myself','Depression'),
('that my life is empty','Depression'),
('that nothing is interesting','Depression'),
('I had no reason for living','Depression'),
('happy','Summary'),
('anxious','Summary'),
('depressed','Summary');

INSERT INTO available_response (score, label, questionnaire_id) VALUES 
(0,'Not at all','GAD-7'),
(1,'Several days','GAD-7'),
(2,'More than half the days','GAD-7'),
(3,'Nearly every day','GAD-7'),
(0,'Not at all','PHQ-9'),
(1,'Several days','PHQ-9'),
(2,'More than half the days','PHQ-9'),
(3,'Nearly every day','PHQ-9'),
(1,'Strongly disagree','Happiness'),
(2,'Disagree','Happiness'),
(3,'Slightly disagree','Happiness'),
(4,'Neither agree or disagree','Happiness'),
(5,'Slightly agree','Happiness'),
(6,'Agree','Happiness'),
(7,'Strongly agree','Happiness'),
(1,'Strongly disagree','Anxiety'),
(2,'Disagree','Anxiety'),
(3,'Slightly disagree','Anxiety'),
(4,'Neither agree or disagree','Anxiety'),
(5,'Slightly agree','Anxiety'),
(6,'Agree','Anxiety'),
(7,'Strongly agree','Anxiety'),
(1,'Strongly disagree','Depression'),
(2,'Disagree','Depression'),
(3,'Slightly disagree','Depression'),
(4,'Neither agree or disagree','Depression'),
(5,'Slightly agree','Depression'),
(6,'Agree','Depression'),
(7,'Strongly agree','Depression'),
(1,1,'Summary'),
(2,2,'Summary'),
(3,3,'Summary'),
(4,4,'Summary'),
(5,5,'Summary'),
(6,6,'Summary'),
(7,7,'Summary'),
(8,8,'Summary'),
(9,9,'Summary'),
(10,10,'Summary');
