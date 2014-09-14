from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse

from django.shortcuts import render, render_to_response

from Accounts.forms import UserProfileForm
from django.template import RequestContext

def index(request):
    context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return render_to_response('profile.html', {}, context)
            else:
                error_message="Your have not activated your account. Please check your email and validate it"
                return render_to_response('registration/login.html', {'error_message':error_message}, context)
                # An inactive account was used - no logging in!

        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            error_message="Login details invalid"
            return render_to_response('registration/login.html', {'error_message':error_message}, context)

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('registration/login.html', {}, context)


def profile(request):
    context=RequestContext(request)
    return render_to_response("profile.html",{},context)

def register(request):
    context = RequestContext(request)
    registered = False
    some_errors= False
    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        profile_form = UserProfileForm(data=request.POST)
        if profile_form.is_valid():
            # Save the user's form data to the database.
            user = User.objects.create_user(username=profile_form.cleaned_data['username'], \
                                            email = profile_form.cleaned_data['email'], \
                                            password = profile_form.cleaned_data['password'], \
                                            first_name=profile_form.cleaned_data['first_name'])
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
                print "Yes the picture exists"
            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True


        else:
            some_errors=True
            return render_to_response(
            'signup.html',
            { 'profile_form': profile_form, 'registered': registered,'some_errors':some_errors},
            context)

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:

        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render_to_response(
            'signup.html',
            { 'profile_form': profile_form, 'registered': registered},
            context)
