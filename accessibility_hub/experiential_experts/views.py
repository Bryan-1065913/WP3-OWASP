from django.shortcuts import render, redirect
from administrators.models import Medewerker, Ervaringsdeskundige, Beperking
from experiential_experts.forms import CreateExpertForm, LoginFormExpert
from companies.models import Onderzoek
from django.urls import reverse

# Authenticatie imports voor de login
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.hashers import check_password


def signup(request):
    beperkingen = Beperking.objects.all()
    if request.method == 'POST':
        form = CreateExpertForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            print(email)
            if Ervaringsdeskundige.objects.filter(email=email).exists():
                messages.success(request, 'E-mail is al in gebruik!')
            else:
                voornaam = request.POST.get('firstName')
                achternaam = request.POST.get('lastName')
                wachtwoord = request.POST.get('password')
                geslacht = request.POST.get('gender')
                telefoonnummer = request.POST.get('phonenumber')
                geboortedatum = request.POST.get('birthday')
                postcode = request.POST.get('zipCode')
                huisnummer = request.POST.get('housenumber')
                soort_beperking = request.POST.getlist('disability')
                hulpmiddelen = request.POST.get('tools')
                bijzonderheden = request.POST.get('particulars')

                naam_toezichthouder = request.POST.get('supervisorName')
                email_toezichthouder = request.POST.get('email_supervisor')
                telefoonnummer_toezichthouder = request.POST.get('phonenumber_supervisor')
                benadering_keuze = request.POST.get('approach_choice')

                if not naam_toezichthouder or not email_toezichthouder or not telefoonnummer_toezichthouder:
                    naam_toezichthouder = None
                    email_toezichthouder = None
                    telefoonnummer_toezichthouder = None

                aanmaken_ervaringsdeskundige = Ervaringsdeskundige.objects.create(
                    voornaam=voornaam,
                    achternaam=achternaam,
                    wachtwoord=wachtwoord,
                    geboortedatum=geboortedatum,
                    telefoonnummer=telefoonnummer,
                    email=email,
                    geslacht=geslacht,
                    postcode=postcode,
                    huisnummer=huisnummer,
                    soort_beperking=soort_beperking,
                    hulpmiddelen=hulpmiddelen,
                    bijzonderheden=bijzonderheden,

                    naam_toezichthouder=naam_toezichthouder,
                    email_toezichthouder=email_toezichthouder,
                    telefoonnummer_toezichthouder=telefoonnummer_toezichthouder,
                    benadering_keuze=benadering_keuze
                )
                if aanmaken_ervaringsdeskundige:
                    return redirect('../login')
                else:
                    messages.success(request, ('Er is iets fout gegaan, probeer het opnieuw.'))
        else:
            messages.success(request, ('Er is iets fout gegaan, probeer het opnieuw'))
    else:
        form = CreateExpertForm()
    return render(request, 'signupExpert.html', {'beperkingen': beperkingen})


