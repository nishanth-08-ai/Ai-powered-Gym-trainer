# StrideSync - AI Enhanced Workout Tracking and Form Validation  

## Overview  
StrideSync is an AI-powered fitness tracking system integrating **computer vision**, **machine learning**, and **natural language processing (NLP)** to provide:  
- **Real-time exercise monitoring & form validation**  
- **BMI calculation & personalized workout plans**  
- **Food composition analysis using YOLOv8**  
- **AI Chatbot for fitness & nutrition guidance**  

## Features  

### 💪 Exercise Tracking & Form Validation  
- Uses **MediaPipe Pose** and **OpenCV** to analyze workout posture.  
- **Repetition counting** based on joint angle calculations.  
- **Real-time feedback** on exercise form (e.g., “Correct your form!”).  

### 🍎 Food Composition Analysis  
- **YOLOv8-based object detection** for food recognition.  
- **Nutritional breakdown** (calories, protein, fats, carbs) based on weight input.  
- **Interactive Web UI** displaying food composition using Chart.js.  

### 🏋️ BMI Calculator & Workout Plans  
- **BMI calculation** based on height and weight input.  
- **Personalized workout recommendations** based on BMI category.  

### 🤖 AI Chatbot for Fitness Guidance  
- **NLP-based chatbot** trained on fitness and nutrition-related queries.  
- Provides responses to:  
  - **Exercise suggestions** (e.g., “What exercises help with weight loss?”)  
  - **Diet plans** (e.g., “What should I eat to lose weight?”)  
  - **Caloric values** (e.g., “How many calories are in a banana?”)  
- Built using **TensorFlow, LSTM, and scikit-learn** for intent classification.  

---

## Technologies Used  
| Category          | Tools & Libraries  |  
|------------------|------------------|  
| **Computer Vision** | OpenCV, MediaPipe, YOLOv8 |  
| **Machine Learning** | TensorFlow, PyTorch, scikit-learn |  
| **Backend** | Flask |  
| **Frontend** | HTML, CSS, JavaScript |  
| **NLP & Chatbot** | LSTM, Tokenizer, LabelEncoder |  
| **Data Visualization** | Chart.js |  

---

