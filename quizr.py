# -*- coding: utf-8 -*-
# https://github.com/sargo/quizr-flask
"""
Quizr - a quiz application created with Flask.
"""

import os, csv
from flask import Flask, session, request, render_template, redirect, url_for


# create app and initialize config
app = Flask(__name__)

# globals
mapping_answers = { 1:"A", 2:"B", 3:"C", 4:"D", 5:"E", 6:"F" }
quiz_list = None

app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development key',
))
app.config.from_envvar('QUIZR_SETTINGS', silent=True)


@app.route('/', methods=['GET', 'POST'])
def welcome_page():
    """
    Welcome page - quiz info and username form.
    """
    username = session.get('username')
    
    if request.method == 'POST':
        if not username:
            username = session['username'] = request.form['username']
        if username:
            session['questions'] = read_csv()
            return redirect(url_for('question_page'))

    return render_template('welcome.html', username=username)


def read_csv(file_path='data/quiz.csv'):
    question_dict = {}
    quiz_list = []
    with open(file_path, 'rb') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=';') # , quotechar='|'
        for index, row in enumerate(csv_reader):
            quiz_list.append({'row': [unicode(cell, 'utf-8') for cell in row]})
    return quiz_list


@app.route('/pytanie', methods=['GET', 'POST'])
def question_page():
    """
    Quiz question page - show question, handle answer.
    """
    # ToDo
    index = 0
    if request.method == 'POST':
        # save answer
        answer = int(request.form.get('answer'))
        index = int(request.form.get('index'))
        # if index > 7:
        #     import pdb; pdb.set_trace()
        quiz_list[index]['answer'] = mapping_answers[answer]
        index += 1
        if index == len(quiz_list):
            return redirect(url_for('result_page'))

    data = {}
    data['total'] = len(quiz_list)
    data['index'] = index
    data['question'] = quiz_list[index]['row'][0]
    data['answers'] = quiz_list[index]['row'][1:-1]
    data['correct'] = quiz_list[index]['row'][-1:]

    return render_template("question.html", data=data)


@app.route('/wynik')
def result_page():
    """
    Last page - show results.
    """
    # ToDo
    correct = 0
    for row in quiz_list:
        if row['answer'] == str(row['row'][-1:][0]):
            correct += 1
    data = {}
    data['total'] = len(quiz_list)
    data['correct'] = correct
    import pdb; pdb.set_trace()
    return render_template("result.html", data=data)


if __name__ == '__main__':
    app.debug = True
    quiz_list = read_csv()
    app.run(host=os.environ['IP'], port=int(os.environ['PORT']))
