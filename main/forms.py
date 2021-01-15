from django import forms

from .models import *


class LoginForm(forms.Form):
    username = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают.')
        return cd['password2']


class GameForm(forms.ModelForm):
    genres = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                            queryset=Genre.objects.all(),
                                            label='Жанры')

    def __init__(self, *args, **kwargs):
        if 'instance' in kwargs:
            initial = kwargs.setdefault('initial', {})
            initial['genres'] = kwargs['instance'].genres.values_list('pk', flat=True)

        super(GameForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = forms.ModelForm.save(self, False)

        old_save_m2m = self.save_m2m

        def save_m2m():
            old_save_m2m()
            instance.genres.clear()
            instance.genres.add(*self.cleaned_data['genres'])

        self.save_m2m = save_m2m

        if commit:
            instance.save()
            self.save_m2m()

        return instance

    class Meta:
        model = Game
        fields = ('name', 'description', 'released', 'image', 'metacritic_rating', 'game_studio', 'publisher')
        labels = {
            'name': 'Название',
            'description': 'Описание',
            'released': 'Год выхода',
            'image': 'Постер',
            'metacritic_rating': 'Рейтинг на метакритике',
            'game_studio': 'Разработчик',
            'publisher': 'Издатель',
        }


class GameStudioForm(forms.ModelForm):
    class Meta:
        model = GameStudio
        fields = ('name', 'description', 'image', 'founded')
        labels = {
            'name': 'Название',
            'description': 'Описание',
            'image': 'Изображение',
            'founded': "Год создания",
        }


class PublisherForm(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = ('name', 'description', 'director', 'founder', 'founded')
        labels = {
            'name': 'Название',
            'description': 'Описание',
            'director': 'Директор',
            'founder': 'Основатель',
            'founded': 'Год создания',
        }


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ('name', 'description')
        labels = {
            'name': 'Название',
            'description': 'Описание',
        }
