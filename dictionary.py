from random import choice


class Word():
    @staticmethod
    def get_words():
        with open("./dict.txt","r") as file:
            words = file.read()
            words = words.split('\n')
        return words

    @classmethod #need over look
    def check_compatibility(cls,guess,word):    
        if guess in cls.get_words():
            word = list(word)
            check_result = []
            for i in range(5) :
                if  guess[i] == word[i]:
                    check_result.append('T')
                    word[i]='*'
                else:
                    check_result.append('F')
            
            for i in range(5):
                if guess[i] in word and check_result[i] != 'T':
                    check_result[i]='P'        

            return ''.join(check_result)
        else:
            return None
        

    @classmethod
    def random_word(cls):
        return choice(cls.get_words())
