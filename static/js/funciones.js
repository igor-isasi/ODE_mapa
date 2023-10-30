// Inicializar variables generales
let numIndicadores;
let ind_keys;
let colormapSeleccionado = false;
let hayIndEconomia = false;
let hayIndCohesion = false;
let hayIndMedioambiente = false;

const numTrafico = 2;
const numEventos = 15;
const numEntidades = 2;
const pageAccessedByReload = (
	(window.performance.navigation && window.performance.navigation.type === 1) ||
	window.performance
	.getEntriesByType('navigation')
	.map((nav) => nav.type)
	.includes('reload')
);

function inicializarFiltros() {
	setFechaIncidencia();
	// Si se marca un colormap que se desmarquen los demás colormap
	[...document.querySelectorAll('.checkboxColormap')].forEach(function(checkboxColormap) {
		checkboxColormap.addEventListener('change', (event) => {
			if (event.currentTarget.checked) {
				if (colormapSeleccionado) {
					[...document.querySelectorAll('.checkboxColormap')].forEach(function(checkboxColormap2) {
						if (checkboxColormap.id != checkboxColormap2.id) {
							checkboxColormap2.checked = false;
						}
					});
				} else {
					colormapSeleccionado = true;
				}
			} else {
				colormapSeleccionado = false;
			}
		});
	});
	// Si se marca el checkbox de todos los eventos que se desmarquen los demás
	document.getElementById('filtroEv1').addEventListener('change', (event) => {
		if (event.currentTarget.checked) {
			for (i = 2; i <= numEventos; i++) {
				document.getElementById('filtroEv' + i).checked = false;
			}
		}
	});
	// Si se marca cualquier checkbox de evento menos el de todos que se desmarque el de todos
	for (i = 2; i <= numEventos; i++) {
		document.getElementById('filtroEv' + i).addEventListener('change', () => {
			document.getElementById('filtroEv1').checked = false;
		});
	}
	document.getElementById('filtroEn1').addEventListener('change', (event) => {
		if (event.currentTarget.checked) {
			for (i = 2; i <= numEntidades; i++) {
				document.getElementById('filtroEn' + i).checked = false;
			}
		}
	});
	for (i = 2; i <= numEntidades; i++) {
		document.getElementById('filtroEn' + i).addEventListener('change', () => {
			document.getElementById('filtroEn1').checked = false;
		});
	}
}

function habilitarFiltros() {
	for (let i = 0; i < ind_keys.length; i ++) {
		document.getElementById('filtroInd' + ind_keys[i].toString()).disabled = false;
		document.getElementById('añoFiltroInd' + ind_keys[i].toString()).disabled = false;
		document.getElementById('colormapInd' + ind_keys[i].toString()).disabled = false;
	}
	for (let indTraf = 1; indTraf <= numTrafico; indTraf++) {
		document.getElementById('filtroTraf' + indTraf.toString()).disabled = false;
	}
	for (let indEv = 1; indEv <= numEventos; indEv++) {
		document.getElementById('filtroEv' + indEv.toString()).disabled = false;
	}
	for (let indEn = 1; indEn <= numEntidades; indEn++) {
		document.getElementById('filtroEn' + indEn.toString()).disabled = false;
	}
	document.getElementById('loadingDiv').style.display = 'none';
	document.getElementById('fechaIncidencia').disabled = false;
	document.getElementById('filtros').style.visibility = "visible";
	document.getElementById('mapa').style.visibility = "visible";
	if (hayIndEconomia) {
		document.getElementById('colormapIndEconomia').disabled = false;
	}
	if (hayIndCohesion) {
		document.getElementById('colormapIndCohesion').disabled = false;
	}
	if (hayIndMedioambiente) {
		document.getElementById('colormapIndMedioambiente').disabled = false;
	}
	document.getElementById('generarMapa').disabled = false;
	document.getElementById('descargarMapa').disabled = false;
	document.getElementById('botonAñadirIndicador').disabled = false;
	document.getElementById('botonEliminarIndicador').disabled = false;
	document.getElementById("botonSubmitAñadirIndicador").disabled = false;
	document.getElementById("botonSubmitEliminarIndicador").disabled = false;
	document.getElementById("selectIndExtra").disabled = false;
	document.getElementById("selectIndEliminar").disabled = false;
}

