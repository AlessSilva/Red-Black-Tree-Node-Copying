import argparse
from RBT_functions import *
import myglobal

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--file", required=True, help="path to input file")
ap.add_argument("-t", "--tree", required=False, help="0 to not show the tree and 1 to show the tree", default=0, type=int)
args = vars(ap.parse_args())


if __name__ == "__main__":

    myglobal.init()

    file1 = open( args["file"] , 'r')
    file2 = open('output.txt', 'w')
    L = []
    lzinho = ""
    display_on = args["tree"]

    for line in file1:
    
        command = line.strip().split(" ")

        if command[0] == "INC":
            Insert( int(command[1]) )
            
            if display_on == 1:
              lines_dysplay = DisplayTree( myglobal.current )
              print(f'INC {command[1]}')
              for l in lines_dysplay:
                 print(l)

        elif command[0] == "REM":
            Remove( int(command[1]) )

            if display_on == 1:
              lines_dysplay = DisplayTree( myglobal.current )
              print(f'REM {command[1]}')
              for l in lines_dysplay:
                 print(l)


        elif command[0] == "SUC":

            version = int(command[2])

            if version > myglobal.current:
                version = myglobal.current

            suc = Successor( int(command[1]), version )
            
            if suc != None:
                lzinho = f'SUC {command[1]} {command[2]}\n{suc}\n'
            else:
                lzinho = f'SUC {command[1]} {command[2]}\nINF\n'
            
            L.append(lzinho)

        elif command[0] == "IMP":
            
            version = int(command[1])

            if version > myglobal.current:
                version = myglobal.current
            
            lzinho = f'IMP {command[1]}\n{PrintTree(version)[1:]}\n'
            
            L.append(lzinho)
        
    file2.writelines(L)
    file2.close()
    file1.close()