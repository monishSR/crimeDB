# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.shortcuts import get_object_or_404

from django.shortcuts import render_to_response

from django.db.models import Q

from .forms import SearchForm, entryForm

from .models import Criminal, Detective, Dependent, Crime, Case, AssignedTo, DependsOn, ConnectedTo

import re

from django.urls import reverse

from django.http import HttpResponseRedirect

from django.contrib.auth.decorators import permission_required

from django.contrib.auth.decorators import login_required

import os

criminal_attr = ('SSN',
                 'first_name',
                 'middle_name',
                 'last_name',
                 'dob',
                 'sex',
                 'height_in_ft',
                 'weight_in_kg',
                 'ethnicity',
                 'hair_colour',
                 'dist_mark',
                 'address',
                 'status',
                 'occupation'
                 )
dependent_attr = ('first_name',
                  'last_name',
                  'relationship',
                  'contact_no')
detective_attr = ('id',
                  'first_name',
                  'last_name')
crime_attr = ('type',)
case_attr = ('id',
             'location')
searchlist = []

records = []

query_string = []

locations=["Kingston upon Thames","Newham","Ealing","Kensington and Chelsea" ,"Bexley","Brent","Harrow","Merton",
           "Hillingdon","Waltham Forest","Lambeth","Richmond upon Thames" ,"Croydon","Westminster","Lewisham",
           "Enfield","Hammersmith and Fulham" ,"Barking and Dagenham","Redbridge","Bromley","Barnet","Camden",
           "Sutton","Southwark","Hackney","Havering","Wandsworth","Islington","Tower Hamlets","City of London",
           "Greenwich","Haringey","Hounslow"]

crimes=["Aiding & Abetting / Accessory","Assault / Battery","Drug Possession","Burglary","Theft / Larceny",
        "Arson","Aggravated Assault / Battery","Attempt","Bribery","Child Abandonment","Child Abuse",
        "Child Pornography","Computer Crime","Conspiracy","Credit / Debit Card Fraud","Criminal Contempt of Court",
        "Cyber Bullying","Disorderly Conduct","Disturbing the Peace","Domestic Violence",
        "Drug Manufacturing and Cultivation","Drug Trafficking / Distribution","DUI / DWI","Embezzlement",
        "Extortion","Forgery","Fraud","Harassment","Hate Crimes","Homicide","Indecent Exposure","Identity Theft","Insurance Fraud","Kidnapping","Manslaughter: Involuntary","Manslaughter: Voluntary","Medical Marijuana","MIP: A Minor in Possession","Money Laundering","Murder: First-degree","Murder: Second-degree","Open Container Law","Perjury","Probation Violation","Prostitution","Public Intoxication","Pyramid Schemes","Racketeering / RICO","Rape","Robbery","Securities Fraud","Sexual Assault","Shoplifting","Solicitation","Stalking","Statutory Rape","Tax Evasion / Fraud","Telemarketing Fraud","Vandalism","White Collar Crimes","Wire Fraud"]

# Create your views here.
def import_db_criminal(request):
    f = open('/home/pygram/crimeDB/src/core/records/Criminal Record.csv', 'r')
    for line in f:
        entry = line.split(',')
        tmp = Criminal.objects.get_or_create(SSN=entry[0],
                                             first_name=entry[1],
                                             middle_name=entry[2],
                                             last_name=entry[3],
                                             dob=entry[4],
                                             sex=entry[5],
                                             height_in_ft=entry[6],
                                             weight_in_kg=entry[7],
                                             ethnicity=entry[8],
                                             hair_colour=entry[9],
                                             dist_mark=entry[10],
                                             address=entry[11],
                                             status=entry[12],
                                             occupation=entry[13])
        print(entry[0])

    f.close()


def import_db_detective(request):
    f = open('/home/pygram/crimeDB/src/core/records/Detective Record.csv', 'r')
    for line in f:
        entry = line.split(',')
        tmp = Detective.objects.get_or_create(id=entry[0],
                                              first_name=entry[1],
                                              last_name=entry[2],
                                              contact_no=entry[3])
        print(entry[0])

    f.close()


def import_db_dependent(request):
    f = open('/home/pygram/crimeDB/src/core/records/Dependent.csv', 'r')
    for line in f:
        entry = line.split(',')
        tmp = Dependent.objects.get_or_create(
            first_name=entry[0],
            last_name=entry[1],
            relationship=entry[2],
            contact_no=entry[3])
        print(entry[0])

    f.close()


def import_db_crime(request):
    f = open('/home/pygram/crimeDB/src/core/records/Crime Record.csv', 'r')
    for line in f:
        entry = line.split(',')
        tmp = Crime.objects.get_or_create(id=entry[0],
                                          type=entry[1])
        print(entry[0])

    f.close()


