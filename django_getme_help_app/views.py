from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from .models import *
import datetime
import random

# Create your views here.

def log(request):
    return render(request,"index.html")

def login_post(request):
    username=request.POST['textfield']
    password=request.POST['textfield2']
    data=Login.objects.filter(username=username,password=password)
    if data.exists():
        data=data[0]
        request.session['lid'] = data.id

        if data.type == 'admin':
            return redirect('/admin_home')
        elif data.type == 'worker':
            return redirect('/worker_home')
        elif data.type == 'pending':
            return HttpResponse("<script>alert('wait for authentication');window.location='/log'</script>")
        elif data.type == 'user':
            return redirect('/user_home')
    else:
        return HttpResponse("<script>alert('Invalid User');window.location='/log'</script>")

def admin_home(request):
    return render(request,"admin/index.html")

def worker_home(request):
    return render(request,"worker/index.html")

def user_home(request):
    return render(request,"user/index.html")


# Admin Module

def admin_view_registered_worker(request):
    data=Worker.objects.filter(LOGIN__type='pending')
    return render(request,"admin/view_registered_workers.html",{"data":data})

def admin_registered_worker_approve(request,log_id):        # Updating the login type pending into worker
    Login.objects.filter(id=log_id).update(type='worker')
    return redirect('/admin_view_registered_worker')

def admin_registered_worker_reject(request,log_id):
    Login.objects.filter(id=log_id).update(type='Reject')
    return redirect('/admin_view_registered_worker')

def admin_view_approved_worker(request):
    data=Worker.objects.filter(Q(LOGIN__type='worker') | Q(LOGIN__type='block'))
    return render(request,"admin/view_approved_workers.html",{"data":data})

def admin_block_worker(request,log_id):
    Login.objects.filter(id=log_id).update(type='block')
    return redirect('/admin_view_approved_worker')
    # return render(request,"admin/view_blocked_workers.html",{"data":data})

def admin_unblock_worker(request,log_id):
    Login.objects.filter(id=log_id).update(type='worker')
    return redirect('/admin_view_approved_worker')

def admin_view_rejected_worker(request):
    data=Worker.objects.filter(LOGIN__type='Reject')
    return render(request,"admin/view_rejected_worker.html",{"data":data})

def admin_view_registered_user(request):
    data=User.objects.all()
    return render(request,"admin/view_registered_user.html",{"data":data})

def admin_view_compliant(request):
    data=Complaint.objects.all()
    return render(request,"admin/view_complaint.html",{"data":data})

def admin_send_reply(request,repid):
    return render(request,"admin/send_reply.html",{"repid":repid})

def admin_send_reply_post(request,repid):
    current_date=datetime.datetime.now().strftime("%Y-%m-%d")
    reply=request.POST['textarea']
    Complaint.objects.filter(id=repid).update(reply=reply,reply_date=current_date)
    return HttpResponse("<script>alert('Reply send');window.location='/admin_view_compliant'</script>")

def admin_view_rating_review(request):
    data=Rating.objects.all()
    return render(request,"admin/view_review_rating.html",{"data":data})

def admin_change_password(request):
    return render(request,"admin/change_password.html")

def admin_change_password_post(request):
    old_password=request.POST['textfield2']
    new_password=request.POST['textfield3']
    confirm_password=request.POST['textfield3']

    Login.objects.get(password=old_password,id=request.session['lid'])

    if new_password == confirm_password:
        if Login.objects.filter(Q(password=new_password) | Q(password=new_password)).exists():
            return HttpResponse("<script>alert('Password already exist');window.location='/admin_change_password'</script>")
        else:
            Login.objects.filter(id=request.session['lid']).update(password=confirm_password)
            return HttpResponse("<script>alert('password updated');window.location='/admin_change_password'</script>")
    else:
        return HttpResponse("<script>alert('password mismatch');window.location='/admin_change_password'</script>")

    # return redirect('/admin_change_password')


# Category Management

def admin_add_category(request):
    return render(request,"admin/add_category.html")

