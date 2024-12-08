import {getPage} from "../global/SPA.js"

/** @type {HTMLButtonElement} */
const button = document.querySelector("#logout")
button.onclick = async () => {
	await getPage("/api/logout")
}