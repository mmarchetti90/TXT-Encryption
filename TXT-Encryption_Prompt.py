##FUNCTIONS

def displayOptions():
    
    print("\nPlease, type the number corresponding to the desired option.")
    print(" 0 - Help")
    print(" 1 - Encode/Decode one txt document")
    print(" 2 - Encode/Decode all txt documents in folder")
    print(" 3 - Terminate script")


def printHelp():
    
    print("\nEncodes or decodes txt files.")
    print("N.B. Accepted characters for keyword:")
    print(" - Letters (case sensitive);")
    print(" - Numbers;")
    print(" - Symbols: , . < > ; : ( ) [ ] { } - _ = + ? ! @ # $ % ^ & * | / ` ~ ;")
    print(" - Spaces;")


def importDocument(file_name = None):
    
    if file_name == None: # Used for importing single specified document
        
        toggle = 0
        
        while not toggle:
            
            try:
                
                file_name = input("\nPlease input the name of the target document: ")
                doc = open(file_name).read()
                toggle = 1
            
            except:
                
                print("Invalid name, please try again.")
    
    else: # Used for importing document from list
        
        doc = open(file_name).read()
    
    return file_name, doc


def getKey():
    
    # Import keyword
    
    toggle = 0
    
    while not toggle:
        
        key = input("\nPlease enter keyword: ")
        invalid = 0
        
        for char in key:
            
            if char not in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789,.<>;:()[]{}-_=+?!@#$%^&*\|/`~":
                
                invalid += 1
        
        if invalid > 0:
            
            print("\nERROR: Invalid keyword, try again...")
            
            continue
        
        toggle = 1
    
    # Specify mode
    
    print()
    
    toggle = 0
    
    while not toggle:
        
        mode = int(input("Type 0 for encryption, 1 for decription: "))
       
        if mode not in [0, 1]:
            
            print("\nERROR: Invalid mode, try again...")
            continue
        
        toggle = 1
    
    return key, mode


def generateEncoder(key, mode):
    
    # Generating dictionary for encoding/decoding
    
    characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789,.<>;:()[]{}-_=+?!@#$%^&*|/`~ "
    indexes = [characters.index(k) for k in key]
    
    if mode:
        
        encoder = {char : [(characters+characters)[characters.index(char) - i] for i in indexes] for char in characters}
    
    else:
        
        encoder = {char : [(characters+characters)[characters.index(char) + i] for i in indexes] for char in characters}
    
    return encoder


def encodeDocument(doc, code, k):
    
    encoded, counter, pos = "", 0, 0
    
    for char in doc:
        
        counter += 1
        
        # Encoding or decoding character (same thing, just different encoder).
        
        if char not in code.keys(): # Leaving unaltered if character is not in the coder
            
            encoded += char
        
        else:
            
            new_char = code[char][pos]
            encoded += new_char
        
        # Changing positional argument of encoder
        
        if counter == len(k):
            
            pos += 1
            counter = 0
        
        if pos == len(k):
            
            pos = 0
    
    return encoded


def saveDocument(name, doc, m, prefix = ""):
    
    # Generating save_name
    
    if not m:
        
        save_name = prefix + name[:-4] + "_Encoded" + name[-4:]
    
    else:
        
        if "_Encoded." in name:
            
            save_name = prefix + name.replace("_Encoded.", ".")
        
        else:
            
            save_name = prefix + name[:-4] + "_Decoded" + name[-4:]
    
    # Saving document
    
    output = open(save_name, "w")
    output.write(doc)
    output.close()


##MAIN

from os import listdir
from os import mkdir
from os.path import isdir

selection = "-1"

while selection != "3":
    
    if selection == "-1":
        
        displayOptions()
    
    selection = input()
    
    if selection == "0":
        
        printHelp()
        selection = "-1"
        
    
    elif selection == "1":
        
        file_name, document = importDocument()
        key, mode = getKey()
        encoder = generateEncoder(key, mode)
        encoded_document = encodeDocument(document, encoder, key)
        saveDocument(file_name, encoded_document, mode)
        selection = "-1"
    
    elif selection == "2":
        
        # Creating list of files to be encoded/decoded
        
        file_list = [l for l in listdir() if l[-4:] == ".txt"]
        print("\nFound " + str(len(file_list)) + " files.")
        
        # Creating save_folder
        
        if not isdir("ProcessedDocuments"):
            
            mkdir("ProcessedDocuments")
        
        save_folder = ".\\ProcessedDocuments\\"
        
        # User defines encoding/decoding key and operation mode
        
        key, mode = getKey()
        
        # Processing files
        
        for fl in file_list:
            
            document = importDocument(fl)[1]
            encoder = generateEncoder(key, mode)
            encoded_document = encodeDocument(document, encoder, key)
            saveDocument(fl, encoded_document, mode, save_folder)
        
        selection = "-1"
    
    elif selection == "3":
        
        print("\nTerminating script...")
    
    else:
        
        print("\nInvalid choice...")
        selection = "-1"
