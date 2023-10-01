import pdfplumber
from pdf2image import convert_from_path
from extract import main
from extractFImg import mainF
import re
def textExtract(path):
    pdf = pdfplumber.open(path)
    text = ""
    tmp = []
    tmpArray = []
    pattern = r"\d+"
    tmpIndex = 0
    for index, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        count = len(tables)
        if count ==0:
            images = convert_from_path(path)
            image_path = 'temp.jpg'
            images[index].save(image_path, 'JPEG')
            if index == 0:
                tmp+=mainF()
            else:
                tmp+=main()
        else:
            for table in tables:
                for row in table:
                    for cell in row:
                        try:
                            tmp.append(cell)
                            tmp.append("\n")
                        except:
                            pass
    pdf.close()
    temp = ""
    for i in tmp:
        if i == None or i == "\n":
            continue
        tmpArray.append(i)
        
    for inx, j in enumerate(tmpArray):
        rows = len(j.split("\n"))
        indexI = j[:2]
        checkNumber = re.findall(pattern, indexI)
        if checkNumber:
            check = int(checkNumber[0])
            offset = abs(tmpIndex-check)
            if offset == 1 and rows == 1 and inx !=0:
                temp = tmpArray[inx]
                tmpArray[inx] = tmpArray[inx+1]
                tmpArray[inx+1] = temp
        else:
            check =100
        tmpIndex = check
    result = "\n".join(tmpArray)
    return result