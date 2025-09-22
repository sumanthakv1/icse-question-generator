import streamlit as st
import pandas as pd
import random
import io

st.title('ICSE Mock Paper Generator')

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

classes = ['9', '10', '11', '12']
class_selected = st.selectbox('Select Class', classes)
subjects = list(QUESTION_BANK.get(class_selected, {}).keys())
if subjects:
    subject_selected = st.selectbox('Select Subject', subjects)
    topics = list(QUESTION_BANK[class_selected][subject_selected].keys())
    topics_selected = st.multiselect('Select Topics', topics)
    generate = st.button('Generate Questions')
    if generate and topics_selected:
        questions = []
        for topic in topics_selected:
            available = QUESTION_BANK[class_selected][subject_selected][topic]
            questions += random.sample(available, min(2, len(available)))
        st.write("### Generated Questions")
        for q in questions:
            st.write("-", q)
        if len(questions) > 0:
            df = pd.DataFrame({'Questions': questions})
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Mock Questions')
            st.download_button(label="Download Excel", data=output.getvalue(), file_name="ICSE_Mock_Questions.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    elif generate and not topics_selected:
        st.warning("Please select at least one topic.")
else:
    st.info("Please wait for subject options to update.")

st.info("Expand the QUESTION_BANK dictionary for real use.")
