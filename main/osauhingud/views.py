from django.shortcuts import render,  get_object_or_404
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
        if len(comp_name) < 3:
            error = "Error: Company name length is less than 3."
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
            print("Form date",found_date)
            print("Current date", current_date)
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

        # Process individual shareholder if data is provided

        if request.POST.get("individual_first_name"):
            individual_first_name = request.POST.get("individual_first_name")
            individual_last_name = request.POST.get("individual_last_name")
            individual_personal_id = request.POST.get("individual_personal_id")
            individual_share = request.POST.get("individual_share")

            try:
                individual_share = int(individual_share)
            except ValueError:
                error = "Error: Individual shareholder share must be a valid integer."
                return render(request, 'add_data.html', {"message": error})

            individual_shareholder = IndividualShareHolder(
                first_name=individual_first_name,
                last_name=individual_last_name,
                personal_id_code=individual_personal_id,
                shareholder_share=individual_share
            )
            individual_shareholder.save()

            # Link individual shareholder to Osauhing via Shareholder
            shareholder = Shareholder(individual=individual_shareholder)
            shareholder.save()
            add_new_osauhing.shareholders.add(shareholder)

        

        # Add legal shareholder
        if request.POST.get("legal_entity_name"):
            legal_entity_name = request.POST.get("legal_entity_name")
            legal_entity_registry_code = request.POST.get("legal_entity_registry_code")
            legal_entity_share = request.POST.get("legal_entity_share")

            try:
                legal_entity_share = int(legal_entity_share)
            except ValueError:
                error = "Error: Legal entity shareholder share must be a valid integer."
                return render(request, 'add_data.html', {"message": error})

            legal_entity_shareholder = LegalEntityShareHolder(
                full_name=legal_entity_name,
                registry_code=legal_entity_registry_code,
                shareholder_share=legal_entity_share
            )
            legal_entity_shareholder.save()

            shareholder = Shareholder(legal_entity=legal_entity_shareholder)
            shareholder.save()
            add_new_osauhing.shareholders.add(shareholder)

        return view_company(request, add_new_osauhing.id)

    return render(request, "add_data.html")


def view_company(request, osauhing_id):
    data = Osauhing.objects.prefetch_related(
        Prefetch('shareholders__individual', queryset=IndividualShareHolder.objects.all()),
        Prefetch('shareholders__legal_entity', queryset=LegalEntityShareHolder.objects.all())
    ).get(pk=osauhing_id)

    # open new html window to view data
    return render(request, 'view_company.html', {"data":data})

