from random import randint # Do not delete this line

def displayIntro():
    hangmanFile = open("hangman-ascii.txt","r")
    lineCounter = 0
    for i in hangmanFile:
        if(lineCounter == 23):
            break
        print(i)
        lineCounter += 1
    hangmanFile.close()

def displayEnd(result):
    hangmanFile = open("hangman-ascii.txt","r")
    wholeText = hangmanFile.readlines()
    if(result):
        for i in range(190,203):
            print(wholeText[i],end="")

    else:
        for i in range(99,112):
            print(wholeText[i],end="")
    hangmanFile.close()

            
def displayHangman(state):
    hangmanFile = open("hangman-ascii.txt","r")
    wholeText = hangmanFile.readlines()

    if(state == 5):
        for i in range(24,33):
            print(wholeText[i],end="") 

    elif(state == 4):
        for i in range(37,46):
            print(wholeText[i],end="") 

    elif(state == 3):
        for i in range(50,59):
            print(wholeText[i],end="") 

    elif(state == 2):
        for i in range(63,72):
            print(wholeText[i],end="") 

    elif(state == 1):
        for i in range(76,85):
            print(wholeText[i],end="") 
    
    elif(state == 0):
        for i in range(89,98):
            print(wholeText[i],end="") 
    hangmanFile.close()
            
def getWord():
    hangmanWordsFile = open("hangman-words.txt","r")
    words = hangmanWordsFile.readlines()
    hangmanWordsFile.close()
    result = words[randint(0,len(words) - 1)]
    return result[0:len(result) - 1] # return without \n for last char


def valid(c):
    validAlphabet = list()
    for i in range(ord("a"),ord("z") + 1):
        validAlphabet.append(chr(i))
    if(c in validAlphabet):
        return True
    return False

def userInput(mistakeCounter,hiddenWord):

    displayHangman(mistakeCounter)
    print("".join(hiddenWord),"\n")
    incomingChar = str(input("Enter English Lowercase Character: "))
    if(valid(incomingChar)):
        return incomingChar
    else:
        return userInput(mistakeCounter,hiddenWord)


def play():

    randomWord = getWord()
    mistakeCounter = 5
    hiddenWord = ["_"] * len(randomWord)
    while(True):
        if(mistakeCounter == 0):
            print("\nHidden word was: " + randomWord)
            return False
        if( not ("_" in "".join(hiddenWord))):
            print("\nGood Job! the word was", "'" + "".join(hiddenWord) + "'" ,"indeed!")
            return True
        
        incomingChar = userInput(mistakeCounter,hiddenWord)
        if(incomingChar in randomWord):
            for i in range(len(randomWord)):
                if(incomingChar == randomWord[i]):
                    hiddenWord[i] = incomingChar
        else:
            mistakeCounter -= 1
            
def hangman():
    while True:
        displayIntro()
        result = play()
        displayEnd(result)
        yerOrNo = str(input("\nDo you want to play again? (yes/no) \n"))
        if(yerOrNo.lower() == "no"):
            return
        
if __name__ == "__main__":
    hangman()