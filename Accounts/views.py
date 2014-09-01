from django.contrib.auth.models import User
from django.shortcuts import render, render_to_response

from Accounts.forms import UserProfileForm
from django.template import RequestContext

def index(request):
    context=RequestContext(request)
    return render_to_response("index.html",context)

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
