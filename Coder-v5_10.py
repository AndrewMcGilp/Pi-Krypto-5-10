#Pygame-Krypto-v5.10 by Andrew McGilp (c)2021
#
#Turn your Raspberry Pi-3/4 into the ***Pi-ENIGMA***
#
#IMPORTANT! Read Me!! Writtin for the Raspberry Pi!
#Press F1 for help.
#Using Thonny Python 3.7.3 (32 bit) on a Raspberry Pi 4 with Raspbian GNU/Linux 10(Buster)
#Must Install tesseract-ocr and pytesseract for image to text function
#sudo apt-get update
#sudo apt-get install tesseract-ocr
#pip3 install pytesseract
#Note pytesseract does not aways convert image to text accurately and needs to be calibrated.
#(1)SYSTEM|Create new System Key/password (Preset password is'codeKey')
#(1.1)Press F12 (1.2)Type in new system password (1.3)Press Enter to save, exit and logon.
#(2)LOGON|Edit user names/public keys/passwords (Admin)
#(2.1)Login USER_NAME=Admin, GROUP_NAME=Group0, PASSWORD=admin(Change Amdin password!)
#(2.2)F10=Add new user, F11=Edit user, F12=Delet user
#(3)The Left and Right CTRL and ALT have hotkey like functions.
#(4)You can Copy/Paste your pictures [jpg/png] to the 'Imgages' folder to use as encryption key.
#Note you must use the same Pi/Os/Krypto-Virsion/Image/Fonts to encode and decode!!
#                        ie.Pi-4/Buster/Pygame KRYPTO-v5_08/Fonts and use the same
#                        image(wallpaper image 'Clouds.jpg' or your own photo .jpg/.png)
#                        and must use the same at both ends!
#Left/Right CTRL & ALT keys have functions!
#Preset users:  Preset passwords:   Preset public key:
#       Admin             admin               userID0
#         Max               dog               userID1
#        Cody               cat               userID2
#      Group0             jumbo              GroupID0
#  
#!Can change default settings
#Default_User_Settings----------1 (line 106-111)+/-
#Default_System_Settings--------3 (line 115-122)+/-
#Default_User_List (line 2561-2577)+/- #Create Default/Preset user list

"""
  NOTICE:

  Please note that this software is used entirely at your own RISK and comes with 
  absolutely no guarantee or warrantee what so ever and by using this software 
  you agree to these terms. It is free to be used by a private individual but not
  free to be used by any (Company, Organisation, Government, etc) without premission.
"""

import pygame, time, io, sys, os
import base64, random, copy, glob
import tempfile, subprocess, platform

from copy import deepcopy
from pygame.locals import DOUBLEBUF
from io import BytesIO
from PIL import Image

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
COLOR_DEPTH = 32

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), DOUBLEBUF, COLOR_DEPTH)

pygame.display.set_caption('Pygame(KRYPTO-v5.10)')
clock = pygame.time.Clock()
pygame.mouse.set_visible(True)
FPS = 30

#Color    R    G    B   Display font colors
WHITE = (225, 225, 225)#Display color White
RED = (200, 50, 50)#Display color Red
GREEN = (80, 200, 80)#Display color Green
ORANGE = (150, 150, 10)#Display color Orange
BLACK = (10, 10 ,10)#Not quit Black
BZLCOL = RED

#Mouse
LEFT = 1
MIDDLE = 2
RIGHT = 3
UP = 4
DOWN = 5

genJunk = True #True to gen dummy chars set (genJunk = False & imgMode = 2) to read user file
capsOn = False
done = False
canI = False
iCan = False
showImg = True
conDel = False
imgCount = 0
editMode = 0
indexNo = 0
listNo = 0
useImgName = True
searchPath = ''
debug = False

