import streamlit as st
import os

from dotenv import load_dotenv

load_dotenv()

from utils import safe_write

from chains import (
    product_manager_chain,
    tech_lead_chain,
    test_lead_chain,
    file_structure_chain,
    file_path_chain,
    code_chain,
    missing_chain,
    new_classes_chain
)

st.title("Code Generator")

request = st.text_area('Please Detail Your Desired Use Case for Code Generation! ', height=150)
app_name = st.text_input('Enter Project Name:')
submit = st.button("submit", type="primary")

if submit and request and app_name:

    dir_path = app_name + '/'

    design = product_manager_chain.run(request)
    design_doc_path = dir_path + '/design' + '/design.txt'
    safe_write(design_doc_path, design)
    st.markdown(""" :blue[Business Requirements : ] """, unsafe_allow_html=True)
    st.write(design)

    class_structure = tech_lead_chain.run(design)
    class_structure_path = dir_path + '/class_structure' + '/class_structure.txt'
    safe_write(class_structure_path, class_structure)
    st.markdown(""" :blue[Technical Design :] """, unsafe_allow_html=True)
    st.write(class_structure)

    test_plan = test_lead_chain.run(design)
    test_plan_path = dir_path + '/test_plan' + '/test_plan.txt'
    safe_write(test_plan_path, test_plan)
    st.markdown(""" :blue[Test Plan :] """, unsafe_allow_html=True)
    st.write(test_plan)

    file_structure = file_structure_chain.run(class_structure)
    file_structure_path = dir_path + '/file_structure' + '/file_structure.txt'
    safe_write(file_structure_path, file_structure)
    st.markdown(""" :blue[File Names :] """, unsafe_allow_html=True)
    st.write(file_structure)

    files = file_path_chain.run(file_structure)
    files_path = dir_path + '/files' + '/files.txt'
    safe_write(files_path, files)
    st.markdown(""" :blue[File Paths :] """, unsafe_allow_html=True)
    st.write(files)

    files_list = files.split('\n')

    missing = True
    missing_dict = {
        file: True for file in files_list
    }

    code_dict = {}

    while missing:

        missing = False
        new_classes_list = []

        for file in files_list:

            code_path = os.path.join(dir_path, 'code', file)
            norm_code_path = os.path.normpath(code_path)

            if not missing_dict[file]:
                safe_write(norm_code_path, code_dict[file])
                st.markdown(""" :red[Code & Unit Tests: 2nd Iteration] """, unsafe_allow_html=True)
                st.write(code_dict[file])
                continue

            code = code_chain.predict(
                class_structure=class_structure,
                structure=file_structure,
                file=file,
            )

            code_dict[file] = code
            response = missing_chain.run(code=code)
            if '<TRUE>' in response:
                missing = missing or missing_dict[file]
            else:
                safe_write(norm_code_path, code)
                st.markdown(""" :blue[Complete Code & Unit Tests: 1st Iteration] """, unsafe_allow_html=True)
                st.write(code)
                continue

            if missing_dict[file]:
                new_classes = new_classes_chain.predict(
                    class_structure=class_structure,
                    code=code
                )
                new_classes_list.append(new_classes)

        class_structure += '\n\n' + '\n\n'.join(new_classes_list)
