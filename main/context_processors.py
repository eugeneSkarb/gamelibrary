from .models import *



def top_content(request):
    developers = GameStudio.objects.raw('SELECT main_gamestudio.id, '
                                        'main_gamestudio.name, COUNT(main_game.game_studio_id) as popularity '
                                        'FROM main_gamestudio '
                                        'INNER JOIN main_game ON main_gamestudio.id = main_game.game_studio_id '
                                        'GROUP BY main_gamestudio.id, main_gamestudio.name '
                                        'ORDER BY popularity DESC LIMIT 5')

    user_games = Game.objects.filter(creator_id=request.user.id).values_list('pk', flat=True)
    user_ratings = {}

    for item in UserRating.objects.filter(user_id=request.user.id).values('game_id', 'rating'):
        user_ratings[item['game_id']] = item['rating']

    return {'genres': Genre.objects.all(),
            'developers': developers,
            'user_games': user_games,
            'user_ratings': user_ratings}
