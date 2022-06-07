from expensewebsite.celery import app

@app.task
def email_sender(email):
    email.send(fail_silently=False)