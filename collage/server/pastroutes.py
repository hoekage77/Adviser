# @collage.app.route('/api/loadfilters/', methods=['GET'])
# def loadfilters():
#     connection = collage.model.get_db()  # open db
#     with connection.cursor(dictionary=True) as cursor:
#         #         # cursor.execute("""CREATE TABLE filters (
#         #         #     filter_id INT AUTO_INCREMENT PRIMARY KEY,
#         #         #     filter_cat VARCHAR(255) NOT NULL,
#         #         #     filter_value VARCHAR(255) UNIQUE NOT NULL,
#         #         #     filter_name VARCHAR(255) UNIQUE NOT NULL
#         #         # )""")
#         #         # cursor.commit()
#         filters = ['1 credit', '2 credits', '3 credits',
#                    '4 credits', '5 credits', '6 credits']
#         for filter in filters:
#             insert_query = """INSERT INTO filters (filter_cat, filter_value, filter_name) VALUES (%s, %s, %s)"""
#             cursor.execute(insert_query, ('Credits', filter, f'c{filter}',))
#     connection.commit()
#     return flask.jsonify(status='Success'), 200

# @collage.app.route('/api/courses/<int:course_id>', methods=['POST'])
# def course_backpack(course_id):
#     op = flask.request.args.get('operation')
#     user_id = flask.request.args.get('user_id')
#     connection = collage.model.get_db()
#     cursor = connection.cursor()

#     if op == 'save':
#         try:
#             cursor.execute('''
#                 INSERT INTO saved_courses (user_id, course_id)
#                 VALUES (%s, %s)
#             ''', (user_id, course_id))
#             connection.commit()
#             return flask.jsonify({'status': 'success', 'message': 'Course saved successfully'}), 200
#         except Exception as e:
#             connection.rollback()
#             return flask.jsonify({'status': 'error', 'message': str(e)}), 500

#     elif op == 'delete':
#         try:
#             cursor.execute('''
#                 DELETE FROM saved_courses
#                 WHERE user_id = %s AND course_id = %s
#             ''', (user_id, course_id))
#             connection.commit()
#             return flask.jsonify({'status': 'success', 'message': 'Course removed successfully'}), 200
#         except Exception as e:
#             connection.rollback()
#             return flask.jsonify({'status': 'error', 'message': str(e)}), 500

#     else:
#         return flask.jsonify({'status': 'error', 'message': 'Invalid operation'}), 400

# This route is for the profile bar

# @collage.app.route('/api/test/', methods=['GET'])
# def test():
#     # Load CSV files
#     course_tags_df = pd.read_csv("./collage/server/lsa_course_tags.csv")
#     course_info_df = pd.read_csv("./collage/server/WN2025.csv")

#     # Filter to keep only unique combinations of Subject and Catalog Nbr
#     course_info_df = course_info_df.drop_duplicates(subset=['Subject', 'Catalog Nbr'])

#     conn = collage.model.get_db()
#     cursor = conn.cursor()

#     print("Cursor created")

#     num_row = 0
#     num_actual_row = 0

#     # Step 1: Populate `courses` table
#     for _, row in course_info_df.iterrows():
#         num_row += 1
#         if num_row % 100 == 0:
#             print(f"Processed {num_row} rows")

#         # Extract only the subject code within parentheses using regex
#         subject_match = re.search(r'\((.*?)\)', row['Subject'])
#         if subject_match:
#             subject = subject_match.group(1)  # Get text inside parentheses
#         else:
#             subject = row['Subject'].strip()  # Fallback if format is unexpected

#         catalog_nbr = row['Catalog Nbr'].strip()
#         course_code = f"{subject} {catalog_nbr}"
#         course_name = row['Course Title']
#         instructor = row['Instructor']

#         # Extract credit hours, handling cases with ranges
#         units_value = row['Units']
#         if pd.notna(units_value):
#             credit_hours = int(float(units_value.split('-')[0].strip()))
#         else:
#             credit_hours = 0  # Default to 0 if Units is NaN

#         # Default values for additional fields
#         location = row.get('Location', '')  # Use empty string if Location is not available
#         open_status = row.get('Open Status', '')

