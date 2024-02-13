<h1>Despliegue de la aplicación en Linux</h1>
<h3>Para desplegar la aplicación de forma local en Linux es necesario tener instalado Docker (https://docs.docker.com/desktop/install/linux-install/).</h3>

Los pasos para desplegar la aplicación de forma local son los siguientes:
<ol>
  <li>Descargar el código.</li>
  <li>Situarse en el directorio raíz de la aplicación (ODE_mapa).</li>
  <li>Introducir el siguiente comando: <strong>docker compose up</strong>. Si el usuario no tiene los permisos necesarios será necesario utilizar el comando como administrador: <strong>sudo docker compose up</strong>.</li>
  <li>Una vez se haya desplegado la aplicación correctamente esta estará disponible en la URL <strong>http://localhost/</strong>. Si la máquina en la que se despliega la aplicación tiene una IP pública y el puerto 80 abierto, la aplicación será accesible desde el exterior mediante su dirección IP (http://{dirección_IP}/).</li>
</ol>

<h3><strong>Importante!</strong> Para poder utilizar los filtros de meteorología hay que seguir los siguientes pasos:</h3>
<ol>
  <li>Crear una cuenta en el siguiente enlace: https://api.euskadi.eus/met01uiLoginWar/?to=https://api.euskadi.eus/met01uiApiKeyUsersWar/index.jsp#/.</li>
  <li>Solicitar una API-KEY.</li>
  <li>Descargar el zip con las claves y descomprimir la carpeta.</li>
  <li>Sustituir los ficheros <strong>privateKey.pem</strong> y <strong>fingerPrint.txt</strong> de la carpeta EuskalmetAPI por los ficheros con mismo nombre descargados en el paso anterior.</li>
</ol>
