from flask import Flask, request, render_template, make_response
from datetime import datetime, timedelta
import re

import random

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    status = None
    comment = None

    if request.method == "POST":
        age = int(request.form['age'])
        monthly_income = int(request.form['monthly_income'])
        criminal_record = request.form['criminal_record'] == 'true'
        paid = request.form['paid'] == 'yes'
        release_date = request.form['release_date'] if criminal_record else None
        payment_date = request.form['payment_date'] if paid else None

        status, comment = evaluate_loan(age, monthly_income, criminal_record, release_date, paid, payment_date)

        # Set cookies for the last status and comment
        response = make_response(render_template("index.html", status=status, comment=comment))
        response.set_cookie("last_status", status, max_age=3600)
        response.set_cookie("last_comment", comment, max_age=3600)
        return response

    #If not POST, try to get the previous data via cookies
    status = request.cookies.get("last_status")
    comment = request.cookies.get("last_comment")
    return render_template("index.html", status=status, comment=comment)


# Grumpy AI Decisions
def moody_comment():
    options = [
        " '-' We're judging you silently.",
        " This is going in your permanent record.",
        " Even your mom wouldn't approve this.",
        " We've seen squirrels with better financial habits.",
        " This application smells like regret.",
        " Your financial future is looking... interesting.",
        " Even our intern thinks this is a bad idea.",
        " We've denied worse... but not by much.",
        " Are you trying to get flagged by the algorithm?",
        " I would've said 'try again later,' but why prolong the pain.. .?",
        " We didn't think it could get worse. You proved us wrong.",
        " If a raccoon filled out this form, I'd be equally confused.",
        " Even the algorithm had to take a walk after reading this.",
        " Our circuits are designed to process numbers, not regret.",
        " SYSTEM STATUS: Confused. CONFIDENCE LEVEL: Deeply shaken.",
        " Surely this must be a test. Or a prank. Right?",
        " I've run this through four models and none of them want to take responsibility.",
        " Ran this through our decision tree. It tried to leaf.",
        " I wasn't trained for this. None of us were.",
        " If I had hands, they'd be in the air right now. In disbelief.",
        " Processing... ERR0R: Input too absurd for even a sarcastic machine.",
        " I'm just a program, but even I think you need supervision.",
        " If a pigeon pecked random answers into this form, it might've done better.",
        " I would've denied it sooner, but I was too busy laughing.",
        " This kind of application makes the algorithm question its own existence.",
        " Even the ERROR messages are confused.",
        " My kernel said no. It didn't even hesitate. It just... said no.",
        " Even my CPU looked away in shame."
    ]
    return random.choice(options)


def evaluate_loan(age, monthly_income, criminal_record, release_date, paid, payment_date):
    age_verdict = check_age(age)
    payment_verdict = check_payment_history(paid, payment_date)
    criminal_verdict = check_criminal_record(criminal_record, release_date)
    income_verdict = check_income(monthly_income)

    #If there are multiple "Pending,approved or denied", select the most severe one (fallback selection)
    verdicts = [age_verdict, payment_verdict, criminal_verdict, income_verdict]
    
    denied_messages = [msg for stat, msg in verdicts if stat == "Loan Denied"]
    if denied_messages:
        return "Loan Denied", max(denied_messages, key=len)

    pending_messages = [msg for stat, msg in verdicts if stat == "Pending"]
    if pending_messages:
        return "Pending", max(pending_messages, key=len)

    approved_messages = [msg for stat, msg in verdicts if stat == "Approved"]
    if approved_messages:
        return "Approved", max(approved_messages, key=len)