#         # Retrieve tags from the course_tags_df DataFrame
#         course_tags_row = course_tags_df[course_tags_df['Course Number'] == course_code]
#         if not course_tags_row.empty:
#             tags = course_tags_row.iloc[0, 3:8].fillna('')  # Fill NaNs with empty strings
#             tag_1, tag_2, tag_3, tag_4, tag_5 = tags.tolist()
#             if num_row % 50 == 0:
#                 print(f"{course_code} found in tags CSV: {tag_1}, {tag_2}, {tag_3}, {tag_4}, {tag_5}")
#         else:
#             if num_row % 50 == 0:
#                 print(f"Not found in tags CSV: {course_code}")
#             continue

#         # Insert course data into the courses table
#         cursor.execute(
#             """
#             INSERT INTO courses (
#                 course_code, credit_hours, instructor_id, topic_description,
#                 course_description, class_topic, icon_url, total_rating, num_ratings,
#                 open_status, tag_1, tag_2, tag_3, tag_4, tag_5
#             )
#             VALUES (%s, %s, NULL, '', '', %s, '', 0.0, 0, %s, %s, %s, %s, %s, %s)
#             """,
#             (course_code, credit_hours, subject, open_status, tag_1, tag_2, tag_3, tag_4, tag_5)
#         )
#         conn.commit()
#         num_actual_row += 1
#         print(f"Inserted {course_code}, Total inserted rows: {num_actual_row}")

#     # Close the database connection
#     cursor.close()
#     conn.close()

# @collage.app.route('/api/catalog/', methods=['POST'])
# # @jwt_required()
# def handle_catalog():
#     # verify_user()
#     connection = collage.model.get_db()  # open db
#     # assume JSON data format is {'user_id": INT}
#     data = flask.request.get_json()
#     user_id = data['user_id']
#     recommendations = recommend_classes(connection, user_id)

#     # the user does not exist
#     if recommendations == None:
#         return flask.jsonify(
#             {"status": "failure"}
#         )

#     recommendations = recommendations.to_dict(orient='records')

#     for course in recommendations:
#         course_id = course['course_id']

#         with connection.cursor(dictionary=True) as cursor:
#             course_info_query = """
#                 SELECT subject code, catalog_number,
#                 credit_hours, instructor_id, course_name,
#                 course_description, class_topic, ai_img_url
#                 FROM courses
#                 WHERE course_id = %s
#             """
#             cursor.execute(course_info_query, (course_id,))
#             course = cursor.fetchone()
#         course['course_id'] = course_id

#         # check whether an AI image has been generated for that course
#         if course['ai_img_url'] == None:
#             prompt = format_prompt(
#                 course['course_description'], course['class_topic'])
#             img_url = generate_image(
#                 model="dall-e-3",
#                 prompt=prompt
#             )
#             course['ai_img_url'] = img_url

#             with connection.cursor(dictionary=True) as cursor:
#                 img_query = """
#                     UPDATE courses
#                     SET ai_img_url = %s
#                     WHERE course_id = %s
#                 """
#                 cursor.execute(img_query, (img_url, course_id))
#                 connection.commit()

#     # return the JSON of "a list of dictionaries"
#     return flask.jsonify(recommendations)

