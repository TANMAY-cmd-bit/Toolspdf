from PyPDF2 import PdfWriter,PdfReader
import os
import fitz
import aspose.pdf as ap
import streamlit as st
import time
import pyperclip
from PIL import Image
from io import BytesIO
import random
import datetime as dt
import time

def mergepdf():
    try:
        st.subheader(":blue[Merge] Multiple :orange[Pdf's]")
        
        uploaded_files = st.file_uploader("Choose files", type=["pdf"], accept_multiple_files=True)

        merger = PdfWriter()
        for pdf in uploaded_files:
            merger.append(pdf)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        merged_file = f"merged_{timestamp}.pdf"
        merger.write(merged_file)
        merger.close()
        if len(uploaded_files) != 0:
            
            print("completed")
            print(os.path.abspath(merged_file))#pdf merged in order of list
            st.success(f"Successfully Merged {len(uploaded_files)} files")
            
            #st.pdf(merged_file)
            # Open the PDF file in binary mode
            with open(merged_file, "rb") as file:
                btn = st.download_button(
                label="Download PDF",  # Text on the download button
                data=file,             # The binary data of the PDF
                file_name=merged_file,  # The name that will be given to the downloaded file
                mime="application/pdf",    # The MIME type of the file
            )

            st.write(os.path.abspath(merged_file))#pdf merged in order of list
    except Exception as e:
        st.error(f"An error occuurred-{e}")

#mergepdf()

def pagenuminput(pdfpath):
    reader = PdfReader(pdfpath)

    st.write(f"Number of pages in pdf: {len(reader.pages)}")
    instr = st.chat_input("enter page number example:  1,3,7-11")
    if instr:
        st.write(f"you entered page: {instr}")
        #str = input("enter (like this 1,3,6-7):  ")
        c_s = instr.split(",")
        dig = []
        s_h = []
        for e in c_s:
            if '-' in e:
                s_h.append(e) 
            else:
                dig.append(e)
                #print(e)
                
        h_sv = []
        for e in s_h:
            h_sv = e.split('-')
            #print(h_sv)
            for j in range(int(h_sv[0]),int(h_sv[1])+1):
                dig.append(j)
                #print(j)

        #print("c_s =  ",c_s)
        #print("dig =  ",dig)
        digits = []
        for e in dig:
            if e == "":
                continue
            digits.append(int(e)-1)
        pages = []
        for e in digits:
            pages.append(int(e))
            #print(pages)
   
        pages_set = set(pages)
        #pageslist = []
        pageslist = list(pages_set)
        pagesstr = " ".join(str(i+1) for i in pageslist)
        st.write(f"selected pages: {pagesstr}")
        return pageslist


def pdf_to_images():

    try:
        st.subheader(":blue[Pdf] to :green[Image]")
        
        pdf_path = st.file_uploader("Choose a file", type=["pdf"])

        imagespath = []
        images = []
        
        if pdf_path:
            pdf = fitz.open(stream=pdf_path.read(), filetype="pdf")
            choice = st.radio("Select Option",["All Pages","Specific Pages","None"],index = 2)
            if choice == "All Pages":
                
                i = 0
                for pg in range(len(pdf)):
                    page = pdf[pg]
                    pix = page.get_pixmap()
                    timestamp = time.strftime("%Y%m%d_%H%M%S")

                    outputfn = f"image-{i}{timestamp}.png"

                    pix.save(outputfn)
                    images.append(outputfn)
                    imagespath.append(os.path.abspath(outputfn))
                    i = i + 1
                #print("images obtained are: ")
                st.write(f"Total pages-{len(images)}")
                pg = 1
                for e in images:
                    st.image(e,caption=f"page-{pg}")
                
                    with open(e, "rb") as file:
                        btn = st.download_button(
                        label=f"Download image-{pg}",
                        data=file,
                        file_name=e,
                        mime="image/png",
                        )
                    pg+=1

            if choice == "Specific Pages":

                pages = pagenuminput(pdf_path)

                if pages:

                    
                    i = 0
                    for pg in pages:
                        page = pdf[pg]
                        pix = page.get_pixmap()
                        timestamp = time.strftime("%Y%m%d_%H%M%S")

                        outputfn = f"image-{i}{timestamp}.png"

                        pix.save(outputfn)
                        images.append(outputfn)
                        imagespath.append(os.path.abspath(outputfn))
                        i = i + 1
                    #print("images obtained are: ")
                    st.write(f"Total Images-{len(images)}")
                    pg = 1
                    i = 0
                    for e in images:
                        st.image(e,caption=f"page-{pages[i]+1}")
                    
                        with open(e, "rb") as file:
                            btn = st.download_button(
                            label=f"Download image-{pg}",
                            data=file,
                            file_name=e,
                            mime="image/png",
                            )
                        pg+=1
                        i += 1

            if choice == "None":
                st.write("Select an Option")


    except Exception as e:
            st.error(f"An error occurred-{e}")
        
        

