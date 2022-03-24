# ----------------------Index Sub Cipher----------------------



def encryptIndexSubstitutionCipher(text):
    mainCode = generateCodeForCipher()
    numericValue = "" 
    counter = 0
    for i in text:
        if(counter == len(text) - 1):
            numericValue += mainCode[i]
        else:
            numericValue += mainCode[i] + " " 
            counter += 1  
    return numericValue

def decryptIndexSubstitutionCipher(text):
    mainCode = generateCodeForCipher()
    value = ""
    string = ""
    count = 0
    for i in text:
        if(i == " "):
            value += getKey(string,mainCode)
            string = ""
            count += 1
        elif(count == len(text)-1):
            string += i
            value += getKey(string,mainCode)
        else:
            string += i
            count += 1
    return value

#additional function for generating dictionary. keys of aplhabet, values from 01 to 26
def generateCodeForCipher():
    mainCode = {}
    increment = 1
    orderOfA = ord("a")
    # 18 because, 9 of i space takes string values in j, so logic is : 17 + 9 = 26
    for i in range(0,18):
        if(i == 0):
            for j in range(1,10):
                numb1 = str(i)
                numb2 = str(j)
                numb = numb1 + numb2
                mainCode[chr(orderOfA)] = numb
                orderOfA += 1
        else:
            number = int(numb) + increment  
            increment += 1  
            mainCode[chr(orderOfA)] = str(number)
            orderOfA += 1
    return mainCode  
      
# ----------------------Morse Code----------------------
morseCode = {
    'a': '._',
    'b': '_...',
    'c': '_._.',
    'd': '_..',
    'e': '.',
    'f': '.._.',
    'g': '__.',
    'h': '....',
    'i': '..',
    'j': '.___',
    'k': '_._',
    'l': '._..',
    'm': '__',
    'n': '_.',
    'o': '___',
    'p': '.__.',
    'q': '__._',
    'r': '._.',
    's': '...',
    't': '_',
    'u': '.._',
    'v': '..._',
    'w': '.__',
    'x': '_.._',
    'y': '_.__',
    'z': '__..'
}

#returns morse code with no sapce from begining and in the end. only between chars
def encryptMorseCode(text):
    code =''
    count = 0
    for i in text:
        if(count == 0):
            code += morseCode[i]
            count += 1
        elif(count == len(text) - 1):
            code += ' ' + morseCode[i]

        else:
            code +=  ' ' + morseCode[i]
            count += 1
            
    return code

def decryptMorseCode(text):
    string = ''
    result = ''
    count = 0
    for i in text:
        if(i == " "):
            result += getKey(string,morseCode)
            string = ''
            count += 1
        elif(count == len(text) - 1):
            string += i
            result += getKey(string,morseCode)
        else:
            string += i
            count += 1
    return result

# additional function to get keys from any dictionary
def getKey(val,dictionary):
    for key, value in dictionary.items():
         if val == value:
            return key
    

# ----------------------Affine Cipher----------------------
def encryptAffineCipher(text, a, b):
    alphOrder = orderingAlpha()
    result = ""
    for i in text:
        func = (alphOrder[i] * a + b) % 26
        result += getKey(func,alphOrder)
    return result

def decryptAffineCipher(text, a, b):
    alphaOrder = orderingAlpha()
    result = ""
    for i in text:
        func = (pow(a,-1,26) * (alphaOrder[i] - b)) % 26
        result += getKey(func,alphaOrder)
    return result
#additional function to order alph from 0 to 25
def orderingAlpha():
    alphOrder = {}
    orderOfChar = ord("a")
    for i in range(26):
        alphOrder[chr(orderOfChar)] = i
        orderOfChar += 1    
    return alphOrder

