
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from studentorg.models import Organization, OrgMember, Student, College, Program
from studentorg.forms import OrganizationForm, OrgMemberForm, StudentForm, CollegeForm, ProgramForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.utils import timezone

class HomePageView(LoginRequiredMixin, ListView):
    model = Organization
    context_object_name = 'home'
    template_name = "home.html"
    ordering = ["name"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_students"] = Student.objects.count()
        context["total_organizations"] = Organization.objects.count()
        context["total_programs"] = Program.objects.count()
        today = timezone.now().date()
        count = (
            OrgMember.objects.filter(date_joined__year=today.year)
            .values("student").distinct().count()
        )
        context["students_joined_this_year"] = count
        return context

# Organization
class OrganizationList(LoginRequiredMixin, ListView):
    model = Organization
    context_object_name = 'organization'
    template_name = 'studentorg/org_list.html'
    paginate_by = 5
    ordering = ["college__college_name", "name"]

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query)
            )
        return qs

class OrganizationCreateView(LoginRequiredMixin, CreateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'studentorg/org_form.html'
    success_url = reverse_lazy('organization-list')

class OrganizationUpdateView(LoginRequiredMixin, UpdateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'studentorg/org_form.html'
    success_url = reverse_lazy('organization-list')

class OrganizationDeleteView(LoginRequiredMixin, DeleteView):
    model = Organization
    template_name = 'studentorg/org_del.html'
    success_url = reverse_lazy('organization-list')

# OrgMember
class OrgMemberList(LoginRequiredMixin, ListView):
    model = OrgMember
    context_object_name = 'orgmember'
    template_name = 'studentorg/orgmember_list.html'
    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')
        sort_by = self.request.GET.get('sort_by', 'student__lastname')

        allowed = ['student__lastname', 'date_joined', '-date_joined']
        if sort_by not in allowed:
            sort_by = 'student__lastname'

        if query:
            qs = qs.filter(
                Q(student__firstname__icontains=query) |
                Q(student__lastname__icontains=query) |
                Q(organization__name__icontains=query)
            )
        return qs.order_by(sort_by)

class OrgMemberCreateView(LoginRequiredMixin, CreateView):
    model = OrgMember
    form_class = OrgMemberForm
    template_name = 'studentorg/orgmember_form.html'
    success_url = reverse_lazy('orgmember-list')

class OrgMemberUpdateView(LoginRequiredMixin, UpdateView):
    model = OrgMember
    form_class = OrgMemberForm
    template_name = 'studentorg/orgmember_form.html'
    success_url = reverse_lazy('orgmember-list')

class OrgMemberDeleteView(LoginRequiredMixin, DeleteView):
    model = OrgMember
    template_name = 'studentorg/orgmember_del.html'
    success_url = reverse_lazy('orgmember-list')

# Student
class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'studentorg/student_list.html'
    paginate_by = 5
    ordering = ["program__prog_name", "lastname"]

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(
                Q(firstname__icontains=query) |
                Q(lastname__icontains=query) |
                Q(middlename__icontains=query)
            )
        return qs

class StudentCreateView(LoginRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'studentorg/student_form.html'
    success_url = reverse_lazy('student-list')

class StudentUpdateView(LoginRequiredMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'studentorg/student_form.html'
    success_url = reverse_lazy('student-list')

class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student
    template_name = 'studentorg/student_del.html'
    success_url = reverse_lazy('student-list')

# College
class CollegeListView(LoginRequiredMixin, ListView):
    model = College
    template_name = 'studentorg/college_list.html'
    paginate_by = 5
    ordering = ['college_name']

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(Q(college_name__icontains=query))
        return qs

class CollegeCreateView(LoginRequiredMixin, CreateView):
    model = College
    form_class = CollegeForm
    template_name = 'studentorg/college_form.html'
    success_url = reverse_lazy('college-list')

class CollegeUpdateView(LoginRequiredMixin, UpdateView):
    model = College
    form_class = CollegeForm
    template_name = 'studentorg/college_form.html'
    success_url = reverse_lazy('college-list')

class CollegeDeleteView(LoginRequiredMixin, DeleteView):
    model = College
    template_name = 'studentorg/college_del.html'
    success_url = reverse_lazy('college-list')

# Program
class ProgramListView(LoginRequiredMixin, ListView):
    model = Program
    template_name = 'studentorg/program_list.html'
    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(
                Q(prog_name__icontains=query) |
                Q(college__college_name__icontains=query)
            )
        return qs.order_by(self.get_ordering())

    def get_ordering(self):
        allowed = ["prog_name", "college__college_name"]
        sort_by = self.request.GET.get("sort_by")
        if sort_by in allowed:
            return sort_by
        return "prog_name"

class ProgramCreateView(LoginRequiredMixin, CreateView):
    model = Program
    form_class = ProgramForm
    template_name = 'studentorg/program_form.html'
    success_url = reverse_lazy('program-list')

class ProgramUpdateView(LoginRequiredMixin, UpdateView):
    model = Program
    form_class = ProgramForm
    template_name = 'studentorg/program_form.html'
    success_url = reverse_lazy('program-list')

class ProgramDeleteView(LoginRequiredMixin, DeleteView):
    model = Program
    template_name = 'studentorg/program_del.html'
    success_url = reverse_lazy('program-list')