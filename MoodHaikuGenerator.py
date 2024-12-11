import random
import nltk
import pronouncing
from typing import List, Set
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer

nltk.download('punkt', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('vader_lexicon', quiet=True)

class MoodHaikuGenerator:
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()
        self.lemmatizer = WordNetLemmatizer()
    
    def analyze_mood(self, user_input):
        #use built in function to calculate emotions associated with words
        sentiment_scores = self.sia.polarity_scores(user_input)
        
        #extract key words 
        emotional_words = self._extract_emotional_words(user_input)

        #use calculated sentiment score to identify mood of user
        compound = sentiment_scores['compound']
        if compound >= 0.05:
            sentiment = 'positive'
        elif compound <= -0.05:
            sentiment =  'negative'
        else:
            sentiment =  'neutral'

        #identify how strong their emotions are
        intensity = abs(sentiment_scores['compound'])
        
        return {'sentiment': sentiment,'emotional_words': emotional_words,'intensity': intensity}
    
    def _extract_emotional_words(self, text):
        # Tokenize and tag parts of speech
        words = word_tokenize(text.lower())
        tagged_words = nltk.pos_tag(words)
        
        # Focus on adjectives, nouns, and verbs that might convey emotion
        emotional_pos = ['JJ', 'NN', 'VB']  # Adjectives, Nouns, Verbs
        emotional_words = [
            word for word, pos in tagged_words 
            if pos in emotional_pos and len(word) > 2
        ]
        
        return emotional_words
    
    def find_related_words(self, words):
        related_words = set()
        for word in words:
            lemma = self.lemmatizer.lemmatize(word.lower())
            related_words.update(self.get_synonyms(lemma))
            related_words.update(self.get_hypernyms(lemma, 20))
        
        return related_words
    
    def get_synonyms(self, word: str) -> Set[str]:
        #finds synonyms using synet
        synonyms_set = set()
        for syn in wordnet.synsets(word):
            synonyms_set.update([lemma.name().replace('_', ' ') for lemma in syn.lemmas()])
        return synonyms_set
    
    def get_hypernyms(self, word: str, depth: int) -> Set[str]:
        hypernyms_set = set()
        for syn in wordnet.synsets(word):
            current_hypernyms = syn.hypernyms()
            for _ in range(depth):
                next_level_hypernyms = []
                for h in current_hypernyms:
                    hypernyms_set.update([hlem.name().replace('_', ' ') for hlem in h.lemmas()])
                    next_level_hypernyms.extend(h.hypernyms())
                current_hypernyms = next_level_hypernyms
                if not current_hypernyms:
                    break
        return hypernyms_set
    
    def generate_haiku(self, mood_analysis):
        #count syllables using pronouncing
        def count_syllables(word):
            pronunciations = pronouncing.phones_for_word(word.lower())
            if pronunciations:
                phonemes = pronunciations[0]
                return sum(char.isdigit() for char in phonemes)
            else:
                return None
        
        #compile words
        emotional_words = mood_analysis['emotional_words']
        related_words = self.find_related_words(emotional_words)
        
        all_words = emotional_words + list(related_words)
        
        
        sylly_1 = []
        sylly_2 = []
        sylly_3 = []
        #organize potential words by syllable count to be fitted 
        for word in all_words:
            count = count_syllables(word)
            if(count == 1):
                sylly_1.append(word)
            elif(count == 2):
                sylly_2.append(word)
            elif(count == 3):
                sylly_3.append(word)

        haiku_words = []
        #choose outline based on sentiment rating and then fill in with related words
        if mood_analysis['sentiment'] == 'positive':
            line2 = ['Soft', 'Kind', 'Sweet']
            template = [
                f"{line2[random.randint(0,len(line2)-1)]} {sylly_2[random.randint(0, len(sylly_2)-1)]} {sylly_2[random.randint(0, len(sylly_2)-1)]}",
                f"Gentle {sylly_2[random.randint(0, len(sylly_2)-1)]} {sylly_1[random.randint(0, len(sylly_1)-1)]} unfolds",
                f"Hope {sylly_3[random.randint(0, len(sylly_3)-1)]} {sylly_1[random.randint(0, len(sylly_1)-1)]}"
            ]
        elif mood_analysis['sentiment'] == 'negative':
            line1 = ['See shadows of', 'Suffering in', 'Fighting through']
            template = [
                f"{line1[random.randint(0,len(line1)-1)]} {sylly_1[random.randint(0, len(sylly_1)-1)]}",
                f"Silent echoes {sylly_3[random.randint(0, len(sylly_3)-1)]}",
                f"Pain {sylly_2[random.randint(0, len(sylly_2)-1)]} {sylly_2[random.randint(0, len(sylly_2)-1)]}"
            ]
        else:
            template = [
                f"Quiet {sylly_3[random.randint(0, len(sylly_3)-1)]}",
                f"Thoughts drift like {sylly_2[random.randint(0, len(sylly_2)-1)]} {sylly_1[random.randint(0, len(sylly_1)-1)]} {sylly_1[random.randint(0, len(sylly_1)-1)]}",
                f"Calm {sylly_2[random.randint(0, len(sylly_1)-1)]} settles"
            ]
        
        return "\n".join(template)
    
    def process(self, user_input):
        # Analyze mood
        mood_analysis = self.analyze_mood(user_input)
        
        # Generate and return haiku
        return self.generate_haiku(mood_analysis)

# Example usage
def main():
    print("Mood Haiku Generator")
    print("Tell me how you're feeling today...")
    
    generator = MoodHaikuGenerator()
    
    while True:
        user_input = input("Your mood: ")
        
        if user_input.lower() in ['quit', 'exit', 'bye']:
            break
        
        try:
            haiku = generator.process(user_input)
            print("\nYour Mood Haiku:")
            print(haiku)
            print("\n")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()