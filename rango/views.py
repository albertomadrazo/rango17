from datetime import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone

from rango.models import Category, Page, UserProfile
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from rango.bing_search import run_query

import json

def index(request):

	category_list = Category.objects.order_by('-likes')[:5]
	page_list = Page.objects.order_by('-views')[:5]
	
	context_dict = {'categories': category_list, 'pages': page_list}

	# Get the number of visits to the site.
	# We use COOKIES.get() function to obtain hte visits cookie.
	# If the cookie exists, the value returned is casted to an integer.
	# If the cookie doesn't exist, we dafault to zero and cast that.
	visits = request.session.get('visits')
	if not visits:
		visits = 1
	reset_last_visit_time = False

	last_visit = request.session.get('last_visit')
	if last_visit:
		last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

		if (datetime.now() -last_visit_time).seconds > 0:
			# ... reasign the value of the cookie to +1 of what it was before...
			visits = visits + 1
			# ... and update the last visit cookie, too.
			reset_last_visit_time = True
	else:
		# Cookie last_visit_doesn't exist, so create it to the current date/time.
		reset_last_visit_time = True

	if reset_last_visit_time:
		request.session['last_visit'] = str(datetime.now())
		request.session['visits'] = visits
	context_dict['visits'] = visits

	response = render(request, 'rango/index.html', context_dict)

	return response


def about(request):
	if request.session.get('visits'):
		count = request.session.get('visits')
	else:
		count = 0

	context_dict = {'aboutmessage': "Everything is about Django", 'visits': count}
	return render(request, 'rango/about.html', context_dict)
	
def category(request, category_name_slug):
	# Create a context dictionary which we can pass to the template rendering engine
	context_dict = {}
	context_dict['result_list'] = None
	context_dict['query'] = None

	if request.method == 'POST':
		query = request.POST['query'].strip()
		if query:
			result_list = run_query(query)
			context_dict['result_list'] = result_list
			context_dict['query'] = query

	try:
		category = Category.objects.get(slug=category_name_slug)
		context_dict['category_name'] = category.name
		pages = Page.objects.filter(category=category).order_by('-views')
		context_dict['pages'] = pages
		context_dict['category_name_url'] = category_name_slug
		context_dict['category'] = category

	except Category.DoesNotExist:
		pass

	if not context_dict['query']:
		context_dict['query'] = category.name

	return render(request, 'rango/category.html', context_dict)

@login_required
def add_category(request):
	# a HTTP POST?
	if request.method == 'POST':
		form = CategoryForm(request.POST)

		# Have we been provided with a valid form?
		if form.is_valid():
			# save hte new category to the database.
			form.save(commit=True);

			# Now call the index() view.
			# The user will be shown the homepage.
			return index(request)

		else:
			# The supplied form contained errors - just print them to the terminal.
			print form.errors
	else:
		# If the request was not a POST, display the form to enter details.
		form = CategoryForm()

	# Bad form (or form details), no form supplied...
	# Render the form with error messages (if any).
	return render(request, 'rango/add_category.html', {'form': form})

@login_required
def add_page(request, category_name_slug):

	try:
		cat = Category.objects.get(slug=category_name_slug)
	except Category.DoesNotExist:
		cat = None

	if request.method == 'POST':
		form = PageForm(request.POST)
		if form.is_valid():
			if cat:
				page = form.save(commit=False)
				page.category = cat
				page.views = 0
				page.first_visit = timezone.now()
				page.last_visit = timezone.now()
				page.save()
				# probably better to use a redirect here.
				return category(request, category_name_slug)
		else:
			print form.errors
	else:
		form = PageForm()

	context_dict = {'form': form, 'category': cat}

	return render(request, 'rango/add_page.html', context_dict)



@login_required
def restricted(request):
	return render(request, 'rango/restricted.html', {})


def search(request):
	result_list = []

	if request.method == 'POST':
		query = request.POST['query'].strip()

		if query:
			# Run our Bing function to get the results list!
			result_list = run_query(query)

	return render(request, 'rango/search.html', {'result_list': result_list})

def track_url(request):
	now = timezone.now()
	if request.method == 'GET':
		if 'pageid' in request.GET:
			page_id = request.GET['pageid']
		else:
			return redirect('rango/')

		page_count = Page.objects.get(id=page_id)
		if page_count:
			page_count.views += 1
			page_count.last_visit = now
			page_count.save()

			url = page_count.url

			return redirect(url)
		else:
			return redirect('rango/')
	else:
		return redirect('rango/')

def add_profile(request):
	if request.method == 'POST':
		name = str(request.GET[u'user'])
		user = User.objects.get(username=name)

		profile = UserProfile(user=user)
		profile.website = request.POST[u'website']
		profile.picture = request.FILES['picture']
		profile.save()

		return redirect('/rango/')

	else:
		profile = UserProfileForm()

		return render(request, 'rango/add_profile.html', {'profile': profile})

@login_required
def like_category(request):

	cat_id = None
	if request.method == 'GET':
		cat_id = request.GET['category_id']
	likes = 0
	if cat_id:
		cat = Category.objects.get(id=int(cat_id))
		if cat:
			likes = cat.likes + 1
			cat.likes = likes
			cat.save()

	return HttpResponse(likes)

def get_category_list(max_results=0, starts_with=''):
	cat_list = []

	if starts_with:
		cat_list = Category.objects.filter(name__istartswith=starts_with)

	if max_results > 0:
		if len(cat_list) > max_results:
				cat_list = cat_list[:max_results]

	return cat_list
		

def suggest_category(request):

	cat_list = []
	starts_with = ''
	if request.method == 'GET':
		starts_with = request.GET['suggestion']
		print starts_with
	cat_list = get_category_list(8, starts_with)

	return render(request, 'rango/cats.html', {'cates': cat_list })

def add_page_ajax(request):
	print "in add_page_ajax()"

	if request.method == 'GET':
		#print "333333333", request.GET
		valor = request.GET['values'].split('>|||<')
		valor = [str(val) for val in valor]
		print "lista_valor: ", valor
		for v in valor:
			print "valor: ", v
	try:
		cat = Category.objects.get(name=valor[2])
	except Category.DoesNotExist:
		cat = None

	new_page = Page()
	new_page.category = cat
	new_page.title = valor[0]
	new_page.url = valor[1]
	new_page.views = 0
	new_page.save()
	print "id", new_page.id
	print "*****", new_page
	valor.append(new_page.id)
	valor = json.dumps(valor)

	return HttpResponse(valor)