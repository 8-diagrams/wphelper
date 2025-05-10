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
            ext_type = resp.headers.get('Content-Type')
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

    @staticmethod
    def rec_data(resp, img_url):
        import hashlib
        fhash = hashlib.md5(img_url.encode()).hexdigest() 
        with open(f"/tmp/{fhash}" , "wb") as f:
            f.write( resp.content )
        data = {'name': f"/tmp/{fhash}.jpeg", 'type':'image/jpeg' }
        import filetype 
        fg = filetype.guess(f"/tmp/{fhash}")
        if fg :
            data= {'name': f"/tmp/{fhash}."+fg.extension, 'type':fg.mime }
        import os
        os.unlink(f"/tmp/{fhash}")
        return data 
    
    def post_img(self, img_url ):
        wp = Client( self.site + '/xmlrpc.php', self.username, self.pwd )
        attachment_id = None 
        try :
            resp = WPHelper._fetchImage( img_url )
            import hashlib 
            print ( resp.headers )
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
                if not data['type'].startswith('image/'):
                    data = WPHelper.rec_data( resp , img_url )
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
                    if not data['type'].startswith('image/'):
                        data = WPHelper.rec_data( resp , face_img_url )

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

    cp = WPHelper( 'https://huiwushi.cc', 'gushifu', 'ZbTiyushijie#1')
    content = '''做人处事信条
一、钱是给内行人赚的——世界上没有卖不出的货，只有卖不出的货的人。
二、想干的人永远在找方法，不想干的人永远在找理由；世界上没有走不通的路，只有想不通的??人
三、销售者不要与顾客争论价格，要与顾客讨论价值。
四、带着目标出去，带着结果回来，成功不是因为快，而是因为有方法。
五、没有不对的客户，只有不够的服务。
六、营销人的职业信念：要把接受别人拒绝作为一种职业生活方式。
七、客户会走到我们店里来，我们要走进客户心里去；老客户要坦诚，新客户要热情，急客户要速
???? 度，大客户要品味，小客户要利益。
八、客户需要的不是产品，而是一套解决方案，卖什么不重要，重要的是怎么卖。
九、客户不会关心你卖什么，而只会关心自己要什么。没有最好的产品，只有最合适的产品。
一、关于修身修养
?????? ★相由心生，改变内在，才能改变面容。一颗阴暗的心托不起一张灿烂的脸。有爱心必有和气；有和气必有愉色；有愉色必有婉容。
?????? ★口乃心之门户。口里说出的话，代表心里想的事。心和口是一致的。
?????? ★一个境界低的人，讲不出高远的话；一个没有使命感的人，讲不出有责任感的话；一个格局小的人，讲不出大气的话。
?????? ★企业跟企业最后的竞争，是企业家胸怀的竞争，境界的竞争。
?????? ★看别人不顺眼，是自己的修养不够。
?????? ★有恩才有德，有德才有福，这就是古人说的"厚德载物"。
?????? ★人的一生就是体道，悟道，最后得道的过程。
?????? ★好人——就是没有时间干坏事的人。
?????? ★同流才能交流，交流才能交心，交心才能交易。
?????? ★同流等于合流，合流等于合心，合心等于交心。
二、关于成功
?????? ★要想成功首先要学会"变态"——改变心态、状态、态度等。
?????? ★成功之道=思考力×行动力×表达力。
?????? ★许多不成功不是因为没有行动前的计划而是缺少计划前的行动。
?????? ★功是百世功，利是千秋利，名是万世名。
三、关于团队
?????? ★什么是团队，看这两个字就知道，有口才的人对着一群有耳朵的人说话，这就是团队。

四、关于沟通
?????? ★沟通必须从正见、正思维、正语、正精进、正念出发，才能取得一致有效的合作。中国人的沟通总是从家里开始的。
?????? ★高品质的沟通，应把注意力放在结果上，而不是情绪上，沟通从心开始。
?????? ★沟通有3个要素：文字语言、声音语言、肢体语言。文字语言传达信息，声音语言传达感觉，肢体语言传达态度。
?????? ★影响沟通效果有3个要素：场合、气氛和情绪。
?????? ★沟通的3个特征：行为的主动性，过程的互动性，对象的多样性。
?????? ★沟通的5个基本步骤：点头、微笑、倾听、回应、做笔记。
?????? ★沟通的5个心：喜悦心、包容心、同理心、赞美心、爱心。
?????? ★沟通是情绪的转移,信息的转移,感情的互动。沟通没有对错，只有立场。
?????? ★人际沟通,最忌讳的就是一脸死相。要学习《亮剑》中李云龙的笑。笑能改变自己，笑能给人以力量，笑能创造良好气氛，笑能 带给他人愉悦，笑是成功的阶梯。


五、关于得失
?????? ★放下才能承担，舍弃才能获得。心有多大，舞台就有多大。话说乾隆有一次在朝上放了个屁，台下的和珅脸就红了；乾隆很高兴，大臣们都以为是和珅放的；和珅很会为皇上"分忧解难"，深得皇上信任。两百多年后的一天，秘书陪市长和局长参加一个会，在电梯里，市长不小心也放了个屁，为缓解"难堪"，市长和局长都看了看秘书，这时，秘书沉不住气了，解释说"不是我放的"。第二天，市长就把秘书给辞了，秘书不解，市长说：你丫的屁大点的事都承担不了，留你何用？
?????? ★杀生是为了放生，吃肉是为了给植物放生。
六、关于人才
?????? ★用人之长，天下无不用之人，用人之短，天下无可用之人。
?????? ★人才不一定有口才，但有口才的人一定是人才。在美国谁会讲话，谁口才好谁就当总统。
?????? ★怀才和怀孕是一样的，只要有了，早晚会被看出来。有人怀才不遇，是因为怀得不够大。
七、关于学习成长
?????? ★知识是学来的，能力是练出来的，胸怀是修来的。
?????? ★不怕念起，就怕觉迟。
?????? ★我们要做到花钱三不眨眼：孝敬老人花钱不眨眼；为铁哥们花钱不眨眼；为了学习成长花钱不眨眼。
?????? ★*说过精通的目的全在于应用。不是知识就是力量，而是使用知识才是力量。
?????? ★*还说，三天不学习就赶不上刘少奇同志了。
?????? ★别人身上的不足，就是自己存在的价值。
?????? ★思考力是万力之源，
?????? ★一个人心智模式不好的话，就容易知识越多越*。
?????? ★一个人成不了大事，是因为朋友太少，朋友质量不高。
?????? ★你把经文放进脑子里，那是你给自己开光。
?????? ★最好的投资地方，是脖子以上。我们有多少人一生都把钱花在了脖子以下了。
?????? 你把《道德经》背下来，老子跟你一辈子。
?????? 你把《孙子兵法》背下来，武圣人跟你一辈子。
?????? 你把《论语》背下来，孔子曾子跟你一辈子。
?????? 你把《心经》、《金刚经》背下来，佛菩萨跟你一辈子。
?????? ★一个不懂传统文化的管理者能成为亿万身价的富豪，但永远不会成为真正的企业家。
?????? ★多花时间成长自己，少花时间去苛责别人嫉妒别人;
?????? ★如果你认为命不好，想改变命运最好的方法就是找个好命的人交朋友。
?????? ★08年以后谁不会讲中文就特别没档次了，08年是中文折磨英文的时候到了，奥运会开始，把所有的报幕都改成中文方式。我学外语是为了教外国人学中文，见到老外不要说：对不起，我英文不好，第一句话要说：你好，你会中文吗？
八、关于聪明和愚笨
?????? ★最笨的人，就是出色的完成了根本不需要干的事。
?????? ★了解别人是精明，了解自己才是智慧。
?????? ★一个人心态要是不好的话，就容易聪明反被聪明误。
九、关于孝道
?????? ★小孝治家，中孝治企，大孝治国。
?????? ★明天道，了人道，开启商道，你的人生才能带来圆融。
?????? ★种下一个善念，收获一种良知；种下一种良知，收获一种道德；种下一种道德，收获一种习惯；种下一种习惯，收获一种性格；种下一种性格，收获一种人生。
十、关于营销
?????? ★销售不是卖，是帮助顾客买。
?????? ★所有营销在中国可用一个字"儒"来代替：儒{人 + 需}；佛{人+ $}。
?????? ★企业只有营销才能实现利润，其他的都是成本，企业最大的成本就是不懂得营销的员工。
?????? ★让顾客连续认同你你就成功了。
?????? ★顾客不仅关心你是谁，他更关心你能给他带来什么好处。
?????? ★顾客不拒绝产品，他也不拒绝服务，他只拒绝平庸。
?????? ★拒绝是一种惯性，当顾客拒绝我们时，我们的工作才刚刚开始"。
十一、关于金钱与财富
?????? ★不要活反了，生活本身就是财富。
?????? ★财散人聚，人聚财来。
?????? ★挣钱只有一个目的：就是花。钱少，自家的，多了，就是大家的，再多了，就是人民的，所以叫人民币。
?????? ★老说没有时间空间的人，这些人是最贫穷的人，最傻的人就知道把钱存在银行，银行是把不爱花钱的人的钱拿来，给爱花钱的人去花。
十二、关于茶和酒
????????★郑板桥说：酒能乱性，所以佛戒之。酒能养性，所以仙家饮之。所以，有酒时学佛，没酒时学仙。
????????★万丈红尘三杯酒，千秋大业一壶茶。
'''
    #cid = cp.post('尝试用 Gemini Pro Vision 来解决目前 RAG 的核心问题之一', content )
    #print ("CID", cid)
    #pic_url = 'https://huiwushi.cc/wp-content/uploads/2024/03/waimaoziliao.png';
    #cp._fetchImage('https://img-home.csdnimg.cn/images/20230921025407.png')
    cid = cp.post('跨境外贸 做人处事信条', content, 4375, category=['跨境外贸'] )
    #pic_id = cp.post_img( pic_url )
    #print ("pic_id , ", pic_id )

    # PIC_ID att_id 是    4375

