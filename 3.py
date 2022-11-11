def skobochki(string):
    counter = 0
    for i in string:
        if i == '(':
            counter+=1
        elif i == ')':
            counter-=1
            if counter == -1:
                return False
        else:
            return False
    if counter == 0:
        return True
    else:
        return False


def tests():
    assert skobochki('()(())()((()()))') == True
    assert skobochki(')()()()()()())') == False
    assert skobochki(288) == False
    assert skobochki('()()()d') == False

    # Можете дописать свои тесты


if __name__ == "__main__":
    tests()
    print("Everything passed")