#pdf_to_images()


def del_pages():
    try:
        st.subheader(":red[Delete] pages in :blue[Pdf]")
        inpdf = st.file_uploader("Choose file", type=["pdf"])
        if inpdf:
            reader = PdfReader(inpdf)
            writer = PdfWriter()
            #st.write(f"Number of pages : {len(reader.pages)}")
        
            pageslist = pagenuminput(inpdf)
            if pageslist:
                delp = []
                notdel = []

                for e in pageslist:
                    if e >= len(reader.pages):
                        notdel.append(e)
                for i in range(len(reader.pages)):
                    if i not in pageslist:
                        #if i >= len(reader.pages):
                        #    notdel.append(i)
                        #    continue
                        writer.add_page(reader.pages[i])
                        #delp.append(i)
                    else:
                        delp.append(i)
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                output_pdf = f"afterdel{timestamp}.pdf"
                with open(output_pdf,"wb") as output_fle:
                    writer.write(output_fle)

                #st.write(os.path.abspath(output_pdf))
                
            
                dp = " ".join(str(i+1) for i in delp)
                nd = " ".join(str(i+1) for i in notdel)


                if(len(notdel) != 0):
                    st.error(f"Pages out of bound you entered-{nd}")
                if(len(delp) == 0):
                    st.success("Deleted pages-0")
                else:
                    st.success(f"Deleted pages-{dp}")
                st.write(f"File saved at - {os.path.abspath(output_pdf)}")
                            

                with open(output_pdf, "rb") as file:
                            btn = st.download_button(
                            label="Download PDF",  # Text on the download button
                            data=file,             # The binary data of the PDF
                            file_name=output_pdf,  # The name that will be given to the downloaded file
                            mime="application/pdf",    # The MIME type of the file
                        )
    except Exception as e:
         st.error(f"An error occured : {e}")
    
        
    
    #pages_del = [0]
#delete_pages()


