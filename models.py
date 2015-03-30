from google.appengine.ext import db
import random

class Words(db.Model):
    number = db.IntegerProperty(required=True)
    eng = db.StringProperty(required=True)
    rus = db.StringProperty(required=True)

    @staticmethod
    def getRandomWord(n):
        wordsCount = Words.all(keys_only=True).count()
        try:
            without_number = int(n)
            if without_number > 1 and without_number*2 > wordsCount:
                number = random.randint(1, without_number - 1)
            else:
                number = random.randint(without_number + 1, wordsCount)
        except ValueError:
            number = random.randint(1, wordsCount)
        q = db.GqlQuery("SELECT * FROM Words " +
                "WHERE number = :number " +
                "ORDER BY eng DESC", number = number)
        oWordsList = q.run(limit=1)

        return oWordsList
