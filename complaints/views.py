from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from .forms import SignUpForm, ComplaintForm, StatusUpdateForm
from .models import Complaint, Category


def is_admin(user):
    return user.is_staff

def login_view(request):

    if request.method == 'POST':

        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():

            user = form.get_user()

            login(request, user)

            if user.is_staff:
                return redirect('admin_complaint_list')
            else:
                return redirect('dashboard')

    else:
        form = AuthenticationForm()

    return render(
        request,
        'complaints/login.html',
        {'form': form}
    )


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            messages.success(
                request,
                "Account created! Welcome to CivicFix."
            )

            return redirect('dashboard')

    else:
        form = SignUpForm()

    return render(
        request,
        'complaints/signup.html',
        {'form': form}
    )


@login_required
def dashboard(request):
    """Logged-in citizen's own complaints + status"""

    complaints = Complaint.objects.filter(
        user=request.user
    )

    return render(
        request,
        'complaints/dashboard.html',
        {'complaints': complaints}
    )


@login_required
def submit_complaint(request):

    if request.method == 'POST':
        form = ComplaintForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user
            complaint.save()

            messages.success(
                request,
                f"Complaint submitted! Your tracking ID: "
                f"{complaint.complaint_id}"
            )

            return redirect('dashboard')

    else:
        form = ComplaintForm()

    return render(
        request,
        'complaints/submit_complaint.html',
        {'form': form}
    )


@login_required
def complaint_detail(request, complaint_id):

    complaint = get_object_or_404(
        Complaint,
        complaint_id=complaint_id
    )

    # Admin can view any complaint
    if request.user.is_staff:
        return render(
            request,
            'complaints/complaint_detail.html',
            {'complaint': complaint}
        )

    # Customer can view only their own complaint
    if complaint.user != request.user:
        messages.error(
            request,
            "You are not allowed to view this complaint."
        )

        return redirect('dashboard')

    return render(
        request,
        'complaints/complaint_detail.html',
        {'complaint': complaint}
    )


@login_required
def delete_complaint(request, complaint_id):
    """Citizen can delete their OWN complaint,
    only while it's still pending.
    """

    complaint = get_object_or_404(
        Complaint,
        complaint_id=complaint_id,
        user=request.user
    )

    if complaint.status != 'pending':
        messages.error(
            request,
            "This complaint is already being processed "
            "and can't be deleted."
        )

        return redirect('dashboard')

    if request.method == 'POST':
        cid = complaint.complaint_id

        complaint.delete()

        messages.success(
            request,
            f"Complaint {cid} deleted."
        )

        return redirect('dashboard')

    return render(
        request,
        'complaints/confirm_delete.html',
        {'complaint': complaint}
    )


@user_passes_test(is_admin)
def admin_complaint_list(request):
    """Admin/staff view:
    all complaints, filterable by category & status
    """

    complaints = Complaint.objects.all()

    category_id = request.GET.get('category')
    status = request.GET.get('status')

    if category_id:
        complaints = complaints.filter(
            category_id=category_id
        )

    if status:
        complaints = complaints.filter(
            status=status
        )

    context = {
        'complaints': complaints,
        'categories': Category.objects.all(),
        'status_choices': Complaint.STATUS_CHOICES,
    }

    return render(
        request,
        'complaints/admin_list.html',
        context
    )


@user_passes_test(is_admin)
def update_status(request, complaint_id):

    complaint = get_object_or_404(
        Complaint,
        complaint_id=complaint_id
    )

    if request.method == 'POST':

        form = StatusUpdateForm(
            request.POST,
            request.FILES,
            instance=complaint
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                f"{complaint.complaint_id} status updated "
                f"to {complaint.get_status_display()}."
            )

            return redirect('admin_complaint_list')

    else:
        form = StatusUpdateForm(
            instance=complaint
        )

    return render(
        request,
        'complaints/update_status.html',
        {
            'form': form,
            'complaint': complaint
        }
    )


@user_passes_test(is_admin)
def admin_delete_complaint(request, complaint_id):
    """Admin can delete ANY complaint —
    e.g. spam or duplicate reports.
    """

    complaint = get_object_or_404(
        Complaint,
        complaint_id=complaint_id
    )

    if request.method == 'POST':

        cid = complaint.complaint_id

        complaint.delete()

        messages.success(
            request,
            f"Complaint {cid} deleted by admin."
        )

        return redirect('admin_complaint_list')

    return render(
        request,
        'complaints/confirm_delete.html',
        {
            'complaint': complaint,
            'is_admin_delete': True
        }
    )