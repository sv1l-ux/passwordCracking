# passwordCracking

### Ataque de diccionario Offline: 
#### Requerimientos:

- Instalar Python : https://www.python.org/downloads/
- Instalar John The Ripper: https://github.com/openwall/john
Tutorial Windows: https://youtu.be/ytxXrskQorA?si=ZOCpFpf0hDjOk4XW
- Instalar SQLmap: https://github.com/sqlmapproject/sqlmap
- Tener el programa app1.py descargado (de este repositorio)
- Tener el archivo requirements.txt descargado (de este repositorio)
- Descargar wordlist clean_wordlists.txt (de este repositorio)

#### Paso 1:
Crear un folder y poner app1.py, requirements.txt y clean_wordlists.txt en él.

#### Paso 2:
Crear un Virtual Environment (Para Windows):
- Primero abre la consola desde el folder en el que está app1.py
- Corre el siguiente comando: `python3 -m venv .\venv1`
- Activa el VE con el comando: `venv1\Scripts\activate`
- Instala las librerías dentro del virtual environment con el comando: `py -m pip install -r requirements.txt`
- Correr app1.py con el comando: `python app1.py`

> Nota: Una vez que ya hayas acabado el laboratorio, escribe en la consola: deactivate

#### Paso 3:
SQL Injection:

Con SQLmap ya descargado, abre el cmd desde el directorio en el que está instalado y corre el comando:

`python sqlmap.py`

Te debe aparecer el logo de sqlmap.
<img width="1111" height="631" alt="correr sqlmap" src="https://github.com/user-attachments/assets/6056ff19-1837-4f60-895b-a980dc843a61" />

Posteriormente, con la página web activa (o sea con app1.py corriendo), ingresa el siguiente comando a la consola:

`python sqlmap.py -u "http://localhost:5001" --data="username=admin&password=test" --dump -vvv --risk=3 --level=5`

Debes esperar a que termine su proceso (Es demorado). Finalmente, cuando te aparezca la opción de guardar la base de datos en un archivo .csv, dices que sí. y copias solo los hashes de contraseñas que te devolvió y lo pones en un archivo de texto aparte, en este laboratorio llamamos el archivo de texto clean_hashes.txt.

Así se vería la tabla que genera al final:
<img width="1104" height="614" alt="despues de correr sqlmap importante" src="https://github.com/user-attachments/assets/e6a45fd4-8a1f-4a7c-8ed7-bc890ce35c3e" />

> Nota: SQLmap también ofrece la opción de crackear las contraseñas. Pero te invito intentar aprender a hacerlo con john the ripper también.
 <img width="1107" height="622" alt="sqlmap password crack" src="https://github.com/user-attachments/assets/7f6011f7-bdad-48a5-ae0b-4f700a65f8ae" />

#### Paso 4:
John The Ripper:

