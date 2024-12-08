// @ts-check
import { getPage } from "../global/main.js"

/** @param {SubmitEvent} e */
async function handleLogin(e) {
	e.preventDefault()
	/** @type {HTMLFormElement} */ // @ts-ignore
	const target = e.target
	/** @type {String} */
	const username = target['username'].value
	/** @type {String} */
	const password = target['password'].value
	await getPage("/api/login")
}

/** @type {HTMLFormElement|null} */
const form = document.querySelector("#login")
if (form == null)
	throw new Error("querySelector: could not find login form")
form.onsubmit = handleLogin