# @collage.app.route('/api/init/', methods=['GET'])
# def initialize_classes():
#     # classes = [{'subject_code': 'ASTRO 106', 'catalog_number': 0, 'credit_hours': 1, 'location': 'North Campus', 'instructor_id': 1,
#     #             'topic_description': 'lsa', 'course_name': 'Aliens', 'course_description': 'evolution, interstellar travel, space exploration, extraterrestrial organisms', 'class_topic': 'natural science', 
#     #             'enrollment_status': 'open', 'ai_img_url': 'https://lh3.googleusercontent.com/d/1-kRA35fv-D5Dc6kC6hL6O6_H60UWD9fp=s220'}]
#     classes = [
#                 {'subject_code': 'ECON 101', 'catalog_number': 0, 'credit_hours': 4, 'location': 'North Campus', 'instructor_id': 1,
#                  'topic_description': 'lsa', 'course_name': 'Principles of Economics I', 'course_description': 'microeconomics, supply and demand, competition, taxes, trade', 'class_topic': 'economics', 
#                  'enrollment_status': 'open', 'ai_img_url': 'https://lh3.googleusercontent.com/d/1MDipcyr_JVs-TADYOc-i4j71xWvivQml=s220'},
#                 {'subject_code': 'EECS 183', 'catalog_number': 0, 'credit_hours': 4, 'location': 'North Campus', 'instructor_id': 1,
#                  'topic_description': 'engineering', 'course_name': 'EECS 183', 'course_description': 'programming, data, algorithms, computing, problem solving', 'class_topic': 'computer science', 
#                  'enrollment_status': 'open', 'ai_img_url': 'https://lh3.googleusercontent.com/d/1LbYOSJnTuDsPhNS8pFE6_y4r3M1ax3aZ=s220'},
#                 {'subject_code': 'Data Science 315', 'catalog_number': 0, 'credit_hours': 4, 'location': 'North Campus', 'instructor_id': 1,
#                 'topic_description': 'lsa', 'course_name': 'Statistics and Artificial Intelligence', 'course_description': 'statistics, artificial intelligence, deep neural networks, data transmission and generation', 'class_topic': 'data science', 
#                 'enrollment_status': 'open', 'ai_img_url': 'https://lh3.googleusercontent.com/d/1cAVe_WcKsT6bpSmV_3Fe-jwAGPWGgGlE=s220'},
#                 {'subject_code': 'FTVM 272', 'catalog_number': 0, 'credit_hours': 3, 'location': 'North Campus', 'instructor_id': 1,
#                 'topic_description': 'lsa', 'course_name': 'Classical Film Theory I', 'course_description': 'film theory, editing, media, digital culture, television', 'class_topic': 'film', 
#                 'enrollment_status': 'open', 'ai_img_url': 'https://lh3.googleusercontent.com/d/1ZiXTIQj1e_RSWcjWdoVpK1k06MkSN-2x=s220'},
#                 {'subject_code': 'IOE 202', 'catalog_number': 0, 'credit_hours': 2, 'location': 'North Campus', 'instructor_id': 1,
#                 'topic_description': 'engineering', 'course_name': 'Operations Engineering and Analytics', 'course_description': 'engineering, mathematical modeling, statistical analysis, manufacturing, optimization, transportation', 'class_topic': 'ioe', 
#                 'enrollment_status': 'open', 'ai_img_url': 'https://lh3.googleusercontent.com/d/1E2tv_166cXK0yi78-sHeQUTI1l-U5aH9=s220'},
#                 {'subject_code': 'MATH 217', 'catalog_number': 0, 'credit_hours': 4, 'location': 'North Campus', 'instructor_id': 1,
#                 'topic_description': 'lsa', 'course_name': 'Linear Algebra', 'course_description': 'problem solving, applications, engineering and sciences, mathematics', 'class_topic': 'mathematics', 
#                 'enrollment_status': 'open', 'ai_img_url': 'https://lh3.googleusercontent.com/d/1uIseE0Gakg3P2GVNcMrlperc57zFQDB5=s220'},
#                 {'subject_code': 'PHIL 183', 'catalog_number': 0, 'credit_hours': 3, 'location': 'North Campus', 'instructor_id': 1,
#                 'topic_description': 'lsa', 'course_name': 'Critical Reasoning', 'course_description': 'logic, decision making, practical and professional reasoning skills, statistics', 'class_topic': 'philosophy', 
#                 'enrollment_status': 'open', 'ai_img_url': 'https://lh3.googleusercontent.com/d/1fzPuvS59CJDaJXLnqCQQjDfVBVwqlR1j=s220'},
#                 {'subject_code': 'PSYCH 223', 'catalog_number': 0, 'credit_hours': 3, 'location': 'North Campus', 'instructor_id': 1,
#                 'topic_description': 'lsa', 'course_name': 'Entrepreneurial Creativity', 'course_description': 'entrepreneurship, leadership, business and technology development, communication', 'class_topic': 'psychology', 
#                 'enrollment_status': 'open', 'ai_img_url': 'https://lh3.googleusercontent.com/d/1KHNTtdPgXVf9nuoE-GvkD-9NUlufLAa2=s220'},
#                 {'subject_code': 'BIO 212', 'catalog_number': 0, 'credit_hours': 3, 'location': 'North Campus', 'instructor_id': 1,
#                  'topic_description': 'lsa', 'course_name': 'Plants and Human Health', 'course_description': 'medicine, health, botany, plants and food', 'class_topic': 'biology', 
#                  'enrollment_status': 'open', 'ai_img_url': 'https://lh3.googleusercontent.com/d/1CIucc6uVl_CQsL3I0MeDSP_iGsJqBTMt=s220'},
#                 {'subject_code': 'PSYCH 337', 'catalog_number': 0, 'credit_hours': 3, 'location': 'North Campus', 'instructor_id': 1,
#                  'topic_description': 'lsa', 'course_name': 'Hormones and Behavior', 'course_description': 'biopsychology, sex, learning and memory, response to stimuli', 'class_topic': 'psychology', 
#                  'enrollment_status': 'open', 'ai_img_url': 'https://lh3.googleusercontent.com/d/1OQnXy7-MqQL39mvns5nc6B6KSuAEJu0w=s220'},
#                 {'subject_code': 'SPANISH 231', 'catalog_number': 0, 'credit_hours': 4, 'location': 'North Campus', 'instructor_id': 1,
#                 'topic_description': 'lsa', 'course_name': 'Second Year Spanish', 'course_description': 'language, culture, Spanish speaking, reading, writing', 'class_topic': 'foreign language', 
#                 'enrollment_status': 'open', 'ai_img_url': 'https://lh3.googleusercontent.com/d/1hWbBp8bFLf7ekcE8qi2DYktuJA-SNf9h=s220'},
#                 # {'subject_code': 'ASTRO 106', 'catalog_number': 0, 'credit_hours': 1, 'location': 'North Campus', 'instructor_id': 1,
#                 # 'topic_description': 'lsa', 'course_name': 'Aliens', 'course_description': 'evolution, interstellar travel, space exploration, extraterrestrial organisms', 'class_topic': 'natural science', 
#                 # 'enrollment_status': 'open', 'ai_img_url': 'https://lh3.googleusercontent.com/d/1-kRA35fv-D5Dc6kC6hL6O6_H60UWD9fp=s220'},
#                 {'subject_code': 'CHEM 260', 'catalog_number': 0, 'credit_hours': 3, 'location': 'North Campus', 'instructor_id': 1,
#                 'topic_description': 'lsa', 'course_name': 'Chemical Principles', 'course_description': 'matter, thermodynamics, chemical kinetics, spectroscopic and electrochemical analysis', 'class_topic': 'natural science', 
#                 'enrollment_status': 'open', 'ai_img_url': 'https://lh3.googleusercontent.com/d/1zRgMJe9_i3Mx2vdgfWroaYVVzkDQBjKD=s220'},
#                 {'subject_code': 'COMM 341', 'catalog_number': 0, 'credit_hours': 3, 'location': 'North Campus', 'instructor_id': 1,
#                 'topic_description': 'lsa', 'course_name': 'Fasion and Media', 'course_description': 'fashion industry, identity, representation, technology, the environment, labor, and the law', 'class_topic': 'communcations', 
#                 'enrollment_status': 'open', 'ai_img_url': 'https://lh3.googleusercontent.com/d/1xir_qVnKJexIT9aGB6JPnUJH6_x6LN2b=s220'},
#                 {'subject_code': 'EARTH 125', 'catalog_number': 0, 'credit_hours': 3, 'location': 'North Campus', 'instructor_id': 1,
#                 'topic_description': 'lsa', 'course_name': 'Evolution and Extinction', 'course_description': '', 'class_topic': 'natural science', 
#                 'enrollment_status': 'open', 'ai_img_url': 'https://lh3.googleusercontent.com/d/1rQsrikEaoXTKzCx482yRUQ4K6KxnTiKt=s220'},
#                 {'subject_code': 'MKT 407', 'catalog_number': 0, 'credit_hours': 3, 'location': 'North Campus', 'instructor_id': 1,
#                 'topic_description': 'business', 'course_name': 'Designing Persuasive Communication', 'course_description': 'persuasion, strategy, film, video, photography, web design, media planning, teamwork', 'class_topic': 'finance', 
#                 'enrollment_status': 'open', 'ai_img_url': 'https://lh3.googleusercontent.com/d/1nHGN8sWh1pPZmCqIAB1isKdGMID45zwR=s220'},
#             ]
#     connection = collage.model.get_db()
#     with connection.cursor(dictionary=True) as cursor:
#         # instructor_query = """INSERT INTO instructors (full_name, department, email) VALUES (%s, %s, %s)"""
#         # cursor.execute(instructor_query, ('Andrew DeOrio', 'Engineering', 'awdeorio@umich.edu'))
#         # connection.commit()
#         for entry in classes:
#             insert_query = """
#                         INSERT INTO courses (subject_code, catalog_number, credit_hours, location, instructor_id,
#                         topic_description, course_name, course_description, class_topic, enrollment_status, ai_img_url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#                     """