def admin_add_category_post(request):
    category=request.POST['textfield']
    cat_obj=Category()
    cat_obj.category=category
    cat_obj.save()
    return HttpResponse("<script>alert('Category Added');window.location='/admin_add_category'</script>")

def admin_category_view(request):
    data=Category.objects.all()
    return render(request,"admin/view_category.html",{"data":data})

def admin_category_delete(request,i):
    Category.objects.get(id=i).delete()
    return HttpResponse("<script>alert('category removed');window.location='/admin_category_view'</script>")

def admin_category_update(request,i):
    data=Category.objects.get(id=i)
    return render(request,"admin/update_category.html",{"data":data})

def admin_category_update_post(request,i):
    category=request.POST['textfield']
    Category.objects.filter(id=i).update(category=category)
    return HttpResponse("<script>alert('category updated');window.location='/admin_category_view'</script>")


# Worker Module

def worker_register(request):
    data = Category.objects.all()
    return render(request,"worker/worker_register.html",{"data":data})

def worker_register_post(request):
    category = request.POST['select']
    name = request.POST['textfield']
    gender = request.POST['RadioGroup1']
    place = request.POST['textfield3']
    post = request.POST['textfield4']
    pin = request.POST['textfield5']
    email = request.POST['textfield6']
    contact = request.POST['textfield7']
    lattitude = request.POST['textfield9']
    longitude = request.POST['textfield10']
    photo=request.FILES['fileField']        # Image Field
    fs=FileSystemStorage()
    dt=datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    fs.save(r"C:\Users\HP\PycharmProjects\django_getme_help\django_getme_help_app\static\\"+dt+'.jpg',photo)
    photo='/static/'+dt+'.jpg'
    password=request.POST['textfield8']

    lob=Login.objects.filter(username=email)
    if lob.exists():
        return HttpResponse("<script>alert('Already Exist');window.location='/worker_register'</script>")
    else:
        log_obj=Login()
        log_obj.username=email
        log_obj.password=password
        log_obj.type='pending'
        log_obj.save()

        work_obj=Worker()
        work_obj.CATEGORY=Category.objects.get(id=category)
        work_obj.name=name
        work_obj.gender=gender
        work_obj.place=place
        work_obj.post=post
        work_obj.pin=pin
        work_obj.email=email
        work_obj.contact=contact
        work_obj.photo=photo
        work_obj.lattitude=lattitude
        work_obj.longitude=longitude

        work_obj.LOGIN = log_obj
        work_obj.save()
        return HttpResponse("<script>alert('Registered Successfully');window.location='/worker_register'</script>")

def worker_view_profile(request):
    data=Worker.objects.get(LOGIN=request.session['lid'])
    return render(request,"worker/view_profile.html",{"data":data})


def worker_edit_profile(request,worker_id):
    data1=Worker.objects.get(id=worker_id)
    data2=Category.objects.all()
    return render(request,"worker/edit_profile.html",{"data1":data1,"data2":data2,"worker_id":worker_id})

def worker_edit_profile_post(request,worker_id):
    try:
        category = request.POST['select']
        name = request.POST['textfield']
        gender = request.POST['RadioGroup1']
        place = request.POST['textfield3']
        post = request.POST['textfield4']
        pin = request.POST['textfield5']
        email = request.POST['textfield6']
        contact = request.POST['textfield7']
        lattitude = request.POST['textfield9']
        longitude = request.POST['textfield10']
        photo = request.FILES['fileField']        # Image Field
        fs = FileSystemStorage()
        dt = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        fs.save(r"C:\Users\HP\PycharmProjects\django_getme_help\django_getme_help_app\static\\"+dt+'.jpg',photo)
        photo = '/static/'+dt+'.jpg'
        Worker.objects.filter(id=worker_id).update(CATEGORY=category,name=name,gender=gender,place=place,
                                                   post=post,pin=pin,email=email,contact=contact,
                                                   lattitude=lattitude,longitude=longitude,photo=photo)
        return HttpResponse("<script>alert('Profile Edited');window.location='/worker_view_profile'</script>")


    except Exception as e:
        category = request.POST['select']
        name = request.POST['textfield']
        gender = request.POST['RadioGroup1']
        place = request.POST['textfield3']
        post = request.POST['textfield4']
        pin = request.POST['textfield5']
        email = request.POST['textfield6']
        contact = request.POST['textfield7']
        Worker.objects.filter(id=worker_id).update(CATEGORY=category,name=name,gender=gender,place=place,
                                                   post=post,pin=pin,email=email,lattitude=lattitude,longitude=longitude,contact=contact)
        return HttpResponse("<script>alert('Profile Edited');window.location='/worker_view_profile'</script>")