try:
    process = str(subprocess.Popen(["grep", "^VERSION_CODENAME", "/etc/os-release"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate())
    osName = (process.split('\\n')[0])[20:]
except:
    osName = 'NONE'#Pi model or os name ie. Pi3/Pi4/PiTop or Jessie/Buster/ect
    print('Could_Not_Get_OS_Name!')
    
#===========================================================================================
    
#Default_User_Settings----------1 !Can change
strPath = 'eDocs/'#Preset path - strPath = '/home/pi/Desktop/'
docName = 'doc'#Preset document name Pi_Enigma
strPin0 = '5468295424' #Preset Pin is 10 digits long
useFontGroup = 1# 0 = font group 0 : 1 = font group 1 : 2 = auto load font group (Caution don't ADD new Fonts!!)
strFn2 = 'Preset footnote!(up to 45 Characters)'#Press Right-ALT Preset footnote number 2 (up to 45 Characters)
#Default_User_Settings----------2 !Don't change
setImgMode = 1# 0 = writes png image  
strKey = '' #Your Public-Key/Public-Name
selFileType = 0# Right ALT 0=.txt+Time-Stamp '-', 1=.png+Time-Stamp '-', 2=.txt+Auto_PIN, 3=.png+Auto_PIN,
#Default_System_Settings--------3 !Can change
prefix = ':#:-' #Preset Unique prefix a (Sys watermark/User-Group/Department-ID) 4-12 Characters
imgfix = '&^%$' #Prefix for selfgen image 4-12 Characters
sysPin = '5468295425' #System Pin is 10 digits long
preKey = 'keyCode'#Preset System Key/Password = keyCode
useZ = True#pin algorithm use offsetZ
useX = True#pin algorithm use X Add sysPin and imgfix to image
#Default_System_Settings--------4 !No need to change
rmFile = True#Remove selfGenImg and tempFile.txt
BgImgPath = 'Settings/Bg0.png' #Background image 0 file name
BgImgPath1 =  'Settings/Bg1.png'#Background image 1 file name
sysImgMode = 2#Must be set to 2 or 3
imgNo = 0 #Use image number
crptMode = 0#
fileExt = '.txt'
maskMsg = 0
caseNo = 0
strName = docName
footNote = ''#'Footnote_Empty!' NOTE!! not encrypted!
#End----------------------------

strUID = ''#strUIDd #Your name or user ID
strGID = ''#strGIDd #The Name of your group
strPWD = ''#strPWDd #Password
strNewUID = ''
strNewGID = ''
strNewPWD = ''
strPF = ''
logonNo = 0
imgMode = 0
dspCol = 50
qtyCol = 78
qtyLns = 12
curNum = 0
scrMode = 3 #Start up screen mode
genList = False
sysSave = False
confirmDel = False
folderNo = 0
folderList = []

fileNo = 0
fileList = []

#List of users User name-  Password  - Public-key will be encrypted
List_Users = []
List_Char = ['_','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','u','r','s','t','v','w','x','y','z',
             'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','U','R','S','T','V','W','X','Y','Z',
             '0','1','2','3','4','5','6','7','8','9','!','@','#','$','%','^','&','*','(',')','+',':','|','<','>','\\','/','[',']',',','.','?']

List_List = [['+'], ['/'], ['0'], ['1'], ['2'], ['3'], ['4'], ['5'], ['6'], ['7'], ['8'], ['9'],
             ['A'], ['B'], ['C'], ['D'], ['E'], ['F'], ['G'], ['H'], ['I'], ['J'], ['K'], ['L'], ['M'],
             ['N'], ['O'], ['P'], ['Q'], ['R'], ['S'], ['T'], ['U'], ['V'], ['W'], ['X'], ['Y'], ['Z'],
             ['a'], ['b'], ['c'], ['d'], ['e'], ['f'], ['g'], ['h'], ['i'], ['j'], ['k'], ['l'], ['m'],
             ['n'], ['o'], ['p'], ['q'], ['r'], ['s'], ['t'], ['u'], ['v'], ['w'], ['x'], ['y'], ['z']]

List_Key0 = ['abcDEF','defABC','ghiJKL','jklGHI','mnoPQU','pquMNO','rs!TV%','tv@RS*','wx#YZ^','yz$WX?', '_-_&_~']
List_Nums = []
List_Code = []
keyList = []
imgPathList = ['NONE']

strImg0 = 'R0lGODlhEAAQALMAAAAAAP//AP///wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA' \
           'AAAAAAAAAAAA\nAAAAACH5BAEAAAIALAAAAAAQABAAQAQ3UMgpAKC4hm13uJnWgR' \
           'TgceZJllw4pd2Xpagq0WfeYrD7\n2i5Yb+aJyVhFHAmnazE/z4tlSq0KIgA7\n'

try:
    imgImg0 = pygame.image.load(BgImgPath1).convert()#BgImgPath
    imgImg1 = pygame.transform.scale(imgImg0, (SCREEN_WIDTH, SCREEN_HEIGHT))
    imgDsp0  = pygame.transform.scale(imgImg0, (240, 160))
    rectX, rectY, sizeX, sizeY =  imgImg0.get_rect()
    offsetX = -int((sizeX - SCREEN_WIDTH) / 2)
    offsetY = -int((sizeY - SCREEN_HEIGHT) / 2)    

except:
    print('Error_:_Must_have_a_background_Image!!_With_Path_(' + BgImgPath1 + ')')
    print('Settings/Bg1.png and Images/ with some Photos or copy-paste some images from wallpaper png or jpg')
    pygame.quit()
    sys.exit()    

strData = ''
strLine0 = ''
strLine1 = 'Enter_System_Password/Empty=Preset_Password|F1=Help'#'Generate_Encoding_Algorithm!'
strLine2 = '**********'
strLine3 = ''
strLine4 = ''
strLine5 = ''
strLine6 = ''
strLine7 = ''
strLine8 = ''#Decode incoming message
strLine9 = ''
strLine10 = ''
strLine11 = ''
strLine12 = ''#Update_me!'#Disp buffer string
strLine13 = ''#Long message disp string

strUIDd = '' 
strGIDd = ''
strPWDd = ''

sizeXY = 800, 600
showPin = 0
showPass = 0
charNum = 0
rectAddY = 0
miaFonts = 0
charM = '_'#Mouse type char
strNum = ''
strAdd = '-'

#Font List for Encrypt pin
nogoodList = ['droidsansfallback']#Note Do not use 'droidsansfallback'!!
if (useFontGroup == 0):#Font list 0
    fontList0 = ['Carlito', 'Dingbats', 'FreeMono', 'FreeSans', 'FreeSerif', 'Gentium', 'Inconsolata', 'Lato', 'Monospace', 'msbm10']
    fontList1 = ['dejavuserif', 'wasy10','dejavusansmono', 'dejavusans', 'Gentium', 'caladea', 'Lato', 'Monospace', 'msbm10', 'cmex10']
elif (useFontGroup == 1):#Font list 1
    fontList0 = ['dejavuserif', 'dejavusansmono', 'pibotocondensed', 'liberationmono', 'dejavusans', 'freesans', 'liberationsans', 'freeserif', 'quicksandlight', 'freemono']
    fontList1 = ['pibotolt', 'liberationserif', 'piboto', 'dejavumathtexgyre', 'freeserif', 'quicksand', 'quicksandmedium', 'notomono', 'dejavumathtexgyre', 'freeserif']
else:#Auto load fonts Please Note if you add new fonts it will not decode older encoded items!!!!
    fontList0 = []
    fontList1 = []
    temtList = pygame.font.get_fonts()
    if (len(temtList) > 10):
        for i in range(10):
            for j in range(len(nogoodList)):
                if (temtList[i] != nogoodList[j]):
                    fontList0.append(temtList[i])                    
            for j in range(len(nogoodList)):
                if (temtList[(len(temtList) - 1 - i)] != nogoodList[j]):
                    fontList1.append(temtList[(len(temtList) - 1 - i)])
    else:
        print('ERROR:Not_Enough_Fonts!!!')
        done = True
        
#Check fonts
for i in range(0,len(fontList0),1):
    search = pygame.font.match_font(fontList0[i])
    if (search == None):
        miaFonts += 1
        print ('Missing-Font:(' + str(miaFonts) + '):' + fontList0[i])
        
for i in range(0,len(fontList1),1):
    search = pygame.font.match_font(fontList1[i])
    if (search == None): 
        miaFonts += 1
        print ('Missing-Font:(' + str(miaFonts) + '):' + fontList1[i])

fontRot = 15
fontScl = 35
fontSize = 16

font0 = pygame.font.SysFont(fontList0[0], fontScl)
font1 = pygame.font.SysFont('freeMono', fontSize)#'FreeMono' 'Courier' 'freesansbold'
font2 = pygame.font.SysFont('freesans', 20, bold=True, italic=False)#Text to image font should be bold and small'freesansbold'

if (pygame.font.match_font('freesans') == None):#Check Text to Image font ('freesans')
    miaFonts += 1
    print ('Missing-Text_to_Image_Font:', 'freesans')
  
if (miaFonts > 0):
    strLine1 = 'ERR:You_Do_Not_Have_All_The_Fonts!_(' + str(miaFonts) + ')_Missing.' 
    print(strLine1)

rectPosX = 250
rectPosY = 200
rectSizeX = 240
rectSizeY = 240

offsetX = 0
offsetY = 0
offsetZ = 0
inputNo = 0
dummyCount = 0


#===============================================================================


def Encode0(strData):#GenCodeList
        
    global List_Code
    global strLine1
    
    goodImg = True

    List_Code.clear()
    List_Code = copy.deepcopy(List_List)

    for i in range(len(List_Code)):
    
        char = List_Code[i][0]
    
        for j in range(len(strData)):
        
            if (char == strData[j]):
                sublist = List_Code[i]
                sublist.append(j)
     
    for i in range(len(List_Code)):
        
        if (len(List_Code[i]) < 500):
            goodImg = False
  
    if (goodImg == False):
        strLine1 = 'Warning!_:_Image_Not_Suitable!'
        #print(strLine1)
        DrawScreen1()
        pygame.display.flip()
        time.sleep(4)

            
def Encode1(strMain):#Encode string
    
    for i in range(len(strMain)):
        char = strMain[i]
        if (genJunk):
            char = char.capitalize()
            Encode2(char)
            rndC = random.randrange(1, 5)
            for i in range(rndC):
                Encode2('~')
        else:
            Encode3(char)


def Encode2(char):#CharFilterIn

    #Filter char
    if (char == '~'):
        char = 'a'
    elif (char == '!'):
        char = 'b'
    elif (char == '@'):
        char = 'c'
    elif (char == '#'):
        char = 'd'
    elif (char == '$'):
        char = 'e'        
    elif (char == '%'):
        char = 'f'
    elif (char == '^'):
        char = 'g'
    elif (char == '&'):
        char = 'h'
    elif (char == '*'):
        char = 'i'         
    elif (char == '('):
        char = 'j'
    elif (char == ')'):
        char = 'k'
    elif (char == '-'):
        char = 'l'
    elif (char == '+'):
        char = 'm'         
    elif (char == '='):
        char = 'n'
    elif (char == '`'):
        char = 'o'
    elif (char == '|'):
        char = 'p'
    elif (char == '<'):
        char = 'q'         
    elif (char == '>'):
        char = 'u'
    elif (char == ']'):# Or }
        char = 'r'
    elif (char == '['):# Or {
        char = 's'
    elif (char == '\\'):
        char = 't'           
    elif (char == '.'):
        char = 'v'
    elif (char == ','):
        char = 'w'
    elif (char == '\''):
        char = 'x'
    elif (char == ':'):# Or ;
        char = 'y'         
    elif (char == '?'):
        char = 'z'
    elif (char == '_' or char == ' '):
        char = '+'
       
    Encode3(char)
    
               
def Encode3(char):#Encode char to number list
    
    for i in range(0, len(List_Code)):
        if (char == List_Code[i][0]):
            break
        
    rndC = random.randrange(1, len(List_Code[i]))
    codeNum = str(List_Code[i][rndC])
    List_Nums.append(codeNum)
  
 
#======================================================================

def Decode0(numList):#Decode Char from number list
  
    global strLine1
    global strLine8
    global strLine10
    global dummyCount
    
    strLine8 = ''
    strLine1 = ''
    
    try:
        for i in range(len(numList)):
            try:
                num = int(numList[i])
                char = strData[num]
                if (genJunk):
                    Decode1(char)
                else:
                    strLine8 += char
            except:
                strLine1 = str(numList[i])
    except:
        strLine1 = 'ERROR_:_Decode0_:_Problem!'
        print(strLine1)

    if (strLine1 == '{}'):
        strLine10 = '{There_is_no_footnote!}'
    else:
        strLine10 = strLine1
    
    if (len(strLine8) > dummyCount and genJunk):#dummyCount != 0):
        strLine1 = 'ERROR:[PIN/User/Key/Image/Image-Mode/OS-Version]'#-Incorrect!'
        UpdateDspMsg(strLine8, '')
    else:
        if (genJunk):
            strLine1 = 'Decoded!'
            UpdateDspMsg(strLine8, '')
        else:
            strLine1 = 'Enter=Next(to_Continue)|TAB=Back|ESC=Quit|F1=Help'
            if (showImg == False):
                UpdateDspMsg(strLine8, '')


def Decode1(char):#CharFilterOut   
  
    global strLine8
    global dummyCount

    if (char == 'a'):#Empty char dummy
        dummyCount += 1
        char = ''
    elif (char == 'b'):
        char = '!'
    elif (char == 'c'):
        char = '@'
    elif (char == 'd'):
        char = '#'
    elif (char == 'e'):
        char = '$'        
    elif (char == 'f'):
        char = '%'
    elif (char == 'g'):
        char = '^'
    elif (char == 'h'):
        char = '&'
    elif (char == 'i'):
        char = '*'         
    elif (char == 'j'):
        char = '('
    elif (char == 'k'):
        char = ')'
    elif (char == 'l'):
        char = '-'
    elif (char == 'm'):
        char = '+'         
    elif (char == 'n'):
        char = '='
    elif (char == 'o'):
        char = '`'
    elif (char == 'p'):
        char = '|'
    elif (char == 'q'):
        char = '<'         
    elif (char == 'u'):
        char = '>'
    elif (char == 'r'):
        char = ']' # Or }
    elif (char == 's'):
        char = '[' # Or {
    elif (char == 't'):
        char = '\\'           
    elif (char == 'v'):
        char = '.'
    elif (char == 'w'):
        char = ','
    elif (char == 'x'):
        char = '\''
    elif (char == 'y'):
        char = ':' # Or ;        
    elif (char == 'z'):
        char = '?'
    elif (char == '+'):
        char = '_'
        
    strLine8 += char

#======================================================================

def ReadFile0():#Read encoded file
    
    global strLine1
    global dummyCount
    global imgMode
    global crptMode
    global imgMode
    global imgNo
    global fileExt
    global searchPath
    global strPin1
    
    dummyCount = 0
    crptMode = 0
    imgNo = 0
    imgMode = 0
    num = 0
    objFile = ''
    strNew = ''
    strMeta = ''
    proceed = False
    listMain = []
    searchPath = ''

    try:
        if (fileExt == '.png'):
            Img2Txt(strPath + strName + '.png')
            f = open('Settings/tempFile.txt', "r")
        else:
            f = open(strPath + strName + '.txt', "r")
            
        if f.mode == 'r':
            objFile = f.read()                  
            f.close()
            proceed = True
            
    except:#
        strLine1 = 'ERROR_:_Could_Not_Find_File:' + strPath + strName + fileExt
        
    if (proceed):
        
        try:
            if (rmFile and fileExt == '.png' and debug == False):#rmFile fileExt == '.png' and 
                os.remove('Settings/tempFile.txt')
        except:
            print('ReadFile0()|Could_Not_Remove_File!')
                
        for i in range(len(objFile)):
            if(objFile[i] != '\n'):
                strNew += objFile[i]       
         
        if (genJunk):
            
            for i in range(len(strNew) - 1):
                search = strNew[i] + strNew[i+1]
                if (search != ']~'):
                    strMeta += strNew[i]
                else:
                    num = i + 1
                    break
                
            num1 = 1
            for i in range(len(strMeta)):
                if (strMeta[i] != '['):
                    num1 +=1
                else:
                    break
             
            searchPath = strMeta[num1:]
            strNew = strNew[num:]

            if (strMeta[0]  == '*'):#imgMode/crptMode  0
                crptMode = 0
            elif (strMeta[0]  == '@'):#imgMode/crptMode  1
                crptMode = 1
            elif (strMeta[0]  == '&'):#imgMode/crptMode  2
                crptMode = 2
            elif (strMeta[0]  == '$'):#imgMode 3
                crptMode = 3
            else:
                print('Over-ride_:_old-version')
                crptMode = 0
                imgMode = setImgMode
                imgNo = 0
     
            if (crptMode < 4):#Use metadata      
                if (useImgName):
                    try:
                        imgMode = int(strMeta[1])
                        imgNo = int(strMeta[2])
                        strMeta = strMeta[4:]
                        strMeta = strMeta
                        #print('Image_Name_:_', strMeta)
                    except:
                        strLine1 = 'ERROR:Could_Not_Read_Metadata!'
                        print(strLine1)
                        return
                    try:    
                        if (len(imgPathList) > 0):
                            for i in range(len(imgPathList)):
                                if (imgPathList[i] == strMeta):
                                    imgNo = i     
                        else:
                            print('ERROR_:_No_Images!')        
                    except:
                        print('ERROR!')
                else:
                    print('No_Meta-Data!')
                    imgMode = 1
                    imgNo = 0
                    strMeta = ''
                    
        if (crptMode == 0 or genJunk == False):#Strait numbers
            objFile = strNew

        elif (crptMode == 1):#Duel crypt to numbers
            num = 10 + int(strPin0[5]) + int(strPin0[6]) + int(strPin0[7])
            for c in strNew:
                x = ord(c)
                x = x - num
                c2 = chr(x)
                objFile = objFile + c2
            
        elif (crptMode == 2):#alphabet to numbers
            
            r = True
            for i in range(len(strNew)):
                sChar = strNew[i]
                if (sChar == '{'):
                    r = False
                if (r):
                    for j in range(len(List_Key0)):
                        strSub = List_Key0[j]
                        for c in range(len(strSub)):
                            if (strSub[c] == sChar):
                                if (j != 10):
                                    objFile += str(j)
                                else:
                                    objFile += '~'  
                else:
                    objFile += sChar
                    
        elif (crptMode == 3):#Needs 2b updated!!!
            objFile = strNew
             
        else:
            print('ERROR_:_ReadFile-Out_Of_Range')       
        
        if (imgMode == 1):
            if (useImgName):
                UpdateImage(imgPathList[imgNo])
 
            else:
                print('Use image file from name')

        if (scrMode != 3):
            strPin1 = GenPin1(strName)#
            if (strPin1 != 'None'):
                UpdatePIN(strPin1, strKey, 1)
            else:
                UpdatePIN(strPin0, strKey, 1)
                            
        listMain = objFile.split('~')
        Decode0(listMain)
        
    else:
        strLine1 = 'ERROR:No_File/File_Empty!'
         
    listMain.clear()
    fileExt = '.txt'
       
        
def CheckForFile(canI):
    
    global strLine1
    
    try:
        f = open(strPath + strName + '.txt', "r") 
        f.close()

        strLine1 = 'WARNING_:_(' + strName + '.txt)_Already_Exists!'
        canI = False
        
    except:
        canI = True
        #print('No such file! Go Ahead Make My Day!!')
    return (canI)


def WriteFile0(content):#Write encoded file 

    global strLine1
    global crptMode
    global imgMode
    global fileExt
    
    strNew = ''
    
    try:#Test to see if Folder Ex
        os.mkdir(strPath)
        strLine1 = 'WriteFile0_:_Made_New_Folder!_>_' + strPath
        #print('WriteFile0_:_Made_New_Folder!_>_' + strPath)
    except:
        pass

    content = '~'.join(content)
       
    if (genJunk):
        
        if (useImgName and imgMode != 0 and imgMode != 4):
            imgName = strPF
        else:
            imgName = 'NONE'
        
        if (crptMode == 0):
            content = '*' + str(imgMode) + str(imgNo) + '[' + imgName + ']~' + content + '~{' + footNote + '}'
            
        elif (crptMode == 1):#Duel crypt 
            num = 10 + int(strPin0[5]) + int(strPin0[6]) + int(strPin0[7])
            for c in content:
                x = ord(c)
                x = x + num
                c2 = chr(x)
                strNew = strNew + c2
                
            content = '@' + str(imgMode) + str(imgNo) + '[' + imgName + ']~' + strNew + '~{' + footNote + '}'

        elif (crptMode == 2):#Convert numbers to letters NeedToComplete
            for i in range(len(content)):
                if (content[i] != '~'):
                    strNew += List_Key0[int(content[i])][random.randrange(0, 5)]
                else:
                    strNew += List_Key0[10][random.randrange(0, 3)]
                    
            content = '&' + str(imgMode) + str(imgNo) + '[' + imgName + ']~'  + strNew + '~{' + footNote + '}'
        
        elif (crptMode == 3):#Same as crypt-mode 0 fo now
            content = '$' + str(imgMode) + str(imgNo) + '[' + imgName + ']~' + content + '~{' + footNote + '}'

    strNew = ''
           
    for i in range(len(content)):
        if (i % qtyCol == 0 and i > 1):
            strNew += '\n'
        strNew += content[i]
        
    try:
        f = open(strPath + strName + '.txt', "w")
        f.write(strNew)#\n
        f.close()
 
    except IOError:
        strLine1 = 'ERROR_:_Could_Not_Create_File!'
        print('ERROR_:_Could_Not_Create_File!')
     
    if (fileExt == '.png'):#'.png'
        Txt2Img(content, (strPath + strName))
        
    fileExt = '.txt'
    crptMode = 0
    content = ''
    strNew = ''
    List_Nums.clear()


def WriteImage():#create public image
    
    global strLine1
    strLine1 = 'Writing_Image_To_Folder!_>_' + strPath
    DrawScreen1()
    pygame.display.flip()
    
    try:#Test to see if Folder Ex
        os.mkdir(strPath)
        strLine1 = 'WriteFile0_:_Made_New_Folder!_>_' + strPath
        #print(strLine1)
    except:
        pass
    
    try:
        imgImg = pygame.image.load(imgPathList[imgNo])
        strP = strPath + strName + '-Img.png'
        pygame.image.save(imgImg, (strP))#'Images/image-Img.png'
        strLine1 = 'Image_Path_:_' + strP
        #print('Image_Path_:_' + strP)
    except:
        strLine1 = 'ERROR_:_Could_Not_Save_Image_To_Folder!'
        print('ERROR_:_imgMode_:_Could_Not_Save_Image_To_Folder!')

def Txt2Img(strLine, fName):#
    
    global strLine1
    global sizeXY
    
    addNo = 0
    lenNo = qtyCol * 2 #
    dspLine0 = 0
    strNew = ''
    sizeXY = 800, 600
    
    if (len(strLine) != 0):
        
        for i in range(len(strLine)):
            strNew += (strLine[i] + ' ')
            
        strLine1 = 'Text_To_Image-START!'
        
        qtyLns = int(len(strNew) / lenNo) + 1#qtyLns = int(len(strLine) / qtyCol) + 1
        
        for i in range(0, qtyLns, 1):
            if (sizeXY[0] < (font2.size(strNew[lenNo * i:lenNo + lenNo * i]))[0]):
                sizeXY = font2.size(strNew[lenNo * i:lenNo + lenNo * i])

        scrX = sizeXY[0] + (sizeXY[1] * 2)
        scrY = sizeXY[1] * int(qtyLns * 1.34)
 
        screen = pygame.display.set_mode((scrX, scrY), DOUBLEBUF, COLOR_DEPTH)
        screen.fill((255,255,255))#Background color WHITE

        for i in range(0, qtyLns, 1):
            dspLine0 = strNew[addNo:(addNo + lenNo)]
            addNo += lenNo
            dspStr0 = font2.render(dspLine0, True, BLACK)#Font color
            screen.blit(dspStr0, (10, ((sizeXY[1] + 5) * i) + 10))

        pygame.display.flip() 

        try:
            rect = pygame.Rect(0, 0, scrX, scrY)#PosX, PosY, RecSizeX, RecSizeY
            sub = screen.subsurface(rect)
            pygame.image.save(sub, fName + '.png')#'Images/image.png'

        except:
            print('ERROR_:_Txt2Img-Subsurface_Rectangle_Outside_Surface_Area!')  
        time.sleep(2)
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), DOUBLEBUF, COLOR_DEPTH)
        strLine1 = 'Text_To_Image-DONE!'
        strLine = ''
                
    else:
        strLine1 = 'ERROR:Txt2Img-String_Empty!'
        print(strLine1)
 