def import_db_case(request):
    f = open('/home/pygram/crimeDB/src/core/records/Case.csv', 'r')
    for line in f:
        entry = line.split(',')
        entry[1] = get_object_or_404(Crime, id=entry[1])
        tmp = Case.objects.get_or_create(id=entry[0],
                                         crime=entry[1],
                                         location=entry[3],
                                         description=entry[2])
        print(entry[0])

    f.close()


def normalize_query(query_str,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_str)]


def get_query(terms, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.

    '''
    query = None  # Query to search for every search term

    for term in terms:
        or_query = None  # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query | or_query
    return query

@login_required
def search(request):
    form = SearchForm(request.POST or None)
    found_entries = None
    del searchlist[:]
    del query_string[:]
    if request.GET.get('Button'):
        print("Button pushed")
    if form.is_valid():
        query_string.append(form.cleaned_data['Search'])
        terms = normalize_query(query_string[0])

        #query matched with detective table
        det_query = get_query(terms, detective_attr)
        det_ids = Detective.objects.filter(det_query).values_list('id', flat=True)
        case_ids = AssignedTo.objects.filter(det_id__in=det_ids).values_list('case_id', flat=True)
        criminal_ssns = ConnectedTo.objects.filter(case_id__in=case_ids).values_list('SSN', flat=True)
        det_2_criminal = Criminal.objects.filter(SSN__in=criminal_ssns)

        #query matched with dependent
        dep_query = get_query(terms, dependent_attr)
        first_names = Dependent.objects.filter(dep_query).values_list('first_name', flat=True)
        second_names = Dependent.objects.filter(dep_query).values_list('last_name', flat=True)
        criminal_ssns = DependsOn.objects.filter(Q(dep_f_name__in=first_names) |
                                                 Q(dep_l_name__in=second_names)).values_list('SSN', flat=True)
        dep_2_criminal = Criminal.objects.filter(SSN__in=criminal_ssns)

        #query matched with case
        case_query = get_query(terms, case_attr)
        case_ids = Case.objects.filter(case_query).values_list('id', flat=True)
        criminal_ssns = ConnectedTo.objects.filter(case_id__in=case_ids).values_list('SSN', flat=True)
        case_2_criminal = Criminal.objects.filter(SSN__in=criminal_ssns)

        #query matched with crime
        crime_query = get_query(terms, crime_attr)
        crime_ids = Crime.objects.filter(crime_query).values_list('id', flat=True)
        case_ids = Case.objects.filter(crime__in=crime_ids).values_list('id', flat=True)
        criminal_ssns = ConnectedTo.objects.filter(case_id__in=case_ids).values_list('SSN', flat=True)
        crime_2_criminal = Criminal.objects.filter(SSN__in=criminal_ssns)

        #query matched with criminal
        criminal_query = get_query(terms, criminal_attr)
        criminal_entries = Criminal.objects.filter(criminal_query)
        found_entries = det_2_criminal | dep_2_criminal | criminal_entries | crime_2_criminal | case_2_criminal
        print(found_entries)
        [searchlist.append(entry.SSN) for entry in found_entries]
        ##for i in range(len(found_entries)-1, 0, -1):
        '''  for j in range(i):

             if find_match(found_entries[j]) < find_match(found_entries[j+1]):
                    temp = found_entries[j]
                    found_entries[j] = found_entries[j+1]
                    found_entries[j+1] = temp
        '''
        ##for entries in found_entries:
            ##print("{0} {1} {2} {3}".format(entries.SSN, entries.first_name, entries.middle_name, entries.last_name)
        if not searchlist:
            context = {'form': form, 'flag': False}
            return render(request, 'search.html', context)

        print('******')
        print(searchlist)
        # return render_to_response('search_result.html',
        #                  {'query_string': query_string, 'found_entries': found_entries})
        return HttpResponseRedirect(reverse('search_result'))
    '''return render_to_response('search/search_results.html',
                          {'query_string': query_string, 'found_entries': found_entries})
    '''
    context = {'form': form, 'flag': True}
    return render(request, 'search.html', context)

@login_required
def analyse(request):
    loc_data = [0 for _ in range(0, 34)]
    string = ''
    form1 = SearchForm()
    form = SearchForm()
    crime_data = [0 for _ in range(0, 62)]
    string = 'None'
    flag = False
    addr = False
    crime_data = [0 for _ in range(0, 62)]
    if request.method == 'GET':
        form = SearchForm()
    else:
        if request.POST.get('dropdown'):
            string = request.POST.get('dropdown')
            string = string + '\n'
            flag = True
            addr = True
            # string=unicode(string,"utf-8")
            print(string)
            record = Case.objects.filter(location=string)
            for x in record:
                crime_data[x.crime.id] += 1
            print(crime_data)
        elif request.POST.get('dropdown1'):
            string = request.POST.get('dropdown1')
            string = string + '\n'
            addr = False
            flag = True
            crime = Crime.objects.get(type=string)
            cases = Case.objects.filter(crime=crime.id)
            for case in cases:
                loc_data[locations.index(case.location.rstrip())] += 1

            print(loc_data)

    context = {'form': form, 'data': crime_data, 'string': string, 'locations': locations, 'flag': flag, 'form1': form1,
               'loc_data': loc_data, 'crimes': crimes, 'addr': addr}
    template = 'analysis.html'
    return render(request, template, context)


def find_tables(record):
    connected = ConnectedTo.objects.filter(SSN=record.SSN).values_list('case_id', flat=True)
    # caserec=Case.objects.get(id=1382)

    cases = Case.objects.filter(id__in=connected)
    case_ids = cases.values_list('id', flat=True)
    crime_ids = cases.values_list('crime', flat=True)
    # crime = Crime.objects.get(id=57)

    crimes_1 = Crime.objects.filter(id__in=crime_ids)

    assnto = AssignedTo.objects.filter(case_id__in=case_ids).values_list('det_id', flat=True)
    # detective=Detective.objects.get(id=50014)

    detectives = Detective.objects.filter(id__in=assnto)

    try:
        d_on = DependsOn.objects.filter(SSN=record.SSN).values_list('dep_f_name', flat=True)
    # dependent=Dependent.objects.get(first_name='Karley')
    # dependent=Dependent.objects.get(first_name=d_on.dep_f_name.first_name,last_name=d_on.dep_l_name.last_name)

        dependents = Dependent.objects.filter(first_name__in=d_on)  # and last_name=d_on.dep_l_name)
    except DependsOn.DoesNotExist:
        dependents = None

    return connected, cases, crimes_1, detectives, dependents


def find_match(entry):

    terms = normalize_query(query_string[0])
    matches = 0
    connected, cases, crimes_1, detectives, dependents = find_tables(entry)

    for f in criminal_attr:
        matches += sum([1 for term in terms if term.lower() in str(getattr(entry, f)).lower()])

    for f in case_attr:
        for case in cases:
            matches += sum([1 for term in terms if term.lower() in str(getattr(case, f)).lower()])

    for f in crime_attr:
        for crime in crimes_1:
            matches += sum([1 for term in terms if term.lower() in str(getattr(crime, f)).lower()])

    for f in detective_attr:
        for detective in detectives:
            matches += sum([1 for term in terms if term.lower() in str(getattr(detective, f)).lower()])

    if dependents is not None:
        for f in dependent_attr:
            for dependent in dependents:
                matches += sum([1 for term in terms if term.lower() in str(getattr(dependent, f))])

    return matches

@login_required
def view_record(request):
    record = Criminal.objects.get(SSN=request.GET.get('SSN'))
    # connected=ConnectedTo.objects.get(SSN='E01002000')
    connected = ConnectedTo.objects.filter(SSN=record.SSN).values_list('case_id', flat=True)
    # caserec=Case.objects.get(id=1382)

    cases = Case.objects.filter(id__in=connected)
    case_ids = cases.values_list('id', flat=True)
    crime_ids = cases.values_list('crime', flat=True)
    # crime = Crime.objects.get(id=57)

    crimes_1 = Crime.objects.filter(id__in=crime_ids)

    assnto = AssignedTo.objects.filter(case_id__in=case_ids).values_list('det_id', flat=True)
    # detective=Detective.objects.get(id=50014)

    detectives = Detective.objects.filter(id__in=assnto)

    dependents = None
    try:
        d_on = DependsOn.objects.filter(SSN=record.SSN).values_list('dep_f_name', flat=True)
    # dependent=Dependent.objects.get(first_name='Karley')
    # dependent=Dependent.objects.get(first_name=d_on.dep_f_name.first_name,last_name=d_on.dep_l_name.last_name)

        dependents = Dependent.objects.filter(first_name__in=d_on)  # and last_name=d_on.dep_l_name)
    except DependsOn.DoesNotExist:
        dependents = None
    finally:
        context = {'record': record, 'cases': cases, 'crimes': crimes_1, 'detectives': detectives, 'dependents': dependents}
        template = 'records.html'

        return render(request, template, context)

    # return render_to_pdf_response(request, template, context)


@login_required
def search_result(request):
    print('**')
    print(searchlist)
    del records[:]
    for x in searchlist:
        record = Criminal.objects.get(SSN=x)
        records.append(record)
    template = 'search_result.html'
    context = {'records': records}
    return render(request, template, context)

def import_db_assignedto(request):
    f = open('/home/pygram/crimeDB/src/core/records/Assigned_to.csv', 'r')
    for line in f:
        entry = line.split(',')
        print(entry[0])
        entry[0] = get_object_or_404(Case, id=entry[0])
        entry[1] = get_object_or_404(Detective, id=entry[1])
        tmp = AssignedTo.objects.get_or_create(case_id=entry[0],
                                               det_id=entry[1])
    f.close()


def import_db_dependson(request):
    f = open('/home/pygram/crimeDB/src/core/records/Depends_on.csv', 'r')
    for line in f:
        entry = line.split(',')
        print(entry[0])
        entry[0] = get_object_or_404(Criminal, SSN=entry[0])
        tmp = DependsOn.objects.get_or_create(SSN=entry[0],
                                              dep_f_name=entry[1],
                                              dep_l_name=entry[2])
    f.close()


def import_db_connectedto(request):
    f = open('/home/pygram/crimeDB/src/core/records/Connected_to.csv', 'r')
    for line in f:
        entry = line.split(',')
        print(entry[0])
        entry[0] = get_object_or_404(Criminal, SSN=entry[0])
        entry[1] = get_object_or_404(Case, id=entry[1])
        tmp = ConnectedTo.objects.get_or_create(SSN=entry[0],
                                                case_id=entry[1])
    f.close()


@login_required
@permission_required('user.is_lawenforcer')
def entry(request):
    title = 'Record Entry Form'
    form = entryForm(request.POST or None)
    context = {'title': title, 'form': form}
    confirm_message = False

    if form.is_valid():
        fname = form.cleaned_data['First_Name']
        lname = form.cleaned_data['Last_Name']
        mname = form.cleaned_data['Middle_Name']
        ssnno = form.cleaned_data['SSN']
        bd = form.cleaned_data['DOB']
        gen = form.cleaned_data['Sex']
        hgt = form.cleaned_data['Height']
        wgt = form.cleaned_data['Weight']
        hc = form.cleaned_data['Hair_Colour']
        d_mark = form.cleaned_data['Distinct_Mark']
        addr = form.cleaned_data['Address']
        occup = form.cleaned_data['Occupation']

        det_id = form.cleaned_data['Detective_ID']
        det_fname = form.cleaned_data['Detective_First_Name']
        det_lname = form.cleaned_data['Detective_Last_Name']
        det_cno = form.cleaned_data['Detective_Contact_No']

        dep_fname = form.cleaned_data['Dependent_fname']
        dep_lname = form.cleaned_data['Dependent_lname']
        dep_rel = form.cleaned_data['Dependent_relationship']
        dep_contact = form.cleaned_data['Dependent_contactno']

        case_id = form.cleaned_data['Case_ID']
        case_crime = form.cleaned_data['Case_crime']
        case_descp = form.cleaned_data['Case_description']
        case_loc = form.cleaned_data['Case_location']

        crml = Criminal.objects.get_or_create(first_name=fname, middle_name=mname, last_name=lname, SSN=ssnno, dob=bd,
                                              sex=gen, height_in_ft=hgt, weight_in_kg=wgt, hair_colour=hc,
                                              dist_mark=d_mark, address=addr, occupation=occup)

        det = Detective.objects.get_or_create(id=det_id, first_name=det_fname, last_name=det_lname, contact_no=det_cno)

        dep = Dependent.objects.get_or_create(first_name=dep_fname, last_name=dep_lname, contact_no=det_cno,
                                              relationship=dep_rel)

        cr = Crime.objects.get(id=case_crime)

        c = Case.objects.get_or_create(id=case_id, crime=cr, description=case_descp, location=case_loc)

        ssnno = get_object_or_404(Criminal, SSN=ssnno)
        case_id = get_object_or_404(Case, id=case_id)
        con = ConnectedTo.objects.get_or_create(SSN=ssnno, case_id=case_id)

        det_id = get_object_or_404(Detective, id=det_id)
        assn = AssignedTo.objects.get_or_create(case_id=case_id, det_id=det_id)

        depon = DependsOn.objects.get_or_create(SSN=ssnno, dep_f_name=dep, dep_l_name=dep)

    template = 'contact.html'
    return render(request, template, context)


def import_db_criminal_img(request):
    from random import choice
    criminals = Criminal.objects.all()
    images = sorted(os.listdir('core/images'))
    for idx, criminal in enumerate(criminals):
        criminal.image = 'test_images/' + images[idx % len(images)]
        criminal.save()