# Service Management

def worker_add_service(request):
    return render(request,"worker/add_service.html")

def worker_add_service_post(request):
    service=request.POST['textfield']
    amount=request.POST['textfield2']
    service_obj=Service()
    service_obj.service = service
    service_obj.amount = amount
    service_obj.WORKER = Worker.objects.get(LOGIN=request.session['lid'])
    service_obj.save()
    return HttpResponse("<script>alert('service added');window.location='/worker_add_service'</script>")

def worker_service_view(request):
    data=Service.objects.all()
    return render(request,"worker/view_service.html",{"data":data})

def worker_service_delete(request,service_id):
    Service.objects.get(id=service_id).delete()
    return HttpResponse("<script>alert('service cleared');window.location='/worker_service_view'</script>")

def worker_service_update(request,service_id):
    data=Service.objects.get(id=service_id)
    return render(request,"worker/update_service.html",{"data":data})

def worker_service_update_post(request,service_id):
    service=request.POST['textfield']
    amount=request.POST['textfield2']
    Service.objects.filter(id=service_id).update(service=service,amount=amount)
    return HttpResponse("<script>alert('service updated');window.location='/worker_service_view'</script>")

def worker_view_request_from_user(request):
    data = Bookings.objects.filter(SERVICE__WORKER__LOGIN__id=request.session['lid'] )
    return render(request,"worker/view_request_from_user.html",{"data":data})

def worker_status_approve(request,rid):
    Bookings.objects.filter(id=rid).update(status='Approve')
    return redirect('/worker_view_request_from_user')

def worker_status_reject(request,rid):
    Bookings.objects.filter(id=rid).update(status='Reject')
    return redirect('/worker_view_request_from_user')

def worker_add_additional_charges(request,bid):
    return render(request,"worker/add_additional_charge.html",{"bid":bid})

def worker_additional_charge_post(request,bid):
    item = request.POST['textfield1']
    amount = request.POST['textfield2']
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    addcharge_obj = Bill()
    addcharge_obj.item = item
    addcharge_obj.date = date
    addcharge_obj.amount = amount
    addcharge_obj.BOOKING = Bookings.objects.get(id=bid)
    addcharge_obj.save()
    return HttpResponse("<script>alert('Additional charge added');window.location='/worker_add_additional_charges/"+bid+"'</script>")

def worker_view_payment(request):
    data=Bookings.objects.filter(SERVICE__WORKER__LOGIN__id = request.session['lid'])
    return render(request,"worker/view_payment.html",{"data":data})

def worker_view_rating_review(request):
    # data=Rating.objects.all()
    data = Rating.objects.filter(BOOKINGS__SERVICE__WORKER = Worker.objects.get(LOGIN=request.session['lid']))
    lis = []
    for i in data:
        rt = []
        nrt = []
        for j in range(int(i.rate)):
            rt.append(j)
        for j in range(5 - int(i.rate)):
            nrt.append(j)
        dict = {'name': i.BOOKINGS.USER.name, 'date': i.date, 'rate': rt, 'norate': nrt ,'review':i.review}
        lis.append(dict)
    return render(request, "worker/view_rating.html", {"data": lis})
    # return render(request,"worker/view_rating.html",{"data":data})

def worker_change_password(request):
    return render(request,"worker/change_password.html")

def worker_change_password_post(request):
    old_password = request.POST['textfield2']
    new_password = request.POST['textfield3']
    confirm_password = request.POST['textfield3']

    Login.objects.get(password=old_password, id=request.session['lid'])

    if new_password == confirm_password:
        if Login.objects.filter(Q(password=new_password) | Q(password=new_password)).exists():
            return HttpResponse("<script>alert('Password already exist');window.location='/worker_change_password'</script>")
        else:
            Login.objects.filter(id=request.session['lid']).update(password=confirm_password)
            return HttpResponse("<script>alert('password updated');window.location='/worker_change_password'</script>")
    else:
        return HttpResponse("<script>alert('password mismatch');window.location='/worker_change_password'</script>")