def Img2Txt(path):
      
    global strLine1
    
    strLine = ''
    strLine1 = 'Image_To_Text-START-Takes_A_While!<Please_Wait>'
    DrawScreen1()
    pygame.display.flip()

    try:
        temp = tempfile.NamedTemporaryFile(delete=False)
        process = subprocess.Popen(['tesseract', path, temp.name], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        process.communicate()

        with open(temp.name + '.txt', 'r') as handle:
            contents = handle.read()

        os.remove(temp.name + '.txt')
        os.remove(temp.name)
    
        for i in range(0, len(contents)):
            if (contents[i] != '\n' and contents[i] != ' ' and contents[i] != ','):
                strLine += contents[i]
                
        strLine = strLine[:-1]
        WriteTemp(strLine)

    except:
        strLine1 = "ERROR:sudo apt-get install tesseract-ocr -y, pip install pytesseract)"        
        print(strLine1)
        print('sudo apt-get update')
        print('sudo apt-get install tesseract-ocr')
        print('pip install pytesseract')
        DrawScreen1()
        pygame.display.flip()
        time.sleep(5)
 
 
def WriteTemp(content):
    
    strNew = ''
    for i in range(len(content)):
        if (i % qtyCol == 0 and i > 1):
            strNew += '\n'
        strNew += content[i]
 
    content = ''
    try:
        f = open('Settings/tempFile.txt', "w")
        f.write(strNew)#\n
        f.close()
        strNew = ''
    except IOError:
        print('Could not create a file!')
        

def UpdatePIN(pin, strKey, num):#PIN and Key

    global hudStr7
    global hudStr8
    global hudStr9
    global hudStr10
    global strLine1
    global font0
    global rectPosX
    global rectPosY 
    global rectSizeX 
    global rectSizeY
    global offsetZ
    global strPF

    keyList.clear()
    offsetZ = 0
    
    fontScl0 = 16
    fontScl1 = 16
    fontScl2 = 16
    fontRot = 0
    eOffsetX = 0
    eOffsetY = 0
    rotation = 0
    scaleAddXY = 0
    
    if (imgMode != 2 and imgMode != 3):
        
        try:
            R = int(pin[2]) * 2 * int(pin[3]) + 25 + int(pin[5]) #print(R)#0-255
            B = int(pin[0]) * 2 * int(pin[7]) + 25 + int(pin[9]) #print(B)#0-255
            G = int(pin[1]) * 2 * int(pin[6]) + 25 + int(pin[3]) #print(G)#0-255
            offsetZ = int(pin[int(pin[1])]) + (int(pin[int(pin[6])]) * 10) + (int(pin[int(pin[3])]) * 100)
            
            fontTyp0 = fontList0[int(pin[5])]#Font type you can swop out PIN's 0-9
            fontTyp1 = fontList0[int(pin[1])]#Font type you can swop out PIN's 0-9
            fontTyp2 = fontList0[int(pin[9])]#Font type you can swop out PIN's 0-9
            fontRot = (15 * int(pin[2]))#Rotate font you can swop out PIN's 0-9
            fontScl0 = ((int(pin[3]) + int(pin[5])) + 12)#Scale font you can swop out PIN's 0-9
            fontScl1 = ((int(pin[4]) + int(pin[8])) + 12)#Scale font you can swop out PIN's 0-9
            fontScl2 = ((int(pin[4]) + int(pin[6])) + 12)#Scale font you can swop out PIN's 0-9

            newPWD0, newUID = UserSearch(strUID, '', 0)#
            if (newUID == ''):
                newUID = strUID

            newPWD1, newKey = UserSearch(strKey, '', 0)#
            if (newKey == ''):
                newKey = strKey

            if (strKey == strGID):
                keyList.append(newKey)
                keyList.append(newKey)
            else:
                keyList.append(newKey)
                keyList.append(newUID)                
                    
            #Set Warning: listed and non listed encode/decode        
            if (logonNo != 4 or strKey == newKey):
                strLine1 = 'Warning:_User/Sender_Not_in_list!'
                #print(strLine1)
                
                if (1 == 1):#Show warning
                    #print(strLine1)
                    DrawScreen1()
                    pygame.display.flip()
                    time.sleep(4)
                
                keyList.clear()
                keyList.append(strUID)
                keyList.append(strKey)

            keyList.sort(key = lambda keyList: keyList)

            font0 = pygame.font.SysFont(fontTyp0, fontScl0)
            hudStr7 = font0.render(keyList[0] + prefix, True, (G,R,B))#R,G,B
            hudStr7 = pygame.transform.rotate(hudStr7, fontRot)
            
            font1 = pygame.font.SysFont(fontTyp1, fontScl1)
            hudStr8 = font1.render(prefix + keyList[1], True, (R,B,G))
            hudStr8 = pygame.transform.rotate(hudStr8, fontRot) 

            font2 = pygame.font.SysFont(fontTyp2, fontScl1)
            hudStr9 = font1.render(prefix + sysKey, True, (B,G,R))
            hudStr9 = pygame.transform.rotate(hudStr9, fontRot)
            
            rectPosX = (int(pin[4]) * int(pin[5])) * 5 + 15
            rectPosY = (int(pin[5]) * int(pin[3])) * 3 + 10
            rectSizeX = (int(pin[6]) * 10) + 240
            rectSizeY = (int(pin[7]) * 10) + 240
            
            #Image offset
            eOffsetX = offsetX - int(pin[8]) * 10  
            eOffsetY = offsetY - int(pin[9]) * 10
                
            scaleAddXY = int(pin[5]) + int(pin[6])
            
            if (int(pin[3]) + int(pin[7]) % 2 == 0):
                rotation = 0  
            else:
                rotation = 180
        except:
            strLine1 = 'ERROR_:_UpdatePIN-PIN_Mode_0'
            print(strLine1)
        
    else:#Image mode 2 Png Password mode & 3 is RGB Password mode 

        try:
            R = int(pin[0]) * 2 * int(pin[7]) + 25 + int(pin[9]) #print(B) 
            B = int(pin[1]) * 2 * int(pin[6]) + 25 + int(pin[3]) #print(G)
            G = int(pin[2]) * 2 * int(pin[3]) + 25 + int(pin[5]) #print(R)
            offsetZ = int(pin[int(pin[2])]) + (int(pin[int(pin[5])]) * 10) + (int(pin[int(pin[7])]) * 100)
            
            fontRot = (15 * int(pin[2]))#Rotate font you can swop out PIN's 0-9
            
            fontTyp0 = fontList1[int(pin[1])]#Font type you can swop out PIN's 0-9
            fontTyp1 = fontList1[int(pin[7])]#Font type you can swop out PIN's 0-9
            fontTyp2 = fontList1[int(pin[8])]#Font type you can swop out PIN's 0-9            
            fontScl0 = ((int(pin[3]) + int(pin[5])) + 12)#Scale font you can swop out PIN's 0-9
            fontScl1 = ((int(pin[4]) + int(pin[1])) + 12)#Scale font you can swop out PIN's 0-9
            fontScl2 = ((int(pin[7]) + int(pin[8])) + 12)#Scale font you can swop out PIN's 0-9
            
            font0 = pygame.font.SysFont(fontTyp0, fontScl0)
            hudStr7 = font0.render(strKey + prefix, True, (G,R,B))#R,G,B
            hudStr7 = pygame.transform.rotate(hudStr7, fontRot)
             
            font1 = pygame.font.SysFont(fontTyp1, fontScl1)
            hudStr8 = font1.render(prefix + strKey, True, (R,G,B))# + strName prefix +    
            hudStr8 = pygame.transform.rotate(hudStr8, fontRot)

            font2 = pygame.font.SysFont(fontTyp2, fontScl1)
            hudStr9 = font1.render(prefix + sysKey, True, (B,G,R))
            hudStr9 = pygame.transform.rotate(hudStr9, fontRot)
            
            rectPosX = (int(pin[4]) * int(pin[5])) * 5 + 15
            rectPosY = (int(pin[5]) * int(pin[3])) * 3 + 10
            rectSizeX = (int(pin[6]) * 10) + 240
            rectSizeY = (int(pin[7]) * 10) + 240
            
            #Image offset
            eOffsetX = offsetX - int(pin[8]) * 10  
            eOffsetY = offsetY - int(pin[9]) * 10
                
            scaleAddXY = int(pin[3]) + int(pin[7])
            
            if (int(pin[4]) + int(pin[8]) % 2 == 0):
                rotation = 0  
            else:
                rotation = 180
                
        except:
            strLine1 = 'ERROR_:_UpdatePIN-PIN_Mode_1'
            print(strLine1)
    
    if (useZ and useX):
        fontTyp4 = fontList0[9]#Font type you can swop out PIN's 0-9
        font4 = pygame.font.SysFont(fontTyp4, fontScl1)
        hudStr10 = font4.render(sysPin + imgfix, True, (250,50,20))#str(pin) + prefix
        hudStr10 = pygame.transform.rotate(hudStr10, fontRot - 25)
    else:
        fontTyp4 = fontList0[5]#Font type you can swop out PIN's 0-9
        font4 = pygame.font.SysFont(fontTyp4, fontScl1)
        hudStr10 = font4.render('', True, (20,50,250))
        hudStr10 = pygame.transform.rotate(hudStr10, fontRot - 50)
        
    if (genJunk):
        
        if (num == 0):#0=Gen image for writing
            if (imgMode == 0):
                strPF = strPath + strName + '-Img.png'        
            else:
                strPF = imgPathList[imgNo]
                
        else:#1=Gen image for reading
            if (imgMode == 0):
                strPF = strPath + strName + '-Img.png'        
            else:
                strPF = searchPath
    else:
        strPF = BgImgPath1
        
    #print(strPF)           
    GenImage(strPF, eOffsetX, eOffsetY, rotation, scaleAddXY, pin)
    keyList.clear()


def SelfGenImg(pin0):#Gen image based on pin
    
    global imgImg0
    global imgDsp0 
    global strLine1
        
    strPF = 'Settings/temp.png'
    
    SCR_WIDTH = 1000
    SCR_HEIGHT = 800
    screen = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT), DOUBLEBUF, COLOR_DEPTH)
    
    strLine = ''
    dspLine0 = 0
    
    rV = 150
    gV = 100
    bV = 255
    
    sL = len(List_Char) - 1
    kP = int(pin0[1])
    gV = int(pin0[9])
    aV = int(pin0[5])
    addNo = 0
    adder = int(SCR_WIDTH - SCR_WIDTH * 0.05)
    lenNo = int((SCR_WIDTH / (fontSize - 5.8)))
    qtyLns = int((SCR_HEIGHT / fontSize ) - 1)
    #print(strPF, '_:_',pin0)
    
    try:
        R = int(pin0[2]) * 2 * int(pin0[3]) + 25 + int(pin0[8]) #print(R)
        B = 255 - (int(pin0[0]) * 2 * int(pin0[7]) + 25 + int(pin0[6])) #print(B) 
        G = int(pin0[1]) * 2 * int(pin0[6]) + 25 + int(pin0[2]) #print(G)
        A = 255 -(int(pin0[3]) * 2 * int(pin0[5]) + 25 + int(pin0[9])) #print(A)
        C = 25 +(int(pin0[1]) * 2 * int(pin0[8]) + 25 - int(pin0[4])) #print(C)
        H = 25 +(int(pin0[2]) * 2 * int(pin0[7]) + 25 - int(pin0[8])) #print(H)
        
        colList0 = [(R,A,B),(A,G,R),(R,A,R),(B,G,A),(H,C,B),(A,R,B),(B,A,R),(B,A,B),(R,A,G),(H,A,B)]
        colList1 = [(A,G,C),(B,A,G),(H,G,H),(A,G,B),(G,R,A),(B,R,C),(B,G,A),(B,A,C),(A,R,G),(A,R,B)]
        colList2 = [(B,B,C),(H,R,G),(R,R,A),(A,R,B),(H,A,C),(R,B,B),(C,G,A),(B,A,C),(C,C,G),(R,A,B)]
        colList3 = [(A,G,H),(B,C,G),(A,G,A),(A,G,C),(C,A,B),(B,R,A),(A,G,A),(B,A,C),(H,R,G),(H,R,B)]
        
    except:
        print('ERROR_:_SelfGenImg!')

    rad = 15
    loopNo = int(pin0[5])
    posY = 0
    boxS = int(SCR_HEIGHT * 0.1)
    
    for i in range(0, 12, 1):#12
        posX = 0
        for j in range(0, 16, 1):
            if (loopNo < 9):
                loopNo += 1
            else:
                loopNo = 0
            val = int(pin0[loopNo])
            if (val == 0):
                val = 5
            pygame.draw.rect(screen, colList0[loopNo], pygame.Rect(posX, posY, 100, 100))
            if (i % 2 == 0):
                pygame.draw.polygon(screen,(0,8 * i,0),((350 - (i * 20),610 + (i * 20)),(200 - (i * 15), 450 - (i * 25)),(450 + (i * 25), -20 + (i * 10))), 1)
                pygame.draw.ellipse(screen,(0 + (j * 12),255 - (i * 15),0),(posX + (i + 5), posY + (j + 5),80,50), 1)
            else:
                pygame.draw.ellipse(screen,(0 + (i * 12),255 - (j * 15),0),(posX + (j + 5), posY + (i + 5),60,30), 1)
                
            pygame.draw.rect(screen, colList3[loopNo], pygame.Rect(posX, posY, 100, 100), val)
            pygame.draw.ellipse(screen,(0 + (i * 11),25 + (j * 13),0),(posX + (j + 3), posY + (i + 7),89,49), 1)#New
            posX += boxS
            
        posY += boxS

    loopNo = int(pin0[8])
    center = int(SCR_WIDTH * .5), int(SCR_HEIGHT * 0.5)
    
    for i in range(0, 32, 1):
        
        if (loopNo < 9):
            loopNo += 1
        else:
            loopNo = 0
        val = int(pin0[loopNo])
        if (val == 0):
            val = 1
            
        if (i % 2 == 1):
            pygame.draw.circle(screen, colList2[val], center, rad, val)
            pygame.draw.polygon(screen,(0,8 * i,0),((350 - (i * 20),610 + (i * 20)),(200 - (i * 15), 450 - (i * 25)),(450 + (i * 25), -20 + (i * 10))), 1)
        else:
            pygame.draw.circle(screen, colList3[val], center, rad, val)
            pygame.draw.circle(screen, colList1[val], (rad, rad), rad + val, 1)
            
        rad += 15

    for i in range(0, qtyLns + adder ):
        for j in range(kP, sL):
            if (j == 5 + i):
                strLine += imgfix
            else:
                strLine += List_Char[j]  
        kP = 0

    for i in range(0, qtyLns + adder , 1):
        dspLine0 = strLine[addNo:addNo + lenNo]
        addNo += lenNo
        gV = aV * i
        if (gV > 250):
             gV = 255
        dspStr0 = font1.render(dspLine0, True, (rV, gV, bV))
        screen.blit(dspStr0, (5, (fontSize * i) + 5)) 
        
    pygame.draw.polygon(screen,colList0[val],((146,0),(291,106),(236,277),(56,277),(0,106)), 2)          
    pygame.draw.polygon(screen,(0,220,0),((-10,610),(400,-10),(810,300)), 1)
    pygame.draw.ellipse(screen,(0,25,255),(250,300,100,200), 1)
    pygame.draw.ellipse(screen,(0,25,255),(200,350,200,100), 1)
    pygame.draw.polygon(screen,(220,20,20),((500,610 + int(pin0[3])),(600 + int(pin0[5]),300),(810+ int(pin0[7]),720)), 1)

    pygame.display.flip()
        
    try:
        rect = pygame.Rect(0, 0, SCR_WIDTH, SCR_HEIGHT)#PosX, PosY, RecSizeX, RecSizeY
        sub = screen.subsurface(rect)
        
        if(rmFile):
            data = pygame.image.tostring(sub, 'RGB')#RGBA_PREMULT RGBX
            imgImg0 = pygame.image.fromstring(data, (SCR_WIDTH, SCR_HEIGHT), 'RGB').convert()
            data = ''
        else:
            pygame.image.save(sub, strPF)
            imgImg0 = pygame.image.load(strPF).convert()
            imgDsp0  = pygame.transform.scale(imgImg0, (240, 160))
        
    except:
        print('ERROR_:_Sub-Image_Save!')
        
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), DOUBLEBUF, COLOR_DEPTH)
    
    
def UpdateImgList():
    
    global imgCount
    global imgPathList
    global setImgMode
    
    try:
        imgPathList.clear()
        imgPathList = glob.glob('Images/*')
        
        if (len(imgPathList) > 0):
            c = 0
            for i in range(len(imgPathList)):
                if (imgPathList[i] == BgImgPath):
                    c = int(i)   
                    imgPathList.remove(imgPathList[c])
        else:
            imgPathList.append('NONE')
            setImgMode = 4 

    except:
        print('ERROR_:UpdateImgList')
        imgPathList.append(BgImgPath)
        
    imgCount = len(imgPathList) - 1


