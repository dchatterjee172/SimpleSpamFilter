import nltk
from nltk.corpus import stopwords
import os
from nltk.tokenize import wordpunct_tokenize
from os import listdir
from os.path import isfile,join
from numpy import zeros
nltk.data.path = ['nltk_data']
stopwords = set(stopwords.words('english'))
spam_path = 'spam/'
ham_path = 'ham/'
english_words=set()
def get_mail(file_name):
    message = ''
    try:
        with open(file_name, 'r') as mail_file:
            for line in mail_file:
                message += line
    except UnicodeDecodeError as e:
        with open(file_name, 'r',encoding="latin-1") as mail_file:
            for line in mail_file:
                message += line
    return message

def get_token(message):
    message=message.lower()
    message=message.replace('//',' ')
    message=message.replace(':',' ');
    message=message.replace('.',' ');
    message=message.replace(',',' ');
    message=message.replace('+',' ');
    message=message.replace('-',' ');
    message=message.replace('@',' ');
    message=message.replace('<',' ');
    message=message.replace('>',' ');
    message=message.replace('(',' ');
    message=message.replace(')',' ');
    message=message.replace('_',' ');
    message=message.replace(';',' ');
    message=message.replace('\\',' ')
    message=message.replace('/',' ')
    all_words = set(wordpunct_tokenize(message))
    msg_words = [word for word in all_words if word not in stopwords and len(word) > 2 and word in english_words]
    return msg_words
def make_training_set(path):
    training_set={}
    mails_in_dir=[mail_file for mail_file in listdir(path) if isfile(join(path, mail_file))]
    total_file_count=len(mails_in_dir)
    for mail_name in mails_in_dir:
        message = get_mail(path + mail_name)
        terms = get_token(message)
        for term in terms:
            if term in training_set:
                training_set[term]=training_set[term] + 1
            else:
                training_set[term]=1
    for term in training_set.keys():
        training_set[term] = float(training_set[term])/total_file_count
    return training_set
def test():
    spam_mails_in_dir = [mail_file for mail_file in listdir(spam_path) if isfile(join(spam_path, mail_file))]
    ham_mails_in_dir = [mail_file for mail_file in listdir(ham_path) if isfile(join(ham_path, mail_file))]
    total_file_countS = len(spam_mails_in_dir)
    total_file_countH = len(ham_mails_in_dir)
    correct=0
    for mail_name in spam_mails_in_dir:
        message=get_mail(spam_path + mail_name)
        term=get_token(message)
        probS=0
        p=zeros(shape=(len(term),))
        l,j=1,1
        for i in range(0,len(term)):
            p[i]=(spam_training_set[term[i]])/(spam_training_set[term[i]]+ham_training_set[term[i]])*2
            l*=p[i]
            j*=(2-p[i])
        probS=l/(l+j)
        if probS>.8:
            correct=correct+1
    print("correctly classified: "+str(correct)+" total: "+str(total_file_countS))
    print(float(correct)/total_file_countS*100)
    correct=0
    for mail_name in ham_mails_in_dir:
        message = get_mail(ham_path + mail_name)
        term = get_token(message)
        probS=0
        p=zeros(shape=(len(term),))
        l,j=1,1
        for i in range(0,len(term)):
            p[i]=(spam_training_set[term[i]])/(spam_training_set[term[i]]+ham_training_set[term[i]])*2
            l*=p[i]
            j*=(2-p[i])
        probS=l/(l+j)
        if probS<.8:
            correct=correct+1
    print('')
    print("correctly classified: "+str(correct)+" total: "+str(total_file_countH))
    print(float(correct)/total_file_countH*100)
with open("wordsEn.txt") as word_file:
    english_words = set(word.strip().lower() for word in word_file)
spam_training_set = make_training_set(spam_path)
print ("spam done")
ham_training_set = make_training_set(ham_path)
print ("ham done")
for msg in spam_training_set:
    if msg not in ham_training_set:
	    ham_training_set[msg]=0.00000001
for msg in ham_training_set:
    if msg not in spam_training_set:
    	spam_training_set[msg]=0.0000002
test() #uncomment to test this on given dataset
test_string=input("enter a message:- ")
term=get_token(test_string)
probS=0
p=zeros(shape=(len(term),))
l,j=1,1
for i in range(0,len(term)):
    p[i]=(spam_training_set[term[i]])/(spam_training_set[term[i]]+ham_training_set[term[i]])*2
    l*=p[i]
    j*=(2-p[i])
probS=l/(l+j)
print(probS)
if probS>.8:
    print ("spam")
else:
    print("ham")