def list_user_chat(request):
    data = User.objects.all()
    return render(request,"worker/chat_with_user.html",{"data":data})

def worker_chat_customer(request,i):
    data=Chat.objects.filter(WORKER=Worker.objects.get(LOGIN=request.session['lid']),USER=User.objects.get(id=i))
    return render(request,"worker/chat.html",{"i":i,"data":data})

def worker_chat_customer_post(request,i):
    chat = request.POST['textfield']
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    chat_obj = Chat()
    chat_obj.chat = chat
    chat_obj.date = date
    chat_obj.type = 'worker'
    chat_obj.USER = User.objects.get(id=i)
    chat_obj.WORKER = Worker.objects.get(LOGIN=request.session['lid'])
    chat_obj.save()
    return HttpResponse("<script>alert('Chat send');window.location='/worker_chat_customer/"+i+"'</script>")


# User module

def user_register(request):
    return render(request,"user/user_register.html")

def user_register_post(request):
    name = request.POST['textfield']
    gender = request.POST['RadioGroup1']
    house_name = request.POST['textfield2']
    place = request.POST['textfield3']
    post = request.POST['textfield4']
    pin = request.POST['textfield5']
    email = request.POST['textfield6']
    contact = request.POST['textfield7']
    password = request.POST['textfield8']

    lob = Login.objects.filter(username=email)
    if lob.exists():
        return HttpResponse("<script>alert('Already Exist');window.location='/user_register'</script>")
    else:
        log_obj = Login()
        log_obj.username = email
        log_obj.password = password
        log_obj.type = 'user'
        log_obj.save()

        user_obj = User()
        user_obj.name = name
        user_obj.gender = gender
        user_obj.house_name = house_name
        user_obj.place = place
        user_obj.post = post
        user_obj.pin = pin
        user_obj.email = email
        user_obj.contact = contact
        user_obj.LOGIN = log_obj
        user_obj.save()
        return HttpResponse("<script>alert('Registered Successfully');window.location='/user_register'</script>")

def user_view_category(request):
    data=Category.objects.all()
    # data = Category.objects.filter(id=wid)
    return render(request,"user/view_categories.html",{"data":data})

# def user_view_workers(request,wid):
#     # data = Worker.objects.filter(CATEGORY=Category.objects.get(id=wid))
#     data = Worker.objects.filter(Q(LOGIN__type='worker') | Q(LOGIN__type='block'))
#     return render(request,"user/view_workers.html",{"data":data})

def user_approved_worker(request,wid):
    data = Worker.objects.filter(Q(LOGIN__type='worker') , CATEGORY=Category.objects.get(id=wid))
    return render(request,"user/view_approved_workers.html",{"data":data,"wid":wid})

def user_view_service(request,id):
    data = Service.objects.filter(WORKER=Worker.objects.get(id=id))
    return render(request,"user/view_services.html",{"data":data,"id":id})

def user_booking_map(request,rid,amount):
    return render(request,"user/booking_map.html",{"rid":rid,"am":amount})

def user_send_request(request,rid,amount):
    la = request.POST['textfield9']
    lo = request.POST['textfield10']

    booking_obj = Bookings()
    booking_obj.date = datetime.datetime.now().strftime("%Y-%m-%d")
    booking_obj.amount = amount
    booking_obj.lattitude = la
    booking_obj.longitude = lo
    booking_obj.status = 'pending'
    booking_obj.payment_status = 'pending'
    booking_obj.USER = User.objects.get(LOGIN=request.session['lid'])
    booking_obj.SERVICE = Service.objects.get(id=rid)
    booking_obj.save()
    return HttpResponse("<script>alert('Request sended');window.location ='/user_view_category'</script>")
    # return render(request,"user/booking_map.html")