def UpdateImage(filePath):

    global imgImg0
    global imgDsp0 
    global strLine1

    try:
        imgImg0 = pygame.image.load(filePath).convert()
        imgDsp0  = pygame.transform.scale(imgImg0, (240, 160))  
    except:
        imgMode = 3
        output = io.BytesIO(base64.b64decode(strImg0))
        imgImg0 = pygame.image.load(output)
        imgDsp0  = pygame.transform.scale(imgImg0, (240, 160))       
        strLine1 = 'ERR|No_Image:' + filePath
        DrawScreen1()
        pygame.display.flip()
        time.sleep(5)

             
def GenImage(fileName, eOffsetX, eOffsetY, rotation, scaleAddXY, pin0):

    global imgImg0
    global strLine1
    global strData
    
    minZ = 50000

    List_Nums.clear()
    
    if (imgMode != 4):
        UpdateImage(fileName)
    else:
        SelfGenImg(pin0)

    rectX, rectY, sizeX, sizeY =  imgImg0.get_rect()
    
    if (sizeX < 960 or sizeY < 720):
        if (genJunk):
            strLine1 = 'ERROR_:_GenImage-Image_Was_Rescaled!'
            #print(strLine1)
        imgImg0 = pygame.transform.scale(imgImg0, (1000, 800))      
        
    rectX, rectY, sizeX, sizeY =  imgImg0.get_rect()
    offsetX = -int((sizeX - SCREEN_WIDTH) / 2)
    offsetY = -int((sizeY - SCREEN_HEIGHT) / 2)
    
    offsetX += eOffsetX
    offsetY += eOffsetY
    
    imgImg0 = pygame.transform.rotate(imgImg0, rotation)
    imgImg0 = pygame.transform.scale(imgImg0, (sizeX + scaleAddXY, sizeY + scaleAddXY)) 
        
    DrawScreen0(1)
    
    strData = ''
    try:
        rect = pygame.Rect(rectPosX, rectPosY, rectSizeX, rectSizeY)#PosX, PosY, RecSizeX, RecSizeY
        sub = screen.subsurface(rect)
        data = pygame.image.tostring(sub, 'RGB')#RGBA_PREMULT RGBX
        
        img = Image.frombytes('RGB', (rectSizeX, rectSizeY), data)#('RGBA', (64, 64), data)
        zdata = BytesIO()
        img.save(zdata, 'PNG')
        strData = (str(base64.b64encode(zdata.getvalue()))[2:-1])
        zdata.close()
        data = ''
            
    except:
        strLine1 = 'ERROR_:_GenImage-Subsurface_Rectangle_Outside_Surface_Area!'
        print(strLine1)
       
    DrawScreen0(0)

    if (imgMode == 4):
        minZ = 25000

    if (offsetZ > 0 and useZ and len(strData) > minZ):
        strData = strData[offsetZ:]
        strLine1 = 'Generating_Encoding_Algorithm!:Using-Z'
    else:
        strLine1 = 'Generating_Encoding_Algorithm!:No-Z'
        
    if (useX):
        strLine1 += '|Using-X'
    else:
        strLine1 += '|No-X'
    
    DrawScreen1()
    pygame.display.flip()
    Encode0(strData)


def Reset():
    
    global footNote
    global strLine0
    global strLine1
    global strLine3
    global strLine8 
    global strLine12
    global inputNo
    global imgMode
    global rmFile
    
    imgMode = setImgMode
    rmFile = True
    footNote = ''
    strLine0 = ''
    strLine3 = ''
    strLine8 = ''
    strLine12 = ''
    inputNo = 0
    strLine1 = 'Sub_Reset!'
    UpdateDspMsg('', '')
    UpdateImgList()

#==============================================================================

