import {getPage} from "../global/SPA.js"

/**
 * @param {number} friendID 
*/
async function acceptFriendInvitation(friendID) {
	await getPage("/api/friend/accept", {
		method: "POST",
		headers: {
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
async function rejectFriendInvitation(friendID) {
	await getPage("/api/friend/reject", {
		method: "POST",
		headers: {
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
	/** @type {HTMLButtonElement} */
	const button = e.submitter
	const friendID = Number(button.getAttribute("user-id"))

	if (button.textContent == "Reject")
		await rejectFriendInvitation(friendID)
	else
		await acceptFriendInvitation(friendID)
}

function main() {
	/** @type {NodeListOf<HTMLFormElement>} */
	const forms = document.querySelectorAll("#invite-pending-form")
	forms.forEach(form => form.onsubmit = handleFriendRequest)
}

main()