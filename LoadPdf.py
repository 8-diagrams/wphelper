import PyPDF2

def decode(input_file):
    import fitz  # 这是PyMuPDF的别名
    pdf_file = fitz.open(input_file)  # pdf_path是PDF文件的路径

    res = ''
    for i in range(len(pdf_file)):
        page = pdf_file.load_page(i)
        res += page.get_text()
    return res 
 

if __name__ == '__main__':
    import sys 
    text = decode( sys.argv[1] )
    print( '---\n', text, '---\n')