# 🚀 Project Name

## 📌 Table of Contents
- [Introduction](#introduction)
- [Demo](#demo)
- [Inspiration](#inspiration)
- [What It Does](#what-it-does)
- [How We Built It](#how-we-built-it)
- [Challenges We Faced](#challenges-we-faced)
- [How to Run](#how-to-run)
- [Tech Stack](#tech-stack)
- [Team](#team)

---

## 🎯 Introduction
* Develop a Gen-AI-powered solution for data profiling to ensure compliance with regulatory requirements.
* Leverage LLMs and ML models to interpret reporting instructions and extract key data validation rules.
* Automatically generate profiling rules and validation code to assess data consistency and accuracy.
* Use unsupervised ML for anomaly detection and flagging suspicious transactions.
* Build a scalable, explainable, and interactive compliance assistant that evolves with regulatory trends![image](https://github.com/user-attachments/assets/a0ff61f1-8974-44ad-aa8b-876fdacf68ad)

## 🎥 Demo
🔗 [Live Demo](#) (if applicable)  
📹 [Video Demo](#) (if applicable)  
🖼️ Screenshots:

<img width="943" alt="image" src="https://github.com/user-attachments/assets/29dc08b2-988c-4a05-b1e6-db20b17cb34c" />


## 💡 Inspiration
The project aims to automate regulatory compliance by leveraging LLMs to extract validation rules from reporting instructions and using ML for anomaly detection. This ensures data accuracy, scalability, and adaptability to evolving regulations while enhancing trust and efficiency.

## ⚙️ What It Does
It automates data profiling and compliance by extracting validation rules from regulatory documents using LLMs and detecting anomalies in financial transactions using ML, ensuring accuracy and adherence to evolving regulations.

## 🛠️ How We Built It
* Used Federal Document to and got rules by using Retreival Augmented Generation (RAG) model by prompting a set of questions.
* Then converted those rules into python methods by leveraging regular expressions
* Input file is passed through these methods for validation and anamoly detection
  
## 🚧 Challenges We Faced
* Auto code generation using python
* rules extraction'
* Prompting and training the model

## 🏃 How to Run
1. Clone the repository  
   ```sh
   git clone https://github.com/ewfx/gaidp-new-gen.git
   ```
2. Install dependencies  
   ```sh
   pip install -r requirements.txt (for Python)
   ```
3. Run the project  
   ```sh
   python app.py
   ```

## 🏗️ Tech Stack
- 🔹 Frontend: Gradio
- 🔹 Backend: Python AIML models - Mistral Hugging Face LLM, RAG(Retreival Argumented Generation)
- 🔹 Other: Huggin Face API , Federal Doc

## 👥 Team
- **Vaibhav CTR** - [GitHub](#) | [LinkedIn](#)
- **Jithesh** - [GitHub](#) | [LinkedIn](#)