def check_age(age):
    if 18 <= age <= 24:
        return "Pending", f" High risk, You're young and reckless, good luck!"
    elif 25 <= age <= 39:
        return "Pending", f"{age} years... Old enough to know better, young enough to still mess it up."
    elif 40 <= age <= 50:
        return "Approved", f"{age} years old, You've seen some things, you know the drill."
    elif age > 99: #fallback for trolls users.
        return "Pending", f"Wait.. . {age} years old? Are you Vampire.. .Look, if our security cameras can't see you, we don't lend to vampires. They're night owls, and our office closes at 5. Anyway: Denied!"
    elif age > 50:
        return "Approved", " You're wise, but not too dangerous."

    return "Loan Denied", f" {age} years old ? Do your parents know you're making financial decisions? {moody_comment()}"


def check_payment_history(paid, payment_date):
    if not paid:
        return "Loan Denied", f"A loan? Without paying the last one? Bold move, my friend, I admire the confidence."
    
    today = datetime.today().date()

    #input validation
    payment_date = datetime.strptime(payment_date, "%Y-%m-%d").date()

    if paid and payment_date:
        delay = today - payment_date

        # fallback if payment date is in the future
        if delay < timedelta(days=-1):
            return "Loan Denied", f"Nice try, time traveler. {payment_date} is in the future! {moody_comment()}"

        if delay > timedelta(days=100000000):
            return "Loan Denied", f"{delay.days}days late? Did you send your payment with a carrier dinosaur? {moody_comment()}"
        elif delay > timedelta(days=100000):
            return "Loan Denied", f"{delay.days} days late? Did you write the payment date on a stone tablet and wait for erosion to deliver it? {moody_comment()}"
        elif delay > timedelta(days=1000):
            return "Loan Denied", f"{delay.days} days late? Blink twice if you were stuck in a time loop. {moody_comment()}"
        elif delay > timedelta(days=100):
            return "Loan Denied", f"{delay.days}  days late? Was the money strapped to a sloth with commitment issues? {moody_comment()}"
        elif delay > timedelta(days=60):
            return "Loan Denied", f"{delay.days} days late? Are you sending the money by pigeon? {moody_comment()}"
        elif delay > timedelta(days=30):
            return "Loan Denied", f"Thirty days late. Not fashionably, just financially. {moody_comment()}"
        elif delay > timedelta(days=20):
            return "Pending", " Severe Late Fees Applied! You might need a second loan to pay the fees."
        elif delay > timedelta(days=10):
            return "Pending", " Additional Fees Applied! You're entering dangerous waters."
        elif delay > timedelta(days=0):
            return "Pending", "Late Fees Applied! Better late than never... but it'll cost you."

        return "Approved", "A punctual human? We thought they went extinct."

    return "Loan Denied", f"Missing payment date? What is this, financial improv night? {moody_comment()}"


def check_criminal_record(has_record, release_date=None):
    if has_record and release_date:

        #inStarting Container

 * Serving Flask app 'chatbot'

 * Debug mode: on

WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.

 * Running on http://127.0.0.1:5000

Press CTRL+C to quit

 * Restarting with stat

 * Debugger is active!

 * Debugger PIN: 102-093-158
put validation
        release_date = datetime.strptime(release_date, "%Y-%m-%d").date()
        years_since_release = (datetime.today().date() - release_date).days // 365
        if years_since_release < 5:
            return "Loan Denied", "Let's give it a few more Tuesdays before we call you 'reformed.'"
        return "Approved", " You've done your time, but we're still watching you."
    
    return "Approved", "Not even a parking ticket? What are you, a cop?"


def check_income(income):
    if income > 200_000_000:
        return "Loan Denied", f"${income}? Bezos, is that you? No loans for trillionaires. Start your own bank !"
    elif income > 1_000_000:
        return "Loan Denied", f"${income}? Are you Bill Gates in disguise? This smells fishy...{moody_comment()}"
    elif income < 1000:
        return "Loan Denied", f"{income} ? This isn't a charity, buddy.{moody_comment()}"
    elif income < 5000:
        return "Pending", "You're on thin ice, but we're keeping an eye on you."
    elif income < 10000:
        return "Approved", "You can pay... with some dignity intact."
    return "Approved", " You probably have a yacht, but we're still not impressed."


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)
