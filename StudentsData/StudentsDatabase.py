
def addStudentInData():
    file = open("Student_data.txt","a")

    while True:
        userIput = input("input : ")
        if(userIput == "save"):
            break

        arr = userIput.split(" ")
    
        if(arr[2] != "A" and arr[2] != "B" and arr[2] != "C"):
            print("wrong Input")
            continue
        grade = int(arr[3])
        if(grade > 10 or grade < 0):
            print("wrong Input")
            continue
        grade = int(arr[4])
        if(grade > 10 or grade < 0):
            print("wrong Input")
            continue
        grade = int(arr[5])
        if(grade > 10 or grade < 0):
            print("wrong Input")
            continue
        joinedArr = "/".join(arr)
        file.write(joinedArr + "\n")
    file.close


def studentsAvarageScore(name,surname):
    file = open("Student_data.txt","r")
    Students = file.readlines()
    file.close()
    for i in Students:
        var = i.split("/")
        if (name == var[0] and surname == var[1]):
            return (int(var[3]) + int(var[4]) + int(var[5]) ) / 3
    return "Student doesnt Exsists"

def avarageByClass(clas):
    file = open("Student_data.txt","r")
    Students = file.readlines()
    studGrades = []
    file.close()
    for i in Students:
        var = i.split("/")
        if(var[2] == clas):
            studGrades.append(int(var[3]))
            studGrades.append(int(var[5]))
            studGrades.append(int(var[4]))
    points = 0
    for i in studGrades:
        points += i
    return points / len(studGrades)

def topStudent():
    file = open("Student_data.txt","r")
    students = file.readlines()
    file.close()
    topStudent = ""
    for i in students:
        for k in students:
            stud1 = i.split("/")
            stud2 = k.split("/")
            if(studentsAvarageScore(stud1[0],stud1[1]) > studentsAvarageScore(stud2[0],stud2[1])):
                topStudent = stud1[0] + " " + stud1[1]
            
    return topStudent

def printData():
    file = open("Student_data.txt","r")
    students = file.readlines()
    file.close()
    print("Name/Surname/Class/GradeinEnglish/GradeInMath/GradeInScience\n")
    for i in students:
        print(i,end="")