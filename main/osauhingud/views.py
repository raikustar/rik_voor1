from django.shortcuts import render
from django.core.exceptions import ValidationError
from django.db.models import Q, Prefetch
from .models import Osauhing, LegalEntityShareHolder, Shareholder, IndividualShareHolder
from datetime import date, datetime

# Create your views here.

def main_page(request):
    query = request.GET.get("search_text", '')

    # prefetch for related shareholders
    companies = Osauhing.objects.all().prefetch_related(
        Prefetch('shareholders__individual', queryset=IndividualShareHolder.objects.all()),
        Prefetch('shareholders__legal_entity', queryset=LegalEntityShareHolder.objects.all())
    )

    # search filter
    if query:
        companies = companies.filter(
            Q(companyname__icontains=query) | 
            Q(registrycode__icontains=query) |
            Q(shareholders__individual__first_name__icontains=query) |
            Q(shareholders__individual__last_name__icontains=query) |
            Q(shareholders__individual__personal_id_code__icontains=query) |
            Q(shareholders__legal_entity__full_name__icontains=query)
        ).distinct()

    return render(request, "home.html", {"data": companies})


def add_company(request):
    if request.method == "POST":
        comp_name = request.POST.get("comp_name")
        reg_code = request.POST.get("reg_code")
        found_date_str = request.POST.get("found_date")
        total_cap_str = request.POST.get("total_cap") 
        
        input_data = {
            "comp_name": comp_name,
            "reg_code": reg_code,
            "found_date": found_date_str,
            "total_cap": total_cap_str
        }
        # Check company names length
        if len(comp_name) < 3 or len(comp_name) > 100:
            error = "Error: Company name length is less than 3 or too long."
            return render(request, 'add_data.html', {"message": error, "input_data":input_data})

        # check if company name already exists
        if Osauhing.objects.filter(companyname=comp_name).exists():
            error = "Error: This company name already exists."
            return render(request, 'add_data.html', {"message": error, "input_data":input_data})

        # Check registry code length
        if len(reg_code) != 7:
            error = "Error: Registry code must be exactly 7 digits."
            return render(request, 'add_data.html', {"message": error, "input_data":input_data})
        
        # Check if registry code is already used
        if Osauhing.objects.filter(registrycode=reg_code).exists():
            error = "Error: This registry code already exists."
            return render(request, 'add_data.html', {"message": error, "input_data":input_data})
        
        # Check if date has been selected
        if found_date_str:
            try:
                found_date = datetime.strptime(found_date_str, "%Y-%m-%d").date()
                
            except ValueError:
                error = "Error: Invalid date format. Please use YYYY-MM-DD."
                return render(request, 'add_data.html', {"message": error, "input_data":input_data})

            current_date = date.today()
            # Check date validity
            if found_date > current_date:
                error = "Error: Invalid date. Select today's date or a previous date to add the company."
                return render(request, 'add_data.html', {"message": error, "input_data":input_data})

        # Check total capital value
        try:
            total_cap = int(total_cap_str)
            if total_cap < 2500:
                error = "Error: Total capital must be at least 2500."
                return render(request, 'add_data.html', {"message": error, "input_data":input_data})
        except ValueError:
            error = "Error: Total capital must be a valid integer."
            return render(request, 'add_data.html', {"message": error, "input_data":input_data})

        # If everything has passed the previous if checks, it will add a new company.
        add_new_osauhing = Osauhing(
            companyname=comp_name,
            registrycode=reg_code,
            foundingdate=found_date,
            totalcapital=total_cap
        )
        add_new_osauhing.save()

        total_capital_sum:int = 0
        # Add individual entity shareholder
        add_individual_shareholder_to_osauhingdb(request, total_capital_sum, add_new_osauhing, input_data)

        # Add legal entity shareholder
        add_legal_shareholder_to_osauhingdb(request, total_capital_sum, add_new_osauhing, input_data, total_cap_str)
                
        return view_company(request, add_new_osauhing.id)

    return render(request, "add_data.html")


