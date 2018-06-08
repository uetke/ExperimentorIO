from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
import json

from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView

from experimentor.forms import NewSignalForm, NewExperimentForm
from experimentor.models import Experiment, Signal, Measurement

from accounts.forms import SignUpForm


def index(request):
    form = SignUpForm()
    return render(request, 'home.html', {'form': form})


@login_required()
def experiments_view(request, username):
    user = get_object_or_404(User, username=username)
    experiments = Experiment.objects.filter(owner=user).order_by('-update_date')
    return render(request, 'experiments/experiments.html', {'experiments': experiments})

@login_required()
def new_signal(request, username, experiment_slug):
    user = get_object_or_404(User, username=username)
    experiment = get_object_or_404(Experiment, owner=user, slug=experiment_slug)
    if not user == request.user or not experiment.owner == request.user:
        reason = "You can't add a signal to another user experiment.<br/>" \
                 "This incident will be reported"
        return render(request, 'no_access.html', {'reason': reason})

    if request.method == 'POST':
        form = NewSignalForm(request.POST)
        if form.is_valid():
            signal = form.save(commit=False)
            signal.experiment = experiment
            signal.save()
            messages.success(request, 'Signal added to experiment')
    else:
        form = NewSignalForm()

    return render(request, 'experiments/new_signal.html', {'experiment': experiment,'form': form})

@login_required()
def new_experiment(request):
    if request.method == 'POST':
        form = NewExperimentForm(request.POST)
        if form.is_valid():
            experiment = form.save(commit=False)
            experiment.owner = request.user
            experiment.save()
            messages.success(request, 'New experiment created')
            return redirect(reverse('new_signal', kwargs={'username': experiment.owner.username, 'experiment_slug': experiment.slug}))

    else:
        form = NewExperimentForm()

    return render(request, 'experiments/new_experiment.html', {'form': form})

@login_required()
def experiment_view(request, username, experiment_slug):
    user = User.objects.get(username=username)
    experiment = Experiment.objects.get(owner=user, slug=experiment_slug)
    return render(request, 'experiments/experiment.html', {'experiment': experiment})

@login_required()
def signal_view(request, username, experiment_slug, signal_slug):
    user = User.objects.get(username=username)
    experiment = Experiment.objects.get(owner=user, slug=experiment_slug)
    signal = Signal.objects.get(experiment=experiment, slug=signal_slug)
    measurements = Measurement.objects.filter(signal=signal).order_by('-updated_time')[:100]

    if signal.value_type not in (Signal.FLOAT, Signal.INTEGER, Signal.ARRAY):
        return render(request, 'experiments/view_signal_no_plot.html', {'signal': signal, 'experiment': experiment})

    if signal.value_type == Signal.ARRAY:
        data = signal.measurements.last().value
        data = json.loads(data)
    else:
        data = []
        for m in measurements:
            try:
                data.append([m.updated_time.timestamp()*1000, float(m.value)])
            except:
                pass

    y_label = signal.name
    if signal.units:
        y_label = y_label + ' (' + signal.units + ')'

    return render(request, 'experiments/view_signal.html', {
        'signal': signal,
        'title': json.dumps(experiment.name + ' / ' + signal.name),
        'y_label': json.dumps(y_label),
        'data_y': json.dumps(data),
        'experiment': experiment,
        # 'data': data,
    })


class UpdateExperiment(LoginRequiredMixin, UpdateView):
    model = Experiment
    fields = ['name', 'visibility', 'description']
    template_name = 'experiments/new_experiment.html'


    def get_object(self, queryset=None):
        experiment = Experiment.objects.get(pk=self.kwargs['pk'])
        return experiment


class IsOwnerOrPublic:
    """
        Checks that the current user is the owner of the element, or that it is public.
    """
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        if request.user == obj.owner or obj.visibility == 2:
            return super(IsOwnerOrPublic, self).dispatch(
                request, *args, **kwargs)

        raise PermissionDenied

class ExperimentView(LoginRequiredMixin, IsOwnerOrPublic, DetailView):
    model = Experiment
    context_object_name = 'experiment'
    template_name = 'experiments/experiment.html'

    def get_object(self, queryset=None):
        user = User.objects.get(username=self.kwargs['username'])
        experiment = Experiment.objects.get(owner=user, slug=self.kwargs['experiment_slug'])
        return experiment


