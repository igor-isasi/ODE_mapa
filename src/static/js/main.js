import * as Filtros from './filtros.js';
import { autocomplete } from './autocomplete.js';
import { validarParametros } from './validaciones.js';
import { convertirMinuscula } from './autocomplete.js';
let ubicaciones;

function main() {
	cargarIndicadores_generarMapa();
	cargarIndicadoresExtra();
	cargarUbicaciones();
	Filtros.cargarOnclickBotones();
}

function cargarIndicadores_generarMapa() {
	// Cargar los años de los indicadores desde un web service
	fetch('/wsañosind')
	.then(response => {
		let contentType = response.headers.get("content-type");
		if (contentType == "application/json") return response.json();
		else return response.text();
	})
	.then(añosInd => {
		if (añosInd == "ApiError") {
			alert("Ha ocurrido un error al intentar conectar con la API de indicadores de Open Data Euskadi.\nNo es posible cargar la página.");
			let html = "<h1>No se ha podido cargar la página</h1>";
    		document.getElementsByTagName('body')[0].innerHTML = html; 
		} else {
			// Cargar los indicadores desde el fichero indicators.json
			fetch('/indicators.json')
			.then(response => response.json())
			.then(indicators => {
				let hayIndEconomia = false;
				let hayIndCohesion = false;
				let hayIndMedioambiente = false;
				let htmlIndEconomia = "<label class='grupoInd'>ECONOMÍA</label><label class='mostrarColormap'><input type='checkbox' class='checkboxColormap' id='colormapIndEconomia'>Mostrar colormap</label><br><div class='bloqueInd'>";
				let htmlIndCohesion = "<label class='grupoInd'>COHESIÓN SOCIAL / CALIDAD DE VIDA</label><label class='mostrarColormap'><input type='checkbox' class='checkboxColormap' id='colormapIndCohesion'>Mostrar colormap</label><br><div class='bloqueInd'>";
				let htmlIndMedioambiente = "<label class='grupoInd'>MEDIOAMBIENTE Y MOVILIDAD</label><label class='mostrarColormap'><input type='checkbox' class='checkboxColormap' id='colormapIndMedioambiente'>Mostrar colormap</label><br><div class='bloqueInd'>";
				let htmlIndicadoresEliminar = "<select class='selectIndEliminar' id='selectIndEliminar'>";
				let ind_keys = [];
				for (let key in indicators) {
					let htmlAñosInd = "";
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
				} else document.getElementById("indEconomia").innerHTML = "";
				if (hayIndCohesion) {
					htmlIndCohesion = htmlIndCohesion + "</div>";
					document.getElementById("indCohesionSocial").innerHTML = htmlIndCohesion;
				} else document.getElementById("indCohesionSocial").innerHTML = "";
				if (hayIndMedioambiente) {
					htmlIndMedioambiente = htmlIndMedioambiente + "</div>";
					document.getElementById("indMedioambiente").innerHTML = htmlIndMedioambiente;
				} else document.getElementById("indMedioambiente").innerHTML = "";
				htmlIndicadoresEliminar = htmlIndicadoresEliminar + "</select>";
				document.getElementById("indicadoresEliminar").innerHTML = htmlIndicadoresEliminar;
				Filtros.inicializarFiltros();
				const pageAccessedByReload = (
					(window.performance.navigation && window.performance.navigation.type === 1) ||
					window.performance
					.getEntriesByType('navigation')
					.map((nav) => nav.type)
					.includes('reload')
				);
				if (pageAccessedByReload == true) Filtros.reiniciarFiltros();
				generarMapa();
			})
		}
	});
}

