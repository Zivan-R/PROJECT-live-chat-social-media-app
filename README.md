## Notes: 
- This app is being rewritten into a Microservices architecture with it's own full DevOps workflow
  
---
  
# PROJECT: Social media app with a live chat [ENG/FR]

![Welcome page](screenshots/welcome.jpg)

**Personal Wall / Espace personnel**  
![personal wall](screenshots/perso-wall.jpg)
  
**You can comment and like status / Possibilité d'aimer et commenter un statut** 
![comment and like status](screenshots/status-com-like.jpg)
  
**Dynamic user search / Recherche dynamique d'utilisateurs**
![user search](screenshots/search-toto.jpg)
  
**Dynamic post search / Recherche dynamique de posts** 
![post search](screenshots/search-post.jpg)
  
**Live chat / Chat en direct**  
![live chat](screenshots/live-chat.jpg)  
  
  
  
  
## Try it on your computer! / Essayez l'appli sur votre ordinateur!
**Prerequisites Check / Vérification des prérequis**
- Ensure the following are installed / Vérifiez que les outils suivants sont bien installés:
  - Python ( https://www.python.org/downloads/ )
  - Node.js & npm ( https://nodejs.org/ )

Check versions:
```bash
python --version
pip --version
node --version
npm --version
```
  
**Get the repo / Récupérer le repo**
```bash
git clone https://github.com/Zivan-R/PROJECT-live-chat-social-media-app.git
cd PROJECT-live-chat-social-media-app
```
  
To make things easier / Pour simplifier le processus:  
  
(Eng) Use two different Terminal instances, one for the Frontend, and one for the Backend  
(Fr) Utilisez deux instances différentes du Terminal, une pour le Frontend, une pour le Backend
  
**Bash setup guide / Guide d'installation Bash (Linux/macOS)**
- Frontend Setup:
  ```bash
  cd vue_frontend/
  npm intall
  npm run dev

  # Check the output and copy paste the URL after "Local:" into your browser
  # Récupérer l'adresse URL dans l'output, après "Local:" et la coller dans votre navigateur
  # (ex: http://localhost:5173/) 
  ```

- Backend Setup
  ```bash
  cd django_backend
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  daphne -p 8000 django_backend.asgi:application
  ```

**Powershell setup guide / Guide d'installation Powershell (Windows)**
- Frontend Setup:
  ```bash
  cd vue_frontend/
  npm intall
  npm run dev

  # Check the output and copy paste the URL after "Local:" (ex: http://localhost:5173/) into your browser
  # Récupérer l'adresse URL dans l'output, après "Local:" (ex: http://localhost:5173/) et la coller dans votre navigateur
  ```

- Backend Setup
  ```bash
  cd django_backend
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  pip install -r requirements.txt
  daphne -p 8000 django_backend.asgi:application
  ```  
  
  
  
  
## Tech Stack:
### Front end
- Vue3 Framework
- Tailwind CSS
- Socket.IO Client

### Back end
- Django Framework
- Socket.IO (python server side for real time communication)

### Database
- SQLite

## [ENG]
***Notes***
This project was made in the context of the 3 months long training "Formation Professionnalisante Python"
provided by *M2i Formation*
It was made in 3 weeks as a final project.
  
- Features:
     - Account creation
     - Authentication
     - REST API
     - A friend system
     - A personnal "wall" accessible to other users
     - The possibility of commenting posts + liking posts and comments
     - A main live chat (a tribute to the good old days of IRC)
     - And of course all of this is recorded in a well organized database. (SQLite for convenience)
  
Logo Credit: Full credit to ***Nicolas Robouam*** for the logo design. 
The logo is entirely his work, and I claim no ownership or rights over it.

The github_protocol.txt and R3_setup_protocol.txt were early attempts at documentation created during the first week of the project. They are not up to date.

## [FR]
***Remarques***
Ce projet a été réalisé dans le cadre de la formation intensive de 3 mois « Formation Professionnalisante Python »
dispensée par M2i Formation.
Il a été développé en 3 semaines en tant que projet final.
  
- Mises à jours à venir :  
  - Migration vers une architecture microservices
  - Transformation vers un projet full DevOps  

- Fonctionnalités :
  - Création de compte
  - Authentification
  - API REST
  - Système d'amis
    - Un "Mur" personnel accessible aux autres utilisateurs
    - Possibilité de commenter des publications + liker les publications et commentaires
    - Un chat principal en direct (hommage aux bons vieux jours de l'IRC)
    - Et bien sûr, tout cela est enregistré dans une base de données bien organisée (SQLite pour la simplicité)
  
Crédit du logo: Tout le crédit revient à ***Nicolas Robouam*** pour la conception du logo. 
Le logo est entièrement son œuvre, et je ne revendique aucun droit ni aucune propriété à son sujet.

Les fichiers github_protocol.txt et R3_setup_protocol.txt sont des premières tentatives de documentation réalisées durant la première semaine du projet. Ils ne sont pas à jour.