def user_view_request(request):
    data = Bookings.objects.filter(USER=User.objects.get(LOGIN=request.session['lid']))
    return render(request,"user/view_request.html",{"data":data})

def user_view_bill(request,bid):
    data = Bill.objects.filter(id=bid)
    return render(request,"user/view_bill.html",{"data":data})

def user_add_rating(request,rid):
    return render(request,"user/rate.html",{"rid":rid})

def user_add_rate_post(request,rid):
    rate = request.POST['star']
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    review = request.POST['textarea']
    rating = Rating.objects.filter(BOOKINGS__SERVICE=Service.objects.get(id=rid) , BOOKINGS__USER=User.objects.get(LOGIN=request.session['lid']))
    if rating.exists():
        rating=rating[0]
        rating.rate = rate
        rating.date = date
        rating.review = review
        rating.save()
    else:
        rate_obj = Rating()
        rate_obj.rate = rate
        rate_obj.date = date
        rate_obj.review = review
        rate_obj.BOOKINGS = Bookings.objects.get(id=rid)
        rate_obj.save()
    return HttpResponse("<script>alert('Rate added');window.location='/user_view_request'</script>")

def user_view_rating(request,rid):
    data = Rating.objects.filter(BOOKINGS__SERVICE__WORKER = Worker.objects.get(LOGIN=request.session['lid']))
    lis=[]
    for i in data:
        rt=[]
        nrt=[]
        for j in range(int(i.rate)):
            rt.append(j)
        for j in range(5-int(i.rate)):
            nrt.append(j)
            dict = {'name': i.BOOKINGS.USER.name, 'date': i.date, 'rate': rt, 'norate': nrt, 'review': i.review}
        lis.append(dict)
    return render(request,"User/view_rate.html",{"data":lis,"rid":rid})

def user_view_credit_point(request):            # Credit Point View
    data = Credit_point.objects.filter(LOGIN = Login.objects.get(id=request.session['lid']))
    return render(request,"user/view_credit_point.html",{"data":data})

def list_worker_chat(request):
    data = Worker.objects.all()
    return render(request,"user/chat_with_worker.html",{"data":data})

def user_chat_worker(request,i):
    data = Chat.objects.filter(USER=User.objects.get(LOGIN=request.session['lid']))
    data1=Chat.objects.filter(WORKER=Worker.objects.get(id=i))
    print(data1)
    return render(request,"user/chat.html",{"i":i,"data":data,"data":data1})

def user_chat_worker_post(request,i):
    chat = request.POST['textfield']
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    chat_obj = Chat()
    chat_obj.chat = chat
    chat_obj.date = date
    chat_obj.type = 'user'
    chat_obj.USER = User.objects.get(LOGIN=request.session['lid'])
    chat_obj.WORKER = Worker.objects.get(id=i)
    chat_obj.save()
    return HttpResponse("<script>alert('Chat send');window.location='/user_chat_worker/"+i+"'</script>")

def user_send_complaint(request):
    return render(request,"user/send_complaint.html")

def user_send_complaint_post(request):
    complaint = request.POST['textarea']
    complaint_date = datetime.datetime.now().strftime("%Y-%m-%d")
    complaint_obj=Complaint()
    complaint_obj.complaint = complaint
    complaint_obj.complaint_date = complaint_date
    complaint_obj.reply = 'pending'
    complaint_obj.reply_date = '0000-00-00'
    complaint_obj.USER = User.objects.get(LOGIN=request.session['lid'])
    complaint_obj.save()
    return HttpResponse("<script>alert('complaint send');window.location='/user_send_complaint'</script>")

def user_view_reply(request):
    data = Complaint.objects.filter(USER__LOGIN=request.session['lid'])
    return render(request,"User/view_reply.html",{"data":data})

def user_change_password(request):
    return render(request,"user/change_password.html")

