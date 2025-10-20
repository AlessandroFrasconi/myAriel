import os
import json
import pickle
from datetime import datetime, timedelta
from flask import Flask, render_template, jsonify, request, session
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from pathlib import Path

# Carica variabili d'ambiente
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'chiave-segreta-temporanea-da-cambiare')
CORS(app)

# Directory per cache
CACHE_DIR = Path('cache')
CACHE_DIR.mkdir(exist_ok=True)

# Configurazione myAriel
MYARIEL_BASE_URL = 'https://myariel.unimi.it'
MYARIEL_LOGIN_URL = f'https://ariel.unimi.it/'

class MyArielScraper:
    def __init__(self):
        self.session = requests.Session()
        self.logged_in = False
        self.cache_file = CACHE_DIR / 'session.pkl'
        self.resources_cache = CACHE_DIR / 'resources.json'
        self.cookies_file = CACHE_DIR / 'cookies.txt'
        
    def load_session(self):
        """Carica sessione salvata se ancora valida"""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'rb') as f:
                    data = pickle.load(f)
                    if datetime.now() < data['expires']:
                        self.session.cookies.update(data['cookies'])
                        self.logged_in = True
                        print("✓ Sessione caricata dalla cache")
                        return True
            except Exception as e:
                print(f"Errore caricamento sessione: {e}")
        return False
    
    def load_cookies_from_browser(self, cookie_string):
        """Carica i cookies dal browser"""
        try:
            # Parse dei cookies
            cookies = {}
            for cookie in cookie_string.split(';'):
                cookie = cookie.strip()
                if '=' in cookie:
                    key, value = cookie.split('=', 1)
                    cookies[key.strip()] = value.strip()
            
            # Imposta i cookies nella sessione per entrambi i domini
            for key, value in cookies.items():
                self.session.cookies.set(key, value, domain='.unimi.it')
                # Imposta anche per ariel.unimi.it specificamente
                self.session.cookies.set(key, value, domain='ariel.unimi.it')
                self.session.cookies.set(key, value, domain='myariel.unimi.it')
            
            # Salva i cookies su file
            with open(self.cookies_file, 'w') as f:
                f.write(cookie_string)
            
            print(f"✓ Cookie importati: {len(cookies)} cookie caricati")
            
            # IMPORTANTE: Imposta logged_in a True dopo aver importato i cookies
            self.logged_in = True
            self.save_session()
            return True, f"Cookie importati: {len(cookies)} cookie"
            
        except Exception as e:
            print(f"✗ Errore importazione cookie: {e}")
            return False, f"Errore: {str(e)}"
    
    def save_session(self):
        """Salva sessione per riutilizzo"""
        try:
            data = {
                'cookies': self.session.cookies,
                'expires': datetime.now() + timedelta(hours=2)  # Sessione valida 2 ore
            }
            with open(self.cache_file, 'wb') as f:
                pickle.dump(data, f)
            print("✓ Sessione salvata")
        except Exception as e:
            print(f"Errore salvataggio sessione: {e}")
    
    def login(self, email=None, password=None, domain=None):
        """Esegue login a myAriel con autenticazione Shibboleth"""
        # Usa credenziali da parametri o da .env
        email = email or os.getenv('MYARIEL_EMAIL')
        password = password or os.getenv('MYARIEL_PASSWORD')
        domain = domain or os.getenv('MYARIEL_DOMAIN', '@studenti.unimi.it')
        
        if not email or not password:
            return False, "Credenziali mancanti"
        
        # Costruisci username completo
        full_username = email if '@' in email else f"{email}{domain}"
        
        try:
            print("→ Step 1: Caricamento pagina di login myAriel...")
            # Segui il redirect alla pagina di selezione IdP
            response = self.session.get(MYARIEL_LOGIN_URL, allow_redirects=True)
            
            # Salva URL corrente per debug
            current_url = response.url
            print(f"  URL corrente: {current_url[:80]}...")
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Step 2: Cerca e seleziona l'Identity Provider (UNIMI)
            print("→ Step 2: Ricerca Identity Provider...")
            
            # Cerca il form di selezione IdP o il link per UNIMI
            idp_form = soup.find('form', {'name': 'idpSelect'}) or soup.find('form', attrs={'name': 'IdPList'})
            
            if idp_form:
                print("  Trovato form selezione IdP")
                # Trova il campo per selezionare UNIMI
                idp_select = idp_form.find('select', {'name': 'user_idp'}) or idp_form.find('select')
                
                if idp_select:
                    # Cerca l'opzione UNIMI
                    unimi_option = None
                    for option in idp_select.find_all('option'):
                        if 'unimi' in option.get('value', '').lower() or 'milano' in option.get_text().lower():
                            unimi_option = option.get('value')
                            break
                    
                    if unimi_option:
                        print(f"  Selezionato IdP: {unimi_option}")
                        # Submit form IdP
                        action_url = idp_form.get('action')
                        if not action_url.startswith('http'):
                            from urllib.parse import urljoin
                            action_url = urljoin(current_url, action_url)
                        
                        idp_data = {'user_idp': unimi_option}
                        # Aggiungi campi nascosti
                        for hidden in idp_form.find_all('input', {'type': 'hidden'}):
                            if hidden.get('name'):
                                idp_data[hidden['name']] = hidden.get('value', '')
                        
                        response = self.session.post(action_url, data=idp_data, allow_redirects=True)
                        soup = BeautifulSoup(response.text, 'html.parser')
                        current_url = response.url
            
            # Step 3: Login con credenziali UNIMI
            print("→ Step 3: Invio credenziali UNIMI...")
            
            # Cerca il form di login vero e proprio
            login_form = (soup.find('form', {'id': 'fm1'}) or 
                         soup.find('form', {'name': 'fm1'}) or
                         soup.find('form', {'method': 'post'}) or
                         soup.find('form'))
            
            if not login_form:
                # Prova a cercare se siamo già loggati
                if 'logout' in response.text.lower() or 'esci' in response.text.lower():
                    self.logged_in = True
                    self.save_session()
                    print("✓ Già autenticato!")
                    return True, "Login effettuato"
                
                print(f"✗ Form di login non trovato. URL: {current_url[:100]}")
                # Salva HTML per debug
                with open('debug_page.html', 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print("  (HTML salvato in debug_page.html)")
                return False, "Form di login non trovato. Verifica che le credenziali siano corrette."
            
            # Prepara i dati di login
            # Cerca i nomi dei campi username e password
            username_field = (login_form.find('input', {'type': 'text'}) or
                            login_form.find('input', {'name': 'username'}) or
                            login_form.find('input', {'name': 'j_username'}) or
                            login_form.find('input', {'id': 'username'}))
            
            password_field = (login_form.find('input', {'type': 'password'}) or
                            login_form.find('input', {'name': 'password'}) or
                            login_form.find('input', {'name': 'j_password'}))
            
            if not username_field or not password_field:
                return False, "Campi username/password non trovati nel form"
            
            username_name = username_field.get('name', 'username')
            password_name = password_field.get('name', 'password')
            
            print(f"  Campi form: {username_name}={full_username}, {password_name}=***")
            
            login_data = {
                username_name: full_username,
                password_name: password,
            }
            
            # Aggiungi tutti i campi nascosti
            for hidden in login_form.find_all('input', {'type': 'hidden'}):
                if hidden.get('name'):
                    login_data[hidden['name']] = hidden.get('value', '')
            
            # Altri campi del form
            for input_field in login_form.find_all('input'):
                field_name = input_field.get('name')
                field_type = input_field.get('type', 'text')
                if field_name and field_name not in login_data and field_type not in ['text', 'password', 'submit', 'button']:
                    login_data[field_name] = input_field.get('value', '')
            
            # Cerca checkbox "remember me" se esiste
            remember_checkbox = login_form.find('input', {'type': 'checkbox'})
            if remember_checkbox and remember_checkbox.get('name'):
                login_data[remember_checkbox['name']] = remember_checkbox.get('value', 'on')
            
            # Esegui il login
            action_url = login_form.get('action', '')
            if not action_url.startswith('http'):
                from urllib.parse import urljoin
                action_url = urljoin(current_url, action_url)
            
            print(f"  POST a: {action_url[:80]}...")
            
            response = self.session.post(
                action_url,
                data=login_data,
                allow_redirects=True,
                timeout=30
            )
            
            # Step 4: Verifica autenticazione
            print("→ Step 4: Verifica autenticazione...")
            final_url = response.url
            print(f"  URL finale: {final_url[:80]}...")
            
            # Controlli per verificare il login
            page_text = response.text.lower()
            
            # Verifica positiva - cerchiamo segni di login riuscito
            success_indicators = [
                'logout' in page_text,
                'esci' in page_text,
                'sign out' in page_text,
                'dashboard' in page_text,
                'my courses' in page_text,
                'i miei corsi' in page_text,
                'myariel.unimi.it/my' in final_url
            ]
            
            # Verifica negativa - segni di login fallito
            failure_indicators = [
                'login failed' in page_text,
                'invalid' in page_text and 'credentials' in page_text,
                'username' in page_text and 'password' in page_text and 'login' in final_url,
                'autenticazione fallita' in page_text,
                'credenziali non valide' in page_text
            ]
            
            if any(success_indicators) and not any(failure_indicators):
                self.logged_in = True
                self.save_session()
                print("✓ Login effettuato con successo!")
                return True, "Login effettuato"
            else:
                print("✗ Login fallito")
                # Salva per debug
                with open('debug_login_failed.html', 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print("  (HTML salvato in debug_login_failed.html)")
                
                # Cerca messaggi di errore specifici
                soup_error = BeautifulSoup(response.text, 'html.parser')
                error_msg = soup_error.find('div', class_=lambda x: x and 'error' in x.lower() if x else False)
                if error_msg:
                    return False, f"Login fallito: {error_msg.get_text(strip=True)}"
                
                return False, "Credenziali errate o login fallito. Verifica email e password."
                
        except Exception as e:
            print(f"✗ Errore durante il login: {e}")
            import traceback
            traceback.print_exc()
            return False, f"Errore: {str(e)}"
    
    def get_courses(self):
        """Recupera la lista dei corsi"""
        if not self.logged_in and not self.load_session():
            success, msg = self.login()
            if not success:
                return None, msg
        
        try:
            # IMPORTANTE: I corsi sono su ariel.unimi.it (non myariel.unimi.it)
            # Bisogna andare su /Offerta/myof ("Il tuo Ariel")
            offerta_url = 'https://ariel.unimi.it/Offerta/myof'
            print(f"→ Accedo a 'Il tuo Ariel': {offerta_url}")
            response = self.session.get(offerta_url)
            print(f"  Status code: {response.status_code}")
            print(f"  URL finale: {response.url}")
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            courses = []
            
            # Cerca i link ai corsi con classe "ariel"
            course_links = soup.find_all('a', class_='ariel', href=lambda x: x and '/course/view.php?id=' in x)
            print(f"  Link trovati con classe 'ariel': {len(course_links)}")
            
            # Se non ne trova, prova senza filtro sulla classe
            if len(course_links) == 0:
                course_links = soup.find_all('a', href=lambda x: x and '/course/view.php?id=' in x)
                print(f"  Link trovati con '/course/view.php?id=' (senza classe): {len(course_links)}")
            
            seen_ids = set()
            for link in course_links:
                course_url = link.get('href')
                course_name = link.get_text(strip=True)
                
                # Filtra link non validi
                invalid_names = [
                    'minimizza tutto',
                    'espandi tutto',
                    'mostra tutto',
                    'nascondi tutto',
                    'expand all',
                    'collapse all',
                    'ctu',
                    'università degli studi di milano',
                    'copyright',
                    'privacy e cookie',
                    'condizioni di utilizzo',
                    'esci',
                    'riepilogo della conservazione dei dati',
                    'alessandro frasconi',
                    'home',
                    'dashboard',
                    ''
                ]
                
                if course_name.lower() in invalid_names or not course_name:
                    continue
                
                # Filtra anche link che non contengono numeri (probabilmente non sono corsi)
                if not any(char.isdigit() for char in course_name):
                    # Se il nome non contiene numeri e non sembra un nome di corso, salta
                    if len(course_name) < 10:  # Link troppo corti probabilmente non sono corsi
                        continue
                
                if not course_url.startswith('http'):
                    # Se è relativo, usa myariel come base
                    course_url = MYARIEL_BASE_URL + course_url
                
                # Estrai ID corso
                course_id = None
                if '?id=' in course_url:
                    course_id = course_url.split('?id=')[1].split('&')[0]
                
                if course_id and course_id not in seen_ids:
                    seen_ids.add(course_id)
                    
                    courses.append({
                        'id': course_id,
                        'name': course_name,
                        'url': course_url
                    })
            
            # Se non troviamo corsi, salviamo la pagina per debug
            if len(courses) == 0:
                print("  ⚠️  Nessun corso trovato - salvo la pagina /Offerta per debug")
                with open('debug_offerta.html', 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print("  (HTML salvato in debug_offerta.html)")
            
            print(f"✓ Trovati {len(courses)} corsi")
            return courses, "OK"
            
        except Exception as e:
            print(f"✗ Errore recupero corsi: {e}")
            return None, str(e)
    
    def get_course_resources(self, course_id):
        """Recupera le risorse di un corso specifico"""
        if not self.logged_in and not self.load_session():
            self.login()
        
        try:
            course_url = f'{MYARIEL_BASE_URL}/course/view.php?id={course_id}'
            response = self.session.get(course_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            resources = []
            
            # Cerca SOLO le sezioni del contenuto del corso (esclude header/footer)
            # Le sezioni vere hanno attributi specifici come data-sectionid o sono dentro #region-main
            main_content = soup.find('div', id='region-main') or soup.find('section', id='region-main') or soup
            
            # Cerca sezioni/argomenti SOLO nel contenuto principale
            sections = main_content.find_all('li', class_=lambda x: x and 'section' in x and 'main' in x) or \
                      main_content.find_all('li', attrs={'data-sectionid': True}) or \
                      main_content.find_all('li', class_=lambda x: x and 'section' in x)
            
            print(f"  → Trovate {len(sections)} sezioni nel corso")
            
            for idx, section in enumerate(sections):
                # Salta sezioni che non hanno contenuto didattico
                if 'emptySection' in str(section.get('class', [])):
                    continue
                    
                section_title_elem = section.find(['h3', 'h2', 'div'], class_=lambda x: x and 'sectionname' in x if x else False)
                section_title = section_title_elem.get_text(strip=True) if section_title_elem else f"Sezione {idx+1}"
                
                # Salta sezioni con titoli generici
                if section_title.lower() in ['generale', 'general', 'sezione 0']:
                    continue
                
                # Trova risorse nella sezione
                section_resources = []
                
                # File e link
                resource_links = section.find_all('a', href=True)
                print(f"  → Sezione '{section_title}': trovati {len(resource_links)} link totali")
                
                for link in resource_links:
                    href = link.get('href')
                    
                    # Estrai il nome pulito della risorsa
                    # Cerca prima lo span con classe 'instancename' (struttura Moodle)
                    instancename = link.find('span', class_='instancename')
                    if instancename:
                        # Rimuovi gli span con classe 'accesshide' (contengono "File", "Cartella", ecc.)
                        for accesshide in instancename.find_all('span', class_='accesshide'):
                            accesshide.decompose()
                        name = instancename.get_text(strip=True)
                    else:
                        # Fallback: prendi tutto il testo
                        name = link.get_text(strip=True)
                    
                    # Lista di parole chiave da ignorare (footer, header, navigazione)
                    # Se il nome del link CONTIENE una di queste parole, viene filtrato
                    invalid_keywords = [
                        'minimizza',
                        'espandi',
                        'mostra',
                        'nascondi',
                        'salta',
                        'ctu',
                        'copyright',
                        'privacy',
                        'cookie',
                        'condizioni di utilizzo',
                        'esci',
                        'conservazione',
                        'pannello laterale',
                        'vai al contenuto',
                        'alessandro',
                        'frasconi'
                    ]
                    
                    # Link esatti da ignorare
                    invalid_exact_names = [
                        'home',
                        'dashboard',
                        '#'
                    ]
                    
                    # Filtra link validi
                    if name and href and len(name) > 2:
                        name_lower = name.lower()
                        
                        # Salta link vuoti o anchor (#)
                        if href == '#' or href.endswith('#') or href.endswith('/#'):
                            print(f"    ✗ Filtrato (link vuoto/anchor): '{name}' → {href}")
                            continue
                        
                        # Salta link con nomi esatti nella blacklist
                        if name_lower in invalid_exact_names:
                            print(f"    ✗ Filtrato (nome esatto invalido): '{name}'")
                            continue
                        
                        # Salta link che CONTENGONO parole chiave invalide
                        if any(keyword in name_lower for keyword in invalid_keywords):
                            print(f"    ✗ Filtrato (contiene parola chiave invalida): '{name}'")
                            continue
                        
                        # IMPORTANTE: Accetta SOLO link che puntano a risorse di Moodle
                        # Esclude link generici di navigazione, profilo, ecc.
                        valid_resource_patterns = [
                            '/mod/resource/',
                            '/mod/url/',
                            '/mod/folder/',
                            '/mod/page/',
                            '/mod/assign/',
                            '/mod/quiz/',
                            '/mod/forum/',
                            '/mod/file/',
                            '/mod/lti/',
                            '/pluginfile.php'
                        ]
                        
                        if not any(pattern in href for pattern in valid_resource_patterns):
                            print(f"    ✗ Filtrato (pattern non valido): '{name}' → {href[:80]}")
                            continue
                        
                        print(f"    ✓ Risorsa valida: '{name}'")
                            
                        if not href.startswith('http'):
                            href = MYARIEL_BASE_URL + href
                        
                        resource_type = 'file'
                        if '/mod/url/' in href:
                            resource_type = 'url'
                        elif '/mod/folder/' in href:
                            resource_type = 'folder'
                        elif '/mod/resource/' in href or '/pluginfile.php' in href:
                            resource_type = 'file'
                        elif '/mod/page/' in href:
                            resource_type = 'page'
                        elif '/mod/assign/' in href:
                            resource_type = 'assignment'
                        elif '/mod/quiz/' in href:
                            resource_type = 'quiz'
                        elif '/mod/forum/' in href:
                            resource_type = 'forum'
                        
                        section_resources.append({
                            'name': name,
                            'url': href,
                            'type': resource_type
                        })
                
                if section_resources:
                    print(f"  ✓ Sezione '{section_title}': {len(section_resources)} risorse aggiunte")
                    resources.append({
                        'section': section_title,
                        'resources': section_resources
                    })
                else:
                    print(f"  ✗ Sezione '{section_title}': nessuna risorsa valida, sezione ignorata")
            
            print(f"✓ Trovate {len(resources)} sezioni con risorse")
            return resources, "OK"
            
        except Exception as e:
            print(f"✗ Errore recupero risorse: {e}")
            return None, str(e)
    
    def get_all_resources(self):
        """Recupera tutte le risorse di tutti i corsi"""
        courses, msg = self.get_courses()
        if not courses:
            return None, msg
        
        all_data = []
        for course in courses:
            print(f"→ Recupero risorse per: {course['name']}")
            resources, _ = self.get_course_resources(course['id'])
            all_data.append({
                'course': course,
                'sections': resources or []
            })
        
        # Salva in cache
        try:
            with open(self.resources_cache, 'w', encoding='utf-8') as f:
                json.dump({
                    'timestamp': datetime.now().isoformat(),
                    'data': all_data
                }, f, ensure_ascii=False, indent=2)
            print("✓ Risorse salvate in cache")
        except Exception as e:
            print(f"Errore salvataggio cache: {e}")
        
        return all_data, "OK"
    
    def load_cached_resources(self):
        """Carica risorse dalla cache se esistono"""
        if self.resources_cache.exists():
            try:
                with open(self.resources_cache, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data['data'], data['timestamp']
            except:
                pass
        return None, None


# Istanza globale dello scraper
scraper = MyArielScraper()


# Routes Flask
@app.route('/')
def index():
    """Pagina principale"""
    return render_template('index.html')


@app.route('/api/login', methods=['POST'])
def api_login():
    """Endpoint per login manuale"""
    data = request.json
    email = data.get('email')
    password = data.get('password')
    domain = data.get('domain', '@studenti.unimi.it')
    
    success, message = scraper.login(email, password, domain)
    return jsonify({'success': success, 'message': message})


@app.route('/api/import-cookies', methods=['POST'])
def import_cookies():
    """Importa cookies dal browser"""
    data = request.json
    cookie_string = data.get('cookies', '')
    
    if not cookie_string:
        return jsonify({'success': False, 'message': 'Nessun cookie fornito'}), 400
    
    scraper = MyArielScraper()
    success, message = scraper.load_cookies_from_browser(cookie_string)
    
    return jsonify({'success': success, 'message': message})

@app.route('/api/debug-page', methods=['POST'])
def debug_page():
    """Salva l'HTML di una pagina per debug"""
    data = request.json
    html = data.get('html', '')
    filename = data.get('filename', 'debug_custom.html')
    
    if html:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        return jsonify({'success': True, 'message': f'Pagina salvata in {filename}'})
    
    return jsonify({'success': False, 'message': 'Nessun HTML fornito'}), 400


@app.route('/api/courses')
def api_courses():
    """Endpoint per ottenere i corsi"""
    courses, message = scraper.get_courses()
    if courses is None:
        return jsonify({'success': False, 'message': message})
    return jsonify({'success': True, 'courses': courses})


@app.route('/api/resources')
def api_resources():
    """Endpoint per ottenere tutte le risorse"""
    # Prova prima dalla cache
    cached, timestamp = scraper.load_cached_resources()
    if cached and request.args.get('refresh') != 'true':
        return jsonify({
            'success': True,
            'data': cached,
            'cached': True,
            'timestamp': timestamp
        })
    
    # Altrimenti recupera da myAriel
    data, message = scraper.get_all_resources()
    if data is None:
        return jsonify({'success': False, 'message': message})
    
    return jsonify({
        'success': True,
        'data': data,
        'cached': False,
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/course/<course_id>/resources')
def api_course_resources(course_id):
    """Endpoint per ottenere risorse di un singolo corso"""
    resources, message = scraper.get_course_resources(course_id)
    if resources is None:
        return jsonify({'success': False, 'message': message})
    return jsonify({'success': True, 'resources': resources})


if __name__ == '__main__':
    print("=" * 60)
    print("🎓 MyAriel Resource Manager")
    print("=" * 60)
    print(f"→ Server in avvio su http://localhost:5001")
    print("→ Premi CTRL+C per fermare")
    print("=" * 60)
    
    # Prova login automatico se ci sono credenziali
    if os.getenv('MYARIEL_EMAIL') and os.getenv('MYARIEL_PASSWORD'):
        print("\n→ Tentativo login automatico...")
        scraper.login()
    
    app.run(debug=True, host='0.0.0.0', port=5001)
