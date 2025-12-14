class MChatChatbot:
    def __init__(self, model_predictor):
        self.predictor = model_predictor

        # M-CHAT questions
        self.questions = {
            "A1": "Does your child look at you when you call his/her name?",
            "A2": "How easy is it for you to get eye contact with your child?",
            "A3": "Does your child point to indicate that s/he wants something? (e.g. a toy that is out of reach)",
            "A4": "Does your child point to share interest with you? (e.g. pointing at an interesting sight)",
            "A5": "Does your child pretend? (e.g. care for dolls, talk on a toy phone)",
            "A6": "Does your child follow where you're looking?",
            "A7": "If someone is upset, does your child try to comfort them? (e.g. hugging)",
            "A8": "Would you describe your child's first words as: typical or unusual?",
            "A9": "Does your child use simple gestures? (e.g. wave goodbye)",
            "A10": "Does your child stare at nothing with no apparent purpose?"
        }

        self.reset_conversation()

    def reset_conversation(self):
        self.current_question_idx = 0
        self.answers = {}
        self.demographics = {}
        self.stage = "introduction"

    #returns what the bot should say next depending on the stage.
    def get_next_question(self):
        if self.stage == "introduction":
            return "Hello! I'm here to help you complete the M-CHAT screening questionnaire. Are you ready to begin? (yes/no)"
        
        elif self.stage == "questions":
            keys = list(self.questions.keys())
            if self.current_question_idx < len(keys):
                key = keys[self.current_question_idx]
                return f"Question {self.current_question_idx + 1}/10: {self.questions[key]}\nPlease answer with 'yes' or 'no'."
            else:
                self.stage = "demographics"
                return "Thank you! Now I need some basic information.\nWhat is your child's age in months?"

        elif self.stage == "demographics":
            if "age" not in self.demographics:
                return "What is your child's age in months?"
            elif "sex" not in self.demographics:
                return "What is your child's sex? (male/female or m/f)"
            elif "jaundice" not in self.demographics:
                return "Was your child born with jaundice? (yes/no)"
            elif "family_asd" not in self.demographics:
                return "Does anyone in your immediate family have autism? (yes/no)"
            else:
                self.stage = "analysis"
                return "Thank you. Analyzing responses now..."
        return None

    #handles user input depending on the stage.
    def process_answer(self, user_input):
        ui = user_input.lower().strip()

        if self.stage == "introduction":
            if "yes" in ui or "ready" in ui:
                self.stage = "questions"
                return self.get_next_question()
            else:
                return "No problem! Let me know when you are ready."

        elif self.stage == "questions":
            if "yes" in ui:
                answer = 1
            elif "no" in ui:
                answer = 0
            else:
                return "Please respond with 'yes' or 'no'."

            key = list(self.questions.keys())[self.current_question_idx]
            self.answers[key] = answer
            self.current_question_idx += 1
            return self.get_next_question()

        elif self.stage == "demographics":
            if "age" not in self.demographics:
                try:
                    age = int(''.join(filter(str.isdigit, user_input)))
                    if 16 <= age <= 60:
                        self.demographics["age"] = age
                        return self.get_next_question()
                    else:
                        return "Please provide age between 16 and 60 months."
                except:
                    return "Invalid age. Please provide a number (e.g., 24)."

            elif "sex" not in self.demographics:
                if "m" in ui:
                    self.demographics["sex"] = "m"
                elif "f" in ui:
                    self.demographics["sex"] = "f"
                else:
                    return "Specify 'male' or 'female'."
                return self.get_next_question()

            elif "jaundice" not in self.demographics:
                if "yes" in ui:
                    self.demographics["jaundice"] = "yes"
                elif "no" in ui:
                    self.demographics["jaundice"] = "no"
                else:
                    return "Answer 'yes' or 'no'."
                return self.get_next_question()

            elif "family_asd" not in self.demographics:
                if "yes" in ui:
                    self.demographics["family_asd"] = "yes"
                elif "no" in ui:
                    self.demographics["family_asd"] = "no"
                else:
                    return "Answer 'yes' or 'no'."
                return self.get_next_question()

        elif self.stage == "analysis":
            return self.generate_result()     #Calls the prediction method.
        return "I didn't understand. Please rephrase."

    #generates the final screening assessment.
    def generate_result(self):
        pred, _ = self.predictor.predict(      #pred, _ : **tuple unpacking** "Take the first return value (pred) and ignore the second. (_), cause the prediction like return ("ASD", 0.85) "
            self.answers,
            self.demographics["age"],
            self.demographics["sex"],
            self.demographics["jaundice"],
            self.demographics["family_asd"]
        )

        qchat_score = sum(self.answers.values())
        self.stage = "complete"

        if pred == "ASD" or pred == 1:
            return f"Assessment Complete\nScore: {qchat_score}/10\nHigher risk for ASD characteristics.\nThis is a screening tool, not a diagnosis."
        else:
            return f"Assessment Complete\nScore: {qchat_score}/10\nLower concern for ASD characteristics.\nThis is a screening tool, not a diagnosis."

    def chat(self, user_message):
        return self.process_answer(user_message)

    def start_conversation(self):
        return self.get_next_question()