#             cursor.execute(insert_query, (entry['subject_code'], entry['catalog_number'], entry['credit_hours'], entry['location'], entry['instructor_id'],
#                         entry['topic_description'], entry['course_name'], entry['course_description'], entry['class_topic'], entry['enrollment_status'], entry['ai_img_url']))
#     connection.commit()
#     print("success")
#     return

# @collage.app.route('/upload/resume/', methods=['POST'])
# def upload_file():
#     if 'file' not in flask.request.files:
#         return flask.jsonify({'error': 'No file part'}), 400

#     file = flask.request.files['file']
#     if file.filename == '':
#         return flask.jsonify({'error': 'No selected file'}), 400

#     if file:
#         connection = collage.model.get_db()
#         data = flask.request.get_json()
#         user_id = data['user_id']
#         file_stream = io.BytesIO(file.read())
#         keywords_string = parse_resume(file_stream)
#         # Updates the users table's keywords column
#         with connection.cursor(dictionary=True) as cursor:
#             keywords_query = """
#                 UPDATE users
#                 SET keywords = %s
#                 WHERE user_id = %s
#             """
#             cursor.execute(keywords_query, (keywords_string, user_id))
#             connection.commit()
#         return flask.jsonify({'success': 'keywords extracted'})

# OAuth setup
# oauth = OAuth(collage.app)

