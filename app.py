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
            ],
            'Trigonometry': [
                "Define sine, cosine, and tangent ratios.",
                "Find the value of sin 30°."
            ],
            'Statistics': [
                "Define mean, median, and mode.",
                "Find the mean of these numbers: 2, 4, 6, 8."
            ],
            'Mensuration': [
                "Find the volume of a cylinder with radius r and height h.",
                "Calculate the surface area of a sphere."
            ]
        },
        'Economics': {
            'Introduction to Economics': [
                "What is Economics?",
                "Explain scarcity and choice."
            ],
            'Production': [
                "Define production in economics.",
                "List the factors of production."
            ],
            'Consumption': [
                "What is consumption?",
                "Differentiate between durable and non-durable goods."
            ],
            'Trade': [
                "What is domestic and international trade?",
                "Explain the importance of trade."
            ],
            'Money': [
                "Define money.",
                "Explain the functions of money."
            ]
        },
        'Commercial Applications': {
            'Trade': [
                "What is trade?",
                "Differentiate between wholesale and retail trade."
            ],
            'Aids to Trade': [
                "What are aids to trade?",
                "Explain the concept of banking."
            ],
            'Business Organizations': [
                "Name the types of business organizations.",
                "What is a partnership?"
            ],
            'Commerce': [
                "Define commerce.",
                "Explain the role of transport in commerce."
            ],
            'Insurance': [
                "What is insurance?",
                "Why is insurance important for businesses?"
            ],
            'Documents of Trade': [
                "What are bills of exchange?",
                "Explain the importance of invoices."
            ]
        }
    }
}

classes = list(QUESTION_BANK.keys())

class_selected = st.selectbox('Select Class', classes)
if class_selected:
    subjects = list(QUESTION_BANK[class_selected].keys())
    subject_selected = st.selectbox('Select Subject', subjects)
    if subject_selected:
        topics = list(QUESTION_BANK[class_selected][subject_selected].keys())
        topics_selected = st.multiselect('Select Topics', topics)
        generate = st.button('Generate Questions')
        
        if generate:
            if not topics_selected:
                st.warning("Please select at least one topic.")
            else:
                questions = []
                for topic in topics_selected:
                    questions += random.sample(
                        QUESTION_BANK[class_selected][subject_selected][topic],
                        min(2, len(QUESTION_BANK[class_selected][subject_selected][topic]))
                    )
                
                st.write("### Generated Questions")
                for idx, q in enumerate(questions, 1):
                    st.write(f"{idx}. {q}")
                
                df = pd.DataFrame({'Questions': questions})
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False, sheet_name='Mock Questions')
                st.download_button(
                    label="Download Excel",
                    data=output.getvalue(),
                    file_name="ICSE_Mock_Questions.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
else:
    st.info("Please select a class to see subjects.")

st.info("You can expand the QUESTION_BANK dictionary to cover other classes and subjects as needed.")
