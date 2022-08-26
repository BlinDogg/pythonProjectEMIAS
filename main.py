import pandas as pd
#import os
from io import BytesIO
import numpy
#from datetime import datetime,date
from pandas.io.excel import ExcelWriter
# Сброс ограничений на количество выводимых рядов
pd.set_option('display.max_rows', None)
# Сброс ограничений на число столбцов
pd.set_option('display.max_columns', None)
# Сброс ограничений на количество символов в записи
pd.set_option('display.max_colwidth', None)

stop_slova = ('бактериальные', 'пневмонии', 'мягкие ткани', 'мочевыводящие пути', 'other', 'вирусные', \
                      'H. zoster', 'H. simplex', 'грибковые (итого)', 'смешанные', 'бронхит', 'синусит', \
                      'стоматит', 'up resp tr inf', 'FUO', 'COVID', 'N больных', 'СУММА посещений', 'ИТОГО посещений', \
                  'стоматит/периодонтит')

l1 = 0
l2 = 0
l3 = 0


#Функция открывает экселевский файл. В планах добавить парсер по папке с программой для
#сбора данных со всех файлов
def opener():
    df = pd.read_excel('33_33_33_infectionsfromMoscow_20082021.xlsx', sheet_name='исходник по ЕМИАС')
    return df


#Данная функция очищает программу от "бесполезных" строк. Их можно увидеть ниже
def cleaner():
    df = opener()
    a = list()
    p=0
    for i in df['ФИО']:

        for j in stop_slova:
            if i == j:
                a.append(p)
        p = p + 1
    for x in reversed(a):

        df = df.drop(index=x)
    fd = pd.notnull(df['ФИО'])
    df = df[fd]
    df = df.reset_index(drop=True)




    return df


#Подсчитывает итоговое количество больных
def stroki():
    pacienti = len(cleaner().index)
    global l1
    l1 = pacienti
    return pacienti

#Функция формирует 1ую таблицу по ТЗ
def Part1():
    df1 = cleaner().iloc[0:stroki(), 0:26]
    return df1


#Значения, с которыми работаем в т2 и т3
def znach():
    df2 = cleaner().iloc[0:l1, 26:len(cleaner().columns)]
    #d = pd.concat([df2, df3], axis=1)
    return df2


#Имена всех больных
def names():
    df3 = cleaner().iloc[0:l1, 0]
    return df3


#Возвращает словарь [название месяца:Его индекс]
def dateS():
    zn = znach()
    a = 0
    ind_mes = {}
    for i in zn:
        if a == 0 or a%18==0:
            z={a:i}
            ind_mes.update(z)
        a = a+1
    #print(ind_mes)
    return ind_mes


#Этот код собирает данные для 2ой таблице в формате списка
def pre_part2():
    a = dateS()
    joba = a.keys()
    o = znach()
    u = names()
    for_tabl = list()
    #print(u)
    for i in joba:

        b = i+8
        try:
            df = o.iloc[0:l1, b]
        except:
            break
        z=0
        for g in df:
            if pd.notnull(g):
                week = a.get(i)                     #код недели
                j,k,l = week.split(' ')             #j - номер недели, k - название месяца, l - год
                ill = g                             #название болезни
                imya = u[z]                         #имя больного
                nach = o.iloc[z, b+1]               #дата начала болезни
                kon = o.iloc[z, b+2]                #дата окончания болезни
                hard = o.iloc[z, b+4]
                n=b+27
                excel_col_name = lambda n: '' if n <= 0 else excel_col_name((n - 1) // 26) + chr(
                    (n - 1) % 26 + ord('A'))
                if z<50:
                    st=z+2
                elif z<102:
                    st=z+19+2
                elif z<145:
                    st=z+38+2
                else:
                    st=z+57+2
                Kod = str(excel_col_name(n))+'-'+str(st)             #код из основной бд
                if pd.isnull(nach):
                    nach = 'Не указал(а)'
                if pd.isnull(kon):
                    kon = 'Не указал(а)'
                pre=(week, imya, ill, nach, kon, hard, Kod, j, k, l)
                for_tabl.append(pre)

                z = z + 1
            else:
                z=z+1

    return for_tabl


#Преобразует список в фрейм и передаёт на запись в tabl2
def Part2():
    df2 = pd.DataFrame(pre_part2())
    global l2
    l2 = len(pre_part2())

    return df2


#Этот код собирает данные для 3ей таблице в формате списка
def pre_part3():
    a = dateS()
    joba=a.keys()
    o = znach()
    u = names()
    for_tabl = list()
    qw = stroki()
    # print(u)
    for i in joba:
        b = i + 13

        df = o.iloc[0:qw, b:b+6]
        df1 = pd.concat([u, df], axis=1)
        df1 = df1.dropna(thresh = 2)
        df1 = df1.reset_index(drop=True)
        counter = len(df1)
        x = 0
        while x < counter:
            lis = df1.iloc[x].tolist()
            week = a.get(i)
            j, k, l = week.split(' ')       # j - номер недели, k - название месяца, l - год
            w = [j, k, l]
            lis.insert(0, week)
            lis = lis+w
            for_tabl.append(lis)
            x = x+1
    return for_tabl


#Преобразует список в фрейм и передаёт на запись в tabl2
def Part3():
    df3 = pd.DataFrame(pre_part3())
    global l3
    l3 = len(pre_part3())
    return df3


#Функция записывает данные таблицы в новый экселевский файл
def tabl():
    bb = BytesIO()
    bb.name = f'test.xlsx'
    bb.encoding = "utf-8"
    df1 = Part1()
    df2 = Part2()  # Тут надо вставить итоговую таблицу 2
    df2 = df2.rename(columns={0: 'Неделя', 1: 'ФИО', 2: 'Инфекция', 3: 'Дата начала инфекции', 4: 'Дата окончания инфекции',\
                              5: 'Тяжесть инфекции', 6: 'Код ячейки из БД',7:'Номер недели', 8: 'Название месяца', 9:'Год'})
    df3 = Part3()               # Тут надо вставить итоговую таблицу 3
    df3 = df3.rename(columns={0: 'Неделя', 1: 'ФИО', 2: 'Кол-во эпизодов посещения амбулаторно',\
                              3: 'Кол-во эпизодов посещения стационарно', 4: 'Кол-во дней посещения амбулаторно w1',\
                              5: 'Кол-во дней посещения стационарно', 6:'костыль', 7: 'Доза основного препарата',\
                              8:'Номер недели', 9: 'Название месяца', 10:'Год'})
    df3 = df3.drop('костыль', axis=1)
    df3 = df3.reset_index(drop=True)

    with ExcelWriter(bb) as writer:
        df1.sample(l1, replace=False).to_excel(writer, sheet_name="Лист 1", index=False)
        df2.sample(l2, replace=False).to_excel(writer, sheet_name="Лист 2", index=False)
        df3.sample(l3, replace=False).to_excel(writer, sheet_name="Лист 3", index=False)

    with open(bb.name, 'wb') as f:
        f.write(bb.getbuffer())


tabl()


