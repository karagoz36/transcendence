import {getPage} from "../global/SPA.js"

/**
 * @param {number} csrfmiddlewaretoken 
 * @param {number} friendID 
*/
async function acceptFriendInvitation(csrfmiddlewaretoken, friendID) {
	await getPage("/api/accept-friend", {
		method: "POST",
		headers: {
			"X-CSRFToken": csrfmiddlewaretoken,
			"content-type": "application/json"
		},
		body: {
			friendID
		}
	})
}

/**
 * @param {number} friendID 
*/
async function rejectFriendInvitation(csrfmiddlewaretoken, friendID) {
	await getPage("/api/reject-friend", {
		method: "POST",
		headers: {
			"X-CSRFToken": csrfmiddlewaretoken,
			"content-type": "application/json"
		},
		body: {
			friendID 
		}
	})
}

/** @param {SubmitEvent} e */
async function handleFriendRequest(e) {
	e.preventDefault()
	/** @type {number} */
	const csrfmiddlewaretoken = e.target['csrfmiddlewaretoken'].value
	/** @type {HTMLButtonElement} */
	const button = e.submitter
	const friendID = Number(button.getAttribute("user-id"))

	if (button.textContent == "Reject")
		rejectFriendInvitation(csrfmiddlewaretoken, friendID)
	else
		await acceptFriendInvitation(csrfmiddlewaretoken, friendID)
}

function main() {
	/** @type {NodeListOf<HTMLFormElement>} */
	const forms = document.querySelectorAll("#invite-pending-form")
	forms.forEach(form => form.onsubmit = handleFriendRequest)
}

main()