def login(request):
    form = LoginFormExpert()
    if request.method == 'POST':
        form = LoginFormExpert(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            wachtwoord = request.POST.get('wachtwoord')
            print(email, wachtwoord)
            ervaringsdeskundige = Ervaringsdeskundige.objects.filter(email=email).first()
            if ervaringsdeskundige and check_password(wachtwoord, ervaringsdeskundige.wachtwoord):
                if ervaringsdeskundige.account_status == 1 or ervaringsdeskundige.account_status == 2:
                    request.session['deskundige_id'] = ervaringsdeskundige.deskundige_id
                    request.session['voornaam'] = ervaringsdeskundige.voornaam
                    request.session['achternaam'] = ervaringsdeskundige.achternaam
                    request.session['email'] = ervaringsdeskundige.email
                    if ervaringsdeskundige.account_status == 2:
                        return redirect(reverse('overzicht_afkeuring', args=[ervaringsdeskundige.deskundige_id]))
                    else:
                        return redirect('../onderzoek_overzicht')
                else:
                    messages.success(request, ('Inloggen mislukt. U moet nog wachten op goedkeuring van uw account!'))
            else:
                messages.success(request, ('Inloggen mislukt. Ongeldige email of wachtwoord.'))
        else:
            messages.success(request, ('Er is iets fout gegaan, probeer het opnieuw.'))
            print('Formulier is niet geldig')
    else:
        print('Geen POST-verzoek ontvangen.')

    context = {'loginform': form}

    return render(request, 'loginExpert.html', context=context)


def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('../ervaringsdeskundigen/login')


def overzicht_ervaringsdeskundige(request):
    ervaringsdeskundige = Ervaringsdeskundige.objects.get(deskundige_id=request.session['deskundige_id'])
    return render(request, 'overzicht_ervaringsdeskundige.html', {'ervaringsdeskundige': ervaringsdeskundige})


def overzicht_afkeuring(request, deskundige_id):
    ervaringsdeskundige = Ervaringsdeskundige.objects.get(deskundige_id=deskundige_id)
    return render(request, 'overzicht_afkeuring.html', {'ervaringsdeskundige': ervaringsdeskundige})


def aanpassen_ervaringsdeskundige(request):
    beperkingen = Beperking.objects.all()
    if request.method == 'POST':
        ervaringsdeskundige = Ervaringsdeskundige.objects.get(deskundige_id=request.session['deskundige_id'])
        ervaringsdeskundige.voornaam = request.POST.get('firstName')
        ervaringsdeskundige.achternaam = request.POST.get('lastName')
        ervaringsdeskundige.wachtwoord = request.POST.get('password')
        ervaringsdeskundige.geslacht = request.POST.get('gender')
        ervaringsdeskundige.telefoonnummer = request.POST.get('phonenumber')
        ervaringsdeskundige.geboortedatum = request.POST.get('birthday')
        ervaringsdeskundige.postcode = request.POST.get('zipCode')
        ervaringsdeskundige.huisnummer = request.POST.get('housenumber')
        ervaringsdeskundige.soort_beperking = request.POST.getlist('disability')
        ervaringsdeskundige.hulpmiddelen = request.POST.get('tools')
        ervaringsdeskundige.bijzonderheden = request.POST.get('particulars')

        naam_toezichthouder = request.POST.get('supervisorName')
        email_toezichthouder = request.POST.get('email_supervisor')
        telefoonnummer_toezichthouder = request.POST.get('phonenumber_supervisor')

        if not naam_toezichthouder or not email_toezichthouder or not telefoonnummer_toezichthouder:
            ervaringsdeskundige.naam_toezichthouder = None
            ervaringsdeskundige.email_toezichthouder = None
            ervaringsdeskundige.telefoonnummer_toezichthouder = None
        else:
            ervaringsdeskundige.naam_toezichthouder = request.POST.get('supervisorName')
            ervaringsdeskundige.email_toezichthouder = request.POST.get('email_supervisor')
            ervaringsdeskundige.telefoonnummer_toezichthouder = request.POST.get('phonenumber_supervisor')
            ervaringsdeskundige.benadering_keuze = request.POST.get('approach_choice')

        ervaringsdeskundige.save()
        messages.success(request, ('Account is succesvol aangepast.'))
        return redirect('../overzicht_ervaringsdeskundige')
    else:
        ervaringsdeskundige = Ervaringsdeskundige.objects.get(deskundige_id=request.session['deskundige_id'])
        return render(request, 'aanpassen_ervaringsdeskundige.html',
                      {'ervaringsdeskundige': ervaringsdeskundige, 'beperkingen': beperkingen})


def onderzoek_overzicht(request):
    if 'deskundige_id' in request.session:
        deskundige_id = request.session['deskundige_id']

        ingeschreven_onderzoeken = Onderzoek.objects.filter(ervaringsdeskundige__deskundige_id=deskundige_id)

        onderzoeken = Onderzoek.objects.all()
        return render(request, 'onderzoek_overzicht.html',
                      {'ingeschreven_onderzoeken': ingeschreven_onderzoeken, 'onderzoeken': onderzoeken,
                       'deskundige_id': deskundige_id})
    else:
        return redirect('../login')


def inschrijven(request, onderzoek_id):
    onderzoek = Onderzoek.objects.get(onderzoek_id=onderzoek_id)
    onderzoek.deskundige_id = request.session['deskundige_id']
    onderzoek.save()

    return redirect('../onderzoek_overzicht/')


def uitschrijven(onderzoek_id):
    onderzoek = Onderzoek.objects.get(onderzoek_id=onderzoek_id)
    onderzoek.deskundige_id = None
    onderzoek.save()

    return redirect('../onderzoek_overzicht/')
