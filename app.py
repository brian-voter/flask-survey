from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []


# DOC STRINGS!!!


@app.get("/")
def get_root():

    title = survey.title
    instructions = survey.instructions

    return render_template("survey_start.html", survey_title=title,
                           survey_instructions=instructions)

@app.post("/begin")
def post_begin():

    return redirect("/questions/0")

@app.get("/questions/<question_num>")
def get_questions(question_num):

    question = survey.questions[int(question_num)]
    return render_template("question.html", question=question)


@app.post("/answer")
def post_answer():

    responses.append(request.form.get("answer"))
    return redirect(f"/questions/{len(responses)}") # this is awful