def view_company(request, osauhing_id):
    data = Osauhing.objects.prefetch_related(
        Prefetch('shareholders__individual', queryset=IndividualShareHolder.objects.all()),
        Prefetch('shareholders__legal_entity', queryset=LegalEntityShareHolder.objects.all())
    ).get(pk=osauhing_id)

    # open new html window to view data
    return render(request, 'view_company.html', {"data":data})


def add_individual_shareholder_to_osauhingdb(request, capital_sum, main_table_db, input_data):
    # Process individual shareholder if data is provided
    if request.method == "POST":
        individual_first_name = request.POST.getlist("individual_first_name[]")
        individual_last_name = request.POST.getlist("individual_last_name[]")
        individual_personal_id = request.POST.getlist("individual_personal_id[]")
        individual_share = request.POST.getlist("individual_share[]")

        for i in range(len(individual_first_name)):
            ind_first_name = individual_first_name[i]
            ind_last_name = individual_last_name[i]
            ind_personal_id = individual_personal_id[i]
            ind_share = individual_share[i]
        
            if not ind_first_name or not ind_last_name or not ind_personal_id or not ind_share:
                break
            
            capital_sum += int(ind_share)
            try:
                ind_share = int(ind_share)
            except ValueError:
                error = "Error: Individual shareholder share must be a valid integer."
                return render(request, 'add_data.html', {"message": error, "input_data":input_data})
            
            try:
                ind_personal_id = int(ind_personal_id)
            except ValueError:
                error = "Error: Individual personal id must be a valid integer."
                return render(request, 'add_data.html', {"message": error, "input_data":input_data})

            if not ind_first_name or not ind_last_name or not ind_personal_id or not ind_share:
                error = "Error: Individual data fields should all be filled."
                return render(request, 'add_data.html', {"message": error, "input_data":input_data})

            try:
                individual_shareholder = IndividualShareHolder(
                    first_name=ind_first_name,
                    last_name=ind_last_name,
                    personal_id_code=ind_personal_id,
                    shareholder_share=ind_share
                )
                individual_shareholder.save()
            
                # Link individual shareholder to Osauhing via Shareholder
                shareholder = Shareholder(individual=individual_shareholder)
                shareholder.save()
                main_table_db.shareholders.add(shareholder)

            except ValidationError as e:
                error = "Error: Validation error."
                return render(request, 'add_data.html', {"message": error, "input_data":input_data})



def add_legal_shareholder_to_osauhingdb(request, capital_sum, main_table_db, input_data, total_cap_str):
    # Add legal entity shareholder if data is provided
    if request.method == "POST":
        legal_entity_name = request.POST.getlist("legal_entity_name[]")
        legal_entity_registry_code = request.POST.getlist("legal_entity_registry_code[]")
        legal_entity_share = request.POST.getlist("legal_entity_share[]")

        for i in range(len(legal_entity_name)):
            leg_entity_name = legal_entity_name[i]
            leg_entity_registry_code = legal_entity_registry_code[i]
            leg_entity_share = legal_entity_share[i]

            if not leg_entity_name or not leg_entity_registry_code or not leg_entity_share:
                break
            
            capital_sum += int(leg_entity_share)

            try:
                leg_entity_share = int(leg_entity_share)
            except ValueError:
                error = "Error: Legal entities share must be a valid integer."
                return render(request, 'add_data.html', {"message": error, "input_data":input_data})

            try:
                leg_entity_registry_code = int(leg_entity_registry_code)
            except ValueError:
                error = "Error: Legal entity registry code must be a valid integer."
                return render(request, 'add_data.html', {"message": error, "input_data":input_data})


            if capital_sum > int(total_cap_str):
                error = "Error: Shareholders combined capital exceeds the original base capital."
                return render(request, 'add_data.html', {"message": error, "input_data":input_data})

            try:
                legal_entity_shareholder = LegalEntityShareHolder(
                    full_name=leg_entity_name,
                    registry_code=leg_entity_registry_code,
                    shareholder_share=leg_entity_share
                )
                legal_entity_shareholder.save()

                shareholder = Shareholder(legal_entity=legal_entity_shareholder)
                shareholder.save()
                main_table_db.shareholders.add(shareholder)

            except ValidationError as e:
                error = "Error: Validation error."
                return render(request, 'add_data.html', {"message": error, "input_data":input_data})