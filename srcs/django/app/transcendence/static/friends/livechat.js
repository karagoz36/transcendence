// @ts-check
import BaseWebSocket from "../global/websockets.js";

class MessagesHandler extends BaseWebSocket {
	/** @param {string} url */
	constructor(url) {
		super(url)
		addEventListener("page-changed", () => {
			if (this.socket.readyState === WebSocket.OPEN) {
				this.socket.onmessage = this.receive.bind(this);
			}
		});
		
	}

    /** @param {MessageEvent} e */
	receive(e) {
		/** @type {HTMLDivElement} */ // @ts-ignore
		const messageContainer = document.querySelector("#messages-container")
		
		// Vérifier si le message existe déjà pour éviter la duplication
		const existingMessage = Array.from(messageContainer.children).some(child => child.innerHTML === e.data);
		if (!existingMessage) {
			const div = document.createElement("div")
			div.innerHTML = e.data
			messageContainer.appendChild(div)
		}
		// Scrolling automatique à chaque nouveau message
		messageContainer.scrollTo({
			top: messageContainer.scrollHeight,
		});
	}
}

function main() {
	const notif = new MessagesHandler("messages")
}

main()