import os
from flask import render_template,url_for, flash, redirect, request
from flaskblog import app
from flaskblog.forms import RegistrationForm, LoginForm, DeleteForm, EditEmailForm, EditNameForm, ChangePassword, AddDateForm
from flaskblog.modelss import User, Article, Exam, user_exam, Quiz, Question, Choice
from flaskblog import db
from flask_login import login_user, login_required, logout_user, current_user
import json
import openai
from flask import jsonify
import datetime
import random




'''
posts = [ {'author': 'Faisal',
           'title': 'Flask Training',
           'content':'WhAt ThE FuCk iS GoInG oN',
           'date_posted': 'September 12, 2023'}
           
           ,


           {'author': 'PanDaa',
           'title': 'MeoW',
           'content':'HeLLo \'-\'',
           'date_posted': 'September 12, 2023'}]
'''

@app.route("/")
@login_required
def home():
    return render_template('index.html', user=current_user)  #posts=posts 

@app.route('/add_article', methods=['POST'])
def add_article():
    if request.method == 'POST':
        # Get the user ID based on your authentication method
        user_id = current_user.id 
        # Create a new article and populate its attributes
        new_article = Article(content=request.form['articleText'], user_id=user_id)
        
        # Add the article to the database and commit the changes
        db.session.add(new_article)
        db.session.commit()
        
        button_id = request.form.get('button_id')
       
        if button_id == 'generateQuizButton':
            return redirect(url_for('quiz', article=request.form['articleText'])) 
        elif button_id == 'generateSummaryButton': 
            return redirect(url_for('summary', article=request.form['articleText']))
        else:
             return redirect(url_for('home'))




@app.route("/about")
def about():
    return render_template('flaskblog\Bikin\templates\index.html',title='About')

