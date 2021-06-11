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
 Odbywa się poprzez wywołanie komendy shell uruchamiającej zmodyfikowaną wersję Juliusa - julius-dnn. Akceptowany format nagrania to 16kHz, RIFF WAV PCM 16 bit, mono, powyżej 30 sekund.
 - **Odtwarzanie audio**
Do realizacji tego celu posłużono się biblioteką pygame.

## Instalacja
Aplikacja przeznaczona jest na komputery z systemem Windows.
Należy sklonować repozytorium:
```
git clone https://github.com/pvrtykv/SpeechTranscription.git
```
Oraz zainstalować wymagane pakiety:
```
cd SpeechTranscription
pip install -r requirements.txt
```
**Uwaga!** W przypadku używania Pythona w wersji 3.7 i powyżej, aby zainstalować pakiet PyAudio, należy uruchomić terminal jako administrator i wprowadzić następujące komendy:
```
pip install pipwin
pipwin install pyaudio
```
Więcej informacji o tym problemie [tutaj](https://stackoverflow.com/questions/52283840/i-cant-install-pyaudio-on-windows-how-to-solve-error-microsoft-visual-c-14)

Dodatkowo należy pobrać archiwum [julius.zip](https://www.dropbox.com/s/yxg5h3etu8zp18g/julius.zip?dl=0) oraz wypakować jego zawartość do folderu julius.
Może być konieczne zainstalowanie najnowszej wersji [VC REDIST x86](https://support.microsoft.com/en-us/topic/the-latest-supported-visual-c-downloads-2647da03-1eea-4433-9aff-95f26a218cc0).
## Opis użytkowania
Uruchomienie programu
```
python SpeechTranscription.py
```
Po uruchomieniu programu pojawi się poniższy ekran.
<p align="left">
  <img src="https://github.com/pvrtykv/SpeechTranscription/blob/master/images/start-menu.PNG?raw=true" />
</p>
Klikamy w Register i mamy możliwość utworzenia nowego użytkownika.
<p align="left">
  <img src="https://github.com/pvrtykv/SpeechTranscription/blob/master/images/register_menu.PNG?raw=true" />
</p>
Przy logowaniu należy wpisać dane któregoś z istniejących kont.
<p align="left">
  <img src="https://github.com/pvrtykv/SpeechTranscription/blob/master/images/login_menu.PNG?raw=true" />
</p>
Gdy logowanie przebiegnie pomyślnie, pojawi się główne menu.
<p align="left">
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

W projekcie znajdują się 3 demonstracyjne nagrania dźwiękowe. Można również pobrać pliki wav z internetu. Posiadanie dyktafonu nie jest więc wymagane do korzystania z aplikacji.
Okno wyświetlające się podczas nagrywania.
<p align="left">
  <img src="https://github.com/pvrtykv/SpeechTranscription/blob/master/images/recording.PNG?raw=true" />
</p>

Przykładowy rezultat transkrypcji.
<p align="left">
  <img src="https://github.com/pvrtykv/SpeechTranscription/blob/master/images/result.PNG?raw=true" />
</p>

## Wykorzystane narzędzia
 - Silnik rozpoznawania mowy [Julius](https://github.com/julius-speech/julius)
 - [Model dla rozpoznawania mowy w języku polskim dla Juliusa](https://sourceforge.net/p/skrybotdomowy/news/2016/10/open-source-polish-speech-models-for-julius/)
 - Github - repozytorium kodu oraz tablica kanban

## Zakres odpowiedzialności
 - **Joanna Hankus**
 Aplikacja okienkowa
 - **Joanna Partyka**
 Transkrypcja mowy
 - **Jan Godlewski**
 Dokumentacja i poprawki