def KMInput():
 
    global strLine0
    global strLine1
    global strLine3
    global charM
    global charNum
    global scrMode
    global setImgMode
    global strNum
    global inputNo
    global logonNo
    global conDel
    global genList
    global BZLCOL
    global confirmDel
    
    useKey = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        elif (event.type == pygame.KEYDOWN):
            
            if (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER):
                UpdateEnter()
                confirmDel = False
                useKey = False
                
            elif (event.key == pygame.K_LCTRL):
                UpdateCTRL(0)
                useKey = False
                
            elif (event.key == pygame.K_RCTRL):
                UpdateCTRL(1)
                useKey = False
            
            elif (event.key == pygame.K_DELETE):
                if (logonNo == 11):
                    if (conDel == False and strUID != strUIDd):
                        strLine1 = 'DEL=CANCEL_DELETE_USER|ENTER=Delete&Exit'
                        conDel = True
                    else:
                        if (strUID != strUIDd):
                            strLine1 = 'DEL=Delete_User|ENTER=Exit'
                        else:
                            strLine1 = 'ERROR:No_Can_Do!|L-ALT=PREV|R-ALT=NEXT'
                            
                        conDel = False 
                else:
                    if (inputNo == 7):
                        
                            if (confirmDel):
                                try:
                                    os.remove((strPath + strName + '.txt'))
                                    strLine1 = 'DELETED_FILE:' + strName + '.txt'
                                    confirmDel = False
                                except:
                                    strLine1 = 'ERROR:Could_Not_Delete_File'
                                try:#Also try to remove Png image 
                                    os.remove((strPath + strName + '.png'))
                                    strLine1 = 'DELETED_FILE:' + strName + '.png'
                                except:
                                    pass
                            else:
                                strLine1 = 'Confirm_Delete=DEL|Cancel_Delete=Enter' 
                                confirmDel = True
                    else:
                        strLine0 = ''
                        strLine1 = 'Deleted_Line/Message!'
                        strNum = ''
                
            elif (event.key == pygame.K_LALT):
                UpdateAlt(0)
                useKey = False
                    
            elif (event.key == pygame.K_RALT):
                UpdateAlt(1)
                useKey = False

            elif (event.key == pygame.K_TAB):
                UpdateTab(0)
                useKey = False
                
            elif (event.key == pygame.K_F1):
                UpdateF1()
                useKey = False
                
            elif (event.key == pygame.K_F2):
                UpdateF2(0)
                useKey = False
                
            elif (event.key == pygame.K_F3):
                UpdateF3(1)
                useKey = False
                
            elif (event.key == pygame.K_F10):
                if (logonNo == 2 and scrMode == 0):
                    UpdateUser(1)#1 = Goto ADD user mode
                useKey = False
                
            elif (event.key == pygame.K_F11):
                if (logonNo == 2 and scrMode == 0):
                    UpdateUser(2)#2 = Goto EDIT user mode
                    UpdateEdit(0)
                useKey = False

            elif (event.key == pygame.K_F12):
                if (logonNo == 2 and scrMode == 0):
                    UpdateUser(3)#3 = Goto DELETE user mode
                    UpdateEdit(0)
                elif (scrMode == 3):
                    if (genList == False):
                        genList = True
                        strLine1 = 'New_Key+ENTER=New/OverWrite_User_List|F12=Cancel'
                    else:
                        genList = False
                        strLine1 = 'ENTER=Logon_To_System|ESC=Quit|F1=Help'

                useKey = False
                
            elif (event.key == pygame.K_ESCAPE):
                
                if (inputNo != 0):
                    Reset()
                else:
                    if (scrMode == 1 or scrMode == 2):
                        scrMode = 0
                        logonNo = 0
                        setImgMode = 0
                        strLine1 = 'Enter=Next/ESC=Return_To_System_Screen'
                        
                    elif (scrMode == 3):
                         scrMode = -1

                    elif (scrMode == 0):
                        if (logonNo != 0):
                            ClearSubWin()
                            logonNo = 0
                        else:
                            BZLCOL = RED
                            strLine1 = 'Enter=Next/ESC=Quit'
                            scrMode = 3
                
                useKey = False
                    
            elif event.key == pygame.K_BACKSPACE:
                if (len(strLine0)>0):
                    strLine0 = strLine0[:-1]
                else:
                    if (inputNo != 0):
                        UpdateTab(0)#inputNo
                        useKey = False
            else:
                if (event.unicode != '~'):
                    if (inputNo == 5 and genJunk):
                        strLine0 += event.unicode.capitalize() 
                    else:
                        strLine0 += event.unicode              

            if (useKey):
                charNum = 0
                charM = '_'
                UpdateChar(strLine0, charM)  
            
        #Mouse input
        pos = pygame.mouse.get_pos()
        posx = pos[0]
        posy = pos[1]#
        
        if (event.type == pygame.MOUSEBUTTONDOWN):
            
            if event.button == LEFT:#Left click
                    UpdateEnter()
                    
            elif event.button == MIDDLE:# Middle click
                if (inputNo == 0 and logonNo > 2):#if (logonNo > 2):
                    if (scrMode != 0):
                        scrMode = 0
                    else:
                        scrMode -= 1
                else:
                    charNum = 0
                    strLine0 += charM
                    UpdateChar(strLine0, charM)
                    charM = '_'
                    UpdateChar(strLine0, charM)

            elif event.button == RIGHT:#Right click
                if (len(strLine0)>0):
                    strLine0 = strLine0[:-1]
                else:
                    if (inputNo == 0 or inputNo ==1):
                        if (scrMode != 3):
                            UpdateCTRL(0)
                    else:
                        UpdateTab(0)#inputNo
                        
                UpdateChar(strLine0, charM)
      
            elif event.button == UP:# Wheel Up
                
                if (inputNo == 0 and logonNo > 2):
                        UpdateAlt(1)
                        
                elif (inputNo == 1):
                    charM = str(charNum)
                    if (charNum < 9):
                        charNum += 1
                    else:
                        charNum = 0
                else:
                    if (charNum < len(List_Char) - 1):
                        charNum += 1
                    else:
                        charNum = 0
                        
                    charM = List_Char[charNum]
                    
                if (inputNo == 5 and genJunk):
                    charM = charM.capitalize()                     
                UpdateChar(strLine0, charM)
                
            elif event.button == DOWN:# Wheel Down
                
                if (inputNo == 0 and logonNo > 2):
                    UpdateAlt(0) 
                    
                elif (inputNo == 1):
                    charM = str(charNum)
                    if (charNum > 1):
                        charNum -= 1
                    else:
                        charNum = 9
                else:
                    if (charNum > 0):
                        charNum -= 1
                    else:
                        charNum = len(List_Char) - 1
                        
                    charM = List_Char[charNum]
                        
                if (inputNo == 5 and genJunk):
                    charM = charM.capitalize() 
                UpdateChar(strLine0, charM)                          


def MaskString(strLine, charA):

    strMask = ''
    n = int(len(strLine))
    for i in range(n):
        strMask += '*'
    if (charA != ''):
        strMask += '[' + charA + ']'   
    return strMask 


def UpdateChar(strLine, charA):
    
    global strLine0 
    global strLine1
    global strLine2
    global strLine3
    global strLine4
    global strLine5
    global strLine6
    global strLine10
    global rectAddY
    global iCan
    global strUIDd
    global strGIDd
    global strPWDd
    
    if (inputNo == 0):

        if (len(strLine) > 19):
            strLine0 = strLine0[:-1]
        
        if (logonNo == 0 or logonNo == 5 or scrMode == 3 ):
            if (scrMode == 3):
                if (showPass == 0):
                    strPWDd = MaskString(strLine, charA)
                else:
                    strPWDd = strLine + '[' + charA + ']'                  
            else:
                strUIDd = strLine + '[' + charA + ']'
            
        elif (logonNo == 1 or logonNo == 6 or logonNo == 9):
            strGIDd = strLine + '[' + charA + ']'
        
        elif (logonNo == 2 or logonNo == 7 or logonNo == 10):

            if (showPass == 0):
                strPWDd = MaskString(strLine, charA)
            else:
                strPWDd = strLine + '[' + charA + ']'         
            
    elif (inputNo == 1):
        
        if (showPin == 0):
            strLine2 = MaskString(strLine, charA) + '_=_' + str(len(strLine0))
        else:
            strLine2 = strLine + '[' + charA + ']' + '_=_' + str(len(strLine0))
                    
    elif (inputNo == 2):
        
        if (showPass == 0):
            strLine3 = MaskString(strLine, charA) + '_=_' + str(len(strLine0))
        else:
            strLine3 = strLine + '[' + charA + ']' 
            
    elif (inputNo == 3):
        strLine4 = strLine  +  '/[' + charA + ']'
        iCan = False

    elif (inputNo == 4):
        strLine5 = strLine + strNum + fileExt + '[' + charA + ']'
        iCan = False

    elif (inputNo == 5):
        
        if (len(strLine) < 501): 
            strLine6 = strLine #+ '[' + charA + ']'
            a = int(len(strLine) / 50)
            totL = 50 - (len(strLine) - a * 50)
            totR = 500 - len(strLine)
            rectAddY = fontSize * a
            if (totR != 0):
                strLine1 = 'Character\'s_left_in_Line=' + str(totL) + '_:_Total=' + str(totR)
            else:
                strLine1 = 'You_Have_No_Characters_Left_Over!'
        else:
            strLine0 = strLine0[:-1]
            strLine1 = 'You_Have_No_Characters_Left_Over!_It\'s_Full!!'

        UpdateDspMsg(strLine6, '[' + charA + ']')
               
    elif (inputNo == 6):
        
        if (len(strLine) < 46): 
            strLine10 = strLine + '[' + charA + ']'
            strLine1 = 'Footnote_NOT_Encrypted!|Character\'s_left_in_Line=' + str(45 - len(strLine))
        else:
            strLine0 = strLine0[:-1]
            strLine1 = 'ERROR_:_Footnote_to_Long'

            
def UpdateEnter():
    
    global strLine0
    global strLine1
    global strLine2
    global strLine3
    global strLine4
    global strLine5
    global strLine6
    global strLine7
    global strLine8
    global strLine10
    global strLine12
    global footNote
    global charM 
    global strKey
    global strPin0
    global inputNo
    global strPath
    global strName
    global charNum
    global canI
    global iCan
    global showPin
    global showPass
    global setImgMode
    global rectAddY
    global sysKey
    global scrMode
    global strPWDd
    global strLine3
    global imgMode
    
    strLine1 = 'None!'
    charNum = 0
    showPass = 0
    showPin = 0
    charM = '_'
    strPWDd = ''

    if (inputNo == 0):
        
        strLine1 = 'Enter=Next(to_Continue)|TAB=Back|ESC=Quit|F1=Help'
        
        if (scrMode == 0):
            UpdateUser(0)
            
        elif (scrMode == 3):
            if (strLine0 != ''):
                sysKey = strLine0
                if (genList):
                    LoadList(0)
                else:
                    LoadList(2)
            else:
                sysKey = preKey
                LoadList(1)
            strLine0 = ''
            scrMode = 0

        else:
            Reset()
            rectAddY = 0
            iCan = False
            strLine1 = 'Enter a 10 digit PIN/press Enter to ues preset PIN!'
            inputNo += 1
            strLine0 = ''          

    elif (inputNo == 1):#)
        
        if (strLine0 != ''):
            try:
                n = int(strLine0)
                if (len(strLine0) == 10):
                    strPin0 = strLine0
                    strLine2 = 'Updated_PIN!'
                    inputNo += 1
                    strLine0 = ''
                    
                else:
                    strLine1 = 'ERROR_:_PIN_Must_Be_10_Digits_Long_And_Not_(' + str(len(strLine0)) + ')!'
                    strLine0 = ''
                    strLine2 = ''
                    
            except:
                strLine1 = 'ERROR_:_PIN_Must_Only_Be_Numbers_And_10_Digits_Long!'
                strLine0 = ''
                strLine2 = ''

        else:
            strLine2 = 'Using_Preset_PIN!'
            strLine1 = 'Key*=Public-Key/Name_of_other_person'
            strKey = ''
            inputNo += 1
            
        showPass = 1
            
    elif (inputNo == 2):#UpdateKey()
        if (strLine0 != ''):
            strKey = strLine0
            if (imgMode != 0 and imgMode != 1 and imgMode != 4):
                UpdatePIN(strPin0, strKey, 0)
                    
            strLine3 = 'Updated_Key!'
            strLine1 = 'Enter new Path/press Enter to use preset Path!'
            inputNo += 1
            strLine0 = ''            
        else:
            strLine1 = 'ERROR:Must_Enter_Public-Key/Name_of_other_person!'
        
    elif (inputNo == 3):#Update File Path
        if (strLine0 != ''):
            strPath = strLine0 + '/'
            strLine4 = strPath
        else:
            strLine4 = strPath
            
        strLine1 = 'Enter a File-Name/press Enter to use preset Name!'
        inputNo += 1
        strLine0 = ''
    
    elif (inputNo == 4):#Update encoded file name
        if (strLine0 != ''):
            strName = strLine0
            strLine5 = strLine0 
        else:
            strLine5 = strName
            
        strLine1 = 'Type an Encrypted message/press Enter to read file!'
        inputNo += 1
        strLine0 = strLine12
         
    elif (inputNo == 5):#Update message
        
        if (strLine0 != ''):
            
            a = int(len(strLine0) / 50)
            totL = 50 - (len(strLine0) - a * 50)
            
            if (totL < 50 and genJunk):
                for i in range(totL):
                    strLine0 += '_'
                    
            strLine1 = 'Press Enter To Encode or Type To Continue!'
            UpdateChar(strLine0, charM)

            if (totL == 50 or genJunk == False):
                strLine1 = 'Footnote (NOT ENCRYPTED!!)/press Enter To Continue!'
                strLine12 = strLine0
                strLine0 = footNote
                inputNo = 6 
                UpdateChar(footNote, '_')
        else:
        
            strLine1 = 'Decoded_:_' + strLine5 + '_:_Press_Enter_To_Continue!'
            ReadFile0()#Read coded file
            strLine7 = strLine8
            inputNo = 7
            
    elif (inputNo == 6):
        
        if (strLine0 != ''):
            footNote = strLine0
            
        canI = CheckForFile(canI)
                
        if (canI or iCan):
            
            imgMode = setImgMode

            if (imgMode == 0 or imgMode == 1 or imgMode == 4):
                
                if (imgMode == 0):# or imgMode == 1):
                    WriteImage()
                
                strPin1 = GenPin1(strName)#
                if (strPin1 != 'None'):
                    UpdatePIN(strPin1, strKey, 0)
                else:
                    UpdatePIN(strPin0, strKey, 0)
            
            if (genJunk):
                strAdd = ''
                rndC = random.randrange(1, 5)
                for i in range(rndC):
                    strAdd += '~'
                strLine12 = strAdd + strLine12
            Encode1(strLine12)#strLine6 strLine0
            strLine6 = ''
            WriteFile0(List_Nums)
            ReadFile0()
            inputNo = 7 
            strLine0 = strName # 
            strLine1 = 'Encoded_File_Name_:_' + strLine5 +'.txt'
            iCan = False
            
        else:   
            strLine0 = strPath # if inputNo = 3
            if (len(strLine0) > 0):
                strLine0 = strLine0[:-1]
            inputNo = 3
            iCan = True

    elif (inputNo == 7):#Result
        strLine1 = 'Enter new Path/press Enter to use preset Path!'
        strLine0 = ''# strName #
        strLine5 = strLine0
        
        if (imgMode != 0 and imgMode != 1 and imgMode != 4):
            inputNo = 3
        else:
            inputNo = 1
            
        footNote = ''
        strLine3 = ''
        strLine8 = ''
        strLine12 = ''
        iCan = False
        rectAddY = 0
        UpdateDspMsg('', '')