@app.route("/register", methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(email= form.email.data, username=form.username.data, password=form.password.data)
        user = User.query.filter_by(email=form.email.data).first()
        user1 = User.query.filter_by(username=form.username.data).first()
        if user:
            flash('Email already exist', 'danger')
        
        elif user1:
            flash('Username already exist', 'danger')

        else:    
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash(f'Account created for {form.username.data}!',category='success')
            return redirect(url_for('home'))
    return render_template('register.html',title='Register', form=form, user=current_user)

@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        user = User.query.filter_by(username=form.username.data).first()#by using this we retrive from database the first user with email = email got from login page

        if user: #if there is user we get from previous query it will be true
            if user.password == form.password.data:
                flash('You have been logged in !', 'success')
                login_user(user, remember=True) # work like the session or cookie it make user status to login and remember it until he logout or flask server restart
                return redirect(url_for('home'))
            else:
                flash('User does not exist.', 'danger')
        else:
            flash('User does not exist.', 'danger')
    return render_template('login.html',title='Login', form=form, user=current_user)


@app.route('/logout')
@login_required # this to make sure you cant acces this page unless you are login
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/account", methods=['GET','POST'])
@login_required
def account():
    form = DeleteForm()
    form1 = EditNameForm()
    form2 = EditEmailForm()
    form3 = ChangePassword()
    if form1.validate_on_submit():
        user = User.query.filter_by(username=current_user.username).first()
        user1 = User.query.filter_by(username=form1.username.data).first()
        
        if user1:
            flash('Username already exist', 'danger')
        else:
            user.username = form1.username.data
            db.session.commit()
            flash('Your Username has been Changed !', 'success')
    if form2.validate_on_submit():
        user1 = User.query.filter_by(email=form2.email.data).first()
        
        if user1:
            flash('Email already exist', 'danger')
        else:
            user = User.query.filter_by(email=current_user.email).first()
            user.email = form2.email.data
            db.session.commit()
            flash('Your Email has been Changed !', 'success')
    if form3.validate_on_submit():
        if current_user.password == form3.oldpassword.data:
            if form3.newpassword.data == form3.confirm_newpassword.data:
                user = User.query.filter_by(username=current_user.username).first()
                user.password = form3.newpassword.data
                db.session.commit()
                flash('Your password has been Changed !', 'success')
            else:
                flash('The confirm new password doesn\'t match the new password , try again', 'danger')
        else:
            flash('Incorrect password, try again', 'danger')
    if form.validate_on_submit():
        if current_user.password == form.password.data:
            flash('Your account has been Deleted !', 'success')
            user = User.query.filter_by(username=current_user.username).first()
            db.session.delete(user)
            db.session.commit()
            #logout_user()
            return redirect(url_for('register'))
        else:
            flash('Incorrect password, try again', 'danger')
    return render_template('newaccount.html', form = form, form1 = form1, form2 = form2, form3 = form3, user=current_user) 
'''
@app.route("/account", methods=['GET','POST'])
@login_required
def account():

    form = DeleteForm()
    form1 = EditNameForm()
    form2 = EditEmailForm()
    form3 = ChangePassword()

    
    if form1.validate_on_submit():
        user = User.query.filter_by(username=current_user.username).first()
        user1 = User.query.filter_by(username=form1.username.data).first()
        
        if user1:
            flash('Username already exist', 'danger')

        else:
            user.username = form1.username.data
            db.session.commit()
            flash('Your Username has been Changed !', 'success')



    if form2.validate_on_submit():
        user1 = User.query.filter_by(email=form2.email.data).first()
        
        if user1:
            flash('Email already exist', 'danger')

        else:
            user = User.query.filter_by(email=current_user.email).first()
            user.email = form2.email.data
            db.session.commit()
            flash('Your Email has been Changed !', 'success')


    if form3.validate_on_submit():
        if current_user.password == form3.oldpassword.data:
            #if form3.newpassword.data == form3.confirm_newpassword.data:
                user = User.query.filter_by(username=current_user.username).first()
                user.password = form3.newpassword.data
                db.session.commit()
                flash('Your password has been Changed !', 'success')

           # else:
            #    flash('The confirm new password doesn\'t match the new password , try again', 'danger')

        else:
            flash('Incorrect password, try again', 'danger')









    if form.validate_on_submit():
        if current_user.password == form.password.data:
            flash('Your account has been Deleted !', 'success')
            user = User.query.filter_by(username=current_user.username).first()
            db.session.delete(user)
            db.session.commit()
            #logout_user()
            return redirect(url_for('register'))
        else:
            flash('Incorrect password, try again', 'danger')


    return render_template('account.html',title='Account', form = form, form1 = form1, form2 = form2, form3 = form3, user = current_user)
'''

@app.route("/quiz", methods=['GET','POST'])
@login_required
def quiz():

    openai.api_key = os.getenv('OPENAI_API_KEY')

    text = request.args.get('article')
    text = text.strip()

    prompt = f"\n\n{text}\nGenerate 10 multiple choice questions that covers the whole provided article and exactly 3 answers choices based on the following article:: number of the question. the question that covers the article.\n a) choice A \n b) choice B \n c) choice C. "

    
    
    response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=prompt,
                max_tokens=3000,  # You can adjust this based on your needs
                n = 10,  # Number of questions to generate
                stop=None,
                temperature=0.7  # You can adjust this for creativity
            )
    '''
    WE WILL USE READY RESPONSE FOR TESTING
    response = {
  "warning": "This model version is deprecated. Migrate before January 4, 2024 to avoid disruption of service. Learn more https://platform.openai.com/docs/deprecations",
  "id": "cmpl-8E7LGA8XOQINqDzGqN9fH7HEuByPY",
  "object": "text_completion",
  "created": 1698375506,
  "model": "text-davinci-002",
  "choices": [
    
    {
      "text": "\n1. What is the main focus of AI?\na. To create intelligent machines that can perform human-like tasks\nb. To revolutionize industries\nc. To improve our daily lives\n\n2. What are some of the ethical considerations of AI?\na. Concerns about job displacement\nb. The impact on employment\nc. Data privacy\n\n3. What are some of the potential applications of AI?\na. Addressing global problems\nb. Improving healthcare\nc. reducing climate change\n\n4. What is the future of AI?\na. More sophisticated AI systems\nb. AI systems becoming more capable\nc. Exciting developments\n\n5. What is one of the challenges of AI?\na. Its potential to revolutionize industries\nb. Ethical considerations\nc. The lack of understanding about AI\n\n6. What are some of the opportunities that AI presents?\na. New job opportunities\nb. The potential to address complex global problems\nc. The opportunity to improve our daily lives\n\n7. What is one of the benefits of AI?\na. Its potential to improve our daily lives\nb. Its ability to revolutionize industries\nc. Its potential to create new job opportunities\n\n8. What is one of the concerns of AI?\na. The impact on employment\nb. Job displacement\nc. The lack of understanding about AI\n\n9. What is the goal of AI?\na. To improve our daily lives\nb. To create intelligent machines\nc. To solve complex global problems\n\n10. What is the future of AI?\na. More sophisticated AI systems\nb. AI systems becoming more capable\nc. Exciting developments",     
      "index": 0,
      "logprobs": None,
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 211,
    "completion_tokens": 4173,
    "total_tokens": 4384
  }
}
'''
    
    titlePrompt = f"\n\n{text}\n create a concise title, that covers the whole provided article \n\n"
    titleResponse = openai.Completion.create(
                engine="gpt-3.5-turbo-instruct",
                prompt=titlePrompt,
                max_tokens=100,  # You can adjust this based on your needs
                
                stop=None,
                temperature=0.7  # You can adjust this for creativity
            )
    
    #print(titleResponse)
    '''
    titleResponse = {
    "id": "cmpl-8Lu1S3LRpWzwY9kDuuJ4jqJezioM9",
    "object": "text_completion",
    "created": 1700230930,
    "model": "gpt-3.5-turbo-instruct",
    "choices": [
        {
        "text": "\"Exploring the Challenges and Opportunities in Artificial Intelligence: Ethics, Employment, and Beyond\"",
        "index": 0,
        "logprobs": None,
        "finish_reason": "stop"
        }
    ],
    "usage": {
        "prompt_tokens": 314,
        "completion_tokens": 18,
        "total_tokens": 332
    }
        }
        '''
    cleaned_title = titleResponse['choices'][0]['text'][1:-1]
    
    questions = []

    for i, item in enumerate(response["choices"]):
        if(i==1):
            break
        text = item["text"].strip().split('\n')
        cleaned_text = [line.strip() for line in text if line.strip()]

        t = False
        if cleaned_text[4] == "2.":  # set a boolean if there is /n after the question number to jump it always
            t = True

        j = 0
        while j < len(cleaned_text) - 3:
            question_text = cleaned_text[j]

            answer_options = cleaned_text[j + 1:j + 4]
            for i, answer in enumerate(answer_options):
                answer_options[i]=answer[2:]

            questions.append({
                "question": question_text,
                "options": answer_options
            })

            j += 4
            if t:
                j += 1
    '''
    #this code to print the questions  in the terminal
    print("\n----------------------------------------------------------------------------------------------------------\n")
    for index, q in enumerate(questions):
        #print(f"Question{index + 1}: {q['question']}")
        print(q['question'])
        for i,a in enumerate(q['options']):
            print(a)
        print("\n")
    '''
    
    optionsOrder = []
    for i in range(10):
        optionNumberOrder =  random.sample(range(0, 3), 3)
        optionsOrder.append(optionNumberOrder)
    
    fromreattempt= "False" 
    return render_template('quiz.html', user=current_user, questions=questions, optionsOrder=optionsOrder,title=cleaned_title, fromreattempt=fromreattempt)


