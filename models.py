from google.appengine.ext import db
import random
import os
import logging
import hashlib
import csv

class Vocabs(db.Model):
    name = db.StringProperty(required=True)
    hashfile = db.StringProperty(required=True)

class Words(db.Model):
    number = db.IntegerProperty(required=True)
    vocab = db.ReferenceProperty(Vocabs, collection_name='vocab_type')
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


def _updateVocabsList():
    template_dir = os.path.join(os.path.dirname(__file__), 'vocabs')
    for root, dirs, files in os.walk(template_dir):
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(template_dir, file)
                file_name = os.path.splitext(file)[0]
                hashfile = hashlib.md5(open(file_path).read()).hexdigest()

                q = Vocabs.all()
                q.filter("hashfile = ", hashfile)
                q.filter("name = ", file_name)
                result = q.get()

                if result is None:
                    oVd = Vocabs.all()
                    oVd.filter("name = ", file_name)
                    oldV = oVd.get()
                    db.delete(oVd)
                    
                    vocabs = Vocabs(name = file_name, hashfile=hashfile)
                    vocabs.put()

                    with open(file_path, 'rb') as csvfile:
                        logging.info('csvfile')
                        logging.info(csvfile)
                        reader = csv.reader(csvfile, delimiter=';', quotechar='"')

                        oWd = Words.all()
                        oWd.filter("vocab = ", oldV)
                        # result = oWd.get()
                        db.delete(oWd)

                        counter = 0;
                        for row in reader:
                            print row
                            try:
                                counter = counter + 1
                                eng =  u'%s' % row[0].decode('utf-8')
                                rus =  u'%s' % row[1].decode('utf-8')
                                c = Words(vocab=vocabs, number=counter, eng=eng, rus=rus)
                                c.put()
                            except db.Error:
                                print db.Error.message
