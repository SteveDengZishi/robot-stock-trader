import pickle
import sys
#writing pickle to file

#a = ['test value','test value 2','test value 3']
#fileObject = open('file_Name','wb') 
#pickle.dump(a,fileObject)   
#fileObject.close()

# we open the file for reading
fileName = input("Which file do you want to unpickle: ")
try:
    with open(fileName,'rb') as infile:
        # load the object from the file into var b
        content = pickle.load(infile) 
        print(content)

except FileNotFoundError:
    sys.exit(0)