@app.route('/submit', methods=['GET'])
@login_required
def submit():
    grade = 0
    questions_data_json = request.args.get('questionsData')
    options_order_json = request.args.get('optionsOrder')
    user_answers_json = request.args.get('userAnswers')
    from_reattempt = request.args.get('fromreattempt')
    quizId = request.args.get('quizId')
    
    
    # Initialize variables
    questions_data = None
    options_order = None
    user_answers = None

    # Parse JSON if the data is not None
    if questions_data_json:
        questions_data = json.loads(questions_data_json)
    if options_order_json:
        options_order = json.loads(options_order_json)
    if user_answers_json:
        user_answers = json.loads(user_answers_json)


    if(from_reattempt == "False"):
    # Parse the JSON data if needed
        return render_template('submit.html', user=current_user, questions=questions_data, optionsOrder=options_order, answers=user_answers)
    
    else:
        for i in range(10):
            user_answer = user_answers[i]
            if user_answer is not None and user_answer != '':
        # Convert user_answer to int and check if the answer is correct
                if options_order[i][int(user_answer)-1] == 0:
                    grade += 1
        curQuiz = Quiz.query.filter_by(id=quizId).first()
        curQuiz.score = grade
        db.session.commit()
        return render_template('resubmit.html', user=current_user, questions=questions_data, optionsOrder=options_order, answers=user_answers,from_reattempt=from_reattempt)
        

