import { getFechaActual, getFechaEsp, getFechaMaxMeteo } from './fechas.js';
import { convertirMayuscula } from './autocomplete.js';

export function validarParametros(fechaIncidencia, fechaMeteo, fechaMeteoUbi, ubiMeteo, ubicaciones) {
	let validacionFechaInc = validarFechaInc(fechaIncidencia);
	let validacionFechaMet = validarFechaMeteo(fechaMeteo);
	let validacionFechaMetUbi = validarFechaMeteoUbi(fechaMeteoUbi);
	let validacionUbi = validarUbicacion(ubiMeteo, ubicaciones);
	if (validacionFechaInc[0] && validacionFechaMet[0] && validacionFechaMetUbi[0] && validacionUbi[0]) {
		return true
	} else {
		let mensaje = "Los parámetros indicados no son correctos. Por favor, revíselos.\n" + 
			validacionFechaInc[1] + validacionFechaMet[1] + validacionFechaMetUbi[1] + validacionUbi[1];
		alert(mensaje);
		return false
	}
}

function validarFechaInc(fecha) {
	let mensaje = '';
	let validado = true;
	if (document.getElementById('filtroTrafIncidencias').checked) {
		if (!fecha || Date.parse(fecha) > Date.parse(getFechaActual())) {
			validado = false;
			mensaje = "\n - La fecha de la incidencia debe ser menor o igual que la fecha " + getFechaEsp(getFechaActual()) + ".";
		}
	}
	return [validado, mensaje];
}

function validarFechaMeteo(fecha) {
	let mensaje = '';
	let validado = true;
	if (document.getElementById('filtroMetPred').checked) {
		if (!fecha || Date.parse(fecha) < Date.parse(getFechaActual()) || Date.parse(fecha) > Date.parse(getFechaMaxMeteo())) {
			validado = false;
			mensaje = "\n - La fecha de la predicción metereológica debe ser mayor o igual que la fecha " + 
				getFechaEsp(getFechaActual()) + " y menor o igual que la fecha " + getFechaEsp(getFechaMaxMeteo()) + ".";
		}
	}
	return [validado, mensaje];
}

function validarFechaMeteoUbi(fecha) {
	let mensaje = '';
	let validado = true;
	if (document.getElementById('filtroMetPredUbi').checked) {
		if (!fecha || Date.parse(fecha) > Date.parse(getFechaMaxMeteo()) || Date.parse(fecha) < Date.parse(getFechaActual())) {
			validado = false;
			mensaje = "\n - La fecha de la predicción metereológica por ubicación debe ser mayor o igual que la fecha " +
				getFechaEsp(getFechaActual()) + " y menor o igual que la fecha " + getFechaEsp(getFechaMaxMeteo()) + ".";
		}
	}
	return [validado, mensaje];
}

function validarUbicacion(ubicacion, ubicaciones) {
	let mensaje = '';
	let validado = true;
	let encontrado = false;
	if (document.getElementById('filtroMetPredUbi').checked) {
		if (ubicacion.length <= 0) {
			validado = false;
			mensaje = "\n - El campo de la ubicación de la predicción metereológica esta vacío.";
		}
		else {
			for (let ubi of ubicaciones) {
				if ((ubicacion == ubi) || (ubicacion == convertirMayuscula(ubi))) {
					encontrado = true;
					break;
				}
			}
			if (!encontrado) {
				validado = false;
				mensaje = "\n - La ubicación introducida no existe o no se encuentra disponible.";
			}
		}
	}
	return [validado, mensaje];
}