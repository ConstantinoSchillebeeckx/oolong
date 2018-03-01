INSERT INTO activity (name, description) VALUES 
('Eat','eat'),
('Sleep','sleep');

INSERT INTO public.auth_user
(password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) VALUES
('pbkdf2_sha256$36000$usemzdFnEivt$Wpb4Z2zJq/YUrg8FFN+y/qzB20pDeJfqg2CE24ey5nc=', NULL, true, 'constantino', 'Constantino', 'Schillebeeckx', 'titou@gmail.com', true, true, '2018-02-26 17:12:31.240'),
('pbkdf2_sha256$36000$wLBJNgE16iS4$1NFzUVoGAmIq6phn61H0LDbeJrcZHSOLbxfzpiivkwc=', '2018-02-27 16:42:57.534', false, 'meow', 'meow', 'meow', 'meow@gmail.com', false, true, '2018-02-27 16:42:57.449');

INSERT INTO questionnaire (name, description, form_header) VALUES 
('GAD-7','Generalized Anxiety Disorder 7 (GAD-7) is a self-reported questionnaire for screening and severity measuring of generalized anxiety disorder (GAD).','Over the last 2 weeks, how often have you been bothered by the following problems? ');

INSERT INTO question (question, questionnaire_id) VALUES
('Feeling nervous, anxious or on edge',1),
('Not being able to stop or control worrying',1),
('Worrying too much about different things',1),
('Trouble relaxing',1),
('Being so restless that it is hard to sit still',1),
('Becoming easily annoyed or irritable',1),
('Feeling afraid as if something awful might happen',1);

INSERT INTO available_response (score, label, questionnaire_id) VALUES 
(0,'Not at all',1),
(1,'Several days',1),
(2,'More than half the days',1),
(3,'Nearly every day',1);
