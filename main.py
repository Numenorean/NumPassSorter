from tqdm import tqdm
import subprocess
import ctypes
import datetime
import config
import time
import sys
import re
import os

ALL_RUSSIA_CODES = [z for i in config.RUSSIA.values() for z in i]
ALL_UKRAINE_CODES = [z for i in config.UKRAINE.values() for z in i]
ALL_KAZAKHSTAN_CODES = [z for i in config.KAZAKHSTAN.values() for z in i]

class Sorter:
    def __init__(self, comboPath):
        now = datetime.datetime.now()
        self.comboPath = comboPath
        self.COUNTRY_CODES = tuple(config.COUNTRY_CODES.values())
        self.time = now.time().strftime('%H_%M_%S')
        self.date = now.date().strftime('%d.%m.%y')
        self.ts_start = time.time()
    
    def normalizeCombo(self, combo):
        combo = combo.replace(';', ':').split(':')
        phone = combo[0]
        phone = ''.join([char for char in phone if char.isdigit()])
        if phone.startswith(self.COUNTRY_CODES) and len(phone) > 10:
            return phone+':'+combo[1]
        else:
            country = self.notFullNumber2Country(phone)
            if country == 'UNNKNOWN':
                return 'UNNKNOWN'
            return config.COUNTRY_CODES[country]+phone+':'+combo[1]
                
    def notFullNumber2Country(self, phone):
        code = phone[:3]
        if code in ALL_RUSSIA_CODES:
            return 'RUSSIA'
        elif code in ALL_UKRAINE_CODES:
            return 'UKRAINE'
        elif code in ALL_KAZAKHSTAN_CODES:
            return 'KAZAKHSTAN'
        else:
            return 'UNNKNOWN'
    
    def getInfoByPhone(self, phone):
        if phone.startswith('79'):
            country = 'RUSSIA'
            code = phone[1:4]
            result = ['RUSSIA', []]
            for operator in config.RUSSIA:
                if code in config.RUSSIA[operator]:
                    result[1].append(operator)
            return result
        elif phone.startswith('38'):
            country = 'UKRAINE'
            code = phone[2:5]
            for operator in config.UKRAINE:
                if code in config.UKRAINE[operator]:
                    return [country, operator]
        elif phone.startswith('77'):
            country = 'KAZAKHSTAN'
            code = phone[1:4]
            result = ['KAZAKHSTAN', []]
            for operator in config.KAZAKHSTAN:
                if code in config.KAZAKHSTAN[operator]:
                    result[1].append(operator)
            return result

    def removeEmptyFiles(self, path):
        for root, dirs, files in os.walk(path):
            for f in files:
                fullname = os.path.join(root, f)
                try:
                    if os.path.getsize(fullname) == 0:
                        print('Удаляю %s' % fullname)
                        os.remove(fullname)
                except WindowsError:
                    continue
        for root, dirs, files in os.walk(path):
            if not files and not dirs:
                os.rmdir(root)
            
            
    
    def sort(self):
        path = f'Результаты\\{self.date}\\{self.time}'
        os.makedirs(f'Результаты\\{self.date}\\{self.time}')

        os.mkdir(path+'\\Украина')
        kyivstar = open(path + '\\Украина\\Киевстар.txt', 'w')
        vodafone = open(path + '\\Украина\\Водафон.txt', 'w')
        lifecell = open(path + '\\Украина\\Лайфселл.txt', 'w')
        threemob = open(path + '\\Украина\\3моб.txt', 'w')
        peoplenet = open(path + '\\Украина\\PEOPLEnet.txt', 'w')
        ukrtelecom = open(path + '\\Украина\\Укртелеком.txt', 'w')
        all_ua = open(path + '\\Украина\\Все.txt', 'w')

        os.mkdir(path+'\\Россия')
        beeline = open(path + '\\Россия\\Билайн.txt', 'w')
        tele2 = open(path + '\\Россия\\Теле2.txt', 'w')
        megafon = open(path + '\\Россия\\Мегафон.txt', 'w')
        mts = open(path + '\\Россия\\МТС.txt', 'w')
        yota = open(path + '\\Россия\\Йота.txt', 'w')
        all_ru = open(path + '\\Россия\\Все.txt', 'w')

        os.mkdir(path+'\\Казахстан')
        aktiv = open(path + '\\Казахстан\\Актив.txt', 'w')
        beeline_kz = open(path + '\\Казахстан\\Билайн.txt', 'w')
        ksell = open(path + '\\Казахстан\\Кселл.txt', 'w')
        tele2_kz = open(path + '\\Казахстан\\Теле2.txt', 'w')
        all_kz = open(path + '\\Казахстан\\Все.txt', 'w')


        unnknown = open(path+'\\Неизвестные.txt', 'w')

        files = [kyivstar, vodafone, lifecell, threemob, peoplenet, ukrtelecom, all_ua, beeline, tele2, megafon, mts, yota, all_ru, aktiv, beeline_kz, ksell, tele2_kz, all_kz, unnknown]
        print('Получаю количество строк в файле...')
        num_lines = sum(1 for line in open(self.comboPath, encoding='utf-8'))
        print('Загружено %s строк\nСортировка...' % num_lines)

        with open(self.comboPath, 'r', errors='ignore') as f2:
            for combo in tqdm(f2, total=num_lines):
                combo_2 = combo
                combo = self.normalizeCombo(combo)
                phone = combo.split(':')[0]
                info = self.getInfoByPhone(phone)
                if not info:
                    unnknown.write(combo_2)
                elif info[0] == 'UKRAINE':
                    if info[1] == 'Киевстар':
                        kyivstar.write(combo)
                    if info[1] == 'Водафон':
                        vodafone.write(combo)
                    if info[1] == 'Лайфселл':
                        lifecell.write(combo)
                    if info[1] == 'ТриМоб':
                        threemob.write(combo)
                    if info[1] == 'PEOPLEnet':
                        peoplenet.write(combo)
                    if info[1] == 'Укртелеком':
                        ukrtelecom.write(combo)
                    all_ua.write(combo)
                elif info[0] == 'RUSSIA':
                    if 'Билайн' in info[1]:
                        beeline.write(combo)
                    if 'Теле2' in info[1]:
                        tele2.write(combo)
                    if 'Мегафон' in info[1]:
                        megafon.write(combo)
                    if 'МТС' in info[1]:
                        mts.write(combo)
                    if 'Йота' in info[1]:
                        yota.write(combo)
                    all_ru.write(combo)
                elif info[0] == 'RUSSIA':
                    if 'Билайн' in info[1]:
                        beeline.write(combo)
                    if 'Теле2' in info[1]:
                        tele2.write(combo)
                    if 'Мегафон' in info[1]:
                        megafon.write(combo)
                    if 'МТС' in info[1]:
                        mts.write(combo)
                    if 'Йота' in info[1]:
                        yota.write(combo)
                    all_ru.write(combo)
                elif info[0] == 'KAZAKHSTAN':
                    if 'Билайн' in info[1]:
                        beeline_kz.write(combo)
                    if 'Актив' in info[1]:
                        aktiv.write(combo)
                    if 'Кселл' in info[1]:
                        ksell.write(combo)
                    if 'Теле2' in info[1]:
                        tele2_kz.write(combo)
                    all_kz.write(combo)
                #if d % n == 0:
                 #   ctypes.windll.kernel32.SetConsoleTitleW('Checked: %s\\%s' % (d, num_lines))
        #final_time = time.time()-self.ts_start
        #input('Потрачено времени: %s' % datetime.datetime.utcfromtimestamp(final_time).strftime("%H:%M:%S.%f"))
        print('Удаляю пустые файлы...')
        for file in files:
            file.close()
        self.removeEmptyFiles(os.path.abspath(path))
        subprocess.Popen('explorer "%s"' % path)
        input()       





if __name__ == '__main__':
    if len(sys.argv) > 1:
        Sorter(sys.argv[1]).sort()
    else:
        Sorter(input('Перетащите базу: ').replace('"', '')).sort()
