from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CardCollectionForm, CardForm
from .models import CardCollection
from config.decorators import non_guest_required


@non_guest_required
def collection_list(request):
    collections = CardCollection.objects.filter(
        author=request.user
    ).prefetch_related('cards')

    return render(
        request,
        'cards/collection_list.html',
        {
            'collections': collections,
        }
    )


@non_guest_required
def collection_create(request):
    if request.method == 'POST':
        form = CardCollectionForm(request.POST)

        if form.is_valid():
            collection = form.save(commit=False)
            collection.author = request.user
            collection.save()

            return redirect(
                'cards:collection_detail',
                collection_id=collection.id,
            )

    else:
        form = CardCollectionForm()

    return render(
        request,
        'cards/collection_create.html',
        {
            'form': form,
        }
    )


@non_guest_required
def collection_detail(request, collection_id):
    collection = get_object_or_404(
        CardCollection,
        id=collection_id,
        author=request.user,
    )

    card_form = CardForm()

    return render(
        request,
        'cards/collection_detail.html',
        {
            'collection': collection,
            'card_form': card_form,
        }
    )


@non_guest_required
def card_create(request, collection_id):
    collection = get_object_or_404(
        CardCollection,
        id=collection_id,
        author=request.user,
    )

    if request.method == 'POST':
        form = CardForm(request.POST)

        if form.is_valid():
            card = form.save(commit=False)
            card.collection = collection
            card.save()

    return redirect(
        'cards:collection_detail',
        collection_id=collection.id,
    )


@non_guest_required
def study_cards(request, collection_id):
    collection = get_object_or_404(
        CardCollection,
        id=collection_id,
        author=request.user,
    )

    cards = list(collection.cards.all())

    if not cards:
        return render(
            request,
            'cards/study_cards.html',
            {
                'collection': collection,
                'empty': True,
            }
        )

    current_index = int(request.GET.get('card', 0))
    show_back = request.GET.get('show_back') == '1'

    if current_index >= len(cards):
        current_index = 0

    card = cards[current_index]

    has_next = current_index < len(cards) - 1
    has_prev = current_index > 0

    return render(
        request,
        'cards/study_cards.html',
        {
            'collection': collection,
            'card': card,
            'current_index': current_index,
            'show_back': show_back,
            'has_next': has_next,
            'has_prev': has_prev,
            'total_cards': len(cards),
        }
    )