def user_change_password_post(request):
    old_password = request.POST['textfield2']
    new_password = request.POST['textfield3']
    confirm_password = request.POST['textfield3']

    Login.objects.get(password=old_password,id=request.session['lid'])

    if new_password == confirm_password:
        if Login.objects.filter(Q(password=new_password) | Q(password=new_password)).exists():
            return HttpResponse("<script>alert('Password already exist');window.location='/user_change_password'</script>")
        else:
            Login.objects.filter(id=request.session['lid']).update(password=confirm_password)
            return HttpResponse("<script>alert('password updated');window.location='/user_change_password'</script>")
    else:
        return HttpResponse("<script>alert('password mismatch');window.location='/user_change_password'</script>")

    # return redirect('/admin_change_password')

# Worker Bank Management

def worker_add_bank(request):
    return render(request,"worker/worker_bank.html")

def worker_add_bank_post(request):
    bank_name = request.POST['textfield']
    account_no = request.POST['textfield2']
    IFSC_code = request.POST['textfield3']


    amount = random.randint(500,100000)             # To add random values for amount
    data = Bank.objects.filter(LOGIN=Login.objects.get(id=request.session['lid']))
    if data.exists():
        return HttpResponse("<script>alert('Could not add Bank');window.location='/worker_view_bank'</script>")
    else:

        bank_obj = Bank()
        bank_obj.bank_name = bank_name
        bank_obj.account_no = account_no
        bank_obj.IFSC_code = IFSC_code
        bank_obj.amount = amount
        bank_obj.LOGIN = Login.objects.get(id=request.session['lid'])
        bank_obj.save()
        return HttpResponse("<script>alert('Bank details added');window.location='/worker_add_bank'</script>")

def worker_view_bank(request):
    data = Bank.objects.filter(LOGIN=Login.objects.get(id=request.session['lid']))
    return render(request,"worker/view_bank.html",{"data":data})

def worker_delete_bank(request,bid):
    Bank.objects.get(id=bid).delete()
    return HttpResponse("<script>alert('Bank details removed');window.location='/worker_view_bank'</script>")

# User Bank Management

def user_add_bank(request):
    return render(request,"user/bank.html")

def user_add_bank_post(request):
    bank_name = request.POST['textfield']
    account_no = request.POST['textfield2']
    IFSC_code = request.POST['textfield3']
    # amount = ''

    amount = random.randint(500,100000)             # To add random values for amount
    bank_obj = Bank()
    bank_obj.bank_name = bank_name
    bank_obj.account_no = account_no
    bank_obj.IFSC_code = IFSC_code
    bank_obj.amount = amount
    bank_obj.LOGIN = Login.objects.get(id=request.session['lid'])
    bank_obj.save()
    return HttpResponse("<script>alert('Bank details added');window.location='/user_add_bank'</script>")

def user_view_bank(request):
    data = Bank.objects.filter(LOGIN=Login.objects.get(id=request.session['lid']))
    return render(request,"user/view_bank.html",{"data":data})

def user_delete_bank(request,bid):
    Bank.objects.get(id=bid).delete()
    return HttpResponse("<script>alert('User Bank details removed');window.location='/user_view_bank'</script>")

def user_make_payment(request,rid):
    bobj = Bookings.objects.get(id=rid)
    request.session['orginalamount'] = bobj.amount
    request.session['requestid'] = rid
    return render(request,"user/payment.html",{"rid":rid})

def user_make_payment_post(request,rid):
    payment = request.POST['RadioGroup1']

    if payment == 'Offline':
        Bookings.objects.filter(id=rid).update(payment_status='offline')
        return HttpResponse("<script>alert('payment process is offline');window.location='/user_view_request'</script>")
    else:
        bobj = Bookings.objects.get(id=rid)
        request.session['paymode'] = 'using online'
        return redirect('/user_bank_details/'+rid+'/'+str(bobj.SERVICE.WORKER.LOGIN.id)+'/'+str(bobj.amount))

def user_bank_details(request,rid,wid,amount):
    return render(request,"user/bank_details.html",{"rid":rid,"wid":wid,"amount":amount})

