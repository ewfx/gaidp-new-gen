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
📹 [Video Demo](#) https://drive.google.com/file/d/19UZSzWJOQJ6ISFHjZF_K7eIFkUsfFUgq/view?usp=sharing 
🖼️ Screenshots:

<img width="602" alt="image" src="https://github.com/user-attachments/assets/e28987ca-524e-4306-baaa-8e534d4baa0c" />
<img width="452" alt="image" src="https://github.com/user-attachments/assets/cf12f7da-3c4d-4850-acd8-328c8be7a1cc" />
<img width="456" alt="image" src="https://github.com/user-attachments/assets/fada8387-7662-4ffc-9ca9-0572a05d9515" />
<img width="457" alt="image" src="https://github.com/user-attachments/assets/222f809b-bdbb-4ad0-b09a-8515e7bf597f" />
<img width="467" alt="image" src="https://github.com/user-attachments/assets/54736dfe-86a2-4d32-b16f-bbbbc33caeeb" />





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
