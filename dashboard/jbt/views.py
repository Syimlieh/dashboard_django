from django.shortcuts import render
from django.contrib import messages, auth
from .forms import UserLoginForm, UserRegistrationForm
from django.urls import reverse
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import WhatDoWant, BriefOverview, GrantApplyFor
from .forms import WhatDoWantForm #, BriefOverview
import requests

url = "https://api.writesonic.com/v2/business/content/chatsonic?engine=premium&language=en"

def WhatDoYouWant(request):
    if request.method == "POST":
        form = WhatDoWantForm(request.POST, request.FILES)
        if form.is_valid():
            inv = form.save(commit=False)
            inv.user = request.user
            inv.save()
            return redirect('/provide_brief', inv.pk)
    else:
        form = WhatDoWantForm()
    return render(request, 'what_do_want.html', {'form': form})

@login_required(login_url="/?next=provide_brief")
def ProvideBrief(request):
    if request.method == "POST":
        print(request.user)
        story = request.POST["story"]
        feature_1 = request.POST["Feature_1"]
        feature_2 = request.POST["Feature_2"]
        feature_3 = request.POST["Feature_3"]
        feature_4 = request.POST["Feature_4"]
        feature_5 = request.POST["Feature_5"]
        competitor_1 = request.POST["Competitor_1"]
        competitor_2 = request.POST["Competitor_2"]
        competitor_3 = request.POST["Competitor_3"]
        app_choice = request.POST["app"]
        obj, created = BriefOverview.objects.update_or_create(
        user=request.user, project_overview=story, feature_1=feature_1, feature_2=feature_2, feature_3=feature_3, feature_4=feature_4, feature_5=feature_5, competitor_1=competitor_1, competitor_2=competitor_2, competitor_3=competitor_3, app_choice=app_choice
        )
        return redirect(reverse('innovatescreen'))
        # try:
        #     project_reco = BriefOverview.objects.get(user=request.user,)
        #     return render(request, "provide_brief_screen.html", {"message": "records already exist"})
        # except BriefOverview.DoesNotExist:
        #     BriefOverview.objects.create(user=request.user, project_overview=story, feature_1=feature_1, feature_2=feature_2, feature_3=feature_3, feature_4=feature_4, feature_5=feature_5, competitor_1=competitor_1, competitor_2=competitor_2, competitor_3=competitor_3, app_choice=app_choice)
        #     return render(request, "provide_brief_screen.html")
        
    return render(request, "provide_brief_screen.html")
     
def InnovateScreen(request):
    get_brf = BriefOverview.objects.filter(user=request.user).latest('id').id
    abc = BriefOverview.objects.get(id=get_brf)
    print(abc.app_choice)
    payload = {
    "enable_google_results": "true",
    "enable_memory": False,
    "input_text": "Based on the overview of the project: "+abc.project_overview+" key features of the project: \n"+abc.feature_1+"\n"+abc.feature_2+"\n"+abc.feature_3+"\n"+abc.feature_4+"\n"+" and main competitors of the project: \n"+abc.competitor_1+"\n"+abc.competitor_2+"\n"+abc.competitor_3+". Create the problem statement, The solution and the technologies/AI/ML that we used in this project."
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-API-KEY": "c242f481-52c8-4ffe-a87f-48f116cb27da"
    }

    response = requests.post(url, json=payload, headers=headers)
    # print("Overview of the project: "+abc.project_overview+" Five key features of the project: /n"+abc.feature_1+"/n"+abc.feature_2+"/n"+abc.feature_3+"/n"+abc.feature_4+"/n"+"Main competitors of the project: /n"+abc.competitor_1+"/n"+abc.competitor_2+"/n"+abc.competitor_3)
    # print("*****************")
    data = response.json()
    return render(request, "innovate_screen.html", {"response":data})

def Home(request):
    if request.method == "POST":
        if request.POST.get('choicechk') != None:
            grant_type = request.POST.get('choicechk')
            obj, created = GrantApplyFor.objects.update_or_create(user=request.user, grant_type=grant_type)
            return redirect(PreQualFeed) 
        if request.POST.get('choicechk') == None:
            print("Checking is None")
            c = {"message": "Must be select any one"}
            return render(request, "home.html", {"message": "Please choose any one"})
    return render(request, "home.html")

def Login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(username=request.POST.get('username_or_email'),
                                     password=request.POST.get('password'))

            if user is not None:
                auth.login(request, user)
                messages.error(request, "You have successfully logged in")

                if request.GET and 'next' in request.GET:
                    next = request.GET['next']
                    return HttpResponseRedirect(next)
                else:
                    return redirect(reverse('what_do_want'))
            else:
                form.add_error(None, "Your username or password was not recognised")

    else:
        # this handles the initial get request
        # return a blank form for user to login
        form = UserLoginForm()

    # prepare args to pass to render function
    #   form:   this is the form which will be rendered to html (UserLoginForm)
    #   next:   if the url of the request included a next query string '?next=' pass it to the form
    #           so that it can be included in the url when the form is resubmitted
    #           see handling of post method: next = request.GET['next']
    args = {'form': form, 'next': request.GET['next'] if request.GET and 'next' in request.GET else ''}
    args.update(csrf(request))
    return render(request, 'login.html', args)

def logout(request):
    auth.logout(request)
    messages.success(request, 'You have successfully logged out')
    return redirect(reverse('login'))

def Register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            #do an early save so that if user input is invalid/ unauthorised new form can be loaded with valide details previously entered
            form.save()

            #user has a valid username and password, if not a user then we will drop out of this code and reload form on line X
    #else:
        #form= UserRegistrationForm()
            user = auth.authenticate(username=request.POST.get('username'),
                                     password=request.POST.get('password1'))

            #if valid user, then return success msg and redirect to home. Else provide error msg.
            if user:
                auth.login(request, user)
                messages.success(request, "You have successfully registered and are now logged into your account")
                return redirect(reverse('what_do_want'))

            else:
                messages.error(request, "Unable to log you in at this time.")

    else:
        form = UserRegistrationForm()

    args = {'form': form}
    args.update(csrf(request))


    return render(request, 'register.html', args)

def PreQualFeed(request):
        gr_type = GrantApplyFor.objects.get(user=request.user)
        g_type = gr_type.grant_type
        data = {
            "grant_type": g_type,
            
        }
        return render(request, "pre_qualification_feed.html")

def InnovationScore(request):
        return render(request, "innovation_score.html")

def PreQualReview(request):
        return render(request, "pre_qualification_tip_review.html")