function bloquearFiltros() {
	for (let i = 0; i < ind_keys.length; i++) {
		document.getElementById('filtroInd' + ind_keys[i].toString()).disabled = true;
		document.getElementById('añoFiltroInd' + ind_keys[i].toString()).disabled = true;
		document.getElementById('colormapInd' + ind_keys[i].toString()).disabled = true;
	}
	for (let indTraf = 1; indTraf <= numTrafico; indTraf++) {
		document.getElementById('filtroTraf' + indTraf.toString()).disabled = true;
		document.getElementById('fechaIncidencia').disabled = true;
	}
	for (let indEv = 1; indEv <= numEventos; indEv++) {
		document.getElementById('filtroEv' + indEv.toString()).disabled = true;
	}
	for (let indEn = 1; indEn <= numEntidades; indEn++) {
		document.getElementById('filtroEn' + indEn.toString()).disabled = true;
	}
	if (hayIndEconomia) {
		document.getElementById('colormapIndEconomia').disabled = true;
	}
	if (hayIndCohesion) {
		document.getElementById('colormapIndCohesion').disabled = true;
	}
	if (hayIndMedioambiente) {
		document.getElementById('colormapIndMedioambiente').disabled = true;
	}
	ocultarPopupAñadirIndicador();
	ocultarPopupEliminarIndicador();
	document.getElementById('mapa').style.visibility = "hidden";
	document.getElementById('loadingDiv').style.display = 'block';
	document.getElementById('generarMapa').disabled = true;
	document.getElementById('descargarMapa').disabled = true;
	document.getElementById('botonAñadirIndicador').disabled = true;
	document.getElementById('botonEliminarIndicador').disabled = true;
}

