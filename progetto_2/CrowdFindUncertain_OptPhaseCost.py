from random import randint

question = "nella foto c'è un gatto?"
cont_phase = 0
cont_answer = 0
m = 4
ALFA = 0
ERROR_RATE = 0.2
roundRobinIndex = 0
percentage = 0.15
userPenalityMap = {"mario": 0, "valerio": 0, "emanuele": 0, "danilo": 0, "claudio": 0, "stefania": 0, "antonella": 0}
userList = list(["mario", "valerio", "emanuele", "danilo", "claudio", "stefania", "antonella"])


def crowdSourcingSystem(CQ):
    global roundRobinIndex
    global cont_answer

    photoUserAnswer = {}  # key: photo value: list of tuple (user,answer)
    userErrorRateMap = {"mario": ERROR_RATE, "valerio": ERROR_RATE, "emanuele": ERROR_RATE, "danilo": ERROR_RATE,
                        "claudio": ERROR_RATE, "stefania": ERROR_RATE, "antonella": ERROR_RATE}
    photoAnswers = {}
    i = 0
    while (i < len(CQ)):
        user = userList[roundRobinIndex]
        if (photoUserAnswer.get(CQ[i][0]) == None):
            photoUserAnswer[CQ[i][0]] = list()
        elemListForEachUser = photoUserAnswer[CQ[i][0]]
        if (photoAnswers.get(CQ[i][0]) == None):
            photoAnswers[CQ[i][0]] = (0, 0)
        answers = photoAnswers[CQ[i][0]]

        # answer = input(CQ[i][1])
        answer = calculateAutoAnswer(CQ[i][0].bool, user, userErrorRateMap)
        cont_answer += 1

        if answer.lower() == "si" or answer.lower() == "yes":
            updatedAnswers = (answers[0] + 1, answers[1])
            photoAnswers[CQ[i][0]] = updatedAnswers
            elemListForEachUser.append((user, "yes"))
            i += 1
            roundRobinIndex = (roundRobinIndex + 1) % len(userList)

        elif answer.lower() == "no":
            updatedAnswers = (answers[0], answers[1] + 1)
            photoAnswers[CQ[i][0]] = updatedAnswers
            elemListForEachUser.append((user, "no"))
            i += 1
            roundRobinIndex = (roundRobinIndex + 1) % len(userList)

        else:
            print("Risposta non valida")
    CQ.clear()
    photoTupleListUser = evaluateSpammers(photoUserAnswer)
    applyPenalityAndRewards(photoTupleListUser)

    return photoAnswers


def calculateAutoAnswer(bool, user, userErrorRateMap):
    answer = randint(1, 100) / 100

    if (answer <= (1 - userErrorRateMap[user])):

        if (bool == 1):
            return "yes"
        else:
            return "no"

    else:
        if (bool == 1):
            return "no"
        else:
            return "yes"


def applyPenalityAndRewards(photoTupleListUser):
    global roundRobinIndex

    for tupleUsersRewardsPenality in photoTupleListUser:

        if (len(tupleUsersRewardsPenality[0]) > 0):

            for goodUser in tupleUsersRewardsPenality[0]:
                if (userPenalityMap.get(goodUser) != None):

                    if (userPenalityMap[goodUser] > 0):
                        userPenalityMap[goodUser] = userPenalityMap[goodUser] - 0.5

        if (len(tupleUsersRewardsPenality[1]) > 0):

            for badUser in tupleUsersRewardsPenality[1]:
                if (userPenalityMap.get(badUser) != None):
                    userPenalityMap[badUser] = userPenalityMap[badUser] + 1
                    if (userPenalityMap[badUser] >= 5.5):
                        userPenalityMap.pop(badUser)
                        userList.remove(badUser)
                        print("--------------BANNED------------:" + badUser)
                        if (roundRobinIndex > 0):
                            roundRobinIndex -= 1