export function generarMapa() {
	let filtros = {};
	let añosInd = {};
	let fechaIncidencia = document.getElementById('fechaIncidencia').value;;
	let fechaMeteo = document.getElementById('fechaMeteo').value;
	let fechaMeteoUbi = document.getElementById('fechaMeteoUbi').value;
	let ubiMeteo = document.getElementById('txtUbicacion').value;
	if (validarParametros(fechaIncidencia, fechaMeteo, fechaMeteoUbi, ubiMeteo, ubicaciones)) {
		Filtros.bloquearFiltros();
		Filtros.bloquearMapa();
		filtros['colormapIndEconomia'] = false;
		filtros['colormapIndCohesion'] = false;
		filtros['colormapIndMedioambiente'] = false;
		Array.from(document.getElementById('filtros').getElementsByTagName('input')).forEach((input) => {
			if (input.type == "checkbox") filtros[input.id] = input.checked;
		});
		Array.from(document.getElementById('filtros').getElementsByTagName('select')).forEach((select) => añosInd[select.id] = select.value);
		fetch('/', {
			headers: {
				"Content-Type": "application/x-www-form-urlencoded"
			},
			method: "POST",
			body: "tipoRequest=mapa" + "&filtros=" + JSON.stringify(filtros) + "&añosInd=" + JSON.stringify(añosInd) + 
				"&fechaIncidencia=" + fechaIncidencia + "&fechaMeteo=" + fechaMeteo + "&fechaMeteoUbi=" + fechaMeteoUbi + 
				"&ubiMeteo=" + convertirMinuscula(ubiMeteo)
		}).then(response => {
			let contentType = response.headers.get("content-type");
			if (contentType == "application/json") return response.json();
			else return response.text();
		}).then(res => {
			const promiseMapa = new Promise((resolve) => {
				fetch('/mapa.html').then(res => res.text()
				).then(html => {
					document.getElementById('mapaIframe').addEventListener("load", () => {
						resolve("Mapa cargado correctamente");
					});
					document.getElementById('mapaIframe').srcdoc = html;
				});
			});
			if (res == "mapa cargado") {
				promiseMapa.then((resolveMessage) => {
					Filtros.habilitarFiltros();
					Filtros.habilitarMapa();
				});
			} else if (res.length > 0 && res.length <= 5) {
				promiseMapa.then((resolveMessage) => {
					Filtros.habilitarFiltros();
					Filtros.habilitarMapa();
				});
				let strErrores = "";
				let errorIndicadores = false;
				let errorMeteo = false;
				let erroresApi = []
				for (let error of res) {
					if (error == "API de indicadores municipales") errorIndicadores = true;
					if (error == "API de Euskalmet") errorMeteo = true;
					if (error == "No se han podido obtener las coordenadas de alguna(s) ubicación(es) seleccionada(s) para las predicciones meteorológicas.") {
						alert(error);
					} else if (error == "Ha ocurrido un error al traducir las coordenadas de alguna(s) entidad(es).") {
						alert(error);
					} else { 
						erroresApi.push(error);
						strErrores = strErrores + error + ", ";
					}
				}
				strErrores = strErrores.split(',').slice(0, -1) + ".";
				if (errorIndicadores) {
					alert("Ha ocurrido un error al intentar conectar con la API de indicadores de Open Data Euskadi." + 
					"\nNo es posible cargar la página.");
					let html = "<h1>No se ha podido cargar la página</h1>";
					document.getElementsByTagName('body')[0].innerHTML = html;
				} else if (erroresApi.length >= 2) {
					let mensaje = "Ha ocurrido un error al solicitar información de las siguientes APIs: " + strErrores + 
					"\nEs posible que la información relacionada con estas APIs no se muestre en el mapa.";
					alert(mensaje);
				} else if (erroresApi.length > 0) {
					if (errorMeteo) {
						let mensaje = "Ha ocurrido un error al solicitar información de la API de Euskalmet." +  
						" Probablemente el error se debe a que todavía no está disponible la predicción para la fecha solicitada." + 
						"\nEs posible que la información relacionada con esta API no se muestre en el mapa.";
						alert(mensaje);
					} else {
						let mensaje = "Ha ocurrido un error al solicitar información de la siguiente API: " + strErrores + 
						"\nEs posible que la información relacionada con esta API no se muestre en el mapa.";
						alert(mensaje);
					}
				}
			} else {
				alert("Ha ocurrido un error al cargar el mapa.");
				location.reload();
			}
		});
	}
}

function cargarIndicadoresExtra() {
	// Cargar los indicadores extra desde el fichero extraIndicators.json
	fetch('/extraindicators.json')
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

export function añadirIndicador() {
	let indicator = document.getElementById('selectIndExtra').value;
	if (indicator != "") {
		Filtros.reiniciarFiltros();
		Filtros.bloquearFiltros();
		Filtros.bloquearMapa();
		let postData = {ind: indicator, tipoRequest: 'añadirIndicador'};
		fetch('/wsañadirindicador', {
			headers: {
				"Content-Type": "application/json"
			},
			method: "POST",
			body: JSON.stringify(postData)
		}).then(res => res.text())
		.then(text => {
			if (text == "Indicador añadido") {
				document.getElementById("filtros").style.visibility = "hidden";
				cargarIndicadoresExtra();
				cargarIndicadores_generarMapa();
			} else {
				alert("Ha ocurrido un error con la conexión a la API de indicadores. No se ha podido añadir el nuevo indicador.")
				location.reload();
			}
			
		});
	} else {
		alert('No se ha seleccionado ningún indicador.')
	}
}

export function eliminarIndicador() {
	let indicator = document.getElementById('selectIndEliminar').value;
	if (indicator != "") {
		Filtros.reiniciarFiltros();
		Filtros.bloquearFiltros();
		Filtros.bloquearMapa();
		let postData = {ind: indicator, tipoRequest: 'eliminarIndicador'};
		fetch('/wseliminarIndicador', {
			headers: {
				"Content-Type": "application/json"
			},
			method: "POST",
			body: JSON.stringify(postData)
		}).then(res => res.text())
		.then((text) => {
			if (text == "Indicador eliminado") {
				document.getElementById("filtros").style.visibility = "hidden";
				cargarIndicadoresExtra();
				cargarIndicadores_generarMapa();
			} else {
				alert('Ha sucedido un error al intentar eliminar el indicador.');
				location.reload();
			}

		});
	} else {
		alert('No se ha seleccionado ningún indicador.')
	}
}

export function reiniciarIndicadores() {
	Filtros.bloquearFiltros();
	Filtros.bloquearMapa();
	fetch('/wsreiniciarindicadores')
	.then(response => response.text())
	.then(text => {
		if (text == "Indicadores reiniciados") {
			document.getElementById("filtros").style.visibility = "hidden";
			cargarIndicadores_generarMapa();
			cargarIndicadoresExtra();
		} else {
			alert('Ha sucedido un error al intentar reiniciar los indicadores.');
			location.reload();
		}
	});
}

export function descargarMapa() {
	const aElement = document.createElement('a');
	aElement.setAttribute('download', 'ODE_mapa');
	let mapa = document.getElementById('mapaIframe').srcdoc;
	var mapaBlob = new Blob([mapa], {type: "text/plain"});
	const href = URL.createObjectURL(mapaBlob);
	aElement.href = href;
	aElement.setAttribute('target', '_blank');
	aElement.click();
	URL.revokeObjectURL(href);
}

function cargarUbicaciones() {
	fetch('/ubimeteotodas.json')
	.then(response => response.json())
	.then(jsonLocations => {
		ubicaciones = Object.keys(jsonLocations);
		autocomplete(document.getElementById('txtUbicacion'), ubicaciones);
	});
}

main();