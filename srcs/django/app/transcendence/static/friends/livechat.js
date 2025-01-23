// @ts-check
import BaseWebSocket from "../global/websockets.js";

class MessagesHandler extends BaseWebSocket {
	/** @param {string} url */
	constructor(url) {
		super(url)
		// addEventListener("page-changed", () => {
		// 	this.socket.onmessage = null
		// 	this.socket.close()
		// })
		this.socket.onmessage = this.receive.bind(this);
		//alternative
	}

    /** @param {MessageEvent} e */
	receive(e) {
		/** @type {HTMLDivElement} */ // @ts-ignore
		const messageContainer = document.querySelector("#messages-container")
		const div = document.createElement("div")
		div.innerHTML = e.data
		messageContainer.appendChild(div)
		// Scrolling automatique à chaque nouveau message
        messageContainer.scrollTo({
            top: messageContainer.scrollHeight,
        });
	}
}

function main() {
	const mess = new MessagesHandler("messages")
}

main()