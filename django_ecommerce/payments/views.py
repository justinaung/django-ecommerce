import datetime

import stripe
from django.conf import settings
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from django_ecommerce.payments.forms import SigninForm, UserForm, CardForm
from django_ecommerce.payments.models import User

stripe.api_key = settings.STRIPE_SECRET


def soon():
    soon = datetime.date.today() + datetime.timedelta(days=30)
    return {'month': soon.month, 'year': soon.year}


def sign_in(request):
    user = None
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():
            results = User.objects.filter(email=form.cleaned_data['email'])
            if results.exist():
                if results[0].check_password(form.cleaned_data['password']):
                    request.session['user'] = results[0].pk
                    return redirect('/')
                else:
                    form.addError('Incorrect email address or password')
            else:
                form.addError('Incorrect email address or password')
    else:
        form = SigninForm()

    print(form.non_field_errors())

    return render(request, 'sign_in.html', {'form': form, 'user': user})


def sign_out(request):
    if request.session['user']:
        del request.session['user']
    return redirect('/')


def register(request):
    user = None
    if request.method == 'POST':
        form = UserForm(request.POST)
        print('@@@@@@@@@@@@@@@@@@@@@')
        print(request)
        print('@@@@@@@@@@@@@@@@@@@@@')
        print(form)
        if form.is_valid():
            # update based on your billing method (subscription vs one time)
            customer = stripe.Customer.create(
                email=form.cleaned_data['email'],
                description=form.cleaned_data['name'],
                card=form.cleaned_data['stripe_token'],
                plan='gold',
            )
            user = User(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                last_4_digits=form.cleaned_data['last_4_digits'],
                stripe_id=customer.id
            )

            # ensure encrpyted password
            user.set_password(form.cleaned_data['password'])

            try:
                user.save()
            except IntegrityError:
                form.addError(user.email + 'is already a member')
            else:
                request.session['user'] = user.pk
                return redirect('/')
    else:
        form = UserForm()

    context_dict = {
        'form': form,
        'months': range(1, 13),
        'publishable': settings.STRIPE_PUBLISHABLE,
        'soon': soon(),
        'user': user,
        'years': range(2011, 2036),
    }
    return render(request, 'register.html', context_dict)


def edit(request):
    uid = request.session.get('user')

    if uid is None:
        return HttpResponseRedirect('/')

    user = User.objects.get(pk=uid)

    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():
            customer = stripe.Customer.retrieve(user.stripe_id)
            customer.card = form.cleaned_data['stripe_token']
            customer.save()

            user.last_4_digits = form.cleaned_data['last_4_digits']
            user.stripe_id = customer.id
            user.save()

            return redirect('/')
    else:
        form = CardForm()

    context_dict = {
        'form': form,
        'publishable': settings.STRIPE_PUBLISHABLE,
        'soon': soon(),
        'months': range(1, 13),
        'years': range(2011, 2036)
    }
    return render(request, 'edit.html', context_dict)
