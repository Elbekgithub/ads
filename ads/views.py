from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.files.uploadedfile import InMemoryUploadedFile

from ads.models import Ad, Comment
from ads.forms import CreateForm,CommentForm

class AdListView(ListView):
	model = Ad
	template_name = "ads/list.html"

class AdDetailView(DetailView):
	model = Ad
	template_name = "ads/detail.html"
	def get(self, request, pk) :
		x = Ad.objects.get(id=pk)
		comments = Comment.objects.filter(ad=x).order_by('-updated_at')
		comment_form = CommentForm()
		context = { 'ad' : x, 'comments': comments, 'comment_form': comment_form }
		return render(request, self.template_name, context)

class AdCreateView(LoginRequiredMixin, View):
	template_name = 'ads/form.html'
	success_url = reverse_lazy('ads:all')
	def get(self, request, pk=None):
		form = CreateForm()
		context = {'form': form}
		return render(request, self.template_name, context)

	def post(self, request, pk=None):
		form = CreateForm(request.POST, request.FILES or None)
		if not form.is_valid():
			context = {'form': form}
			return render(request, self.template_name, context)
		ad = form.save(commit=False)
		ad.owner = self.request.user
		ad.save()
		return redirect(self.success_url)


class AdUpdateView(LoginRequiredMixin, View):
	template_name = 'ads/form.html'
	success_url = reverse_lazy('ads:all')
	def get(self, request, pk):
		ad = get_object_or_404(Ad, id = pk, owner = self.request.user)
		form = CreateForm(instance=ad)
		context = {'form':form}
		return render(request, self.template_name, context)

	def post(self, request, pk=None):
		ad = get_object_or_404(Ad, id = pk, owner = self.request.user)
		form = CreateForm(request.POST, request.FILES or None, instance=ad)

		if not form.is_valid():
			context = {'form':form}
			return render(request, self.template_name, context)
		ad = form.save(commit=False)
		ad.save()

		return redirect(self.success_url)


class AdDeleteView(DeleteView):
	model = Ad
	template_name = 'ads/delete.html'

def stream_file(request, pk) :
    ad = get_object_or_404(Ad, id=pk)
    response = HttpResponse()
    response['Content-Type'] = ad.content_type
    response['Content-Length'] = len(ad.picture)
    response.write(ad.picture)
    return response


class CommentCreateView(LoginRequiredMixin, View):
	def post(self, request, pk):
		ad = get_object_or_404(Ad, id=pk)
		comment = Comment(text=request.POST['comment'], owner=self.request.user, ad=ad)
		comment.save()
		return redirect(reverse('ads:ad_detail', args=[pk]))

class CommentDeleteView(DeleteView):
	model = Comment
	template_name = 'ads/comment_delete.html'
	def get_success_url(self):
		ad = self.object.ad
		return reverse('ads:ad_detail', args=[ad.id])