# google = oauth.register(
#     name='google',
#     client_id='YOUR_CLIENT_ID',  # TODO: change this
#     client_secret='YOUR_CLIENT_SECRET',
#     access_token_url='https://accounts.google.com/o/oauth2/token',
#     access_token_params=None,
#     authorize_url='https://accounts.google.com/o/oauth2/auth',
#     authorize_params=None,
#     userinfo_endpoint='https://www.googleapis.com/oauth2/v1/userinfo',  # This is only needed if using openId to fetch user info
#     client_kwargs={'scope': 'openid profile email'},
# )


# @collage.app.route('/api/accounts/', methods=['POST'])
# def handle_accounts():
#     """Handles login/logout, creating/deleting/editing accounts, and updating passwords."""
#     main_url = "/"
#     form = flask.request.form
#     op = form.get("operation")

#     if op == "login":
#         try:
#             token = google.authorize_access_token()
#             resp = google.get('userinfo')
#             user_info = resp.json()
#             flask.session['email'] = user_info['email']
#             context = {
#                 "status": "success"
#             }
#         except Exception as e:
#             context = {
#                 "status": "failure"
#             }
#         return flask.jsonify(**context)

#     elif op == "logout":
#         flask.session.pop('email', None)
#         return flask.redirect(main_url)

