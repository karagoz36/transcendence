// @ts-check
import {getPage} from "../global/SPA.js"

/** @param {MouseEvent} e */
async function openChat(e) {
   	/** @type {HTMLButtonElement|EventTarget|null} */
	const button = e.target
	if (!button) return
    /** @type {HTMLButtonElement|null} */
    const modalButton = document.querySelector("#send-message")
	if (modalButton == null)
		return
	/** @type {string|null} */ // @ts-ignore
	const userId = button.getAttribute("user-id")
	if (userId == null)
			return


	/** Mettre à jour le titre du modal */
    /** @type {string|null} */ // @ts-ignore
	const username = button.getAttribute("user-name")
    if (username == null)
        return
    const modalLabel = document.getElementById("chatModalLabel");
    if (modalLabel) {
        modalLabel.textContent = `${username}`;
    }

    // /** Mettre à jour le lien et le texte */
    // const userLink = document.getElementById("chatModalUserLink");
       // if (userLink instanceof HTMLAnchorElement) {
    //     userLink.textContent = username;
    //     userLink.href = `/profile/${userId}`; // URL vers la page de profil de l'utilisateur
    // }
    modalButton.setAttribute("user-id", userId)
	await getPage("/api/friend/open-message", {
            method: "POST",
            headers: {"content-type": "application/json"},
            body: {                 
            	"friendID": Number(userId),
            }
    }, false, "#messages-container");

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
	}, false, "#messages-container");
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

function main() {
	/** @type {NodeListOf<HTMLFormElement>|null} */
	const forms = document.querySelectorAll("form#send-message-form")
	if (forms == null)
		return
	forms.forEach(form => form.onsubmit = sendMessage)
	/** @type {NodeListOf<HTMLButtonElement>|null} */
	const buttons = document.querySelectorAll("button#open-chat-modal")
	buttons.forEach(button => button.onclick = openChat)
}

main()