def UpdateCTRL(num):
    
    global scrMode
    global setImgMode
    global inputNo
    global logonNo
    global editMode 
    global crptMode
    global fileExt
    global strPath
    global strLine0
    global strLine1
    global strLine4
    global strLine7
    global strLine8
    global strLine13
    
    if (scrMode !=0 and scrMode != 3):
        if (inputNo == 0):
            
            if (num == 0):
                if (setImgMode > 0):
                    setImgMode -= 1
                else:
                    setImgMode = 4                
            else:
                if (setImgMode < 4):
                    setImgMode += 1
                else:
                    setImgMode = 0

            if (setImgMode == 0):
                strLine1 = 'Image_Mode:0_(Save_Selected_Image_With_Encryption)'
            elif (setImgMode == 1):
                strLine1 = 'Image_Mode:1_(Select_Image_Use_pin_algorithm-0)'                
            elif (setImgMode == 2):
                strLine1 = 'Image_Mode:2_(Select_Image_Use_pin_algorithm-1)'
            elif (setImgMode == 3):
                strLine1 = 'Image_Mode:3_(Use_One_Image_For_Multible_Mesages)'
            elif (setImgMode == 4):
                strLine1 = 'Image_Mode:4_(Self-Gen_Image)'            
                
        elif (inputNo == 3):
            UpdateFolder(num + 1) 

        elif (inputNo == 4):
            UpdateFile(num + 1)
 
        elif (inputNo == 5 and len(strLine0) > 0):
            if (fileExt == '.txt' or fileExt == '.png'):#Lock out the other if in png mode
                if (num == 1):
                    if (crptMode < 3):
                        crptMode += 1
                    else:
                        crptMode = 0
                else:
                    if (crptMode > 0):
                        crptMode -= 1
                    else:
                        crptMode = 3
            else:
                crptMode = 0
                
            if (crptMode == 0):
                strLine1 = 'Crypto_Mode-0_(Std_Number_Mode)'
            elif (crptMode == 1):
                strLine1 = 'Crypto_Mode-1_(Duel_Scamble_Mode)'                
            elif (crptMode == 2):
                strLine1 = 'Crypto_Mode-2_(Number_To_Alphabet_Mode)'
            elif (crptMode == 3):
                strLine1 = 'Crypto_Mode-3_(Std_Number_Mode)'
          
        elif (inputNo == 6):
            UpdateF2(3)
            
        elif (inputNo == 7):
            inputNo = 3
            strLine7 = ''
            strLine8 = ''
            strLine13 = ''
        else:
            strLine1 = 'CTRL_Has_No_Function_At_This_Time!'


def UpdateFolder(num):#Gen folder name or make folder list

    global folderList
    global folderNo
    global strPath
    global strLine1
    global strLine4
    
    try:
        folderList.clear()
        tempList = glob.glob("*")
        
        if (len(tempList) > 0):
            for i in range(len(tempList)):
                if (tempList[i] != 'Settings' and ((tempList[i])[-3:]) != '.py' and tempList[i] != 'Images'):
                   folderList.append(tempList[i])
        else:
             os.mkdir(strPath)
               
        try:

            if (num == 0):
                folderNo = 0
            elif (num == 1):
                if (folderNo > 0):
                    folderNo -= 1
                else:
                    folderNo = len(folderList) - 1                    
            elif (num == 2):
                if (folderNo < len(folderList) - 1):
                    folderNo += 1
                else:
                    folderNo = 0                    
            elif (num == 3):
                strPath = "eDocs/"
            elif (num == 4):
                strPath = strKey + '/'
            else:
                strPath = "hello/"
            
            if (len(tempList) > 0):
                if (num < 3):
                    strPath = folderList[folderNo] + "/"
                    strLine4 = strPath                    
                else:
                    folderNo = 0
                    strLine4 = strPath
            else:
                strLine1 = "ERROR:Folder_Empty!"
                
        except:
            folderNo = 0
            strPath = "hello/"
            strLine4 = strPath
            
    except:
        strLine1 = "Error:def UpdateFolder!"
    
    UpdateChar((strPath)[:-1], '')
    

def UpdateFile(num):#Gen file name/make file list/change file format

    global fileList
    global fileNo
    global strName
    global strLine0
    global strLine1
    global strLine5
    global fileExt
    global strPin0
    global selFileType
    global strAdd
    
    try:
        fileList.clear()
        tempList = glob.glob((strPath + "*" + fileExt))    
        for i in range(len(tempList)):
            fileList.append((tempList[i])[len(strPath):-4])

        try:
            if (num == 0):#Reset
                fileNo = 0
                selFileType = 0
                
            elif (num == 1):#File list down
                if (fileNo > 0):
                    fileNo -= 1
                else:
                    fileNo = len(fileList) - 1        
            elif (num == 2):#File list up
                if (fileNo < len(fileList) - 1):
                    fileNo += 1
                else:
                    fileNo = 0
            elif (num == 3):#Toggle file ext .txt-.png
                
                strName = ''
                
                if (selFileType == 0):
                    selFileType = 1
                    fileExt = '.txt'
                    strAdd = '-'
                    
                elif (selFileType == 1):
                    selFileType = 2
                    fileExt = '.png'
                    strAdd = '-'
                    
                elif (selFileType == 2):
                    selFileType = 3
                    if (imgMode == 0 or imgMode == 1 or imgMode == 4):
                        strAdd = '^'
                    else:
                        strAdd = '-'
                    fileExt = '.txt'
                    
                elif (selFileType == 3):
                    selFileType = 0
                    if (imgMode == 0 or imgMode == 1 or imgMode == 4):
                        strAdd = '^'
                    else:
                        strAdd = '-'
                    fileExt = '.png'
                    
                if (strAdd == '^'):
                    strLine1 = 'New_File_Extention(' + fileExt  + '):Press_R-ALT=Auto-PIN'#':Auto-PIN=Yes'
                else:
                    strLine1 = 'New_File_Extention(' + fileExt  + '):Press_R-ALT=Time-Stamp'#':Auto-PIN=No'

                fileNo = 0
                
            elif (num == 4):
                
                strNew = time.strftime("%D%H%M%S", time.localtime())
                strTime = ''
                
                for i in range (len(strNew)):
                    if (strNew[i] != '/'):
                        strTime += strNew[i]

                if (strLine0 == ''):
                    strName = docName + strAdd + strTime
                else:
                    strName = strLine0 + strAdd + strTime
                strLine1 = 'Auto-PIN/Time-Stamp:New_Name:' + strName
            else:
                fileNo = 0
                strName = "hello"
                
            if (len(fileList) > 0):
                if (num == 3):
                    strName = ''
                elif (num == 4):
                    pass
                else:
                    strName = fileList[fileNo]
            else:
                if (num != 3 and num != 4):
                    strLine1 = "ERROR:Folder_Empty!"
        except:
            strLine1 = "ERROR:Folder_Empty(2)!"
            strName = ''
            
        strLine0 = strName
        strLine5 = strName
        UpdateChar(strName, '')
        
    except:
        print("Error:def UpdateFile!(2)")
        

def GenPin1(stLine):

    try:
        listMain = stLine.split('^')
        strTime = listMain[1]

        intA = int(strTime[:4])
        intB = int(strTime[-3:])
        intC = int(strTime[4:8])
        intD = int(strTime[5:9])

        intE = (intA * intB * intC * intD + intA + intB + intC + intD)
        
        strPin1 = str(intE)[:10]
        
        if (len(strPin1) < 10):
            for i in range(10 -len(strPin1)):
                strPin1 += '5'

        return strPin1

    except:
        return 'None'


def UpdateAlt(num):
    
    global imgNo
    global strNum
    global strLine0
    global strFn2
    global strLine1
    global showPin
    global showPass
    global maskMsg 
    global rmFile
    
    if (num == 0):#Left ALT Key
        
        if (inputNo == 0):
            
            if (scrMode == 0):
                if (logonNo == 8 or logonNo == 11 and conDel == False):
                    UpdateEdit(2)
                else:
                    showPass = 0
                    UpdateChar(strLine0, '*') 
                    
            elif (scrMode == 1 or scrMode == 2):
                if (imgNo > 0):
                    imgNo -= 1
                else:
                    imgNo = imgCount

                strLine1 = 'No:' + str(imgNo) + '_:_Path:' + imgPathList[imgNo]
                UpdateImage(imgPathList[imgNo])
                
            elif (scrMode == 3):
                showPass = 0
                UpdateChar(strLine0, '*') 

        elif (inputNo == 1):
            showPin = 0
            UpdateChar(strLine0, '*')
            
        elif (inputNo == 2):
            showPass = 0
            UpdateChar(strLine0, '*')
            
        elif (inputNo == 3):
            UpdateFolder(3)
            
        elif (inputNo == 4):
            UpdateFile(3)
            
        elif (inputNo == 5 or inputNo == 7):#Main encrypted message
            UpdateF3(-1)
                
        elif (inputNo == 6):#Scroll footnote
            UpdateF2(1)
        
    else:#Right ALT Key

        if (inputNo == 0):

            if (scrMode == 0):
                if (logonNo == 8 or logonNo == 11 and conDel == False):
                    UpdateEdit(1)
                else:
                    showPass = 1
                    UpdateChar(strLine0, '_')                    

            elif (scrMode == 1 or scrMode == 2):         
                if (imgNo < imgCount):
                    imgNo += 1
                else:
                    imgNo = 0
             
                strLine1 = 'No:' + str(imgNo) + '_:_Path:' + imgPathList[imgNo]
                UpdateImage(imgPathList[imgNo])
                
            elif (scrMode == 3):
                showPass = 1
                UpdateChar(strLine0, '_')

        elif (inputNo == 1):
            showPin = 1
            UpdateChar(strLine0, '_')
            
        elif (inputNo == 2):
            showPass = 1
            UpdateChar(strLine0, '_')
        
        elif (inputNo == 3):
            UpdateFolder(4)
            
        elif (inputNo == 4):
            UpdateFile(4)
            
        elif (inputNo == 5 or inputNo == 7):#Main encrypted message
            UpdateF3(1)
                
        elif (inputNo == 6):#Use preset footnote
            UpdateF2(2)

        
def UpdateTab(num):#inputNo
    
    global inputNo
    global strLine0
    global strLine12
    global logonNo
    
    if (inputNo == 5):
        strLine12 = strLine0
        
    strLine0 = ''
    
    if (inputNo == 6):
        strLine0 = strLine12
          
    if (inputNo != 0):
        if (num == 0):
                
            if (inputNo > 1):
                inputNo -= 1
            else:
                inputNo = 1
                
        else:
            if (inputNo < 6):
                inputNo += 1
            else:
                inputNo = 1               
    else:

        if (num == 0):
            
            if (logonNo != 11):
                if (logonNo != 0 and logonNo != 5 and logonNo != 8):
                    logonNo -= 1
                else:
                    logonNo += 2   
        else:
            if (logonNo < 2):
                logonNo += 1
            else:
                logonNo = 0
                
                
