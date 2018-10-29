from flask import Flask, render_template, redirect, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
 
DBUSER = 'sam'
DBPASS = 'scpwrd'
DBHOST = 'db'
DBPORT = '5432'
DBNAME = 'testdb'

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}'.format(
        user=DBUSER,
        passwd=DBPASS,
        host=DBHOST,
        port=DBPORT,
        db=DBNAME)

app.secret_key = 'skey'

db = SQLAlchemy(app)

class games(db.Model):
    id = db.Column('game_id', db.Integer, primary_key=True)
    status = db.Column(db.String(20))
    player_turn = db.Column(db.Integer)
    tile_1 = db.Column(db.String(2))
    tile_2 = db.Column(db.String(2))
    tile_3 = db.Column(db.String(2))
    tile_4 = db.Column(db.String(2))
    tile_5 = db.Column(db.String(2))
    tile_6 = db.Column(db.String(2))
    tile_7 = db.Column(db.String(2))
    tile_8 = db.Column(db.String(2))
    tile_9 = db.Column(db.String(2))

    def __init__(self, status, player_turn, tile_1, tile_2, tile_3, tile_4, tile_5, tile_6, tile_7, tile_8, tile_9):
        self.status = status
        self.player_turn = player_turn
        self.tile_1 = tile_1
        self.tile_2 = tile_2
        self.tile_3 = tile_3
        self.tile_4 = tile_4
        self.tile_5 = tile_5
        self.tile_6 = tile_6
        self.tile_7 = tile_7
        self.tile_8 = tile_8
        self.tile_9 = tile_9

def check_winners(tile_list):
    for i in [0,3,6]:
        if tile_list[i] != '--':
            if tile_list[i] == tile_list[i+1] == tile_list[i+2]:
                return tile_list[i] + 's win'
    for i in [0,1,2]:
        if tile_list[i] != '--':
            if tile_list[i] == tile_list[i+3] == tile_list[i+6]:
                return tile_list[i] + 's win'
    if tile_list[0] == tile_list[4] == tile_list[8] != '--':
        return tile_list[0] + 's win'
    if tile_list[2] == tile_list[4] == tile_list[6] != '--':
        return tile_list[2] + 's win'
    return 'In progress'

@app.route('/', methods=['GET', 'POST'])
def home():
    game = db.session.query(games).order_by(games.id.desc()).limit(1).first()
    if request.method == 'POST':
        if 'tile' in request.form:
            tile = request.form['tile']
            if getattr(game, tile) != '--':
                flash('Invalid move')
            else:
                if game.player_turn == 1:
                    setattr(game, tile, 'X')
                    game.player_turn = 2
                    game.status = check_winners([getattr(game, 'tile_' + str(i)) for i in range(1,10)])
                else:
                    setattr(game, tile, 'O')
                    game.player_turn = 1
                    game.status = check_winners([getattr(game, 'tile_' + str(i)) for i in range(1,10)])
                db.session.commit()
            return redirect(url_for('home'))
    return render_template('board.html', games=game)

@app.route('/new_game')
def refresh():
        game = games(
            'In progress',
            1,
            '--',
            '--',
            '--',
            '--',
            '--',
            '--',
            '--',
            '--',
            '--')

        db.session.add(game)
        db.session.commit()
        
        return redirect(url_for('home'))
 
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, host='0.0.0.0')