#like the split pdf
def extract_pg_as_pdf():
    try:
        st.subheader(":red[Split] :blue[Pdf]")
        pdf_path = st.file_uploader("Choose file",type=["pdf"])
        if pdf_path:
            pageslist = pagenuminput(pdf_path)
            if pageslist:
                reader = PdfReader(pdf_path)
                writer = PdfWriter()
                writer2 = PdfWriter()
                ob = []
                pl = []
                for e in pageslist:
                    if e >= len(reader.pages):
                        ob.append(e)
                    else:
                        pl.append(e)
                nmp = []
                for i in range(len(reader.pages)):
                    if i in pl:
                        writer.add_page(reader.pages[i])
                    else:
                        nmp.append(i)
                        writer2.add_page(reader.pages[i])
                        
                output_pdf = f"{pageslist}extract.pdf"
                output_pdf2 = f"nonMentionedpages.pdf"
                
                with open(output_pdf,"wb") as output_fle:
                    writer.write(output_fle)
                    
                with open(output_pdf2,"wb") as output_fle2:
                    writer2.write(output_fle2)

                ep = " ".join(str(i+1) for i in pl)
                
                
                nmpstr = " ".join(str(i+1) for i in nmp)

                if(len(ob) != 0):
                    obstr = " ".join(str(i+1) for i in ob)
                    st.error(f"pages out of bound you entered-{obstr}")

                if (len(pl) != 0):   
                    plstr = " ".join(str(i+1) for i in pl)
                    st.success(f"Mentioned pages - {plstr} saved as Pdf ")
                    st.write(f"File saved at - {os.path.abspath(output_pdf)}")
                    with open(output_pdf, "rb") as file:
                            btn = st.download_button(
                            label="Download PDF",  # Text on the download button
                            data=file,             # The binary data of the PDF
                            file_name=output_pdf,  # The name that will be given to the downloaded file
                            mime="application/pdf",    # The MIME type of the file
                        )

                if(len(nmp) != 0 ):
                    nmpstr = " ".join(str(i+1) for i in nmp)
                    st.success(f"Not Mentioned pages -{nmpstr} saved as Pdf")
                    st.write(f"File saved at - {os.path.abspath(output_pdf2)}")
                    with open(output_pdf2, "rb") as file:
                            btn = st.download_button(
                            label="Download PDF",  # Text on the download button
                            data=file,             # The binary data of the PDF
                            file_name=output_pdf2,  # The name that will be given to the downloaded file
                            mime="application/pdf",    # The MIME type of the file
                        )
    except Exception as e:
        st.error(f"An errror occured : {e}")

#pageslist = [0,2]
#extract_pg_as_pdf()    


def lock_pdf():
    try:
        from faker import Faker
        st.subheader("L:red[o]c:red[k] :blue[Pdf]")
        inpdf = st.file_uploader("Choose file",type=["pdf"])
        if inpdf:
            choice = st.radio("",["enter password","generate password"])
            if choice == "enter password":
                password = st.text_input("Enter Password for Pdf:",type = "password")
                if password:
                    reader = PdfReader(inpdf)
                    writer = PdfWriter()
                    
                    for i in range(len(reader.pages)):
                        writer.add_page(reader.pages[i])
                        
                    writer.encrypt(password)
                    
                    output_pdf = "locked.pdf"
                    with open(output_pdf,"wb") as f:
                        writer.write(f)
                    st.success("Locked pdf")
                    if st.button("Show Password"):
                    # Copy the password to clipboard using pyperclip
                        st.write(password)
                        
                

                    st.write(f"pdf saved at {os.path.abspath(output_pdf)}")
                    with open(output_pdf, "rb") as file:
                            btn = st.download_button(
                            label="Download PDF",  # Text on the download button
                            data=file,             # The binary data of the PDF
                            file_name=output_pdf,  # The name that will be given to the downloaded file
                            mime="application/pdf",    # The MIME type of the file
                        )
                            
            if choice == "generate password":
                length = st.number_input("enter passsword length: ",8,100)
                if length:
                    from faker import Faker
                    fake = Faker()
                    password = fake.password(length = length)
                    if password:
                        
            
                        reader = PdfReader(inpdf)
                        writer = PdfWriter()
                        
                        for i in range(len(reader.pages)):
                            writer.add_page(reader.pages[i])
                            
                        writer.encrypt(password)
                        
                        output_pdf = "locked.pdf"
                        with open(output_pdf,"wb") as f:
                            writer.write(f)
                            
                        st.success("Locked pdf")
                        
                        st.write("First Copy then Download")
                        if st.button("Show Password"):
                        # Copy the password to clipboard using pyperclip
                            st.write(password)
                            
                    

                        st.write(f"pdf saved at {os.path.abspath(output_pdf)}")
                        with open(output_pdf, "rb") as file:
                                btn = st.download_button(
                                label="Download PDF",  # Text on the download button
                                data=file,             # The binary data of the PDF
                                file_name=output_pdf,  # The name that will be given to the downloaded file
                                mime="application/pdf",    # The MIME type of the file
                            )
    except Exception as e:
        st.error(f"An error occured : {e}")
    
#lock_pdf()

