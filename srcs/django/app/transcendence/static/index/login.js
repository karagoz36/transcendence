// @ts-check
import { getPage } from "../global/SPA.js"

/** @param {SubmitEvent} e */
async function handleLogin(e) {
	e.preventDefault()
	/** @type {HTMLFormElement} */ // @ts-ignore
	const target = e.target
	/** @type {String} */
	const username = target['username'].value
	/** @type {String} */
	const password = target['password'].value
	/** @type {String} */
	const csrfmiddlewaretoken = target['csrfmiddlewaretoken'].value
	await getPage("/api/login/", {
		method: "POST",
		body: {username, password},
		headers: {"X-CSRFToken": csrfmiddlewaretoken}
	})
}

/** @type {HTMLFormElement|null} */
const form = document.querySelector("#login")
if (form == null)
	throw new Error("querySelector: could not find login form")
form.onsubmit = handleLogin