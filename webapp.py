from flask import Flask, render_template, request, session
import re
import random
import os.path
import pickle
from collections import Counter
from datetime import datetime

app = Flask(__name__)

@app.route('/getform')
def get_and_display_form():
    return render_template('index.html',
                           the_title="Welcome!", )

@app.route('/processform', methods=['POST'])
def process_the_form():
    session["starttime"] = 0
    session["starttime"] = datetime.now()

    ranWord = random.choice(bigWordList)
    ##print(ranWord)
    ranWord = ranWord.lower()
    session["ranWord"] = ranWord

    return render_template('play.html',
                           the_ranword=ranWord,
                           the_title="Tick Tock")

@app.route('/processinput', methods = ['POST'])
def process_the_input():
    errorsTest = ""
    test = []
    guesses = []
    inputs = []
    dublicates = []
    notindictionary = []
    absentletters = []
    sameword = []
    errors = []
    guessLength = 7
    guessed = ""
    notindict = ""
    temp = ""

    session['Input'] = request.form['input'].lower().split()
        #Error checks
    for word in  session['Input']:
        word = word.lower()
        ranWord = session["ranWord"]
        session['cr'] = Counter(str(ranWord))
        session['cg'] = Counter(str(word))
        session['cg'] = session['cg'] - session['cr']
        inputs.append(word)
        if word in smallWordList:
            if(word in guesses):
                dublicates.append(word)
            elif(len(session['cg']) == 0):
                if(not word == ranWord):
                        #Append guess to the list
                        guesses.append(word)
                else:
                    sameword.append(word)
            else:
                for value, count in session['cg'].most_common():
                    absentletters.append(value)
                    ##i = ""
        else:
            notindictionary.append(word)

    if(len(dublicates) > 0):
        temp = "You are using dublicates in your list :"+ ','.join(dublicates)
        errors.append(str(temp))
    if(len(sameword) > 0):
        temp = "You are using the same word as the random word :" + ','.join(sameword)
        errors.append(str(temp))
    if(len(absentletters) > 0):
        temp = "You are using letters that are not in the random word :"+ ','.join(absentletters)
        errors.append(str(temp))
    if(len(notindictionary) > 0):
        temp = "You are using words that are not in the dictionary :"+ ','.join(notindictionary)
        errors.append(str(temp))
    if not len(guesses) == 7:
        temp = "You have only entered " + str(len(inputs)) +  " guesses. Please enter 7"
        errors.append(str(temp))
        ##errors = ','.join(errors)


        ##error1_ = errors(0).split()
        return render_template('youlose.html',
                                    errors=errors,
                                    the_title="Unlucky Pal"
                                  )
    else:
        endtime = datetime.now()
        resulttime = endtime - session["starttime"]
        session["resulttime"] = str(resulttime)
        return render_template('youwin.html',
                                  the_error=errors,
                                  the_time=session["resulttime"],
                                  the_title="You Win!")
@app.route('/highscores', methods=['POST'])
def process_the_table():
    leaderboard = {}
    top10 = {}
    ##top10RanWord = {}
    ranWordDict = {}
    placement = []
    positions = [1,2,3,4,5,6,7,8,9,10]
    ##To check if the file exists, if not create one
    if(os.path.isfile('static/highscoretable3.pickle') == False):
        with open('static/highscoretable3.pickle', 'wb') as pf:
            pickle.dump(leaderboard, pf)
    else:
        #Read in the file containing the leaderboard and assign to dictionary
        with open('static/highscoretable3.pickle', 'rb') as pf:
            leaderboard = pickle.load(pf)

    ##if(os.path.isfile('ranwordkey.pickle') == False):
    ##    with open('ranwordkey.pickle', 'wb') as pf:
    ##        pickle.dump(ranWordDict, pf)
    ##else:
        #Read in the file containing the leaderboard and assign to dictionary
    ##    with open('highscoretable.pickle', 'rb') as pf:
    ##        ranWordDict = pickle.load(pf)

    playername = request.form['name']
    #Assign player score and name to dictionary
    leaderboard[session["resulttime"]] = playername
    ##ranWordDict[session["resulttime"]] = session["ranWord"]

    #Write the updated leaderboard back to the file
    with open('static/highscoretable3.pickle', 'wb') as pf:
            pickle.dump(leaderboard, pf)

    #Display the leaderboard top 10
    for k in sorted(leaderboard)[:10]:
        print(leaderboard[k], '->', k)
        top10[k] = leaderboard[k]
    print("\n")

    ##for k in sorted(ranWordDict)[:10]:
        ##print(le[k], '->', k)
    ##    top10RanWord[k] = ranWordDict[k]
    ##print("\n")

    #Sort through the whole dictionary and append times to list in order
    for k in sorted(leaderboard):
        placement.append(k)
    for k in sorted(leaderboard):
        placement.append(leaderboard[k])
    #Find the actual postion of the player
    position = placement.index(session["resulttime"]) + 1
    #Only print players postion if they are outside the top 10
    if(position > 10):
        print("You placed",'',position,'',"out of",'',len(placement) - 1)


    return render_template('highscore.html',
                           the_total=len(leaderboard),
                           the_position=position,
                           the_leaderboard = top10)
                          ## the_ranword = top10RanWord,
                           ##the_positions = positions)

if __name__ == '__main__':
    app.secret_key = "lfvDLFKgDFKGdfgadfLKhndFjAgdaFAHdfgj:DFAjhhjhjhdfLJ"
    import re
    import random
    import os.path
    import pickle
    from collections import Counter
    from datetime import datetime

    bigWordList = []
    smallWordList = []
    refinedList = []

    index = 0
    with open ('static/words.txt', errors = 'ignore') as df:
        rawdata = df.read()

    words = rawdata.split()

    ##To get rid of all words with less than 3 letters
    for i in range(len(words)):
        if(len(words[i])) >=3:
            index+=1
            refinedList.insert(index,words[i])

    ##Split the remaining words into two lists, one of words more than 7 letters long
    ##And the other one with words with 3 or more letters
    for i in range(len(refinedList)):
        if(len(refinedList[i])) > 7:
            index+=1
            bigWordList.insert(index,refinedList[i])
        if(len(refinedList[i])) >=3:
            index+=1
            smallWordList.insert(index,refinedList[i])
    app.run(debug=True)
