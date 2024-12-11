// @ts-check
import { getPage } from "../global/SPA.js"

/** @param {SubmitEvent} e */
async function handleRegister(e) {
	e.preventDefault()
	/** @type {HTMLFormElement} */ // @ts-ignore
	const target = e.target
	/** @type {String} */
	const username = target['username'].value
	/** @type {String} */
	const password = target['password'].value
	/** @type {String} */
	const csrfmiddlewaretoken = target['csrfmiddlewaretoken'].value
	await getPage("/api/register", {
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
	const form = document.querySelector("#register")
	if (form == null)
		throw new Error("querySelector: could not find register form")
	form.onsubmit = handleRegister
}

main()