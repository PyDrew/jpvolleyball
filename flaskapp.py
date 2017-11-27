__author__ = 'Drew'

import os
import json
import voting
from flask import Flask
from flask import render_template, url_for, request, redirect

app = Flask(__name__)

# Where are we going to store data files?
try:
    # OpenShift environment
    data_dir = os.environ['OPENSHIFT_DATA_DIR']
except KeyError:
    # Local development environment
    data_dir = 'static'

def LoadPlayerFile():
    return json.load(open(os.path.join(data_dir, 'players.json')))
    
def DumpPlayerFile(data):
    fp = open(os.path.join(data_dir, 'players.json'), 'w')
    json.dunp(data, fp)

def LoadVoteFile():
    return json.load(open(os.path.join(data_dir, 'votes.json')))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/teams')
def teams():
    return render_template('teams.html')


@app.route('/schedule')
def schedule():
    return render_template('schedule.html')


@app.route('/standings')
def standings():
    return render_template('standings.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/sportsmanship')
def sportsmanship():
    # player_file = os.path.join(data_dir, "players.json")
    active_players = [
        "Alex Roskowski",
        "Alex Tannock",
        "Al Leclair",
        "Andrew Fox",
        "Artie White",
        "Brian Burnham",
        "Brian Davidge",
        "Brian Galipeau",
        "Bryan Lowe",
        "Carlos Desousa",
        "Danielle DaSilva",
        "Drew Marchand",
        "Drew O'Donnell",
        "Emmerson Brown",
        "Geoff Vincelette",
        "Ian Dalpe",
        "Jenn Prentice",
        "Josh Laboissonniere",
        "John Tarnuzzer",
        "Kasey Cameron",
        "Kenny Villa",
        "Lauren Fatse",
        "Madi Royer",
        "Michelle Morin",
        "Mike Giuliano",
        "Monica Alexio",
        "Nick Mainville",
        "Pam Legare"
        "Pat Sylvestre",
        "Paul Macrina",
        "Rob Rock",
        "Ryan Dupuis",
        "Scott Hampson",
        "Sean Whittle",
        "Shawn Hoyle",
        "Tim Kounlavauth"
        "Tom Marcoux",
        "Tommy Figuerido",
        "Vanessa Normandin",
        "Vicki Walters",
        "Walker Strick",
        "Zach Dalton",
    ]
    # if os.path.exists(player_file):
    #     all_players = json.load(open(player_file))
    #     active_players = []
    #     for p,p_data in all_players.iteritems():
    #         if p_data['status'] == "active":
    #             active_players.append(p)
    # else:
    #     active_players = []
    return render_template('sportsmanship.html', players=sorted(active_players))


@app.route('/handle_vote', methods=['POST'])
def handle_vote():
    vote = request.form['vote']
    comment = request.form['comment']

    # New code: Use JSON to track votes and voting IP addresses - no repeat voters
    request_ip = request.access_route[-1]
    voting.LogVoteAttempt(request.access_route)
    response = voting.AddVote(vote, comment, request_ip)
    return render_template('postvote.html', response=response)


@app.route('/voting_results')
def voting_results():
    vote_file = (os.path.join(data_dir,'votes.json'))
    if os.path.exists(vote_file):
        vote_data = json.load(open(vote_file))
        return render_template("voting_results.html", votes=vote_data['votes'])
    
    return render_template("index.html")

@app.route('/clear_voting_ips', methods=['POST'])
def clear_voting_ips():
    voting.ClearVotingIPAddresses()
    return redirect('/voting_results')

@app.route('/clear_voting_data', methods=['POST'])
def clear_voting_data():
    voting.ClearVotingData()
    return redirect('/voting_results')

@app.route('/admin')
def admin():
    return redirect('/')

'''
@app.route('/admin/players', methods=['GET','POST'])
def player_admin():
    players = LoadPlayerFile()
    player_data = []
    for p, p_data in players.iteritems():
        player_data.append({'name': p, 'status': p_data['status']})
    return render_template('player_admin.html', players=sorted(player_data))


@app.route('/admin/add_player', methods=['GET','POST'])
def add_player():
    if request.method == 'POST':
        form = request.form
        players = LoadPlayerFile()
        players[form['player_name']] = {
                'mobile_phone': form['player_mobile'],
                'home_phone': form['player_home'],
                'email': form['player_email'],
                'status': form['player_status'],
                'team': form['player_team'],
                'rank': form['player_rank']
        }
        DumpPlayerFile(players)
        return redirect('/admin/players')
    return render_template('add_player.html')
'''

with app.test_request_context():
    print( url_for('index') )
    print( url_for('static', filename='images/templatemo_body.jpg') )

if __name__ == '__main__':
    app.run(host="0.0.0.0")
