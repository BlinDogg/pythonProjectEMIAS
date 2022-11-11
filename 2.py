def sqrt_(num):
    root = int(num/2)
    counter_max = root
    counter = 0
    while counter < counter_max:
        if root*root == num:
            return int(root)
        elif root*root > num:
            counter +=1
            root = int(root/2)
        elif root*root < num:
            counter += 1
            root += 1


def tests():
    assert sqrt_(96314596) == 9814
    assert sqrt_(961333186576) == 980476
    assert sqrt_(64) == 8
    assert sqrt_(3) == None
    assert sqrt_(-16) == None

    #Можете дописать свои тесты



if __name__ == "__main__":
    tests()
    print("Everything passed")