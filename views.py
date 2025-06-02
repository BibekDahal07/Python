from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Lawyer
from django.core.paginator import Paginator
from django.db.models import Q
from .models import LegalRight
from django.shortcuts import render, get_object_or_404
from .models import LegalDocument
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile


def home(request):
    return render(request, 'index.html')

def rights_view(request):
    search_term = request.GET.get('search', '').strip()
    
    # Start with all rights
    rights = LegalRight.objects.all()
    
    if search_term:
        # Search in multiple fields
        rights = rights.filter(
            Q(title__icontains=search_term) |
            Q(summary__icontains=search_term) |
            Q(detailed_info__icontains=search_term) |
            Q(tags__icontains=search_term)
        )
    
    # Group by category
    categories = {}
    for right in rights:
        if right.category not in categories:
            categories[right.category] = []
        categories[right.category].append(right)
    
    return render(request, 'rights/rights.html', {
        'categories': categories,
        'search_term': search_term
    })

def lawyers(request):
    # Get all distinct specialties and languages for filters
    specialties = dict(Lawyer.SPECIALTY_CHOICES)
    all_languages = set()
    for choice in Lawyer.LANGUAGE_CHOICES:
        all_languages.add(choice[0])
    
    # Get filter parameters from request
    search_term = request.GET.get('search', '').lower()
    specialty = request.GET.get('specialty', 'all')
    language = request.GET.get('language', 'all')
    
    # Apply filters
    lawyers_list = Lawyer.objects.all().order_by('name')
    
    if search_term:
        lawyers_list = lawyers_list.filter(
            Q(name__icontains=search_term) |  # Changed from models.Q to Q
            Q(location__icontains=search_term)  # Changed from models.Q to Q
        )
    
    if specialty != 'all':
        lawyers_list = lawyers_list.filter(specialty=specialty)
    
    if language != 'all':
        lawyers_list = lawyers_list.filter(languages__contains=language)
    
    # Pagination
    paginator = Paginator(lawyers_list, 4)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_term': search_term,
        'selected_specialty': specialty,
        'selected_language': language,
        'specialties': specialties,
        'languages': sorted(all_languages),
        'total_lawyers': Lawyer.objects.count(),
        'filtered_count': lawyers_list.count(),
    }
    
    return render(request, 'lawyers.html', context)

def forum(request):
    return render(request, 'forum.html')

def documents_view(request):
    category = request.GET.get('category', 'all')
    
    if category == 'all':
        documents = LegalDocument.objects.all()
    else:
        documents = LegalDocument.objects.filter(category=category)
    
    categories = dict(LegalDocument.CATEGORY_CHOICES)
    
    return render(request, 'documents.html', {
        'documents': documents,
        'current_category': category,
        'categories': categories,
    })

def document_detail(request, doc_id):
    document = get_object_or_404(LegalDocument, id=doc_id)
    return render(request, 'document_detail.html', {
        'document': document,
        'fields': document.fields.all(),
    })

def generate_document(request, doc_id):
    document = get_object_or_404(LegalDocument, id=doc_id)
    
    if request.method == 'POST':
        # Process form data
        form_data = {}
        for field in document.fields.all():
            value = request.POST.get(field.name, '')
            form_data[field.name] = value
        
        # Render the document template with form data
        html_string = render_to_string('generated_document.html', {
            'document': document,
            'form_data': form_data,
            'fields': document.fields.all(),
        })
        
        # Generate PDF
        html = HTML(string=html_string)
        result = html.write_pdf()
        
        # Create response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{document.title}.pdf"'
        response.write(result)
        
        # Increment download count
        document.downloads += 1
        document.save()
        
        return response
    
    return document_detail(request, doc_id)

def emergency(request):
    return render(request, 'emergency.html')

# Signup View
def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')  # Redirect to home after sign-up
    else:
        form = UserCreationForm()
    return render(request, 'main/signup.html', {'form': form})

# Login View
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # use .get() safely
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # or wherever you want to redirect
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'main/login.html')

# Logout View
@login_required
def logout_view(request):
    logout(request)
    return redirect('home') 
