import sys 
import os.path 
import os 


def visit(dir):
    for item in os.listdir( dir ):
        
        path = dir + "/" + item 
        if os.path.isfile( path ) :
            subp = item.split(".")
            ext = subp[-1].lower()
            #print ( '[FILE]->' , item , ext )
            if ext in ["doc", "pdf", "htm"]:
                print ( '[FILE]->' , item )
                print ( '[PATH]->', path )
                doPathItem( path , ext  )
        else:
            print ( '[DIR]->' , item )
            visit( path )

flog = open("./w.log", 'w')
def markLog( f, s):
    f.write( s )
    f.write("\n")

def doPathItem( path, ext ):

    try:
        path = path.replace("\\",'/')
        print("do=>> ", path )
        if ext == 'docx':
            import LoadDoc 
            text = LoadDoc.getTextFromDoc_Libre( path )
        elif ext == 'pdfx':
            import LoadPdf
            text = LoadPdf.decode( path )
        elif ext == 'htm':
            f = open( path )
            text = f.read( )
            f.close()
        else:
            print("ignore now")
            return 
        print(f" parse file ok {len(text)} "+ path )
        if text and len(text) :
            #post article 
            print ("PATH=>", path )
            title = path.replace("D:/waimao/", "").replace("/", '-').replace(".doc","").replace(".pdf","").replace(".htm","")
            print ( title, text )
            import WpTestcao
            cp = WpTestcao.WPHelper( 'https://huiwushi.cc', 'gushifu', 'ZbTiyushijie#1')
            content = text + '<br/>--------------------------------------------------------------------------------------<br/>'
            content += '节选自《30G外贸实操 文字+视频 教程》，全套精美排版资料：<a href="https://shop.davinci-pay.com/buy/34">请点击此处</a>'
            content += '<br/>--------------------------------------------------------------------------------------<br/>'
            cret = cp.post( title, content, 4375, category=['跨境外贸'] )
            #import sys
            import datetime 
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            print( now, title, f"post {cret}" )
            markLog(flog, title )
            import sys 
            #sys.exit(1)
    except Exception as e:
        import traceback
        print(f"Exception: {traceback.format_exc() }")
        return  
    
if __name__ == '__main__':
    
    dir= 'D:\waimao'
    visit(dir)
    flog.close()