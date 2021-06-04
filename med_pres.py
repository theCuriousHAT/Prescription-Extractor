# -*- coding: utf-8 -*-
"""
Created on Sun May 16 16:37:57 2021

@author: ajay.rawat
"""

import streamlit as st
import os
import pandas as pd
from bs4 import BeautifulSoup
import urllib
from PIL import Image
import io
import requests
import pytesseract

directory = os.path.dirname(__file__)
os.chdir(directory)

pytesseract.pytesseract.tesseract_cmd = os.path.join(directory,'Tesseract-OCR','tesseract.exe')


from medacy.model.model import Model
model = Model.load_external('medacy_model_clinical_notes')

im = Image.open(os.path.join(directory,'logos','Prescription Extractor-logos.jpeg'))

st.set_page_config(page_title="Prescription Extractor", page_icon=im)


def open_image(image):
    image_open = Image.open(image)
    return image_open


def image_to_text(opened_image):
    raw_text = pytesseract.image_to_string(opened_image)
    return raw_text


def cleanMe(text):
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    text = text.replace(r"[^a-zA-Z\d\_]+"," ")
    return text 


def extract_info(image_text):
    #clean_text = cleanMe(image_text)
    annotation = model.predict(image_text)
    tag_list = []
    text_list = []
    for i in annotation.annotations:
        tags = i[0]
        text = i[3]
        tag_list.append(tags)
        text_list.append(text)
        df = pd.DataFrame()
        df['Tags'] = tag_list
        df['Text'] = text_list
    return df

def file_selector():
    st.title("Prescription Extractor")
    uploaded_file = st.file_uploader("Upload Files",type=['png','jpeg','jpg'])
    if uploaded_file is not None:
        
        st.sidebar.image(uploaded_file)
        #file_details = {"FileName":uploaded_file.name,"FileType":uploaded_file.type,"FileSize":uploaded_file.size}
        #st.write(file_details)
        img = open_image(uploaded_file)
        image_text = image_to_text(img)
        clean_text = cleanMe(image_text)
        if st.button("Process"):
            pres = extract_info(image_text)
            st.write(pres)
        
    else:
        st.text("Please upload the Prescription")
            


if __name__== "__main__":
    file_selector()
    
    
    