def evaluateSpammers(photoUserAnswer):
    photoTupleListUser = list()
    threshold = 0.8
    list_1 = list()
    list_2 = list()
    tupleListUser = (list_1, list_2)

    for key in photoUserAnswer.keys():
        numNoAnswer = 0
        numYesAnswer = 0

        userAnswerList = photoUserAnswer[key]
        for elem in userAnswerList:

            if (elem[1] == "yes" or elem[1] == "si"):
                numYesAnswer += 1
            else:
                numNoAnswer += 1

        if (numNoAnswer == 0 and numYesAnswer == 0):
            percentualNo = 0
            percentualYes = 0

        else:
            percentualYes = numYesAnswer / (numYesAnswer + numNoAnswer)
            percentualNo = numNoAnswer / (numYesAnswer + numNoAnswer)

        if (percentualNo >= threshold):
            tupleListUser = searchUser("no", userAnswerList)
            photoTupleListUser.append(tupleListUser)

        if (percentualYes >= threshold):
            tupleListUser = searchUser("yes", userAnswerList)
            photoTupleListUser.append(tupleListUser)

    return photoTupleListUser


def searchUser(answer, userAnswerList):
    listUserToApplyPenality = list()
    listUserToApplyReward = list()

    # for key in userAnswerList.keys():
    #     userAnswer = userAnswerList[key]
    for elem in userAnswerList:
        if (elem[1] == answer):
            listUserToApplyReward.append(elem[0])
        else:
            listUserToApplyPenality.append(elem[0])

    # una delle due potrebbe essere vuota. è il caso di tutte risposte affermative o negativa con consenso unanime.

    return (listUserToApplyReward, listUserToApplyPenality)




def unc_opt_cost_algorithm(Items, K1):

    global ALFA
    global cont_phase
    ALFA = m / 2
    founds = list()
    itemsToTest = Items[:]
    total_answers = {}
    for x in range(len(Items)):
        total_answers[Items[x]] = (0, 0)
    pointCostMap = {}
    ComputeYForEachPoint(pointCostMap)

    if (m > 1):
        while (not RightValueALFA(pointCostMap)):
            ComputeYForEachPoint(pointCostMap)

    while len(founds) < K1:

        if (len(itemsToTest) < (K1 - len(founds))):
            break
        cont_phase += 1
        ItemsLowestCost = getLowestCostItems(K1 - len(founds), total_answers, pointCostMap, itemsToTest)
        CQ = list()
        for item in ItemsLowestCost:
            fewestYes = fewestYesQuestionsToZero(item, total_answers)
            fewestNo = fewestNoQuestionsToAlfa(item, total_answers)

            for x in range(min(fewestYes, fewestNo)):
                CQ.append((item, question))
        partial_answers = crowdSourcingSystem(CQ)
        updateAnswers(partial_answers, total_answers)
        for item in ItemsLowestCost:
            rectangularStrategy(total_answers[item], item, itemsToTest, founds)

    elemTruePositives = searchInFounds(founds)

    print("numero di domande chieste: " + str(cont_answer))
    print("numero di fasi computate: " + str(cont_phase))
    print("numero di domande per fase: " + str(cont_answer / cont_phase))
    print("precision: " + str(elemTruePositives / K1))
    print("\n\n")

    return elemTruePositives / K1


def searchInFounds(L):
    elemTruePositives = 0

    for elem in L:

        if (elem.bool == 1):
            elemTruePositives += 1

    return elemTruePositives


def rectangularStrategy(answers, item, itemsToTest, founds):
    if answers[0] == m - 1:

        itemsToTest.remove(item)
        founds.append(item)

    elif (answers[1] == m - 1):

        itemsToTest.remove(item)


class Photo:

    def __init__(self, objectsInPhoto, bool):
        self.objectsInPhoto = objectsInPhoto  # instance variable unique to each instance
        self.bool = bool




def getLowestCostItems(elemLeft, total_answers, pointCostMap, itemsToTest):
    copyItemsToTest = itemsToTest[:]

    listElemMinCost = list()

    while (elemLeft > 0):

        minCost = pointCostMap[total_answers[copyItemsToTest[0]]]
        elemMinCost = copyItemsToTest[0]

        for elem in copyItemsToTest:

            if (pointCostMap[total_answers[elem]] < minCost):
                minCost = pointCostMap[total_answers[elem]]
                elemMinCost = elem

        listElemMinCost.append(elemMinCost)
        copyItemsToTest.remove(elemMinCost)
        elemLeft -= 1

    return listElemMinCost


