# Speech Transcription
## Wstęp
Aplikacja realizująca transkrypcję mowy do tekstu w języku polskim. Projekt wykonywany w ramach przedmiotu Studio projektowe 1.
## Wymagania
 - Rejestracja użytkowników
 - Logowanie 
 - Nagrywanie audio 
 - Transkrypcja nagrania do pliku tekstowego
 - Bezpieczne przechowywanie plików
 - Działanie w trybie offline

Powyższe wymagania zostały spełnione
## Opis funkcjonalności
- **Logowanie i rejestracja**
Hasła użytkowników haszowane są za pomocą funkcji SHA-512. Przy logowaniu hasz wprowadzonego hasła jest porównywany z haszem zapisanym w pliku.
 - **Szyfrowanie i deszyfrowanie plików**
Symetryczne szyfrowanie zrealizowane przy pomocy klasy Fernet biblioteki cryptography.
 - **Nagrywanie audio**
Zrealizowane z użyciem biblioteki wave i pyaudio.
 - **Transkrypcja nagrania**
 Odbywa się poprzez wywołanie komendy shell uruchamiającej zmodyfikowaną wersję Juliusa - julius-dnn. 
 - **Odtwarzanie audio**
Do realizacji tego celu posłużono się biblioteką pygame.

## Instalacja
Należy sklonować repozytorium:
```
git clone https://github.com/pvrtykv/SpeechTranscription.git
```
Oraz zainstalować wymagane pakiety:
```
cd SpeechTranscription
pip3 install -r requirements.txt
```
Dodatkowo należy pobrać plik [julius.zip](https://www.dropbox.com/s/yxg5h3etu8zp18g/julius.zip?dl=0) oraz wypakować jego zawartość do folderu julius.
Może być konieczne zainstalowanie najnowszej wersji [VC REDIST x86](https://support.microsoft.com/en-us/topic/the-latest-supported-visual-c-downloads-2647da03-1eea-4433-9aff-95f26a218cc0).
## Opis użytkowania
Uruchomienie programu
```
python3 SpeechTranscription.py
```
By móc korzystać z programu należy się zarejestrować, a następnie zalogować. Następnie z menu głównego należy wybrać interesującą nas opcję.

<p align="center">
  <img src="https://github.com/pvrtykv/SpeechTranscription/blob/master/images/menu.png?raw=true" />
</p>

## Opcje w menu
 Dostęp do opcji jest możliwy po zalogowaniu. 
 - **Record**
 Nagrywanie dźwięku przez użytkownika.
 - **Play**
 Odtwarzanie nagranego wcześniej dźwięku.
 - **Open text file**
 Dostęp do plików tekstowych zawierających transkrypcję.
 - **Transcribe**
 Wykonuje przy pomocy Juliusa transkrypcję nagrań do pliku txt.
 - **Log out**
 Wylogowanie z aplikacji.


## Wykorzystane narzędzia
 - Silnik rozpoznawania mowy [Julius](https://github.com/julius-speech/julius)
 - [Model dla rozpoznawania mowy w języku polskim dla Juliusa](https://sourceforge.net/p/skrybotdomowy/news/2016/10/open-source-polish-speech-models-for-julius/)
 - Github - repozytorium kodu oraz tablica kanban

## Zakres odpowiedzialności
