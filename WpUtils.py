#coding:utf-8
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo
from wordpress_xmlrpc.methods import posts
from wordpress_xmlrpc.methods import taxonomies
from wordpress_xmlrpc import WordPressTerm
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts
 
class WPHelper:
    def __init__(self, site, username, pwd):
        self.site = site
        self.username = username
        self.pwd = pwd
    
    @staticmethod
    def _getExt( resp ):
        ext = 'jpg'
        con_type = resp.headers.get('Content-Type') 
        arr = con_type.split("/")
        if len(arr)> 1:
            ext = arr[1]
        return ext
     
    @staticmethod
    def _getCT(resp ):
        ext_type = 'image/jpeg' 
        if resp.headers.get('Content-Type'):
            ext_type = 'image/jpeg' 
        return ext_type 
    
    @staticmethod
    def _fetchImage( url):
        try:
            import requests 
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
            resp = requests.get(url, headers=headers)
            #print ( resp.headers )
            if resp.status_code == 200:
                return resp
            return None 
        except Exception as e:
            return None
          
    def post_img(self, img_url ):
        wp = Client( self.site + '/xmlrpc.php', self.username, self.pwd )
        attachment_id = None 
        try :
            resp = WPHelper._fetchImage( img_url )
            import hashlib 
            fhash = hashlib.md5(img_url.encode()).hexdigest()  
            ext = WPHelper._getExt( resp )
            if resp:
                # prepare metadata
                import random
                cc = random.randint(10000,90000)
                data = {
                        'name': f'{fhash}{cc}.{ext}',
                        'type': WPHelper._getCT( resp ),  # mimetype
                }
                data['bits'] = resp.content 
                
                response = wp.call(media.UploadFile(data))
                # response == {
                #       'id': 6,
                #       'file': 'picture.jpg'
                #       'url': 'http://www.example.com/wp-content/uploads/2012/04/16/picture.jpg',
                #       'type': 'image/jpeg',
                # }
                attachment_id = response['id']
        except Exception as e:
            import traceback
            print ( traceback.format_exc() )
            return  
        return attachment_id 
        

    def post(self, title, content, face_img_url=None, post_tag = [],  category = []):
        wp = Client( self.site + '/xmlrpc.php', self.username, self.pwd )
        attachment_id = None 
        if face_img_url:
            if type(face_img_url) == int :
                attachment_id = face_img_url
            else:
                resp = WPHelper._fetchImage( face_img_url )
                import hashlib 
                fhash = hashlib.md5(face_img_url.encode()).hexdigest()  
                ext = WPHelper._getExt( resp )
                if resp:
                    # prepare metadata
                    import random
                    cc = random.randint(10000,90000)
                    data = {
                            'name': f'{fhash}{cc}.{ext}',
                            'type': WPHelper._getCT( resp ),  # mimetype
                    }
                    data['bits'] = resp.content 
                    
                    response = wp.call(media.UploadFile(data))
                    # response == {
                    #       'id': 6,
                    #       'file': 'picture.jpg'
                    #       'url': 'http://www.example.com/wp-content/uploads/2012/04/16/picture.jpg',
                    #       'type': 'image/jpeg',
                    # }
                    attachment_id = response['id']
        
        post = WordPressPost()
        post.title = title
        post.content = content
        post.post_status = 'publish'  #文章状态，不写默认是草稿，private表示私密的，draft表示草稿，publish表示发布
        post.terms_names = {
            'post_tag': post_tag, #文章所属标签，没有则自动创建
            'category': category  #文章所属分类，没有则自动创建
        }
        if attachment_id:
            post.thumbnail = attachment_id  
        post.id = wp.call(posts.NewPost(post))
        return post.id 
    

if __name__ == '__main__':

    cp = WPHelper( 'https://macdown.net', 'macdown.net', 'OPdN6wj%uPEDW$X90^')
    content = '''结论：
1. 正文效果还行。
2. 表格效果一般。

Prompt 和转换不出来的表格如图。'''
    #cid = cp.post('尝试用 Gemini Pro Vision 来解决目前 RAG 的核心问题之一', content )
    #print ("CID", cid)
    pic_url = 'https://img-home.csdnimg.cn/images/20230921025407.png';
    #cp._fetchImage('https://img-home.csdnimg.cn/images/20230921025407.png')
    #cid = cp.post('尝试用 Gemini Pro Vision 来解决目前 RAG 的核心问题之一', content, pic_url, category=['AI推荐', '资源分享'] )
    pic_id = cp.post_img( pic_url )
    print ("pic_id , ", pic_id )