function cargarIndicadores_generarMapa() {
	// Cargar los años de los indicadores desde un web service que saca la info de la base de datos
	fetch('../webServiceAñosInd')
	.then(response => {
		let contentType = response.headers.get("content-type");
		if (contentType == "application/json") {
			return response.json();
		} else {
			return response.text();
		}
	})
	.then(añosInd => {
		if (añosInd == "ApiError") {
			alert("Ha ocurrido un error al intentar conectar con la API de indicadores de Open Data Euskadi.\nNo es posible cargar la página.");
			var html = "<h1>No se ha podido cargar la página</h1>";
    		document.getElementsByTagName('body')[0].innerHTML = html; 
		} else {
			// Cargar los indicadores desde el fichero indicators.json
			fetch('../indicators.json')
			.then(response => response.json())
			.then(indicators => {
				hayIndEconomia = false;
				hayIndCohesion = false;
				hayIndMedioambiente = false;
				let htmlIndEconomia = "<label class='grupoInd'>ECONOMÍA</label><label class='mostrarColormap'><input type='checkbox' class='checkboxColormap' id='colormapIndEconomia'>Mostrar colormap</label><br><div class='bloqueInd'>";
				let htmlIndCohesion = "<label class='grupoInd'>COHESIÓN SOCIAL / CALIDAD DE VIDA</label><label class='mostrarColormap'><input type='checkbox' class='checkboxColormap' id='colormapIndCohesion'>Mostrar colormap</label><br><div class='bloqueInd'>";
				let htmlIndMedioambiente = "<label class='grupoInd'>MEDIOAMBIENTE Y MOVILIDAD</label><label class='mostrarColormap'><input type='checkbox' class='checkboxColormap' id='colormapIndMedioambiente'>Mostrar colormap</label><br><div class='bloqueInd'>";
				let htmlIndicadoresEliminar = "<select class='selectIndEliminar' id='selectIndEliminar'>";
				ind_keys = [];
				for (let key in indicators) {
					let htmlAñosInd = "";
					numIndicadores = numIndicadores + 1;
					ind_keys.push(key);
					añosInd[key].reverse();
					for (let año of añosInd[key]){
						htmlAñosInd = htmlAñosInd + "<option value=" + año + ">" + año + "</option>";
					}
					let htmlIndicador = "<div class='elementoFiltro'><label><input type='checkbox' id='filtroInd" + key + "'>" + indicators[key][1] + "</label>" + 
						"<select class='añoFiltro' id='añoFiltroInd" + key + "'>" + htmlAñosInd + "</select>" + 
						"<label class='mostrarColormap'><input type='checkbox' class='checkboxColormap' id='colormapInd" + key + "'>Mostrar colormap</label><br></div>";
					if (indicators[key][0] == "Economía / Competitividad") {
						hayIndEconomia = true;
						htmlIndEconomia = htmlIndEconomia + htmlIndicador;
					} else if(indicators[key][0] == "Cohesión social / Calidad de vida") {
						hayIndCohesion = true;
						htmlIndCohesion = htmlIndCohesion + htmlIndicador;
					} else if(indicators[key][0] == "Medioambiente y Movilidad") {
						hayIndMedioambiente = true;
						htmlIndMedioambiente = htmlIndMedioambiente + htmlIndicador;
					}
					htmlIndicadoresEliminar = htmlIndicadoresEliminar + "<option value='" + key + ":" + indicators[key][0] + ":" + indicators[key][1] + ":" + indicators[key][2] + "'>" + key + ": " + indicators[key][1] + "</option>";
				}
				if (hayIndEconomia) {
					htmlIndEconomia = htmlIndEconomia + "</div>";
					document.getElementById("indEconomia").innerHTML = htmlIndEconomia;
				} else {
					document.getElementById("indEconomia").innerHTML = "";
				}
				if (hayIndCohesion) {
					htmlIndCohesion = htmlIndCohesion + "</div>";
					document.getElementById("indCohesionSocial").innerHTML = htmlIndCohesion;
				} else {
					document.getElementById("indCohesionSocial").innerHTML = "";
				}
				if (hayIndMedioambiente) {
					htmlIndMedioambiente = htmlIndMedioambiente + "</div>";
					document.getElementById("indMedioambiente").innerHTML = htmlIndMedioambiente;
				} else {
					document.getElementById("indMedioambiente").innerHTML = "";
				}
				htmlIndicadoresEliminar = htmlIndicadoresEliminar + "</select>";
				document.getElementById("indicadoresEliminar").innerHTML = htmlIndicadoresEliminar;
				inicializarFiltros();
				if (pageAccessedByReload == true) {
					reiniciarFiltros();
				}
				generarMapa();
			})
		}
	});
}

