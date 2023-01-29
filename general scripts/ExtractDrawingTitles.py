from pdfminer.layout import LAParams, LTTextBox
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
import types
import os, glob

## loop through PDF drawings and record title, revision and number in CSV format to console. 

folderLocation = "C:\\path\\to\\drawings\\folder\\drawings"

drawings=[]

for filename in glob.glob(os.path.join(folderLocation, '*.pdf')):
   with open(os.path.join(os.getcwd(), filename), 'rb') as fp: 
      # do your stuff

    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    pages = PDFPage.get_pages(fp)
  
    for page in pages:
        print('Processing next page...')
        interpreter.process_page(page)
        layout = device.get_result()
        dwg = types.SimpleNamespace()
        dwg.number = "1"
        dwg.title = "1"
        dwg.revision = "1"
        isRevNext = False
        isNumNext = False
        isTitleNext = False

        for lobj in layout:
            if isinstance(lobj, LTTextBox):
                x, y, text = lobj.bbox[0], lobj.bbox[3], lobj.get_text()
                print('At %r is text: %s' % ((x, y), text))

                if isRevNext:
                    dwg.revision = text.replace("\n", "")
                    isRevNext = False
                    print("set revision")
                if isNumNext:
                    dwg.number = text.replace("\n", "")
                    isNumNext = False
                    print("set number")
                if isTitleNext:
                    dwg.title = text.replace("\n", "")
                    isTitleNext = False
                    print("set title")


                if text.strip() == "REV:":
                    isRevNext = True
                if text.strip() == "SHEET NUMBER":
                    isNumNext = True
                if text.strip() == "SHEET TITLE":
                    isTitleNext = True

                # somw drawings it popps out in this part, texts are joined in one block insead of line by line
                if "PURPOSE OF ISSUE" in text:
                    textNoBreaks = text.replace("\n", " ")
                    textNoBreaks = textNoBreaks.replace("  ", " ")
                    if "PROJECT NUMBER" in textNoBreaks:
                        titleStart = textNoBreaks.index("TITLE")+5
                        titleEnd = textNoBreaks.index("SHEET NUMBER")
                        dwg.title = textNoBreaks[titleStart:titleEnd].strip()

                        numberStart = textNoBreaks.index("SHEET NUMBER")+12
                        numberEnd = len(textNoBreaks)-1
                        if "SCALE" in textNoBreaks:
                            numberEnd = textNoBreaks.index("SCALE")

                        dwg.number = textNoBreaks[numberStart:numberEnd].strip()

                elif  "PURPOSEOFISSUE" in text:
                    textNoBreaks = text.replace("\n", " ")
                    textNoBreaks = textNoBreaks.replace("  ", " ")
                    if "PROJECTNUMBER" in textNoBreaks:
                        titleStart = textNoBreaks.index("TITLE")+5
                        if "SHEETNUMBER" in textNoBreaks:
                            titleEnd = textNoBreaks.index("SHEETNUMBER")
                            dwg.title = textNoBreaks[titleStart:titleEnd].strip()

                            numberStart = textNoBreaks.index("SHEETNUMBER")+12
                            numberEnd = len(textNoBreaks)-1
                            if "SCALE" in textNoBreaks:
                                 numberEnd = textNoBreaks.index("SCALE")
                            dwg.number = textNoBreaks[numberStart:numberEnd].strip()

        print(dwg)
        drawings.append(dwg)

number = len(drawings)
print("List: "+str(number))
for dw1 in drawings:
    #print(str(dw))
   # print(dw1)
    pn = "10234568"
    title = dw1.title
	# some words are joined without spaces, hence add spaces and get rid of double spaces a couple of times....
    if "DETAILS" in title:
        title=title.replace("DETAILS", " DETAILS ")
    if "SLAB" in title:
        title=title.replace("SLAB", " SLAB ")
    if "OF" in title:
        title=title.replace("OF", " OF ")
    if "FLOOR" in title:
        title=title.replace("FLOOR", " FLOOR ")
    if "TRANSFER" in title:
        title=title.replace("TRANSFER", " TRANSFER ")
    if "GROUND" in title:
        title=title.replace("GROUND", " GROUND ")

    title=title.replace("  ", " ")
    title=title.replace("  ", " ")
    title=title.replace("  ", " ")
    title=title.replace("  ", " ")

    s = ""+dw1.number + ","+dw1.revision+"," +""+title
    print(s)