def extract_img_from_pdf() :
    import fitz  # PyMuPDF
    import os
    from PIL import Image
    import io
    from PyPDF2 import PdfReader
    import streamlit as st

    #try:
        

    st.subheader(":green[Extract] :blue[Image] in :red[Pdf]")
    
    inpdf = st.file_uploader("Choose file",type=["pdf"])
    if inpdf:
        pdf = fitz.open(stream=inpdf.read(), filetype="pdf")
        imgcount = 0
        
        
        choice = st.radio("Choose Operation",["None","All pages","Specific pages"],label_visibility="collapsed")
        if choice == "Specific pages":
            pageslist = pagenuminput(inpdf)
            
            if pageslist:
                ob = []
                reader = PdfReader(inpdf)
                for e in pageslist:
                    if(e >= len(reader.pages)):
                        ob.append(e)
                for page_num in range(len(pdf)):
                    if page_num in pageslist:
                        page = pdf.load_page(page_num)
                        image_list = page.get_images(full=True)
                        
                        st.write(f"Pg.no {page_num + 1} has {len(image_list)} images")
                        
                        c = 0
                        import io
                        for img_index, image in enumerate(image_list):
                            xref = image[0]  # Image reference
                            
                            img = pdf.extract_image(xref)
                            img_bytes = img["image"]
                            import io
                            # Create a PIL Image from the byte data
                            img_pil = Image.open(io.BytesIO(img_bytes))
                            
                            image_filename = f"pg{page_num+1}img{c+1}.png"
                            
                            img_pil.save(image_filename)
                            
                            imgcount += 1
                            st.success(f"page-{page_num + 1} image-{c+1}")
                            st.image(image_filename,caption=f"page-{page_num+1}img{c+1} :{os.path.abspath(image_filename)}")
                            with open(image_filename, "rb") as file:
                                        btn = st.download_button(
                                        label=f"Download image-{c+1}",
                                        data=file,
                                        file_name=image_filename,
                                        mime="image/png",
                                        )
                            c = c + 1
                st.write(f"Totally {imgcount} images found")
                if(len(ob) != 0):
                    obstr = " ".join(str(i+1) for i in ob)
                    st.error(f"pages out of bound you entered: {obstr}")

        if choice == "All pages":
            
            for page_num in range(len(pdf)):
            
                page = pdf.load_page(page_num)
                image_list = page.get_images(full=True)
                
                st.write(f"Pg.no {page_num + 1} has {len(image_list)} images")
                
                c = 0
                for img_index, image in enumerate(image_list):
                    xref = image[0]  # Image reference
                    
                    img = pdf.extract_image(xref)
                    img_bytes = img["image"]
                    
                    # Create a PIL Image from the byte data
                    img_pil = Image.open(io.BytesIO(img_bytes))
                    
                    image_filename = f"pg{page_num+1}img{c+1}.png"
                    
                    img_pil.save(image_filename)
                    
                    imgcount += 1
                    st.success(f"page-{page_num + 1} image-{c+1}")
                    st.image(image_filename,caption=f"page-{page_num+1}img{c+1} :{os.path.abspath(image_filename)}")
                    with open(image_filename, "rb") as file:
                                btn = st.download_button(
                                label=f"Download image-{c+1}",
                                data=file,
                                file_name=image_filename,
                                mime="image/png",
                                )
                    c = c + 1
            st.write(f"Totally {imgcount} images found")

        if choice == "None":
            st.write("select option")
        
#extract_img_from_pdf()    

    

              
def find_and_replace_pdf():

    st.subheader(":blue[Replace] :green[Text] in :red[pdf] ")
   
    inpdf = st.file_uploader("Choose file",type=["pdf"])
    find_str = ""
    replace_str = ""
    font_size = 12
    if inpdf:
        
        find_str = st.text_input("enter text to find: ")
        replace_str = st.text_input("enter text to replace: ")
        font_size = st.number_input("enter the font size : ",12,100)
       

    if (find_str != "" and replace_str != "") :
        document = ap.Document(inpdf)
        absorber = ap.text.TextFragmentAbsorber(find_str)
        document.pages.accept(absorber)
        collection = absorber.text_fragments
        for text_fragment in collection:
            # Replace the text with the new text
            text_fragment.text = replace_str
            
            # Apply the custom font size to the replaced text
            text_fragment.text_state.font_size = font_size
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        outputpdf = f"replacedtxt{timestamp}.pdf"

        document.save(outputpdf)
        st.write(f"Pdf saved as {os.path.abspath(outputpdf)}")
        with open(outputpdf, "rb") as file:
                                btn = st.download_button(
                                label=f"Download pdf",
                                data=file,
                                file_name=outputpdf,
                                mime="application/pdf",
                                )
