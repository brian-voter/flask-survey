from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

TOTAL_QUESTIONS = len(survey.questions)

@app.get("/")
def get_root():
    """returns survey start page with survey instruction"""

    title = survey.title
    instructions = survey.instructions

    return render_template("survey_start.html", survey_title=title,
                           survey_instructions=instructions)

@app.post("/begin")
def post_begin():
    """redirect to the question number 0"""

    return redirect("/questions/0")

@app.get("/questions/<int:question_num>")
def get_question(question_num):
    """If survey not yet completed, returns question page for the given question
    number, or redirects to the correct question page.

    If survey is already complete, redirect to /completion
    """

    num_answered = len(session.get("responses", []))

    # user already completed all questions
    if num_answered >= TOTAL_QUESTIONS:
        flash("You already completed this survey.")
        return redirect("/completion")

    # user tried to go to the wrong question page, redirect to the next question
    if question_num != num_answered:
        flash("Redirected from invalid question number")
        return redirect(f"/questions/{num_answered}")

    # user is requesting their next question, so we render it
    question = survey.questions[question_num]
    return render_template("question.html", question=question)


@app.post("/answer")
def post_answer():
    """appends user response to responses and redirect to next question
    or completion page"""

    responses = session.get("responses", [])
    responses.append(request.form.get("answer"))
    session["responses"] = responses

    num_answered = len(responses)

    if(num_answered >= TOTAL_QUESTIONS):
        return redirect("/completion")

    return redirect(f"/questions/{num_answered}")

@app.get("/completion")
def thank_you():
    """renders completion page with questions and responses,
    or if survey is incomplete, redirects to next question"""

    num_answered = len(session.get("responses", []))

    # user has not completed the survey, redirect to the next question
    if num_answered != TOTAL_QUESTIONS:
        flash("Survey incomplete, redirected to next question.")
        return redirect(f"/questions/{num_answered}")

    return render_template("completion.html", questions = survey.questions,
                           responses=session.get("responses"))
