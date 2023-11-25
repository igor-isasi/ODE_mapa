export function setFechaIncidencia() {
	const diaActualF = getFechaActual();
	document.getElementById('fechaIncidencia').value = diaActualF;
	document.getElementById('fechaIncidencia').max = diaActualF;
}

export function setFechaMeteo(elementId) {
	const fechaActualF = getFechaActual();
	const fechaMaxF = getFechaMaxMeteo();
	document.getElementById(elementId).value = fechaActualF;
	document.getElementById(elementId).min = fechaActualF;
	document.getElementById(elementId).max = fechaMaxF;
}

/* function setFechaEventosAdmin() {
	const diaActual = new Date();
	const año = diaActual.getFullYear();
	let mes = diaActual.getMonth() + 1;
	let dia = diaActual.getDate();
	if (dia < 10) dia = '0' + dia;
	if (mes < 10) mes = '0' + mes;
	const diaActualF = año + '-' + mes + '-' + dia;

	document.getElementById('fechaEventosAdmin').value = diaActualF;
	document.getElementById('fechaEventosAdmin').max = diaActualF;
} */

export function getFechaActual() {
	const diaActual = new Date();
	const año = diaActual.getFullYear();
	let mes = diaActual.getMonth() + 1;
	let dia = diaActual.getDate();
	if (dia < 10) dia = '0' + dia;
	if (mes < 10) mes = '0' + mes;
	const diaActualF = año + '-' + mes + '-' + dia;
	return diaActualF;
}

export function getFechaEsp(fecha) {
	const año = fecha.split('-')[0];
	const mes = fecha.split('-')[1];
	const dia = fecha.split('-')[2];
	const fechaEsp = dia + '-' + mes + '-' + año;
	return fechaEsp;
}

export function getFechaMaxMeteo() {
	const añoActual = parseInt(getFechaActual().split('-')[0]);
	const mesActual = parseInt(getFechaActual().split('-')[1]);
	const diaActual = parseInt(getFechaActual().split('-')[2]);
	const fechaMax = new Date(añoActual, mesActual-1, diaActual + 5);
	const añoMax = fechaMax.getFullYear();
	let mesMax = fechaMax.getMonth() + 1;
	let diaMax = fechaMax.getDate();
	if (diaMax < 10) diaMax = '0' + diaMax;
	if (mesMax < 10) mesMax = '0' + mesMax;
	const fechaMaxF = añoMax + '-' + mesMax + '-' + diaMax;
	return fechaMaxF;
}