@app.route('/save', methods=['POST'])
@login_required
def save():
    questions_data = request.form.get('questionsData')
    options_order = request.form.get('optionsOrder')
    user_answers = request.form.get('userAnswers')
    grade = request.form.get('grade')
    title = request.form.get('title')

    # Parse the JSON data if needed

    questions_data = json.loads(questions_data)

    user_id = current_user.id 
    
    new_quiz = Quiz(name=title, score=grade, user_id=user_id)    
    
    db.session.add(new_quiz)
    db.session.commit()
    
    quiz_id = new_quiz.id
    #quiz = Quiz.query.order_by(Quiz.id.desc()).first()
    for index, question in enumerate(questions_data):
        new_question = Question(text=question['question'], quiz_id=quiz_id)
        db.session.add(new_question)
        db.session.commit()
        question_id= new_question.id
        for choice in question['options']:
            new_choice = Choice(text=choice, question_id=question_id)
            db.session.add(new_choice)
            db.session.commit()
        

    return redirect(url_for('history'))

@app.route('/editQuizGrade', methods=['POST'])
def editQuizGrade():
    print('Request received.')
    key1_value = request.form.get('key1')
    key2_value = request.form.get('key2')

    print(key1_value)
    print(key2_value)

    # Process and save data to the database (replace with your database logic)
    # ...

    # Return an empty response or a small piece of data (optional)
    return ''

@app.route("/summary", methods=['GET','POST'])
@login_required
def summary():
    openai.api_key = os.getenv('OPENAI_API_KEY')

    text = request.args.get('article')
    text = text.strip()

    prompt = f"Summarize the following article: {text}"

    
    response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=3000,  # You can adjust this based on your needs
                #n = 10,  # Number of questions to generate
                stop=None,
                temperature=0.7  # You can adjust this for creativity
            )
    '''
    response = openai.Completion.create(
    engine="davinci",
    prompt=prompt,
    max_tokens=600,  # Adjust the number of tokens for your desired summary length
)'''

# Get and print the generated summary
    summary = response.choices[0].text
   
    return render_template('summary.html', user=current_user, summary=summary)



@app.route("/calendar", methods=['GET','POST'])
@login_required
def calendar():
    exams = []
    for exam in current_user.exams:
        temp = {"id" : exam.id,
                "course" : exam.course,
                "date"   : exam.date
                }
        exams.append(temp)
    sorted_exams = sorted(exams, key=lambda x: x["date"]) #sort the exams from the closest date, the first argument is the directory we want to sort, the second one is the key, we defined a function using lambda that gets the date for each element
    '''
    lambda is like defining a method we could sort it like that
    # Define a custom sorting function to extract the date from a dictionary
    def get_date(item):
        return item["date"]

    # Sort the 'exams' list using the custom sorting function
    sorted_exams = sorted(exams, key=get_date)
    '''
    current_date = datetime.date.today()
    return render_template('calendar.html', user=current_user, exams=sorted_exams, current_date=current_date)


@app.route("/addDate", methods=['GET','POST'])
@login_required
def addDate():
    form = AddDateForm()
    
    if form.validate_on_submit():
        if form.date.data<datetime.date.today():
            flash('Date cannot be in the past.', 'danger')
        else:
            new_exam = Exam(date= form.date.data, course = form.course.data)
            #user = User.query.filter_by(username=current_user.username).first()
            #db.session.delete(user)
            #user.exams.append(new_exam)
            
            exam = Exam.query.filter_by(date=form.date.data, course=form.course.data).first()
            flag = False
            #for exam in current_user.exams:
                # if new_exam.date == exam.date and new_exam.course == exam.course:
                        #flag = True
            if exam or flag:
                flash('exam already exist', 'danger')

            else:
                current_user.exams.append(new_exam)    
                db.session.add(new_exam)
                db.session.commit()
                flash(f'Exam date added for {current_user.username}!',category='success')
                return redirect(url_for('calendar'))
        
    return render_template('addDate.html',title='addDate', form=form, user=current_user)