def user_bank_details_post(request,rid,wid,amount):
    bank_name = request.POST['textfield']
    account_no = request.POST['textfield2']
    IFSC_code = request.POST['textfield3']
    amount = request.POST['textfield4']
    data = Bank.objects.filter(bank_name = bank_name,account_no = account_no,IFSC_code = IFSC_code,     # Checking the account already exist
                            LOGIN=request.session['lid'])

    if data.exists():
        if int(data[0].amount)  >= int(amount):
            userbank = Bank.objects.filter(LOGIN = Login.objects.get(id=request.session['lid']))
            balance = int(userbank[0].amount) - int(amount)
            userbank = Bank.objects.filter(id = userbank[0].id)
            userbank.update(amount = balance)
            Bookings.objects.filter(id=rid).update(payment_status ='Online')

            workerbank = Bank.objects.filter(LOGIN = Login.objects.get(id=wid))
            balance = int(workerbank[0].amount) + int(amount)
            workerbank.update(amount = balance)

            if request.session['paymode'] == 'using credit point':
                ucredit = Credit_point.objects.filter(LOGIN=Login.objects.get(id=request.session['lid']))
                if ucredit.exists():
                    cr = int(ucredit[0].credit_point) - int(request.session['credit'])
                    ucredit.update(credit_point=cr)

            if int(amount) >= 1000:

                ucredit = Credit_point.objects.filter(LOGIN = Login.objects.get(id=request.session['lid']))
                if ucredit.exists():
                    cr = int(ucredit[0].credit_point) + 10
                    ucredit.update(credit_point = cr)
                else:

                    cobj = Credit_point()  # Adding Credit point
                    cobj.credit_point = 10
                    cobj.LOGIN = Login.objects.get(id=request.session['lid'])
                    cobj.save()

                bobj = Bookings.objects.get(id=rid)
                wcredit = Credit_point.objects.filter(LOGIN=Login.objects.get(id=bobj.SERVICE.WORKER.LOGIN.id))
                if wcredit.exists():
                    cr = int(wcredit[0].credit_point) + 10
                    wcredit.update(credit_point=cr)
                else:
                    crobj = Credit_point()
                    crobj.credit_point = 10
                    crobj.LOGIN = Login.objects.get(id=bobj.SERVICE.WORKER.LOGIN.id)
                    crobj.save()

                return HttpResponse("<script>alert('Bank amount added');window.location='/user_view_request'</script>")
        else:
            return HttpResponse("<script>alert('Inefficient balance');window.location='/user_view_request'</script>")
    else:
        return HttpResponse("<script>alert('Does not have account');window.location='/user_view_request'</script>")

def worker_view_credit_point(request):
    data = Credit_point.objects.filter(LOGIN = Login.objects.get(id=request.session['lid']))
    return render(request,"worker/view_credit_point.html",{"data":data})

def worker_credit_convert(request,cid):                 # credit point conversion to account
    credit_point = Credit_point.objects.filter(LOGIN = Login.objects.get(id=request.session['lid']))
    workerbank = Bank.objects.filter(LOGIN = Login.objects.get(id=request.session['lid']))
    balance = int(workerbank[0].amount) + int(credit_point[0].credit_point)
    workerbank.update(amount = balance)
    credit_point.update(credit_point = 0)

    return HttpResponse("<script>alert('credit inserted to bank');window.location='/worker_view_credit_point/"+cid+"'</script>")


def ajax_view_credit_points(request):
    amt = request.session['orginalamount']
    q = Credit_point.objects.filter(LOGIN = Login.objects.get(id=request.session['lid']))

    if q.exists():
        if int(q[0].credit_point)>0:
            payable = q[0].credit_point  # credit point to amount conversion (10 points = 1rupee)
            balance = int(amt) - int(payable)  # calculating balance amount
            request.session['gtm'] = balance
            request.session['credit'] = payable

            return JsonResponse({"data": "ok", "credit": q[0].credit_point, "payable": payable, "balance": balance})
        else:
            return JsonResponse({"data": "no"})  # no credit points

    else:
        return JsonResponse({"data": "no"})  # no credit points

def credit_payment_mode(request):
    rid = request.session['requestid']
    bobj = Bookings.objects.get(id=rid)
    request.session['paymode'] = 'using credit point'
    return redirect('/user_bank_details/' + rid + '/' + str(bobj.SERVICE.WORKER.LOGIN.id) + '/' + str(request.session['gtm']))




