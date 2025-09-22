from flask import Flask, render_template, request, send_file, redirect, url_for
import random
import pandas as pd
import io

app = Flask(__name__)

QUESTION_BANK = {
    '9': {
        'Maths': {
            'Algebra': [
                "What is x if 2x + 3 = 7?",
                "Expand (a+b)^2."
            ],
            'Geometry': [
                "Define a parallelogram.",
                "What is the area of a triangle?"
            ]
        }
    }
}

generated_questions = []

@app.route('/', methods=['GET', 'POST'])
def home():
    global generated_questions
    classes = ['9', '10', '11', '12']
    subjects = list(QUESTION_BANK['9'].keys())
    topics = []
    questions = []
    selected_class = ''
    selected_subject = ''
    if request.method == 'POST':
        selected_class = request.form['class']
        selected_subject = request.form['subject']
        topics = list(QUESTION_BANK[selected_class][selected_subject].keys())
        if 'topics' in request.form:
            selected_topics = request.form.getlist('topics')
            questions = []
            for topic in selected_topics:
                questions += random.sample(QUESTION_BANK[selected_class][selected_subject][topic], 2)
            generated_questions = questions
    return render_template('index.html', 
                           classes=classes, 
                           subjects=subjects, 
                           topics=topics, 
                           questions=questions, 
                           selected_class=selected_class, 
                           selected_subject=selected_subject)

@app.route('/download')
def download():
    global generated_questions
    if not generated_questions:
        return redirect(url_for('home'))
    df = pd.DataFrame({'Questions': generated_questions})
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Mock Questions')
    output.seek(0)
    return send_file(output,
                     download_name="ICSE_Mock_Questions.xlsx",
                     as_attachment=True,
                     mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

if __name__ == '__main__':
    app.run()
