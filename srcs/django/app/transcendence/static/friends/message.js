// @ts-check
import {getPage} from "../global/SPA.js"
export { openChat };

/** @param {CustomEvent} e */
function suppressModalBackDrop(e) {
    if (e.detail == ".main-container") {
        const backdrop = document.getElementsByClassName("modal-backdrop")
        if (backdrop.length > 0) {
            backdrop[0].remove()
        }
    }
}

addEventListener('page-changed', suppressModalBackDrop)

/** @param {number} userID */
async function updateModal(userID) {
	await getPage("/api/friend/open-message", {
        method: "POST",
        headers: {"content-type": "application/json"},
        body: {                 
        	"friendID": userID,
        }
    }, false, ".modal-content");

    const modal = document.getElementById("chatModal");
    if (modal)
        modal.addEventListener("shown.bs.modal", () => {
            const messagesContainer = document.querySelector("#chatModal .modal-body");
            if (messagesContainer) {
                messagesContainer.scrollTo({
                    top: messagesContainer.scrollHeight,
                });
            }
        });
}

/** @param {MouseEvent} e */
async function openChat(e) {
    /** @type {string|null} */ // @ts-ignore
	const userId = e.target.getAttribute("user-id")
	if (userId == null)
        return
    await updateModal(Number(userId))
    setupModalEvents()
}

/** @param {SubmitEvent} event */
async function sendMessage(event) {
	event.preventDefault();
	if (!event.target) return
	/** @type {string} */
	const message = event.target["message"].value
	/** @type {HTMLButtonElement} */ // @ts-ignore
	const button = event.submitter
	const friendID = Number(button.getAttribute("user-id"))

	await getPage("/api/friend/send-message", {
		method: "POST",
		headers: {"content-type": "application/json"},
		body: {			
			"friendID": friendID,
			"message": message
		}
	}, false, ".modal-content");
    setupModalEvents()
	event.target["message"].value = "";
	const modal = document.getElementById("chatModal");
    if (modal){
        const messagesContainer = document.querySelector("#chatModal .modal-body");
        if (messagesContainer) {
            messagesContainer.scrollTo({
                top: messagesContainer.scrollHeight,
            });
        };
    }
}

function setupModalEvents() {
	/** @type {NodeListOf<HTMLFormElement>|null} */
	const forms = document.querySelectorAll("form#send-message-form")
	if (forms == null)
		return
	forms.forEach(form => form.onsubmit = sendMessage)

	/** @type {NodeListOf<HTMLButtonElement>|null} */
	const buttons = document.querySelectorAll("button#open-chat-modal")

	buttons.forEach(button => {
        button.onclick = openChat
    })
}

function main() {
    setupModalEvents()
	/** @type {NodeListOf<HTMLButtonElement>|null} */
	const buttons = document.querySelectorAll("button#open-chat-modal")
    const params = new URLSearchParams(window.location.search);
    /** @type {string|null} */
    const id = params.get("id")

    buttons.forEach(button => {
        if (id && button.getAttribute("user-id") == id) {
            button.click()
        }
    })
}

main()