# read a pdf or word file and convert it to a markdown file
import pdf2docx
import mammoth
from markdownify import markdownify 

def pdf_to_markdown(pdf_file_path, md_file_path):
    # intermediary docx file
    tmp_docx_file_path = md_file_path+".html"
    
    # Create a Converter object
    cv = pdf2docx.Converter(pdf_file_path)
    # Convert specified PDF page to docx 
    cv.convert(tmp_docx_file_path, start=0, end=None)
    cv.close()

    # convert the docx file to markdown
    word_to_markdown(tmp_docx_file_path, md_file_path)


# code to convert pdf to markdown
def word_to_markdown(word_file_path, md_file_path):
    # intermediary html file
    tmp_html_file_path = md_file_path+".html"
    # convert
    with open(word_file_path, "rb") as docx_file:
        result = mammoth.convert_to_html(docx_file)
        html = result.value # The generated HTML
        messages = result.messages # Any messages, such as warnings during conversion
        with open(tmp_html_file_path, "w", encoding="utf-8") as html_file:
            html_file.write(html)

    with open(tmp_html_file_path, "r") as html_file:
        html = html_file.read()
        markdown = markdownify(html)
        with open(md_file_path, "w") as md_file:
            md_file.write(markdown)

if __name__ == "__main__":
    word_to_markdown("./resumes/test-word.docx", "./resumes/test-word.md")
    # pdf_to_markdown("./resumes/test-pdf.pdf", "./resumes/test-pdf.md")
