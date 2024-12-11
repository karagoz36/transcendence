// @ts-check
import {getPage} from "../global/SPA.js"

async function submitForm(e) {
	const csrfmiddlewaretoken = e.target['csrfmiddlewaretoken'].value
}

/** @param {SubmitEvent} e */
async function addFriend(e) {
	e.preventDefault()
	if (!e.target)
		throw new Error("addFriend: e.target null")
	/** @type {string} */
	const csrfmiddlewaretoken = e.target['csrfmiddlewaretoken'].value
	/** @type {string} */
	const username = e.target['username'].value
	await getPage("/api/add-friend", {
		method: "POST",
		body: {username},
		headers: {
			"X-CSRFToken": csrfmiddlewaretoken,
			"content-type": "application/json",
		}
	})
}

function fillUsernameField() {
	const urlParams = new URLSearchParams(window.location.search)
	const username = urlParams.get("username")
	if (!username) return
	/** @type {HTMLInputElement} */ // @ts-ignore
	const usernameField = document.querySelector("#friend-username-input")
	usernameField.value = username
}

function main() {
	fillUsernameField()
	/** @type {HTMLFormElement} */ // @ts-ignore
	const inputMessage = document.querySelector("#add-friend-form")
	if (inputMessage)
		inputMessage.onsubmit = addFriend
	console.log("test")
}

main()