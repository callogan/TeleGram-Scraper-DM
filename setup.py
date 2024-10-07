#!/bin/env python3

"""

you can re run setup.py
if you have added some wrong value

"""
import pandas as pd

re = "\033[1;31m"
gr = "\033[1;32m"
cy = "\033[1;36m"
lb = "\033[1;34m"
wh = "\033[1;37m"

import os
import sys
import time


#######################################################################################################################
def shutdown():
    print("\nIf you want to proceed, input in the shell: ", lb + "python setup.py")
def config_setup():  # setting up configuration function
    import configparser
    banner()
    cpass = configparser.RawConfigParser()
    cpass.add_section('cred')
    xid = input(gr + "[+] input api ID :  " + re)
    cpass.set('cred', 'id', xid)
    xhash = input(gr + "[+] input hash ID : " + re)
    cpass.set('cred', 'hash', xhash)
    xphone = input(gr + "[+] input the phone number : " + re)
    cpass.set('cred', 'phone', xphone)
    setup = open('config.data', 'w')
    cpass.write(setup)
    setup.close()
    print(gr + "[+] settings are saved !")

def requirements():  # setting up libraries cython, numpy, pandas
    def csv_lib():
        banner()
        print(gr + '[' + cy + '+' + gr + ']' + cy + 'Loading...')
        os.system("""
			pip3 install cython numpy pandas
			python3 -m pip install cython numpy pandas
			""")

    banner()  # показ баннера
    print(gr + '[' + cy + '+' + gr + ']' + cy + 'setting up csv merge will take up to 10 minutes.')
    input_csv = input(gr + '[' + cy + '+' + gr + ']' + cy + 'You wanto to use the function '
                                                            '"join tables" (y/n)): ').lower()
    if input_csv == "y":
        csv_lib()
    else:
        pass
    print(gr + "[+] Setting up modules...")
    os.system("""
		pip3 install telethon requests configparser
		python3 -m pip install telethon requests configparser
		touch config.data
		""")

    print(gr + "[+] Setting up has been completed.\n")

def merge_csv():  # the function to merge csv
    import pandas as pd           # module loading
    banner()                       # displaying of the banner
    f1 = input("Input file names via whitespace (file1.csv file2.csv) ").split()
    df1, df2 = pd.read_csv(f1[0]), pd.read_csv(f1[1])
    merge = pd.concat([df1,df2])
    merge = merge.drop_duplicates()
    #merge = df1.merge(df2, on='username')
    merge.to_csv("output.csv", index=False)
    print(gr + '[' + cy + '+' + gr + ']' + cy + 'joining' + f1[0] + ' & ' + f1[1] + ' ...')
    print(gr + '[' + cy + '+' + gr + ']' + cy + 'processing big files might take awhile ... ')
    print(gr + '[' + cy + '+' + gr + ']' + cy + 'the file is saved "output.csv" \n')


#######################################################################################################################
def banner():
    print(f"""
	{re}╔═╗{cy}┌─┐┌┬┐┬ ┬┌─┐
	{re}╚═╗{cy}├┤  │ │ │├─┘
	{re}╚═╝{cy}└─┘ ┴ └─┘┴
	""")


banner()
print("1. Standard setting up (recommended) \n"
    "2. Setting up the configuration of api\n"
	"3. Setting up libraries \n"
	"4. Join 2 files .csv in one\n"
	"5. Update the app to latest version\n"
	"6. Help")
cm = int(input(gr +"Choose the number and push Enter: "))
if cm == 1: requirements(), config_setup(), shutdown()
elif cm == 2: config_setup(), shutdown()
elif cm == 3: requirements(), shutdown()
elif cm ==6: print(wh + " Standard setting up (recommended) - full setting up all the necessary configuration\n"
						"Setting up the configuration of api - linking the Telegram account (via SMS code)\n"
						"Setting up libraries - setting up all the suggested libraries is recommended"
						"\nJoin 2 files .csv in one - 2 lists will be joined, with removing duplicates"
						"\nupdate the app to latest version - updating of the software."), shutdown()
elif cm == 4: merge_csv(), shutdown()