# ----------------------Caesar Cipher----------------------
def encryptCaesarCipher(text, key1, key2):
        #low case chars
    lowerChars = {}
    count = 0
    for i in range (ord("a"), ord("z") + 1):
        lowerChars[chr(i)] = count
        count += 1

    #upper case chars
    count = 0
    upperChars = {}
    for i in range (ord("A"), ord("Z") + 1):
        upperChars[chr(i)] = count
        count += 1

    #code
    digitInText = 0
    result = ""
    loop = 0
    numb = 0
    for i in text:
        if(loop % 2 == 0):
            x = key1
        else:
            x = key2
        if(i.isalpha()):
            if(i.islower()):
                if(lowerChars[i] + x > 25):
                    numb = (lowerChars[i] + x) % 26
                    result += getKey(numb,lowerChars)
                else:
                    result += getKey(lowerChars[i] + x,lowerChars)
            elif(i.isupper()):
                if(upperChars[i] + x > 25):
                    numb = (upperChars[i] + x) % 26
                    result += getKey(numb,upperChars)
                else:
                    result += getKey(upperChars[i] + x,upperChars)
        elif(i.isdigit()):
            if(int(i) + x > 9):
                    digitInText = (int(i) + x) % 10
                    result += str(digitInText)
            else:   
                    result += str(int(i) + x) 
        else:
            result += i
        loop += 1
    return  result    



    
def decryptCaesarCipher(text, key1, key2):
    #low case chars
    lowerChars = {}
    count = 0
    for i in range (ord("a"), ord("z") + 1):
        lowerChars[chr(i)] = count
        count += 1

    #upper case chars
    count = 0
    upperChars = {}
    for i in range (ord("A"), ord("Z") + 1):
        upperChars[chr(i)] = count
        count += 1

    #code
    digitInText = 0
    result = ""
    loop = 0
    numb = 0
    for i in text:
        if(loop % 2 == 0):
            x = key1
        else:
            x = key2
        if(i.isalpha()):
            if(i.islower()):
                if(lowerChars[i] - x < 0):
                    numb = (lowerChars[i] - x) % 26
                    result += getKey(numb,lowerChars)
                else:
                    result += getKey(lowerChars[i] - x,lowerChars)
            elif(i.isupper()):
                if(upperChars[i] - x < 0):
                    numb = (upperChars[i] - x) % 26
                    result += getKey(numb,upperChars)
                else:
                    result += getKey(upperChars[i] - x,upperChars)
        elif(i.isdigit()):
            if(int(i) - x < 0):
                    digitInText = (int(i) - x) % 10
                    result += str(digitInText)
            else:   
                    result += str(int(i) - x) 
        else:
            result += i
        loop += 1
    return  result  

# ----------------------Transposition Cipher----------------------
def encryptTranspositionCipher(text, key):
    arrayOfStrings = []
    for i in range(0,len(text),key):
        to = i + key
        arrayOfStrings.append(text[i:to])
    
    
    transformedStrings = []
    count = 0
    string = ""
    for k in range(key):
        for i in arrayOfStrings:
            if(count < len(i)):
                string += i[count]
        transformedStrings.append(string)
        string = ""        
        count += 1
    
    result = ""

    for strings in transformedStrings:
        result += strings
    return result



def decryptTranspositionCipher(text, key):

    
    if(len(text) % key == 0):
        jumping = int(len(text) / key)
        string = ""
        for j in range(jumping):
            for i in range(j,len(text),jumping):
                string += text[i]
        
        return string

  
    # this logic almost ended me :)) ->>

    lenOfSubstring = int(len(text)/key) + 1
    repeat = int(len(text)%key)
    initialValueOfDiv = int(len(text)/key)
    lengthOfText = len(text)

    string = []
    count = 0
    while True:
        if(len("".join(string)) == lengthOfText):
            break
        if(repeat != 0):
            string.append(text[count:lenOfSubstring])
            if(repeat == 1):
                count = lenOfSubstring
                z = count + initialValueOfDiv
            else:
                count = lenOfSubstring
            lenOfSubstring += initialValueOfDiv + 1
            repeat -= 1          
          
        else:
            
            string.append(text[count:z])
            count = z
            z += initialValueOfDiv
    
    result = ""
    ar = []    
    for k in range(len(string[0])):
        for i in string:
            if(k < len(i)):
                result += i[k]
        ar.append(result)
        result = ""
    
    return "".join(ar)

#--------------------END--------------------