def UpdateF1():#Update F1 Help
    
    global strLine1
    
    if (inputNo == 0):
        if (logonNo == 0):
            if (scrMode == 3):
                strLine1 = 'F12=Create-Overwrite(User-List_&_System_Key)'
            else:
                strLine1 = 'User-Name_&_Password/Your_Public-Key_no_Password' 
        elif (logonNo == 1):
            strLine1 = 'Group-Name/Group_Public-Key/Leave_Empty=Auto-Fill' 
        elif (logonNo == 2):
            strLine1 = 'Password_&_Enter|Administrator-Enter/F10/F11/F12'
        elif (logonNo == 5):
            strLine1 = 'Add_A_New_User_Name|ENTER=Next|TAB=Back|ESC=Exit'
        elif (logonNo == 6):
            strLine1 = 'Enter_A_New_User_ID|ENTER=Next|TAB=Back|ESC=Exit'
        elif (logonNo == 7):
            strLine1 = 'Enter_A_New_User_Password|ENTER=Save&Exit|TAB=Back'
        elif (logonNo == 8):
            strLine1 = 'L-ALT=Prev-User|R-ALT=Next-User|ENTER=Next|ESC=Exit'
        elif (logonNo == 9):
            strLine1 = 'Enter_A_New_User_ID|ENTER=Next|TAB=Back|ESC=Exit'
        elif (logonNo == 10):
            strLine1 = 'Enter_A_New_User_Password|ENTER=Save&Exit|TAB=Back'
        elif (logonNo == 11):
            strLine1 = 'L-ALT=Prev|R-ALT=Next|DEL=Delete|ENTER=Delete&Exit'
        else:
            strLine1 = 'L/R-ALT=Select_Image|L/R-CTRL=Image-Mode'
            
    elif (inputNo == 1):   
        strLine1 = 'L-ALT=Hide_PIN|R-ALT=Show_PIN|PIN[Numbers_Only_*10]'
    elif (inputNo == 2):   
        strLine1 = 'L-ALT=Hide_Key|R-ALT=Show_Key|ESC=Back|ESC*3=Quit'    
    elif (inputNo == 3):   
        strLine1 = 'L/R-CTRL=Find_Path|L/R-ALT=Auto_Path_Gen'     
    elif (inputNo == 4):   
        strLine1 = 'L/R-CTRL=Find_File|L-ALT=Format|R-ALT=Auto_File&PIN'    
    elif (inputNo == 5):   
        strLine1 = 'DEL=Delete_All|BACK=Back_1|ENTER*2=Next|TAB=Back'    
    elif (inputNo == 6):   
        strLine1 = 'L-ALT=Save_Footnote(1)|R-ALT>>>=Use_Footnote(1-3)'   
    elif (inputNo == 7):
        strLine1 = 'ECS=SubReset|ALT=Mask|DEL=Delet_File|L/R-CTRL=Rt'
    else:
        strLine1 = 'UpdateF1_:_Sorry_Out_of_Range!'

def UpdateF2(num):#Update F2 Footnote
    
    global strFn2
    global strLine0
    global strLine1
    global caseNo
    
    aNum = 'N'
    bNum = 'N'
    cNum = 'N'

    if (strKey == strGID):
        strInfo = strGID
    else:
        strInfo = strUID
                
    if (BZLCOL == BLACK):#Logon system is true
        aNum = 'Y'
    if (logonNo == 4):#Logon user is true
        bNum = 'Y'
    if (useZ):#Use offsetZ is true
        cNum = 'Y'

    if (num == 0 or num == 1):
        if (caseNo < 2):
            caseNo += 1
        else:
            caseNo = 0
            
    if (caseNo == 0):
        strLine1 = strFn2
    elif (caseNo == 1):
        strLine1 = 'Key*=' + strInfo + '|Img-Mode=' + str(setImgMode) + ':' + str(crptMode) + '|Logon=' + aNum + bNum + cNum + '|' + osName
    else:
        strLine1 = platform.platform()

    if (num == 0):#Footnote info
        UpdateChar('', '')
        
    elif (num == 1 or num == 2):#Use footnote next
        strLine0 = strLine1
        UpdateChar(strLine0, '')
        
    elif (num == 3):#Save preset foot note
        strFn2 = strLine0
        UpdateChar(strLine0, '')
        strLine1 = 'Saved_New_Preset_Footnote!'
        caseNo = 0

    else:
        strLine1 = 'ERROR:Footnote_Out_Of_Range!'
        

def UpdateF3(num):#F3 Mask message
    
    global maskMsg
    
    maskMsg += num
    
    if (maskMsg < 0):
        maskMsg = 2
    elif (maskMsg > 2):
        maskMsg = 0
     
def SaveList():
    
    global genJunk
    global imgMode
    global strPath
    global strLine1
    global strName
    
    oldPath = strPath
    oldName = strName

    genJunk = False
    imgMode = sysImgMode
    content = ''
    strPath = 'Settings/'
    strName = 'publicList'

    UpdatePIN(sysPin, sysKey, 0)#Internal password  SaveList() = LoadList(num) must be the same
    
    try:
        for sub_List in List_Users:
            subContent = '+'.join(sub_List) + '/'
            content += subContent
    except:
        print('ERROR_:_ListToString-Out_Of_Range!')

    Encode1(content)
    WriteFile0(List_Nums)

    strPath = oldPath 
    strName = oldName 
    genJunk = True
    imgMode = 0
    content = ''
    strLine1 = 'Updated_User_List'

def LoadList(num):
    
    global genJunk
    global imgMode
    global strPath
    global strName
    global BZLCOL
    global sysSave
    
    oldPath = strPath
    oldName = strName

    genJunk = False
    imgMode = sysImgMode
    content = ''
    strPath = 'Settings/'
    strName = 'publicList'
    
    List_Users.clear()
    #0=Create encrypted user list | 1=Use Default user list | 2=Load encrypted user list
    try:
        if (num == 0):#Create preset user list
            BZLCOL = WHITE
            List_Users.append(['Admin', 'admin', 'userID0'])
            List_Users.append(['Max', 'dog', 'userID1'])
            List_Users.append(['Cody', 'cat', 'userID2'])
            List_Users.append(['Group0', 'jumbo', 'GroupID0'])
            SaveList()
            BZLCOL = BLACK
            
        elif (num == 1):#Use preset user list (no system login)
            BZLCOL = ORANGE
            sysSave = False
            #Make your own default list!
            List_Users.append(['Admin', 'admin', 'userID0'])
            List_Users.append(['Max', 'dog', 'userID1'])
            List_Users.append(['Cody', 'cat', 'userID2'])
            List_Users.append(['Group0', 'jumbo', 'GroupID0'])
   
        elif (num == 2):#Load user list (system login)
            BZLCOL = WHITE
            sysSave = True
            UpdatePIN(sysPin, sysKey, 1)#Internal password  SaveList() = LoadList(num) must be the same
            ReadFile0()
            List_Users.clear()
            content = strLine8.split('/')
    
            for i in range(len(content) - 1):
                subList = content[i]
                subList = subList.split('+')
                List_Users.append(subList)
            if (List_Users[0][0] == 'Admin'):
                BZLCOL = BLACK
                for i in range(len(List_Users)):
                    if (len(List_Users[i]) != 3):
                        BZLCOL = RED
                        break
            else:
                BZLCOL = RED
    except:
        BZLCOL = RED
        strLine1 = 'ERROR_:_LoadList-Out_Of_Range!'

    strPath = oldPath 
    strName = oldName 
    genJunk = True
    imgMode = 0
    content = ''  
    
def ClearSubWin():

    global strUID
    global strGID
    global strPWD
    global strUIDd
    global strGIDd
    global strPWDd
    global strNewUID
    global strNewGID
    global strNewPWD
    global strLine0
    global charM
    
    strPWD = ''
    strUIDd = ''
    strGIDd = ''
    strPWDd = ''
    strNewUID = ''
    strNewGID = ''
    strNewPWD = ''
    strLine0 = ''
    charM = ''
    
    UpdateChar('', '')
    
def UpdateUser(num):

    global strLine0
    global strLine1
    global strUID
    global strGID
    global strPWD
    global strUIDd
    global strGIDd
    global strPWDd
    global logonNo
    global scrMode
    global strNewUID
    global strNewGID
    global strNewPWD
    
    try:
        strNewADM = List_Users[0][0]
    except:
        print('ERROR_:_UpdateUser-List_Is_Empty!')


    if (logonNo == 0):
        strUID = strLine0
        if (strLine0 != ''):
            logonNo = 1
        else:
            strLine1 = 'ERROR:Must_Enter_User-Name/Public-Key!|F1 for Help!'
        strUIDd = strUID
      
    elif (logonNo == 1):
        
        if (strLine0 != ''):
            strGID = strLine0
        else:
            strGID = 'Group0'
        strGIDd = strGID   
        logonNo = 2
        strLine1 = 'Enter=Next(to_Continue!)|ESC=Exit|TAB=Back|F1=Help'
        
    elif (logonNo == 2):
        
        if (strLine0 != ''):
            
            newPWD, newUID = UserSearch(strUID, '', 0)
            
            if (newUID != ''):
                
                if (newPWD == strLine0):

                    strPWD = strLine0
                    if (num == 0):#Normal Logon
                        logonNo = 4
                        scrMode = 2
                    elif (num == 1 and strUID == strNewADM):#Add user logon
                        logonNo = 5
                        strLine1 = 'ADD_USER|Enter=Next|ESC=Exit or F1 for Help!'
                    elif (num == 2 and strUID == strNewADM):#Edit user logon
                        logonNo = 8
                        strLine1 = 'EDIT_USER|Enter=Next|ESC=Exit or F1 for Help!'                        
                    elif (num == 3 and strUID == strNewADM):#Delete user logon
                        logonNo = 11
                        strLine1 = 'DELETE_USER|Enter=Next|ESC=Exit or F1 for Help!'
                    else:
                        logonNo = 4
                        scrMode = 2
                        
                    ClearSubWin()
                else:
                    logonNo = 0
                    strLine1 = 'Password_Incorrect!'
                    strPWD = ''
                    time.sleep(2)
                    ClearSubWin()
                    #print(strLine1)
            else:
                logonNo = 0
                strLine1 = 'No_Such_User!'
                time.sleep(2)
                ClearSubWin()
                #print(strLine1) 
        else:
            ClearSubWin()           
            logonNo = 3
            scrMode = 2

    elif (logonNo == 3):#Quick logon no password
        
        strUID = strUIDd
        strGID = strGIDd
        strPWD = strPWDd
        logonNo == 3
        scrMode = 2
        
    elif (logonNo == 4):#Not used
        logonNo = 5
        
    elif (logonNo == 5):#Edit ADD new User to List 

        if (strLine0 != ''):
            newPWD, newKey = UserSearch(strLine0, '', 0)
            if (newPWD == '' and newKey == ""):
                strNewUID = strLine0
                logonNo = 6
            else:
                strLine1 = 'All_Ready_Used!'
                strUIDd = strLine1
        else:
            strLine1 = 'Must_Have_Name!'
            strUIDd = strLine1

    elif (logonNo == 6):#Edit User List Screen
        
        if (strLine0 != ''):
            newPWD, newKey = UserSearch(strLine0, '', 2)

            if (newPWD == '' and newKey == ""):
                strNewGID = strLine0
                logonNo = 7
            else:
                strLine1 = 'All_Ready_Used!'
                strGIDd = strLine1
        else:
            strLine1 = 'Must_Have_Key!'
            strGIDd = strLine1       
        
        
    elif (logonNo == 7):#Edit User List Screen

        if (strLine0 != ''):
            strNewPWD = strLine0
            sub_List = [strNewUID, strNewPWD, strNewGID]
            List_Users.append(sub_List)
            if (sysSave):
                SaveList()
            ClearSubWin()
            logonNo = 0
        else:
            strPWDd = 'Must_Have_Password!'
            
    elif (logonNo == 8):#Edit User List User Name
        logonNo = 9

    elif (logonNo == 9):#Edit User List User ID
        if (strLine0 != ''):
            strNewGID = strLine0
            UpdateEdit(5)
        logonNo = 10

    elif (logonNo == 10):#Edit User List User Password
        
        if (strLine0 != ''):
            strNewPWD = strLine0
            UpdateEdit(6)
            print('logonNo == 10 - Save and exit')
        if (sysSave):
            SaveList()
        ClearSubWin()
        logonNo = 0
        
    elif (logonNo == 11):#Delete User from List
        
        if (conDel):
            UpdateEdit(3)
            if (sysSave):
                SaveList()
        else:
            strLine1 = 'L-ALT=User-Prev|R-ALT=User-Next|'
            
        ClearSubWin()
        logonNo = 0

    else:
        print('UpdateUser_:_Out_of_Range!')
        ClearSubWin()
        logonNo = 0

    strLine0 = ''
    
    
