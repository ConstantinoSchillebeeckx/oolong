INSERT INTO activity (name, description) VALUES 
('Drink','Drinking event.'),
('Eat','Eating event.'),
('Sleep','Sleeping event.'),
('Medication','Taking medication.'),
('Sex','Having sex.'),
('Bathroom','Using the bathroom.'),
('Exercise','Doing exercise.'),
('Relax','Relaxing.');

INSERT INTO public.auth_user
(password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) VALUES
('pbkdf2_sha256$36000$usemzdFnEivt$Wpb4Z2zJq/YUrg8FFN+y/qzB20pDeJfqg2CE24ey5nc=', NULL, true, 'constantino', 'Constantino', 'Schillebeeckx', 'titou@gmail.com', true, true, '2018-02-26 17:12:31.240'),
('pbkdf2_sha256$36000$wLBJNgE16iS4$1NFzUVoGAmIq6phn61H0LDbeJrcZHSOLbxfzpiivkwc=', '2018-02-27 16:42:57.534', false, 'meow', 'meow', 'meow', 'meow@gmail.com', false, true, '2018-02-27 16:42:57.449');

INSERT INTO questionnaire (name, description, form_header) VALUES 
('GAD-7','Generalized Anxiety Disorder 7 (GAD-7) is a self-reported questionnaire for screening and severity measuring of generalized anxiety disorder (GAD).','Over the last <b>2 weeks</b>, how often have you been bothered by the following problems?'),
('PHQ-9','The PHQ-9 is a 9-question instrument given to patients in a primary care setting to screen for the presence and severity of depression.','Over the last <b>2 weeks</b>, how often have you been bothered by any of the following problems?'),
('Custom','My own custom questionnaire.','Over the last <b>day</b>, how did you feel?');

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
('I felt hopeful','Custom');

INSERT INTO available_response (score, label, questionnaire_id) VALUES 
(0,'Not at all','GAD-7'),
(1,'Several days','GAD-7'),
(2,'More than half the days','GAD-7'),
(3,'Nearly every day','GAD-7'),
(0,'Not at all','PHQ-9'),
(1,'Several days','PHQ-9'),
(2,'More than half the days','PHQ-9'),
(3,'Nearly every day','PHQ-9'),
(1,'Strongly disagree','Custom'),
(2,'Disagree','Custom'),
(3,'Slightly disagree','Custom'),
(4,'Neither agree or disagree','Custom'),
(5,'Slightly agree','Custom'),
(6,'Agree','Custom'),
(7,'Strongly agree','Custom');