function generarMapa() {
	let filtros = {};
	let añosInd = {};
	let colormap = {};
	let fechaIncidencia;
	bloquearFiltros();
	//Indicadores, años y colormap
	for (let i = 0; i < ind_keys.length; i++) {
		filtros['filtroInd' + ind_keys[i].toString()] = document.getElementById('filtroInd' + ind_keys[i].toString()).checked;
		añosInd['filtroInd' + ind_keys[i].toString()] = document.getElementById('añoFiltroInd' + ind_keys[i].toString()).value;
		colormap['colormapInd' + ind_keys[i].toString()] = document.getElementById('colormapInd' + ind_keys[i].toString()).checked;
	}
	colormap['colormapIndEconomia'] = false;
	colormap['colormapIndCohesion'] = false;
	colormap['colormapIndMedioambiente'] = false;
	if (hayIndEconomia) {
		colormap['colormapIndEconomia'] = document.getElementById('colormapIndEconomia').checked;
	}
	if (hayIndCohesion) {
		colormap['colormapIndCohesion'] = document.getElementById('colormapIndCohesion').checked;
	}
	if (hayIndMedioambiente) {
		colormap['colormapIndMedioambiente'] = document.getElementById('colormapIndMedioambiente').checked;
	}
	//Trafico
	for (let indTraf = 1; indTraf <= numTrafico; indTraf++) {
		filtros['filtroTraf' + indTraf.toString()] = document.getElementById('filtroTraf' + indTraf.toString()).checked;
		fechaIncidencia = document.getElementById('fechaIncidencia').value;
	}
	//Eventos
	for (let indEv = 1; indEv <= numEventos; indEv++) {
		filtros['filtroEv' + indEv.toString()] = document.getElementById('filtroEv' + indEv.toString()).checked;
		document.getElementById('filtroEv' + indEv.toString()).disabled = true;
	}
	//Entidades
	for (let indEn = 1; indEn <= numEntidades; indEn++) {
		filtros['filtroEn' + indEn.toString()] = document.getElementById('filtroEn' + indEn.toString()).checked;
		document.getElementById('filtroEn' + indEn.toString()).disabled = true;
	}
	fetch('/', {
		headers: {
			"Content-Type": "application/x-www-form-urlencoded"
		},
		method: "POST",
		body: "tipoRequest=mapa" + "&filtros=" + JSON.stringify(filtros) + "&añosInd=" + JSON.stringify(añosInd) + "&colormap=" + JSON.stringify(colormap) + "&fechaIncidencia=" + fechaIncidencia
	}).then(response => {
		let contentType = response.headers.get("content-type");
		if (contentType == "application/json") {
			return response.json();
		} else {
			return response.text();
		}
	}).then(res => {
		const promiseMapa = new Promise((resolve) => {
			document.getElementById('mapa').innerHTML = '<iframe src="mapa.html/" height="99%" width="99%"></iframe>';
			setTimeout(() => resolve("Mapa cargado correctamente"), 4500)
		});
		if (res == "mapa cargado") {
			promiseMapa.then((resolveMessage) => {
				habilitarFiltros();
			});
		} else {
			promiseMapa.then((resolveMessage) => {
				habilitarFiltros();
			});
			let strErrores = "";
			let errorIndicadores = false;
			for (error of res) {
				if (error == "API de indicadores municipales") {
					errorIndicadores = true;
				}
				strErrores = strErrores + error + ", ";
			}
			strErrores = strErrores.split(',').slice(0, -1) + ".";
			if (errorIndicadores == true) {
				alert("Ha ocurrido un error al intentar conectar con la API de indicadores de Open Data Euskadi.\nNo es posible cargar la página.");
				var html = "<h1>No se ha podido cargar la página</h1>";
				document.getElementsByTagName('body')[0].innerHTML = html;
			}
			else if (res.length >= 2) {
				let mensaje = "Ha ocurrido un error al solicitar información de las siguientes APIs: " + strErrores + 
				"\nEs posible que la información relacionada con estas APIs no se muestre en el mapa.";
				alert(mensaje);
			} else if (res.length > 0) {
				let mensaje = "Ha ocurrido un error al solicitar información de la siguiente API: " + strErrores + 
				"\nEs posible que la información relacionada con esta API no se muestre en el mapa.";
				alert(mensaje);
			}
		}
	});
}

function reiniciarFiltros() {
	for (let i = 0; i < ind_keys.length; i ++) {
		document.getElementById('filtroInd' + ind_keys[i].toString()).checked = false;
	}
	for (let indTraf = 1; indTraf <= numTrafico; indTraf++) {
		document.getElementById('filtroTraf' + indTraf.toString()).checked = false;
	}
	for (let indEv = 1; indEv <= numEventos; indEv++) {
		document.getElementById('filtroEv' + indEv.toString()).checked = false;
	}
	for (let indEn = 1; indEn <= numEntidades; indEn++) {
		document.getElementById('filtroEn' + indEn.toString()).checked = false;
	}
	ocultarPopupAñadirIndicador();
	ocultarPopupEliminarIndicador();
}

