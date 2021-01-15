from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from .forms import *
from .models import Game, Genre, GameStudio


def index(request):
    if request.GET.get('search') is not None:
        games = Game.objects.filter(name__icontains=request.GET['search']).order_by('-created')
    else:
        paginator = Paginator(Game.objects.all().order_by('-created'), 20)

        page_number = request.GET.get('page', '1')
        games = paginator.get_page(page_number)

    return render(request, 'main/index.html', {'games': games, 'search': request.GET.get('search', '')})


def genre(request, id=1):
    genre_info = Genre.objects.get(id=id)
    games = genre_info.games.all()

    return render(request, 'pages/genre.html', {'genre': genre_info, 'games': games})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/')
                else:
                    messages.error(request, 'Аккаунт заблокирован')
            else:
                messages.error(request, 'Неправильный логин или пароль')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('/')


def register(request):
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()

            cd = user_form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            login(request, user)

            return redirect('/')
        else:
            messages.error(request, 'Неправильно введены данные')
    else:
        user_form = RegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def user_profile(request):
    games = Game.objects.filter(creator_id=request.user.id)

    return render(request, 'account/profile.html', {'games': games})


@login_required
def add_game(request):
    game_form = GameForm()
    publisher_form = PublisherForm()
    game_studio_form = GameStudioForm()
    genre_form = GenreForm()

    return render(request, 'pages/add_game.html', {'game_form': game_form,
                                                   'game_studio_form': game_studio_form,
                                                   'publisher_form': publisher_form,
                                                   'genre_form': genre_form})


@login_required
def create_game(request):
    if request.method != 'POST':
        return redirect('/')

    game_form = GameForm(request.POST, request.FILES)
    if game_form.is_valid():
        new_game = game_form.save(commit=False)
        new_game.creator_id = request.user.id
        new_game.save()
        game_form.save()
        messages.success(request, 'Игра успешно добавлена')
        return render(request, 'pages/add_game.html', {'game_form': GameForm(),
                                                       'game_studio_form': GameStudioForm(),
                                                       'publisher_form': PublisherForm(),
                                                       'genre_form': GenreForm()})
    else:
        messages.error(request, 'Неверно заполнены данные')
        return render(request, 'pages/add_game.html', {'game_form': game_form,
                                                       'game_studio_form': GameStudioForm(),
                                                       'publisher_form': PublisherForm(),
                                                       'genre_form': GenreForm()})


@login_required
def create_game_studio(request):
    if request.method != 'POST':
        return redirect('/')

    game_studio_form = GameStudioForm(request.POST, request.FILES)
    if game_studio_form.is_valid():
        game_studio_form.save()
        messages.success(request, 'Разработчик успешно добавлен')
        return render(request, 'pages/add_game.html', {'game_form': GameForm(),
                                                       'game_studio_form': GameStudioForm(),
                                                       'publisher_form': PublisherForm(),
                                                       'genre_form': GenreForm()})
    else:
        messages.error(request, 'Неверно заполнены данные')
        return render(request, 'pages/add_game.html', {'game_form': GameForm(),
                                                       'game_studio_form': game_studio_form,
                                                       'publisher_form': PublisherForm(),
                                                       'genre_form': GenreForm()})


@login_required
def create_publisher(request):
    if request.method != 'POST':
        return redirect('/')

    publisher_form = PublisherForm(request.POST)
    if publisher_form.is_valid():
        publisher_form.save()
        messages.success(request, 'Издатель успешно добавлен')
        return render(request, 'pages/add_game.html', {'game_form': GameForm(),
                                                       'game_studio_form': GameStudioForm(),
                                                       'publisher_form': PublisherForm(),
                                                       'genre_form': GenreForm()})
    else:
        messages.error(request, 'Неверно заполнены данные')
        return render(request, 'pages/add_game.html', {'game_form': GameForm(),
                                                       'game_studio_form': GameStudioForm(),
                                                       'publisher_form': publisher_form,
                                                       'genre_form': GenreForm()})


@login_required
def create_genre(request):
    if request.method != 'POST':
        return redirect('/')

    genre_form = GenreForm(request.POST)
    if genre_form.is_valid():
        genre_form.save()
        messages.success(request, 'Жанр успешно добавлен')
        return render(request, 'pages/add_game.html', {'game_form': GameForm(),
                                                       'game_studio_form': GameStudioForm(),
                                                       'publisher_form': PublisherForm(),
                                                       'genre_form': GenreForm()})
    else:
        messages.error(request, 'Неверно заполнены данные')
        return render(request, 'pages/add_game.html', {'game_form': GameForm(),
                                                       'game_studio_form': GameStudioForm(),
                                                       'publisher_form': PublisherForm(),
                                                       'genre_form': genre_form})


def game(request, id=1):
    game_obj = Game.objects.get(id=id)

    if game_obj.metacritic_rating > 74:
        rating_color = 'game-score--green'
    elif game_obj.metacritic_rating > 49:
        rating_color = 'game-score--yellow'
    else:
        rating_color = 'game-score--red'

    genres_string = ', '.join(list(game_obj.genres.all().values_list('name', flat=True)))

    try:
        user_rating = UserRating.objects.get(user_id=request.user.id, game_id=id)
    except UserRating.DoesNotExist:
        user_rating = None

    if user_rating is not None:
        user_rating = user_rating.rating

    return render(request, 'pages/game.html', {'game': game_obj,
                                               'rating_color': rating_color,
                                               'genres_string': genres_string,
                                               'user_rating': user_rating})


def developer(request, id=1):
    game_studio = GameStudio.objects.get(id=id)
    games = game_studio.game_set.all()

    return render(request, 'pages/developer.html', {'game_studio': game_studio, 'games': games})


@login_required
def rate_game(request, id=1):
    if request.GET.get('score') is None:
        messages.error(request, 'Некорректный запрос')
    else:
        UserRating.objects.update_or_create(game_id=id,
                                            user_id=request.user.id,
                                            rating=request.GET.get('score'))
        messages.success(request, 'Ваша оценка сохранена')

    return redirect('/games/' + str(id))