def RightValueALFA(pointCostMap):
    valueConfront = p1(0, 0) * pointCostMap[1, 0] + p0(0, 0) * pointCostMap[0, 1] + 1
    global ALFA

    if (abs(ALFA - valueConfront) < 0.2):
        return True

    elif (ALFA - valueConfront >= 0.2):
        ALFA = ALFA - (ALFA / 2)

    else:
        ALFA = ALFA + (ALFA / 2)

    return False


def ComputeYForEachPoint(pointCostMap):
    for n1 in range(m):
        for n2 in range(m):
            pointCostMap[n1, n2] = Y(n1, n2, pointCostMap)


def Pr3(bool, n1, n2):
    if (bool == 1):
        return pow((1 - ERROR_RATE), n1) * pow(ERROR_RATE, n2)
    else:
        return pow(ERROR_RATE, n1) * pow((1 - ERROR_RATE), n2)


def Pr2(answer, bool):
    if ((answer == 'YES' and bool == 1) or (answer == 'NO' and bool == 0)):
        return (1 - ERROR_RATE)
    else:
        return ERROR_RATE


def p1(n1, n2):
    return (Pr3(1, n1, n2) * Pr2('YES', 1)) + (Pr3(0, n1, n2) * Pr2('YES', 0))


def p0(n1, n2):
    return (Pr3(1, n1, n2) * Pr2('NO', 1)) + (Pr3(0, n1, n2) * Pr2('NO', 0))


def Y(n1, n2, pointCostMap):
    if (n1 == 0 and n2 == 0):
        return ALFA

    elif (n1 != m - 1 and n2 != m - 1):

        return min(ALFA, ((p1(n1, n2) * Y(n1 + 1, n2, pointCostMap)) + (p0(n1, n2) * Y(n1, n2 + 1, pointCostMap)) + 1))

    elif (n1 == m - 1):
        return 0
    else:
        return ALFA


def updateAnswers(partial_answers, total_answers):
    for object in partial_answers.keys():
        new_answers = partial_answers.get(object)
        prev_answers = total_answers.get(object)
        updated_answers = (new_answers[0] + prev_answers[0], new_answers[1] + prev_answers[1])
        total_answers[object] = updated_answers


def fewestNoQuestionsToAlfa(item, total_answers):
    return m - 1 - total_answers[item][1]


def fewestYesQuestionsToZero(item, total_answers):
    return m - 1 - total_answers[item][0]


def databaseItems():
    photoList = list()

    for i in range(10000):

        x = randint(1, 100) / 100

        if (x <= percentage):

            photoList.append(Photo("foto dove c'è un gatto", 1))
        else:
            photoList.append(Photo("foto dove NON c'è un gatto", 0))

    return photoList


def main():
    photoList = databaseItems()

    global cont_phase
    global cont_answer
    global userPenalityMap
    global userList
    answer = 0
    phase = 0
    answerPhase = 0
    precision = 0

    for i in range(10):
        cont_answer = 0
        cont_phase = 0
        userPenalityMap = {"mario": 0, "valerio": 0, "emanuele": 0, "danilo": 0, "claudio": 0, "stefania": 0,
                           "antonella": 0}
        userList = list(["mario", "valerio", "emanuele", "danilo", "claudio", "stefania", "antonella"])

        precision += unc_opt_cost_algorithm(photoList, 300)
        answer += cont_answer
        phase += cont_phase
        answerPhase += cont_answer / cont_phase

    print("AVERAGES\n\n")

    print("answer: " + str(answer / 10))
    print("phase: " + str(phase / 10))
    print("answer/phase: " + str(answerPhase / 10))
    print("precision: " + str(precision / 10))


if __name__ == '__main__':
    main()




