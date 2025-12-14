import joblib
import numpy as np 
import pandas as pd
import ollama

class MChatPredictor:
    def __init__(self):
        self.model  = joblib.load(r"C:\Users\dell\OneDrive\Documents\Machine Learning\CISWIEProject\asd_RF_pipeline.pkl")
        print("Model loaded successfully!", flush=True)

    def predict(self, answers, age, sex, jaundice, family_asd):
        answers = {f"A{i}": answers.get(f"A{i}", 0) for i in range(1, 11)}
        qchat_score = sum(answers.values())

        features = pd.DataFrame([{
            **answers,  
            'Age': age,
            'Sex': str(sex).lower(),
            'Jaundice': str(jaundice).lower(),
            'Family_mem_with_ASD': str(family_asd).lower(),
            'Qchat-Score': qchat_score
        }])

        print("=== Features for prediction ===", flush=True)
        print(features, flush=True)
        print(f"Score: {qchat_score}", flush=True)


        try:
            prediction = self.model.predict(features)[0]
            probability = self.model.predict_proba(features)[0] if hasattr(self.model, "predict_proba") else None

            return prediction, probability
        except Exception as e:
            print(f"Error during prediction: {e}", flush=True)
            return None, None


def chat_with_llm(messages):
    try:
        result = ollama.list()
        models = result['models']
        print("Installed models:", models)


        if not models:
            raise Exception("No Ollama models found. Please ensure Ollama is running and models are installed.")

        model_name = models[0]['model']
        print(f"Using model: {model_name}", flush=True)

        #Make the chat request
        response = ollama.chat(
            model=model_name,
            messages=messages,
        )
        return response['message']['content']
    except Exception as e:
        print(f"Error during LLM chat: {e}", flush=True)
        return "This is a mock response because Ollama is not running."




