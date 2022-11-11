# n = int(input())
#
# excel_col_name = lambda n: '' if n <= 0 else excel_col_name((n - 1) // 26) + chr((n - 1) % 26 + ord('A'))
#
# print(excel_col_name(n))
def func(x):
    return  x<1

lst = [-4,-2,0,2,4]
res = filter(func, lst)

print(list(res))