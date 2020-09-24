from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from PIL import Image
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from myblog.models import User,Article,Tag,ArticleComment,Category


#def login(request):
#    return render(request,'login.html')

def login(request):
    if request.method=='POST':
        user_name=request.POST.get('username','')
        pass_word=request.POST.get('password','')
        user=User.objects.filter(username=user_name)
        if user:
           user=User.objects.get(username=user_name)
           if pass_word==user.password:
               request.session['IS_LOGIN']=True
               request.session['username']=user_name
               avatar='media/'+user_name+'.png'
               request.session['avatar']=avatar
               #return render(request,'login_suc.html',{'user':user})
               home(request)
           else:
               return render(request,'login.html',{'error':'密码错误！'})
        else:
            return render(request,'login.html',{'error':'用户名不存在！'})
    else:
        return render(request,'login.html')

def register(request):
    if request.method =='POST':
        user_name=request.POST.get('username','')
        pass_word_1=request.POST.get('password_1','')
        pass_word_2=request.POST.get('password_2','')
        email=request.POST.get('email','')
        avatar=request.FILES.get('avatar')
        if User.objects.filter(username=user_name):
            return render(request,'register.html',{'error':'用户已存在！'})
        if (pass_word_1 != pass_word_2):
            return render(request,'register.html',{'error':'两次密码输入不一致'})
        user=User()
        if avatar:
            user.avatar = 'media/' + user_name + '.png'
            img = Image.open(avatar)
            size = img.size
            print(size)
            # 因为是要圆形，所以需要正方形的图片
            r2 = min(size[0], size[1])
            if size[0] != size[1]:
                img = img.resize((r2, r2), Image.ANTIALIAS)#高质量调整大小
            # 最后生成圆的半径
            r3 = int(r2/2)
            img_circle = Image.new('RGBA', (r3 * 2, r3 * 2), (255, 255, 255, 0))
            pima = img.load()  # 像素的访问对象
            pimb = img_circle.load()
            r = float(r2 / 2)  # 圆心横坐标
            for i in range(r2):
                for j in range(r2):
                    lx = abs(i - r)  # 到圆心距离的横坐标
                    ly = abs(j - r)  # 到圆心距离的纵坐标
                    l = (pow(lx, 2) + pow(ly, 2)) ** 0.5  # 三角函数 半径

                    if l < r3:
                        pimb[i - (r - r3), j - (r - r3)] = pima[i, j]
            img_circle.save('myblog/static/media/'+user_name+'.png')
        user.username=user_name
        user.password=pass_word_1
        user.email=email
        user.save()
        return render(request,'login.html')
    else:
        return render(request,'register.html')

def home(request):
    is_login=request.session.get('IS_LOGIN',False)
    if is_login:
        posts=Article.objects.all()
        paginator=Paginator(posts,10)    #每页显示10篇
        page=request.GET.get('page')
        try:
            post_list=paginator.page(page)
        except PageNotAnInteger:
            post_list=paginator.page(1)
        except EmptyPage:
            post_list=paginator.page(paginator.num_pages)
        username=request.session['username']
        avatar=request.session['avatar']
        return render(request,'home.html',{'post_list':post_list,'avatar':avatar})
    return render(request,'login.html')    
        
    
    