#find_and_replace_pdf()
    
    
def pdf_to_audio():
    try:

        def text_audio_file(text):

            with st.spinner("please wait..."):
                
                current_datetime = dt.datetime.now()
                cdt = current_datetime
                start = time.time()
                data = gtts.gTTS(text,tld = 'co.in')
                file_name = f"sample{cdt.year}{cdt.month}{cdt.day}{cdt.hour}{str(random.randint(1,999))}.mp3"
                if path.exists(file_name):
                    os.remove(file_name)
                data.save(file_name)
                end = time.time()
            st.write("time taken...",(end - start),"seconds")
            st.success(f"congratulations file created as {file_name}")
            return file_name

        st.title(":red[Pdf] to :blue[Audio file]")

        st.subheader("no time to read then listen")
        st.write("upload your pdf file and enter the page number and get your audio file")

        upload = st.file_uploader("upload your pdf file:")

        if upload is not None:
            st.write("succesfully uploaded")
            if upload.type == "application/pdf":
                st.success("pdf file is uploaded")

                from PyPDF2 import PdfReader
                import gtts , playsound as mic
                from os import path

                pdf = PdfReader(upload)
                pdf_text = []
                for i in range(0,len(pdf.pages)):
                    print(f"Page {i+1}:")
                    page = pdf.pages[i].extract_text()
                    pdf_text.append(page)


                cho = st.radio("select the type",["audio file of particular page","audio file of complete pdf"])

                if cho == "audio file of particular page":

                    page_num = st.number_input("enter the page number from pdf whose audio to be generated: ",1,len(pdf.pages),step=1,)
                    page_num = int(page_num)
                    c = st.radio("preview the text",["NO","YES"])
                    if c == "YES":
                        st.write(f"the text in pgno {page_num} is \n\n {pdf_text[int(page_num)-1]}")

                    ch = st.radio("generate audio file",["NO","YES"])
                    if ch == "YES":
                        
                        fileN = text_audio_file(pdf_text[int(page_num)-1])
                        st.audio(fileN,format = "audio/mp3")


                else:
                    text = ''
                    for i in range(0,len(pdf.pages)):
                        text = text + pdf.pages[i].extract_text()
                    choi = st.radio("preview the text: ",["NO","YES"])
                    if choi == "YES":
                        st.write(f"The text in pdf as below: \n\n\n {text}")

                    choic = st.radio("Generate the Audio ?",["NO","YES"])
                    if choic == "YES":
                        fileName = text_audio_file(text)
                        st.audio(fileName,format="audio/mp3")










            else:
                st.error("not a pdf file")
                st.error("kindly upload a pdf file!,.")
    except Exception as e:
         st.error(f"aAn error occured {e}")
#pdf_to_audio()  
    
    
    
st.header(":blue[PDF] :green[Tools]")

st.info("Choose your Operation")
option = st.radio("CO",["None","Merge Pdf","Delete Pages in Pdf","Obtain Pdf as Image","Extract Image in Pdf","Lock Pdf","Split Pdf","Pdf to Audio"],label_visibility="collapsed")
if option:
    st.write(option)

    if option == "Merge Pdf":
        mergepdf()

    if option == "Delete Pages in Pdf":
        del_pages()
    
    if option == "Obtain Pdf as Image":
        pdf_to_images()
    
    if option == "Extract Image in Pdf":
        extract_img_from_pdf()

    if option == "Lock Pdf":
        lock_pdf()
    
    if option == "Split Pdf":
        extract_pg_as_pdf()

    if option == "Pdf to Audio":
         pdf_to_audio()
        

    


         