# @collage.app.route('/api/loadfilters/', methods=['GET'])
# def loadfilters():
#     connection = collage.model.get_db()  # open db
#     with connection.cursor(dictionary=True) as cursor:
#         # cursor.execute("""CREATE TABLE filters (
#         #     filter_id INT AUTO_INCREMENT PRIMARY KEY,
#         #     filter_cat VARCHAR(255) NOT NULL,
#         #     filter_value VARCHAR(255) UNIQUE NOT NULL,
#         #     filter_name VARCHAR(255) UNIQUE NOT NULL
#         # )""")
#         # cursor.commit()
#         filters = [{'category': 'School',
#                     'filter_value': 'sarchitecture',
#                     'filter_name': 'Architecture'
#                     },
#                     {'category': 'School',
#                     'filter_value': 'sart and design',
#                     'filter_name': 'Art & Design'
#                     },
#                     {'category': 'School',
#                     'filter_value': 'sbusiness',
#                     'filter_name': 'Business'
#                     },
#                     {'category': 'School',
#                     'filter_value': 'sdentistry',
#                     'filter_name': 'Dentistry'
#                     },
#                     {'category': 'School',
#                     'filter_value': 'seducation',
#                     'filter_name': 'Education'
#                     },
#                     {'category': 'School',
#                     'filter_value': 'sengineering',
#                     'filter_name': 'Engineering'
#                     },
#                     {'category': 'School',
#                     'filter_value': 'senvironmental and sustainability',
#                     'filter_name': 'Environmental & Sust.'
#                     },
#                     {'category': 'School',
#                     'filter_value': 'sinformation',
#                     'filter_name': 'Information'
#                     },
#                     {'category': 'School',
#                     'filter_value': 'slsa',
#                     'filter_name': 'LSA'
#                     },
#                     {'category': 'School',
#                     'filter_value': 'spublic health',
#                     'filter_name': 'Public Health'
#                     },
#                     {'category': 'School',
#                     'filter_value': 'spublic policy',
#                     'filter_name': 'Public Policy'
#                     },
#                     {'category': 'Credits',
#                     'filter_value': 'c1',
#                     'filter_name': '1 Credit'
#                     },
#                     {'category': 'Credits',
#                     'filter_value': 'c2',
#                     'filter_name': '2 Credits'
#                     },
#                     {'category': 'Credits',
#                     'filter_value': 'c3',
#                     'filter_name': '3 Credits'
#                     },
#                     {'category': 'Credits',
#                     'filter_value': 'c4',
#                     'filter_name': '4 Credits'
#                     },
#                     {'category': 'Credits',
#                     'filter_value': 'c5',
#                     'filter_name': '5 Credits'
#                     },
#                     {'category': 'Credits',
#                     'filter_value': 'c6',
#                     'filter_name': '6 Credits'
#                     },
#                     {'category': 'Major',
#                     'filter_value': 'manthropology',
#                     'filter_name': 'Anthropology'
#                     },
#                     {'category': 'Major',
#                     'filter_value': 'mbiology',
#                     'filter_name': 'Biology'
#                     },
#                     {'category': 'Major',
#                     'filter_value': 'mcommunications',
#                     'filter_name': 'Communications'
#                     },
#                     {'category': 'Major',
#                     'filter_value': 'mcomputer science',
#                     'filter_name': 'Computer Science'
#                     },
#                     {'category': 'Major',
#                     'filter_value': 'meconomics',
#                     'filter_name': 'Economics'
#                     },
#                     {'category': 'Major',
#                     'filter_value': 'mfinance',
#                     'filter_name': 'Finance'
#                     },
#                     {'category': 'Major',
#                     'filter_value': 'mfilm',
#                     'filter_name': 'Film'
#                     },
#                     {'category': 'Major',
#                     'filter_value': 'mforeign language',
#                     'filter_name': 'Foreign Language'
#                     },
#                     {'category': 'Major',
#                     'filter_value': 'mioe',
#                     'filter_name': 'Industrial Operations Engineering'
#                     },
#                     {'category': 'Major',
#                     'filter_value': 'mmathematics',
#                     'filter_name': 'Mathematics'
#                     },
#                     {'category': 'Major',
#                     'filter_value': 'mmusic',
#                     'filter_name': 'Music'
#                     },
#                     {'category': 'Major',
#                     'filter_value': 'mnatural science',
#                     'filter_name': 'Natural Science'
#                     },
#                     {'category': 'Major',
#                     'filter_value': 'mneuroscience',
#                     'filter_name': 'Neuroscience'
#                     },
#                     {'category': 'Major',
#                     'filter_value': 'mphilosophy',
#                     'filter_name': 'Philosophy'
#                     },
#                     {'category': 'Major',
#                     'filter_value': 'mpsychology',
#                     'filter_name': 'Psychology'
#                     },
#                     {'category': 'Major',
#                     'filter_value': 'mother',
#                     'filter_name': 'Other'
#                     },
#                     ]
#         for filter in filters:
#             insert_query = """
#                         INSERT INTO filters (filter_cat, filter_value, filter_name) VALUES (%s, %s, %s)"""
#             cursor.execute(insert_query, (filter['category'], filter['filter_value'], filter['filter_name']))
#     connection.commit()
#     return flask.jsonify(status='Success'), 200