@app.route("/deleteExam", methods=['POST'])
@login_required
def deleteExam():
    exams = db.session.query(Exam).all() #TO DELETE ALL THE EXAMS IN THE PAST
    for exam in exams:
        if(exam.date<datetime.date.today()):
            db.session.delete(exam)
            db.session.commit()

    checkboxes = request.form.getlist('checkbox[]')
    for exam_id in checkboxes:
        exam = Exam.query.filter_by(id=exam_id).first()
        if exam:
            flash(f'{exam.course} Exam has been deleted!',category='success')
            db.session.delete(exam)
            db.session.commit()
    return redirect(url_for('calendar'))


@app.route("/history", methods=['GET','POST'])
@login_required
def history():
    
    quizzes = Quiz.query.filter_by(user_id = current_user.id).all()

    quizzeslist = []
    for quiz in quizzes:
        quizzeslist.append({
                "id": quiz.id,
                "name": quiz.name,
                "grade": quiz.score
            })

    return render_template('history.html',quizzes = quizzeslist)


@app.route("/reattempt", methods=['POST'])
@login_required
def reattempt():
    if request.method == 'POST':
        quiz_id = request.form.get('quizId')
        #quiz = Quiz.query.filter_by(id = quiz_id).first()
        questionss = Question.query.filter_by(quiz_id = quiz_id).all()
        #options = Choice.query.filter_by(question_id = 21).all()
        title = Quiz.query.get_or_404(quiz_id).name
        
        questions=[]

        for question in questionss:
            options = Choice.query.filter_by(question_id = question.id).all()
            Choices=[]
            for option in options:
                Choices.append(option.text[1:])
            
            questions.append({
                "question": question.text,
                "options": Choices
            })    

    
    optionsOrder = []
    for i in range(10):
        optionNumberOrder =  random.sample(range(0, 3), 3)
        optionsOrder.append(optionNumberOrder)
    return render_template('quiz.html', user=current_user, questions=questions, optionsOrder=optionsOrder, quizId=quiz_id, title=title)
    #return redirect(url_for('history'))

@app.route("/deleteQuiz", methods=['POST'])
@login_required
def deleteQuiz():
    if request.method == 'POST':
        quiz_id = request.form.get('quizId')

    quiz = Quiz.query.get_or_404(quiz_id)

    # Check if the logged-in user is the owner of the quiz
    if current_user.id == quiz.user_id:
        # Assuming cascade is set up correctly, deleting the quiz will delete associated questions and choices
        db.session.delete(quiz)
        db.session.commit()
        flash('Quiz deleted successfully!', 'success')
    else:
        flash('You are not authorized to delete this quiz.', 'danger')

    return redirect(url_for('history'))

@app.route("/deleteSelectedQuizzes", methods=['POST'])
@login_required
def deleteSelectedQuizzes():
    if request.method == 'POST':
        selected_quiz_ids_str = request.form.get('selectedQuizIds')
        
        # Convert the string representation of the list to an actual list of integers
        selected_quiz_ids = [int(quiz_id.strip('"')) for quiz_id in selected_quiz_ids_str.strip("[]").split(",")]

        for quiz_id in selected_quiz_ids:
            quiz = Quiz.query.get_or_404(quiz_id)
            # Check if the logged-in user is the owner of the quiz
            if current_user.id == quiz.user_id:
                # Assuming cascade is set up correctly, deleting the quiz will delete associated questions and choices
                db.session.delete(quiz)
                db.session.commit()
                flash('Quiz deleted successfully!', 'success')
            else:
                flash('You are not authorized to delete this quiz.', 'danger')
    
        return redirect(url_for('history'))