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

function main() {
	/** @type {HTMLFormElement} */ // @ts-ignore
	const inputMessage = document.querySelector("#add-friend-form")
	// inputMessage.onsubmit = addFriend
	inputMessage.onsubmit = addFriend
}

main()