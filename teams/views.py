from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Documents, Team, Player
from .forms import DocumentForm, PlayerForm, TeamForm
from cms.ajax import AjaxCreateView, AjaxUpdateView, AjaxDeleteView, AjaxFilesUpload
from django.views.generic import View
from django.http import JsonResponse
from django.template.loader import render_to_string
import time


@login_required
def home(request):
    return redirect('teams:teams-list')


@login_required
def teams_list(request):
    teams = Team.objects.all()
    context = {"title": "Teams", "team_list": teams}
    return render(request, 'teams/teams.html', context)


class TeamCreate(LoginRequiredMixin, AjaxCreateView):
    model = Team
    form_class = TeamForm
    ajax_modal = 'ajax/form_modal.html'
    ajax_list = 'teams/teams_list.html'


class TeamUpdate(LoginRequiredMixin, AjaxUpdateView):
    model = Team
    form_class = TeamForm
    ajax_modal = 'ajax/form_modal.html'
    ajax_list = 'teams/teams_list.html'


class TeamDelete(LoginRequiredMixin, AjaxDeleteView):
    model = Team
    ajax_modal = 'ajax/delete_modal.html'
    ajax_list = 'teams/teams_list.html'


@login_required
def players_list(request, team):
    team_obj = get_object_or_404(Team, pk=team)
    title = "Players on {}".format(team_obj)
    players = team_obj.player_set.all()
    context = {"title": title, "team": team_obj, "player_list": players}
    return render(request, 'teams/players.html', context)


class PlayerCreate(LoginRequiredMixin, AjaxCreateView):
    model = Player
    form_class = PlayerForm
    ajax_modal = 'ajax/form_modal.html'
    ajax_list = 'teams/players_list.html'


class PlayerUpdate(LoginRequiredMixin, AjaxUpdateView):
    model = Player
    form_class = PlayerForm
    ajax_modal = 'ajax/form_modal.html'
    ajax_list = 'teams/players_list.html'


class PlayerDelete(LoginRequiredMixin, AjaxDeleteView):
    model = Player
    ajax_modal = 'ajax/delete_modal.html'
    ajax_list = 'teams/players_list.html'


@login_required
def document_list(request, team):
    team_obj = get_object_or_404(Team, pk=team)
    title = "Files on {}".format(team_obj)
    files = team_obj.file_set.all()
    context = {"title": title, "book": team_obj, "file_list": files}
    return render(request, 'teams/documents.html', context)


class DocumentUpload(LoginRequiredMixin, AjaxFilesUpload):
    model = Documents
    form_class = DocumentForm
    ajax_list = 'teams/documents_list.html'


class DocumentDelete(LoginRequiredMixin, AjaxDeleteView):
    model = Documents
    ajax_modal = 'ajax/delete_modal.html'
    ajax_list = 'teams/documents_list.html'