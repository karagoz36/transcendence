// @ts-check
import {getPage} from "../global/SPA.js"

/** @param {SubmitEvent} e */
async function addFriend(e) {
	e.preventDefault()
	if (!e.target)
		throw new Error("addFriend: e.target null")
	/** @type {string} */
	const username = e.target['username'].value
	await getPage("/api/friend/add", {
		method: "POST",
		headers: {
			"content-type": "application/json",
		},
		body: {username},
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
	// inputMessage.onsubmit = addFriend
	inputMessage.onsubmit = addFriend
}

main()