import pickle


class SentimentService:
    def __init__(self):
        self.model, self.clf = self.load_model()

    def load_model(self):
        with open(r'C:\Users\alieves\Desktop\snippet-generation\core\sentiments\model.pkl', 'rb') as file:
            model, clf = pickle.load(file)
        file.close()
        return model, clf

    def predict(self, text: str):
        x_test = self.model.transform([text.lower()])
        score = self.clf.predict(x_test)
        return score[0]
