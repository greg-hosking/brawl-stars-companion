from flask import Blueprint, render_template, request
import requests


views = Blueprint('views', __name__)


@views.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@views.route('/profile', methods=['GET'])
def profile():
    # API token and base url
    token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImRlM2MzZDViLTVlNzYtNDE0ZC04M2MwLTVjMzFmZjhlYWE5YiIsImlhdCI6MTYyMDQzNzU5Niwic3ViIjoiZGV2ZWxvcGVyLzZlNTE4NDlkLWQwNzAtNzRmMC03OGNhLWY0NjAwNDIyYTY4ZCIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiNzMuNjAuMTIzLjE0NCJdLCJ0eXBlIjoiY2xpZW50In1dfQ.eza1W85wu36KbNX5dE0kY0FYUSeYuhe7viGr36J6_-M6cMIb_Z-jejaQoD2DsVZhZbRrRRNd_L7wX2EU0FGtWw'
    headers = {'Authorization': 'Bearer ' + token}
    base_url = 'https://api.brawlstars.com/v1/players/%23'

    # Get the player tag from the request url
    player_tag = request.args.get('playerTagInput')[1:].upper()
    # Build the GET request url using the new player tag
    url = base_url + player_tag

    # Make the request
    response = requests.get(url, headers=headers)
    player_data = response.json()

    # Check whether the player tag was valid (if the player tag does not exist,
    # then the returned data will be {'reason': 'notFound'}...)
    if 'reason' in player_data:
        return render_template('profile.html', player_data=None)

    # If the player tag returned data, find the brawler with the highest trophies
    brawlers = player_data['brawlers']
    highest_trophy_brawler = brawlers[0]
    for brawler in brawlers:
        if brawler['trophies'] > highest_trophy_brawler['trophies']:
            highest_trophy_brawler = brawler

    return render_template('profile.html', player_data=player_data, highest_trophy_brawler=highest_trophy_brawler)


@views.route('/brawlers', methods=['GET'])
def brawlers():
    return render_template('brawlers.html')


@views.route('/events', methods=['GET'])
def events():
    return render_template('events.html')


@views.route('/guide', methods=['GET'])
def guide():
    return render_template('guide.html')