def UpdateEdit(num):
    
    global strUIDd
    global strGIDd
    global strPWDd
    global indexNo
    global strLine1
    
    totU = len(List_Users) -1 

    if (num == 0):#Look-see mode
        strLine1 = 'L-ALT=Prev-User|R-ALT=Next-User|ENTER=Next'
                    
    elif (num == 1):#Look-see mode up
        strLine1 = 'USER-NUMBER_|_' + str(indexNo + 1) + '_of_' + str(totU + 1)

        if (indexNo < totU):
            indexNo += 1
        else:
            indexNo = 0

    elif (num == 2):#Look-see mode up
        strLine1 = 'USER-NUMBER_|_' + str(indexNo + 1) + '_of_' + str(totU + 1)

        if (indexNo > 0):
            indexNo -= 1
        else:
            indexNo = totU 
            
    elif (num == 3):#DELETE
        if (strUIDd != strUID):
            UserRemove(strUIDd)
            indexNo = 0
        else:
            strLine1 = 'YOU_CANOT_DELETE_YOURSELF'

    elif (num == 5):#Edit update users users Key
        EditUser(strUIDd, strNewGID, 2)
        strLine1 = 'Updated_The_Public_Key_of_' + strUIDd
            
    elif (num == 6):#Edit update users users Password
        EditUser(strUIDd, strNewPWD, 1)
        strLine1 = 'Updated_The_Password_of_' + strUIDd

    try:
        subList = List_Users[indexNo]
        strUIDd = subList[0]
        strGIDd = subList[2]
        strPWDd = subList[1]
    except:
        indexNo = 0
        strUIDd = 'Empty'
        strGIDd = 'Empty'
        strPWDd = 'Empty'        
        
def UserSearch(search, passwd, num):#Check logon password

    global strLine1
    global listNo
    
    passwd = ''
    userid = ''
    listNo = 0
    
    try:
        for sublist in List_Users:
            listNo += 1
            if (sublist[num] == search):
                passwd = sublist[1]
                userid = sublist[2]
                break
    except:
        strLine1 = 'ERROR_:_UserSearch-Out_Of_Range!'
        print(strLine1)

    return (passwd, userid)

def EditUser(search, newStr, num):

    global strLine1
    
    try:
        for sub_List in List_Users:
    
            if (sub_List[0] == search):
                sub_List.pop(num)
                sub_List.insert(num, newStr)
                break
    except:
        strLine1 = 'ERROR_:_EditUser-Out_Of_Range!'
        print(strLine1)   

def UserRemove(search):
    
    global strLine1
    global conDel
    
    try:
        i = 0
        for sub_List in List_Users:
    
            if(sub_List[0] == search):
                List_Users.remove(List_Users[i])
                strLine1 = 'DELETE_USER!_:_' + search
                ClearSubWin()
                break
            i += 1
    except:
        strLine1 = 'ERROR_:_Could_Not_DELETE_USER!' + search
        print(strLine1)
        
    conDel = False
   

def UpdateDspMsg(strLine, strExt):
    
    global strLine13
    
    if (strExt != '[_]'):
        strLine13 = strLine + strExt
    else:
        strLine13 = strLine # + strExt

    
#==============================================================================
            
def DrawScreen0(scrMode0):#Back screen
    
    if (scrMode0):
        
        screen.fill(ORANGE)
        screen.blit(imgImg0, (offsetX , offsetY))
        screen.blit(hudStr7, (rectPosX + 120, rectPosY + 10))
        screen.blit(hudStr8, (rectPosX + 20, rectPosY + 10))
        screen.blit(hudStr9, (rectPosX + 70, rectPosY + 10))
        screen.blit(hudStr10, (rectPosX + 95, rectPosY + 15))
        
        pygame.draw.rect(screen, RED, pygame.Rect(rectPosX - 2, rectPosY - 2, rectSizeX + 4, rectSizeY + 4), 1)
        
        if (debug):
            pygame.display.flip()
            time.sleep(5)

    else:
        screen.fill(GREEN)
        screen.blit(imgImg1, (0 , 0))
        
        pygame.draw.rect(screen, GREEN, pygame.Rect(9, 13, 588, 20))
        pygame.draw.rect(screen, BZLCOL, pygame.Rect(5, 10, 595, 25), 2) 
        pygame.draw.rect(screen, WHITE, pygame.Rect(15, 195, 360, 70))
        pygame.draw.rect(screen, BZLCOL, pygame.Rect(10, 190, 370, 80), 2)
        
        if (scrMode == 0 and logonNo < 3):
            
            hudStr1 = font1.render('LOGON| %s' %strLine1[:53], True, WHITE)#strLine1 inputNo
            hudStr2 = font1.render('USER_NAME_| %s' %strUIDd, True, RED)#strLine1 inputNo
            hudStr3 = font1.render('GROUP_NAME| %s' %strGIDd, True, GREEN)#strLine1 inputNo
            hudStr4 = font1.render('PASSWORD__| %s' %strPWDd, True, BLACK)#strLine1
            
            screen.blit(hudStr1, (15, 15))
            screen.blit(hudStr2, (20, 200))
            screen.blit(hudStr3, (20, 220))
            screen.blit(hudStr4, (20, 240))
            
            pygame.draw.rect(screen, BLACK, pygame.Rect(15, logonNo * 20 + 200, 360, 18), 1)
            
        else:
            
            hudStr1 = font1.render('EDIT| %s' %strLine1[:53], True, WHITE)#strLine1 inputNo
            hudStr2 = font1.render('USER_NAME_| %s' %strUIDd, True, RED)#strLine1 inputNo
            hudStr3 = font1.render('PUBLIC_KEY| %s' %strGIDd, True, GREEN)#strLine1 inputNo
            hudStr4 = font1.render('PASSWORD__| %s' %strPWDd, True, BLACK)#strLine1
                
            screen.blit(hudStr1, (15, 15))
            screen.blit(hudStr2, (20, 200))
            screen.blit(hudStr3, (20, 220))
            screen.blit(hudStr4, (20, 240))
            
            if (logonNo > 4 and logonNo < 8):
                posY = (logonNo - 5) * 20 + 200
            elif (logonNo > 7 and logonNo < 11):
                posY = (logonNo - 8) * 20 + 200
            else:
                posY = (logonNo - 11) * 20 + 200
            
            if (conDel):
                pygame.draw.rect(screen, RED, pygame.Rect(15, 200, 360, 60), 1)
            else:
                pygame.draw.rect(screen, BLACK, pygame.Rect(15, posY, 360, 18), 1)         
    
def DrawScreen1():#Main screen
    
    screen.fill(ORANGE)
    
    if (logonNo == 4):
        hudStr1 = font1.render('Msg~|%s' %strLine1[:53], True, BLACK)#strLine1
    else:
        hudStr1 = font1.render('Msg~|%s' %strLine1[:53], True, RED)#strLine1 
    hudStr2 = font1.render('PIN#|%s' %strLine2[:53], True, GREEN)
    hudStr3 = font1.render('Key*|%s' %strLine3[:53], True, GREEN)
    hudStr4 = font1.render('Path|%s' %strLine4[:53], True, GREEN)
    hudStr5 = font1.render('Name|%s' %strLine5[:53], True, GREEN)
    if (maskMsg > 1):
        hudStr6 = font1.render('Msg#|Masked' , True, RED)#strLine6 strLine9
    else:
        hudStr6 = font1.render('Msg#|%s' %strLine9 , True, GREEN)#strLine6 strLine9

    if (len(strLine10) < 50):
         hudStr7 = font1.render('Msg@|%s' %strLine10, True, GREEN)#strLine1 strLine10 strLine12 canI
    else:
        hudStr7 = font1.render('Msg@|ERROR_:_', True, RED)#strLine1 strLine10 strLine12 canI
      
    if (maskMsg == 0):
        hudStr8 = font1.render('Msg=|%s' %strLine11, True, GREEN)#strLine11
    else:
        hudStr8 = font1.render('Msg+|Mask_Mode:%s' %str(maskMsg), True, RED)#strLine6 strLine9

    
    screen.blit(imgImg1, (0 , 0))
    
    pygame.draw.rect(screen, BZLCOL, pygame.Rect(5, 5, 595, 175), 2)
    pygame.draw.rect(screen, WHITE, pygame.Rect(10, 10, 585, 165))#, 2

    screen.blit(hudStr1, (15, 15))
    screen.blit(hudStr2, (15, 35))
    screen.blit(hudStr3, (15, 55))
    screen.blit(hudStr4, (15, 75))
    screen.blit(hudStr5, (15, 95))
    screen.blit(hudStr6, (15, 115))
    screen.blit(hudStr7, (15, 135))
    screen.blit(hudStr8, (15, 155))

    pygame.draw.rect(screen, BLACK, pygame.Rect(10, inputNo * 20 + 15, 50, 18), 1)

    
def DrawScreen2(strLine):#Long message text screen draw auto header    
    
    global curNum
    global strLine9
    global strLine11
     
    addNo = 0
    
    if (maskMsg > 0):
        strLine = MaskString(strLine, '')
    
    pygame.draw.rect(screen, BZLCOL, pygame.Rect(5, 185, 595, 220), 2)
    pygame.draw.rect(screen, GREEN, pygame.Rect(10, 190, 585, 210))#, 2

    if (inputNo == 5):
        if (curNum < 15):
            strLine = strLine + '|'
        elif (curNum < 30):
            strLine = strLine + ' '
        else:
            curNum = 0
        curNum += 1
            
    for i in range(0, qtyLns, 1):
        dspLine0 = strLine[addNo:addNo + dspCol]
        addNo += dspCol
        dspStr0 = font1.render(dspLine0, True, WHITE)
        screen.blit(dspStr0, (44, (fontSize * i) + 195))
        
    if (inputNo == 5):
        pygame.draw.rect(screen, BZLCOL, pygame.Rect(40, 195 + rectAddY, 510, 18), 1)
        if (len(strLine13) > 45):
            add = len(strLine13) - 45
        else:
            add = 0
        strLine9 = strLine13[0+add:45+add]
    elif (inputNo == 6):
        pygame.draw.rect(screen, BLACK, pygame.Rect(40, 195, 510, rectAddY + 2), 1)
    elif (inputNo == 7):
        strLine11 = strLine13[0:45]
    else:
        strLine11 = ''
    
    
def DrawScreen3():
    
    pygame.draw.rect(screen, BZLCOL, pygame.Rect(50, 210, 250, 170), 2)
    screen.blit(imgDsp0, (55, 215))

def DrawScreen4():
    
    screen.fill((50, 50, 50))
    hudStr0 = font1.render('SYSTEM|%s' %strLine1[:53], True, WHITE)#strLine1 inputNo
    hudStr1 = font1.render('SYSTEM-KEY|%s' %strPWDd, True, RED)#strLine1
    
    pygame.draw.rect(screen, GREEN, pygame.Rect(9, 13, 588, 20))
    pygame.draw.rect(screen, BZLCOL, pygame.Rect(5, 10, 595, 25), 2) 
    
    pygame.draw.rect(screen, GREEN, pygame.Rect(9, 113, 348, 20))
    pygame.draw.rect(screen, BZLCOL, pygame.Rect(5, 110, 355, 25), 2) 

    screen.blit(hudStr0, (15, 15)) 
    screen.blit(hudStr1, (15, 115))
    
    pygame.draw.rect(screen, BZLCOL, pygame.Rect(50, 210, 250, 170), 2)
    screen.blit(imgDsp0, (55, 215))

def SysSetup():
    
    global imgImg0
    global imgImg1
    global imgDsp0
    global strLine1
    
    try:
        os.mkdir('Settings')
        output = io.BytesIO(base64.b64decode(strImg0))
        imgImg0 = pygame.image.load(output)
        imgImg1 = pygame.transform.scale(imgImg0, (SCREEN_WIDTH, SCREEN_HEIGHT))
        imgDsp0  = pygame.transform.scale(imgImg0, (240, 160))        
        strLine1 = 'Made_Folder(Settings):Plz_Copy&Past&Rename_Photo(Bg1.png)'
        print(strLine1)
    except:
        pass

    try:
        os.mkdir('Images')
        strLine1 = 'Made_Folder(Images):Plz_Copy-Past_Photos_To_Folder'
        print(strLine1)
    except:
        UpdateImgList()
        
    try:
        os.mkdir(strPath)
    except:
        pass
        
        
SysSetup()

#================================================================

while not done: # main game loop

    KMInput()
    
    if (scrMode == 0):
        DrawScreen0(False)

    elif (scrMode == 1):
        DrawScreen1()

    elif (scrMode == 2):
        DrawScreen1()
        DrawScreen2(strLine13)
        if (inputNo == 0 and showImg):
            DrawScreen3()
            
    elif (scrMode == 3):
        DrawScreen4()
        
    else:
        screen.fill(ORANGE)
        done = True
    
    pygame.display.flip()
    clock.tick(FPS)
    
#__________________EXIT_THE_GAME____________    

pygame.quit()
sys.exit()





