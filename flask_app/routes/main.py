from flask import Blueprint, render_template
from flask_login import login_required
from flask_app import db
from flask_app.src.scripts.server_stats import get_server_stats

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    server_stats = get_server_stats()
    return render_template('index.html', server_stats=server_stats)

# [EXEMPLE DE ROUTE]
#@main.route('/exemple', methods=['GET']) => Chemin de la route avec la méthode GET
#
#@login_required => Ne pas mettre si pas d'authentification requise, ou si vous êtes entrain de dev la page ;)
#
#def exemple(): => Définition de la fonction pour la route. /!\ Doit porter le même nom que la route
#
#    server_stats = get_server_stats() => Si besoin de valeur
#
#    return render_template('index.html', server_stats=server_stats) ==> Méthode pour affiché une VUE, mettre les variables après pour pouvoir les affichers dans le template.
#
#@auth.route('/signup', methods=['POST']) => Chemin de la route avec la méthode POST [POUR LES RETOURS DE FORMULAIRE]
#def exemple_post(): => Définition de la fonction pour la route. /!\ Doit porter le suffix _post avec le même nom que la route
#    exemple_value = request.form.get('exemple') => Récupération du champ d'un formulaire avec l'attribue name='exemple' de définie
#
#    return redirect(url_for('main.exemple')) ==> Méthode pour rediriger vers une autre page.

# [NOUVELLE ROUTE ICI]