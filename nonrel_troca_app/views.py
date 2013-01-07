# Create your views here.

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from models import *
from forms import *
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.views.generic import ListView

from django.utils import simplejson



def categories(request):
	return render(request, 'select_categories.html', )



def getAjaxCategories(request):

	if request.GET['category']:
		parent = request.GET['category']
		#import pdb; pdb.set_trace()
	
	if request.is_ajax():
		if parent:
			p = Category.objects.get( categoryTitle = parent )
			
			crumbs = p.howToOrder().split('>')

			items = list(Category.objects.filter( parentCategory = p ).values_list('categoryTitle'))		
			#message = simplejson.dumps(items)
			m = {'items': items, 'crumbs': crumbs}
			message = simplejson.dumps(m)

		else:
			#reached the end of the categories.
			message = 'no more cats'
	else:
		#this should be a response for non ajax requests...
		message = 'god damn'

	#import time
	#time.sleep(3)
	return HttpResponse(message, mimetype='application/json')



def index(request):
    items = GenericItem.objects.all()
    return render(request, 'index.html', {'Items': items})



def detail(request, item_id):
    try:
        item = GenericItem.objects.get(pk=item_id)
        owner = User.objects.get(pk=item.owner_id)
    except GenericItem.DoesNotExist:
        raise Http404
    return render(request, 'item_detail.html', {'item': item, 'owner': owner})



def thanks(request):
	return render(request, 'thanks.html', {})



@login_required
def genericItem(request):
	if request.method == 'POST':
		form = GenericItemForm(request.POST)

		print "request is post."

		if form.is_valid():
			#process the data in form.cleaned_data
			t = form.cleaned_data['title']
			d = form.cleaned_data['description']
			v = form.cleaned_data['value']

			#item = GenericItem(owner_id=request.user.id, title=t, description=d, value=v, location=None, offers=[])
			item = GenericItem(owner_id=request.user.id, title=t, description=d, value=v, location=None, offers=[])
			item.save()

			return HttpResponseRedirect('/thanks/')

	else:
		form = GenericItemForm()

	return render(request, 'item.html', {
		'form': form,
	} )


@login_required
def makeOffer(request, item_id):
	
	wantedItem = GenericItem.objects.get(pk=item_id)
	myItems = GenericItem.objects.filter(owner_id = request.user.id)

	if request.method == 'POST':
		selected_items = request.POST.getlist('items_selected')

		#import pdb; pdb.set_trace()

		if len(selected_items) < 1:
			return render(request, 'make_offer.html', {
				'wantedItem': wantedItem,'myItems': myItems, 'error':'Must select an item.'
			})

		else:
			items_in_offer = list()
			for i in selected_items:
				wholeItem = GenericItem.objects.get(pk=i)
				partialitem = ItemInOffer(itemTitle=wholeItem.title, value=wholeItem.value, item=wholeItem)
				items_in_offer.append(partialitem)

			offer = Offer(title='An offer', author_id=request.user.id, author=request.user.username, items=items_in_offer)

			#import pdb; pdb.set_trace()

			wantedItem.offers.append(offer)
			wantedItem.save()

			return HttpResponseRedirect('/thanks/')

	else:
		
		return render(request, 'make_offer.html', {
			'wantedItem': wantedItem,'myItems': myItems
		})




#Could not use standard @login_required decorator since this is a ClassBased GenericView...
class ItemsForLoggedUser(ListView):
	
	context_object_name = 'myItems'
	template_name = 'myItems.html'

	#Overloading the get_queryset method of ListView
	def get_queryset(self):
		the_id = self.request.user.id
		return GenericItem.objects.filter(owner_id = the_id)









