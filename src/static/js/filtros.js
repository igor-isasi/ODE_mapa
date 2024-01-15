import { generarMapa, descargarMapa, añadirIndicador, eliminarIndicador, reiniciarIndicadores } from "./main.js";
import * as Fechas from "./fechas.js";

export function cargarOnclickBotones() {
	document.getElementById('botonAñadirIndicador').addEventListener('click', () => mostrarPopupAñadirIndicador());
	document.getElementById('botonEliminarIndicador').addEventListener('click', () => mostrarPopupEliminarIndicador());
	document.getElementById('botonReiniciarIndicadores').addEventListener('click', () => reiniciarIndicadores());
	document.getElementById('reiniciarFiltros').addEventListener('click', () => reiniciarFiltros());
	document.getElementById('generarMapa').addEventListener('click', () => generarMapa());
	document.getElementById('descargarMapa').addEventListener('click', () => descargarMapa());
	document.getElementById('xAñadirIndicador').addEventListener('click', () => ocultarPopupAñadirIndicador());
	document.getElementById('botonSubmitAñadirIndicador').addEventListener('click', () => añadirIndicador());
	document.getElementById('xEliminarIndicador').addEventListener('click', () => ocultarPopupEliminarIndicador());
	document.getElementById('botonSubmitEliminarIndicador').addEventListener('click', () => eliminarIndicador());
}

export function inicializarFiltros() {
	Fechas.setFechaIncidencia();
	Fechas.setFechaMeteo('fechaMeteo');
	Fechas.setFechaMeteo('fechaMeteoUbi');
	//setFechaEventosAdmin();
	// Si se marca un colormap que se desmarquen los demás colormap
	let colormapSeleccionado = false;
	Array.from(document.querySelectorAll('.checkboxColormap')).forEach(function(checkboxColormap) {
		checkboxColormap.addEventListener('change', (event) => {
			if (event.currentTarget.checked) {
				if (colormapSeleccionado) {
					Array.from(document.querySelectorAll('.checkboxColormap')).forEach(function(checkboxColormap2) {
						if (checkboxColormap.id != checkboxColormap2.id) checkboxColormap2.checked = false;
					});
				} else colormapSeleccionado = true;
			} else colormapSeleccionado = false;
		});
	});
	// Si se marca el checkbox de todos los eventos que se desmarquen los demás
	document.getElementById('filtroTodosEv').addEventListener('change', (event) => {
		if (event.currentTarget.checked) {
			Array.from(document.querySelectorAll('[id^="filtroEv"]')).forEach((filtroEv) => filtroEv.checked = false);
		}
	});
	// Si se marca cualquier checkbox de evento menos el de todos que se desmarque el de todos
	Array.from(document.querySelectorAll('[id^="filtroEv"]')).forEach((filtroEv) => {
		filtroEv.addEventListener('change', () => document.getElementById('filtroTodosEv').checked = false);
	});
	document.getElementById('filtroTodosEn').addEventListener('change', (event) => {
		if (event.currentTarget.checked) {
			Array.from(document.querySelectorAll('[id^="filtroEn"]')).forEach((filtroEn) => filtroEn.checked= false);
		}
	});
	Array.from(document.querySelectorAll('[id^="filtroEn"]')).forEach((filtroEn) => {
		filtroEn.addEventListener('change', () => document.getElementById('filtroTodosEn').checked = false);
	})
}

export function habilitarFiltros() {
	Array.from(document.getElementById('filtros').getElementsByTagName('*')).forEach((element) => element.disabled = false);
	Array.from(document.getElementById('popups').getElementsByTagName('*')).forEach((element) => element.disabled = false);
	document.getElementById('loadingDiv').style.display = 'none';
	document.getElementById('filtros').style.visibility = "visible";
	document.getElementById('mapa').style.visibility = "visible";
}

export function bloquearFiltros() {
	ocultarPopupAñadirIndicador();
	ocultarPopupEliminarIndicador();
	Array.from(document.getElementById('filtros').getElementsByTagName('*')).forEach((element) => element.disabled = true);
	Array.from(document.getElementById('popups').getElementsByTagName('*')).forEach((element) => element.disabled = true);
	document.getElementById('mapa').style.visibility = 'hidden';
	document.getElementById('loadingDiv').style.display = 'block';
}

export function reiniciarFiltros() {
	Array.from(document.getElementById('filtros').getElementsByTagName('*')).forEach((element) => element.disabled = false);
	Array.from(document.getElementById('popups').getElementsByTagName('*')).forEach((element) => element.disabled = false);
	Array.from(document.getElementById('filtros').getElementsByTagName('select')).forEach((select) => select.value = select.options[0].value);
	Array.from(document.getElementById('filtros').getElementsByTagName('input')).forEach((input) => {
		if (input.type == "checkbox") input.checked = false;
	});
	document.getElementById('txtUbicacion').value = "";
	ocultarPopupAñadirIndicador();
	ocultarPopupEliminarIndicador();
	Fechas.setFechaIncidencia();
	Fechas.setFechaMeteo('fechaMeteo');
	Fechas.setFechaMeteo('fechaMeteoUbi');
}

export function mostrarPopupAñadirIndicador() {
	ocultarPopupEliminarIndicador()
	document.getElementById('popupAñadirIndicador').style.display = 'block';
}

export function ocultarPopupAñadirIndicador() {
	document.getElementById('popupAñadirIndicador').style.display = 'none';
}


export function mostrarPopupEliminarIndicador() {
	ocultarPopupAñadirIndicador();
	document.getElementById('popupEliminarIndicador').style.display = 'block';
}

export function ocultarPopupEliminarIndicador() {
	document.getElementById('popupEliminarIndicador').style.display = 'none';
}