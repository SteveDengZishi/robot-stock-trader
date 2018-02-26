import pickle

#writing pickle to file

#a = ['test value','test value 2','test value 3']
#fileObject = open('file_Name','wb') 
#pickle.dump(a,fileObject)   
#fileObject.close()

# we open the file for reading
infile = open('dma.pickle','rb')  
# load the object from the file into var b
content = pickle.load(infile) 
print(content)