function setFechaIncidencia() {
	const diaActual = new Date();
	const año = diaActual.getFullYear();
	let mes = diaActual.getMonth() + 1;
	let dia = diaActual.getDate();
	if (dia < 10) dia = '0' + dia;
	if (mes < 10) mes = '0' + mes;
	const diaActualF = año + '-' + mes + '-' + dia;

	document.getElementById('fechaIncidencia').value = diaActualF;
	document.getElementById('fechaIncidencia').max = diaActualF;
}

function mostrarPopupAñadirIndicador() {
	ocultarPopupEliminarIndicador()
	document.getElementById('popupAñadirIndicador').style.display = 'block';
}

function ocultarPopupAñadirIndicador() {
	document.getElementById('popupAñadirIndicador').style.display = 'none';
}

function cargarIndicadoresExtra() {
	// Cargar los indicadores extra desde el fichero extraIndicators.json
	fetch('../extraIndicators.json')
	.then(response => response.json())
	.then(indicators => {
		let htmlIndExtra = "<select class='selectIndExtra' id='selectIndExtra'>";
		for (let key in indicators) {
			htmlIndExtra = htmlIndExtra + "<option value='" + key + ":" + indicators[key][0] + ":" + indicators[key][1] + ":" + indicators[key][2] + "'>" + key + ": " + indicators[key][1] + "</option>";
		}
		htmlIndExtra = htmlIndExtra + "</select>";
		document.getElementById("indicadoresExtra").innerHTML = htmlIndExtra;
	});
}

function añadirIndicador() {
	document.getElementById("botonSubmitAñadirIndicador").disabled = true;
	document.getElementById("selectIndExtra").disabled = true;
	bloquearFiltros();
	let indicator = document.getElementById('selectIndExtra').value;
	if (indicator != "") {
		let postData = {ind: indicator, tipoRequest: 'añadirIndicador'};
		fetch('/webServiceAñadirIndicador', {
			headers: {
				"Content-Type": "application/json"
			},
			method: "POST",
			body: JSON.stringify(postData)
		}).then(res => res.text())
		.then(text => {
			if (text == "Indicador añadido") {
				document.getElementById("filtros").style.visibility = "hidden";
				reiniciarFiltros();
				cargarIndicadoresExtra();
				cargarIndicadores_generarMapa();
			} else {
				alert("Ha ocurrido un error con la conexión a la API de indicadores. No se ha podido añadir el nuevo indicador.")
				location.reload();
			}
			
		});
	}
}

function mostrarPopupEliminarIndicador() {
	ocultarPopupAñadirIndicador();
	document.getElementById('popupEliminarIndicador').style.display = 'block';
}

function ocultarPopupEliminarIndicador() {
	document.getElementById('popupEliminarIndicador').style.display = 'none';
}

function eliminarIndicador() {
	document.getElementById("botonSubmitEliminarIndicador").disabled = true;
	document.getElementById("selectIndEliminar").disabled = true;
	bloquearFiltros();
	let indicator = document.getElementById('selectIndEliminar').value;
	if (indicator != "") {
		let postData = {ind: indicator, tipoRequest: 'eliminarIndicador'};
		fetch('/webServiceEliminarIndicador', {
			headers: {
				"Content-Type": "application/json"
			},
			method: "POST",
			body: JSON.stringify(postData)
		}).then(res => res.text())
		.then(() => {
			document.getElementById("filtros").style.visibility = "hidden";
			reiniciarFiltros();
			cargarIndicadoresExtra();
			cargarIndicadores_generarMapa();
		});
	}
}

function descargarMapa() {
	fetch('mapa.html', { method: 'get', mode: 'no-cors', referrerPolicy: 'no-referrer' })
	  .then(res => res.blob())
	  .then(res => {
		const aElement = document.createElement('a');
		aElement.setAttribute('download', 'ODE_mapa');
		const href = URL.createObjectURL(res);
		aElement.href = href;
		aElement.setAttribute('target', '_blank');
		aElement.click();
		URL.revokeObjectURL(href);
	  });
  };