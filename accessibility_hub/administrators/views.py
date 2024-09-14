from .forms import CreateEmployeeForm, LoginForm
from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from .models import Medewerker, Ervaringsdeskundige, Beperking
from companies.models import Organisatie, Onderzoek, Vraag
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from .forms import LoginForm



def login_view(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            gebruikersnaam = form.cleaned_data.get('gebruikersnaam')
            wachtwoord = form.cleaned_data.get('wachtwoord')

            user = authenticate(request, username=gebruikersnaam, password=wachtwoord)
            if user is not None:
                auth_login(request, user)

                medewerker = Medewerker.objects.filter(gebruikersnaam=gebruikersnaam).first()
                if medewerker:
                    request.session['medewerker_id'] = medewerker.medewerker_id
                    request.session['voornaam'] = medewerker.voornaam
                    request.session['achternaam'] = medewerker.achternaam
                    request.session['gebruikersnaam'] = medewerker.gebruikersnaam
                    request.session['emailadres'] = medewerker.emailadres
                    request.session['admin'] = medewerker.admin

                return redirect('../portal')
            else:
                messages.error(request, 'Inloggen mislukt. Ongeldige gebruikersnaam of wachtwoord.')
        else:
            messages.error(request, 'Formulier is niet geldig. Probeer opnieuw.')
    else:
        print('Geen POST-verzoek ontvangen.')

    context = {'loginform': form}
    return render(request, 'login.html', context=context)

def signup(request):
    if request.method == 'POST':
        form = CreateEmployeeForm(request.POST)
        gebruikersnaam = request.POST.get('gebruikersnaam')
        emailadres = request.POST.get('email')
        if Medewerker.objects.filter(gebruikersnaam=gebruikersnaam).exists(): 
            messages.success(request, ('Gebruikersnaam is al ingebruik!'))
        elif Medewerker.objects.filter(emailadres=emailadres).exists():
            messages.success(request, ('Email is al ingebruik!'))
        elif form.is_valid():
                form.save()
                return redirect('../portal')
        else:
            messages.success(request, ('Er is iets fout gegaan, probeer het opnieuw'))

    else:
        form = CreateEmployeeForm()
    return render(request, 'signup.html', {'form': form})  

def logout_view(request):
    logout(request)
    request.session.flush()
    messages.success(request, ('U bent uitgelogd!'))
    return redirect('../login') 

def get_deskundige_in_behandeling_ajax(request):
    in_behandeling = 0
    ervaringsdeskundige_status =  Ervaringsdeskundige.objects.filter(account_status=in_behandeling).values(
        'deskundige_id', 'voornaam', 'achternaam', 'geboortedatum', 'email', 'telefoonnummer', 'soort_beperking', 'created_at', 'account_status'
    )
    data = {
        'ervaringsdeskundigen': list(ervaringsdeskundige_status),
    }
    return JsonResponse(data)

def get_alle_deskundige_ajax(request):
    goedgekeurd = 1
    afgekeurd = 2 
    ervaringsdeskundigen = Ervaringsdeskundige.objects.filter(Q(account_status=goedgekeurd) | Q(account_status=afgekeurd)).values(
        'deskundige_id', 'voornaam', 'achternaam', 'geboortedatum', 'email', 'telefoonnummer', 'soort_beperking', 'created_at', 'account_status'
    )
    data = {
        'ervaringsdeskundigen': list(ervaringsdeskundigen),
    }
    return JsonResponse(data)

def portal(request):
    onderzoeken = Onderzoek.objects.all()
    medewerkers = Medewerker.objects.all()
    organisaties = Organisatie.objects.all()
    beperkingen = Beperking.objects.all()
    return render(request, 'portal.html',
                  {'onderzoeken': onderzoeken, 'medewerkers': medewerkers, 'organisaties': organisaties, 'beperkingen': beperkingen})

def ervaringsdeskundige(request, deskundige_id):
    ervaringsdeskundige = Ervaringsdeskundige.objects.get(deskundige_id=deskundige_id)
    return render(request, 'experts.html', {'ervaringsdeskundige': ervaringsdeskundige})

def goedkeuren_deskundige(request, deskundige_id):
    if request.method == 'POST':
        ervaringsdeskundige = Ervaringsdeskundige.objects.get(deskundige_id=deskundige_id)
        ervaringsdeskundige.account_status = '1'
        ervaringsdeskundige.bericht_status = None
        ervaringsdeskundige.save()
        messages.success(request, ('Account status is succesvol aangepast.'))
        return redirect('../../ervaringsdeskundige/' + str(deskundige_id))

def afkeuren_deskundige(request, deskundige_id):
    if request.method == 'POST':
        ervaringsdeskundige = Ervaringsdeskundige.objects.get(deskundige_id=deskundige_id)
        bericht_status = request.POST.get('bericht_status')
        ervaringsdeskundige.bericht_status = bericht_status
        print(bericht_status)
        ervaringsdeskundige.account_status = '2'
        ervaringsdeskundige.save()
        messages.success(request, ('Account status is succesvol aangepast.'))
        return redirect('../../ervaringsdeskundige/' + str(deskundige_id))

def medewerker(request, medewerker_id):
    medewerker = Medewerker.objects.get(medewerker_id=medewerker_id)
    return render(request, 'employee.html', {'medewerker': medewerker})


def verwijder_medewerker(request, medewerker_id):
    medewerker = get_object_or_404(Medewerker, medewerker_id=medewerker_id)
    medewerker.delete()
    return redirect('administrators:portal')


def organisatie(request, id):
    organisatie = Organisatie.objects.get(id=id)
    return render(request, 'organisation.html', {'organisatie': organisatie})


def verwijder_organisatie(request, id):
    organisatie = get_object_or_404(Organisatie, id=id)
    organisatie.status = 'Afgekeurd'
    organisatie.save()

    message = (
        f'Beste {organisatie.first_name} {organisatie.last_name},\n\n'
        f'Uw aanvraag is afgekeurd. Helaas kunnen wij u geen toegang geven tot de applicatie.\n\n'
        f'Met vriendelijke groet,\n'
        'Het team van de Accessibility Hub'
    )

    send_mail(
        'Afkeuring van uw aanvraag',
        message,
        settings.EMAIL_HOST_USER,
        [organisatie.email],
        fail_silently=False,
    )
    return redirect('administrators:medewerkersportal')


def accepteer_organisatie(request, id):
    organisatie = get_object_or_404(Organisatie, id=id)
    organisatie.status = 'Geaccepteerd'
    organisatie.save()

    message = (
        f'Beste {organisatie.first_name} {organisatie.last_name},\n\n'
        f'Uw aanvraag is geaccepteerd. U kunt nu inloggen op de website.\n'
        f'Hier is uw persoonlijke API-sleutel: {organisatie.token}\n\n'
        f'Met vriendelijke groet,\n'
        'Het team van de Accessibility Hub'
    )

    send_mail(
        'Goedkeuring van uw aanvraag',
        message,
        settings.EMAIL_HOST_USER,
        [organisatie.email],
        fail_silently=False,
    )
    return redirect('administrators:medewerkersportal')


def mail(request):
    if request.method == 'POST':
        message = request.POST.get('message', '')
        email = request.POST.get('email', '')
        subject = request.POST.get('subject', '')

        if message and email and subject:
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            return redirect('administrators:signup')
        else:
            print("Dat ging mis")
            return render(request, 'mail.html')

    return render(request, 'mail.html')


def check_updates_organisaties(request):
    recent_organisaties = Organisatie.objects.filter(status='Nieuw').order_by('date_joined')[:10]

    data = [{'id': organisatie.id, 'bedrijfsnaam': organisatie.bedrijfsnaam, 'email': organisatie.email,
             'first_name': organisatie.first_name,
             'last_name': organisatie.last_name, 'status': organisatie.status, 'date_joined': organisatie.date_joined}
            for organisatie in
            recent_organisaties]

    return JsonResponse(data, safe=False)


def onderzoek(request, onderzoek_id):
    onderzoek = Onderzoek.objects.get(onderzoek_id=onderzoek_id)
    vragen = Vraag.objects.filter(onderzoek_id=onderzoek_id)
    return render(request, 'research.html', {'onderzoek': onderzoek, 'vragen': vragen})


def check_updates_onderzoek(request):
    recent_onderzoeken = Onderzoek.objects.filter(status='Nieuw')[:10]

    data = [{'id': onderzoek.onderzoek_id, 'titel': onderzoek.titel, 'organisatie': onderzoek.organisatie.bedrijfsnaam,
             'startdatum': onderzoek.startdatum, 'einddatum': onderzoek.einddatum, 'status': onderzoek.status}
            for onderzoek in
            recent_onderzoeken]

    return JsonResponse(data, safe=False)


def verwijder_onderzoek(request, onderzoek_id):
    onderzoek = get_object_or_404(Onderzoek, onderzoek_id=onderzoek_id)
    onderzoek.status = 'Afgekeurd'
    onderzoek.save()

    message = (
        f'Beste {onderzoek.organisatie.bedrijfsnaam},\n\n'
        f'Uw onderzoek is afgewezen.\n\n'
        f'Met vriendelijke groet,\n'
        'Het team van de Accessibility Hub'
    )

    send_mail(
        'Afkeuring van uw onderzoek',
        message,
        settings.EMAIL_HOST_USER,
        [onderzoek.organisatie.email],
        fail_silently=False,
    )
    return redirect('administrators:medewerkersportal')


def accepteer_onderzoek(request, onderzoek_id):
    onderzoek = get_object_or_404(Onderzoek, onderzoek_id=onderzoek_id)
    onderzoek.status = 'Geaccepteerd'
    onderzoek.save()

    message = (
        f'Beste {onderzoek.organisatie.bedrijfsnaam},\n\n'
        f'Uw onderzoek is geaccepteerd.\n\n'
        f'Met vriendelijke groet,\n'
        'Het team van de Accessibility Hub'
    )

    send_mail(
        'Goedkeuring van uw onderzoek',
        message,
        settings.EMAIL_HOST_USER,
        [onderzoek.organisatie.email],
        fail_silently=False,
    )
    return redirect('administrators:medewerkersportal')