Debes seguir los pasos del video adjunto para instalar john the ripper (https://youtu.be/ytxXrskQorA?si=ZOCpFpf0hDjOk4XW) si no lo hiciste, la forma de escribir los comandos puede ser diferente. Asegúrate de usar rutas absolutas si los archivos que tienes están en diferentes folders.

Para crackear las contraseñas, corremos el siguiente comando:

`john --wordlist="clean_wordlist.txt" .\clean_hashes.txt --format=Raw-SHA1`

Donde:

`clean_wordlist.txt` es el diccionario que utilizamos.

`.\clean_hashes.txt` es donde guardamos los hashes de las contraseñas que obtuvimos a través de la inyección SQL.

y `--format=Raw-SHA1` indica el algoritmo de hash con el que fueron hasheadas las contraseñas (como atacantes no se conoce qué algoritmo se usó, pero se puede utilizar un hash type identifier).
<img width="571" height="96" alt="hash type identifier" src="https://github.com/user-attachments/assets/5c20348f-9cd1-4e43-ab59-68ccafe91eb7" />

Finalmente, en la consola van a aparecer las contraseñas que se lograron crackear. Puedes probar las credenciales en la página web.
<img width="667" height="209" alt="john the ripper crackeo hecho" src="https://github.com/user-attachments/assets/21e7d6a9-2007-421c-9f87-2fc5f0309d42" />

### Ataque de diccionario Online:
#### Requerimientos:
- Tener descargado VMware o VirtualBox: https://www.virtualbox.org/wiki/Downloads
- Tener la máquina de Metasploitable 2: https://docs.rapid7.com/metasploit/metasploitable-2/
- Tener una máquina de Kali Linux
- Asegurarse que Kali Linux tenga instalado Burpsuite: https://portswigger.net/burp/communitydownload
- Descargar wordlist Rockyou.txt (si es que ya no se tiene descargado, para saber si lo tiene, correr el comando locate rockyou.txt): https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt

#### Paso 1:
Se debe tener ambas máquinas encendidas (Kali Linux y Metasploitable 2).

Desde la consola de Kali Linux, determinar la IP de la máquina de Metasploitable 2 con el comando:

`netdiscover -i eth0`

> (Normalmente la interfaz es eth0, pero puede ser diferente en tu caso, asegúrate que sí es usando ifconfig)

buscar el dispositivo que diga que el vendor es de un servicio de máquinas virtuales (como VMware).

#### Paso 2:
BurpSuite:

Abrir Burpsuite, seguir todos los pasos común y corriente y activar la opción que dice "intercept" de "off" a "on".

En Firefox, irse a settings, buscar proxy y configurar el proxy manualmente. Ponerle la dirección IP 127.0.0.1 y el puerto 8080.

Posteriormente ir a Firefox e ingresar en el buscador la IP de la máquina de metasploitable 2. Dirigirse al enlace que dice dvwa (damn vulnerable web app).

Allí ingresar unas credenciales aleatorias en el login y enviar. Al volver a Burpsuite, va a aparecer una solicitud de POST interceptada, hacer clic.

La última línea de la solicitud HTPP interceptada especifica cuáles son los placeholders que vamos a rellenar para hacer el ataque de diccionario.
<img width="983" height="522" alt="post burpsuite" src="https://github.com/user-attachments/assets/c1422118-012b-4fb1-a441-50804d076dfc" />

Aquí ya podemos dejar de interceptar con BurpSuite.

#### Paso 3:
Hydra:

Primero debemos tener el diccionario rockyou.txt descargado. normalmente ya lo está, para encontrarlo se utiliza:  `locate rockyou.txt`, puede que esté con la extensión gzip, si es así, correr el comando de la imagen:
<img width="573" height="542" alt="rockyougzip" src="https://github.com/user-attachments/assets/7ed5d259-1baf-4ec0-959d-785df59717cf" />

Dentro del mismo directorio que está el rockyou.txt, ejecutamos el siguiente comando:

`hydra -l admin -P rockyou.txt IPmetasploitable2 http-post-form 'dvwa/login.php:username=^USER^&password=^PASS^&Login=Login:Login failed'`

Donde: 

`-l admin` indica que queremos que pruebe todas las combinaciones únicamente con el usuario "admin"

`-P rockyou.txt` indica que queremos determinar si la contraseña es alguna de las entradas de este diccionario.

`http-post-form` lo utilizamos para indicar que el método que se utiliza para la solicitud HTTP es POST (Lo cual lo determinamos al capturar la solicitud con BurpSuite)

`'dvwa/login.php:username=^USER^&password=^PASS^&Login=Login:Login failed'` este tiene varios elementos, primero: dvwa/login.php indica en qué directorio de la página estamos. Lo que sigue después de los primeros ":" es los placeholders que determinamos con BurpSuite, pero en lugar de dejar las credenciales con las que capturamos la primer solicitud, ponemos ^USER^ y ^PASS^ respectivamente. Posteriormente, agregamos Login failed puesto que este es el texto que apareció cuando rechazó el login de prueba.

Finalmente, después de ejecutar este código, en la consola se mostraran los usuarios y respectivas contraseñas que se pudieron crackear.
