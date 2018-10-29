# flask_docker_nought_crosses

A basic Flask application using Docker, postgres and SQLAlchemy to run a noughts and crosses game.

Each database row is a new game, which contains the following info:
- status of the game (In progress/ Xs win/ Os win)
- the player who is about to move (player 1 is always Xs)
- 9 columns for the tiles (either 'X', 'O' or '--')

To run, navigate to root directory and run:

    $ docker-compose up --build
    
After the first time, use: 

    $ docker-compose up --build

This creates a docker container for the application and the db and creates the database based on the schema. It should only create the db once i.e. it won't create a new one every time you run this.

Code isn't particularly resilient and no tests are included, however, there is a really slick looking frontend which makes up for it.
