// @ts-check
import { getPage } from "../global/SPA.js"

/** @param {SubmitEvent} e */
async function handleLogin(e) {
	e.preventDefault()
	if (!e.target)
		throw new Error("handleLogin: e.target null")
	/** @type {String} */
	const username = e.target['username'].value
	/** @type {String} */
	const password = e.target['password'].value
	/** @type {String} */
	const csrfmiddlewaretoken = e.target['csrfmiddlewaretoken'].value
	await getPage("/api/login", {
		method: "POST",
		body: {username, password},
		headers: {
			"X-CSRFToken": csrfmiddlewaretoken,
			"content-type": "application/json",
		}
	})
}

function main() {
	/** @type {HTMLFormElement|null} */
	const form = document.querySelector("#login")
	if (form == null)
		throw new Error("querySelector: could not find login form")
	form.onsubmit = handleLogin
}

main()