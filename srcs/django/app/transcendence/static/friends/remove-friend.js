// @ts-check
import {getPage} from "../global/SPA.js"

/** @param {number} friendID */
async function removeFriend(friendID) {
	await getPage("/api/friend/remove", {
		method: "POST",
		headers: {
			"content-type": "application/json",
		},
		body: {friendID},
	})
}

function main() {
    /** @type {NodeListOf<HTMLButtonElement>} */
    const buttons = document.querySelectorAll("#remove-friend")

    buttons.forEach(button => {
        button.onclick = async () => {
            const friendID = Number(button.getAttribute("user-id"))
            await removeFriend(friendID)
        }
    })
}

main()