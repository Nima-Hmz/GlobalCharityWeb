from django.shortcuts import render , redirect
from django.views import View
from blog.models import blogModel
from django.core.paginator import Paginator , PageNotAnInteger , EmptyPage

from .models import *
from django.contrib import messages

from django.views.generic import TemplateView
from accounts.models import User
from django.db.models import Sum

from newsletters.models import *

# Index View
class IndexView(View):
    def get(self, request):
        blogs = blogModel.objects.filter(status=True).order_by('-updated')
        lovely_blogs = blogModel.objects.filter(status=True , lovely = True).order_by('-updated')[:3]

        # Retrieve top 16 users with their total donations
        top_users = User.objects.annotate(total_donations=Sum('total_donate')).order_by('-total_donations')[:16]

        # Slice the top users into four groups of 4 users each
        top_users1, top_users2, top_users3, top_users4 = [top_users[i:i+4] for i in range(0, 16, 4)]

        # Calculate total donations for each group of users
        total_donations = sum(user.total_donate for user in top_users)
        total_donations1 = sum(user.total_donate for user in top_users1)
        total_donations2 = sum(user.total_donate for user in top_users2)
        total_donations3 = sum(user.total_donate for user in top_users3)
        total_donations4 = sum(user.total_donate for user in top_users4)

        # Calculate final donation
        # final_donation = total_donations1 + total_donations2 + total_donations3 + total_donations4

        # Calculate percentage for each user
        for user in top_users1:
            user.percent = (user.total_donate / total_donations) * 100 if total_donations!= 0 else 0

        for user in top_users2:
            user.percent = (user.total_donate / total_donations) * 100 if total_donations!= 0 else 0

        for user in top_users3:
            user.percent = (user.total_donate / total_donations) * 100 if total_donations!= 0 else 0

        for user in top_users4:
            user.percent = (user.total_donate / total_donations) * 100 if total_donations!= 0 else 0


        paginator = Paginator(blogs , 2)
        page = request.GET.get('page',1)

        try :
            result = paginator.page(page)
        except PageNotAnInteger :
            result = paginator.page(1)
        except EmptyPage:
            result = paginator.page(paginator.num_pages)


        context = {
            'blogs' : result,
            'Lblogs' : lovely_blogs,
            'top_users': top_users,
            'top_users1': top_users1,
            'top_users2': top_users2,
            'top_users3': top_users3,
            'top_users4': top_users4,
            'total_donations': total_donations,
            'total_donations1': total_donations1,
            'total_donations2': total_donations2,
            'total_donations3': total_donations3,
            'total_donations4': total_donations4,
            # 'final_donation': final_donation
        }
        return render(request, 'home/index.html' , context=context)
    
    def post(self, request):

        context = {
            'users': User.objects.all()
        }

        return render(request, 'home/index.html', context)
    


# About Us View
class AboutView(View):
    def get(self, request):
        lovely_blogs = blogModel.objects.filter(status=True , lovely = True).order_by('-updated')[:3]

        details = Aboutus.objects.all()[:1]

        return render(request, 'home/about.html' , {'Lblogs' : lovely_blogs, 'details' : details})


# Contact Us
class ContactUsView(View):
    def get(self, request):
        contact_info = ContactUsInfo.objects.all()
        
        context = {
            'info' : contact_info,
            
        }
        return render(request, 'home/contact.html' , context=context)

    def post(self , request):
        name = request.POST['InputName']
        email = request.POST['InputEmail']
        subject = request.POST['InputSubject']
        message = request.POST['InputMessage']

        if name and email and subject and message:
            ticket = ContactUs(title=subject , full_name=name , email=email , message=message)
            ticket.save()
            ticket._meta.verbose_name_plural = "تماس با ما * "
            messages.success(request , 'پیام شما با موفقیت ارسال شد' , 'success')
            return redirect('home:contact_us')
        else:
            messages.error(request , 'پر کردن فیلد ها اجباری است' , 'danger')
            return redirect('home:contact_us')
        
class NewslettersView(View):
    def post(self , request):
        email = request.POST['email-field']

        member = NewsletterEmailsModel.objects.filter(email=email)

        if email:
            if member.exists():
                messages.error(request , 'این ایمیل قبلا ثبت شده است' , 'danger')
            else:
                new_member = NewsletterEmailsModel(email=email)
                new_member.save()

                messages.success(request , 'انجام شد' , 'success')

        return redirect('home:index')

