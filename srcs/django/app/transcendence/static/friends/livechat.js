// @ts-check
import BaseWebSocket from "../global/websockets.js";

class MessagesHandler extends BaseWebSocket {
	/** @param {string} url */
	constructor(url) {
		super(url)
		addEventListener("page-changed", (e) => {
			if (e.detail != ".modal-content"){
				this.socket.onmessage = null
				this.socket.close()
			}
		})
	}

    /** @param {MessageEvent} e */
	receive(e) {
		/** @type {HTMLDivElement} */ // @ts-ignore
		const messageContainer = document.querySelector("#messages-container")
		const div = document.createElement("div")
		div.innerHTML = e.data
		messageContainer.appendChild(div)
        messageContainer.scrollTo({
            top: messageContainer.scrollHeight,
        });
	}
}

function main() {
	const mess = new MessagesHandler("messages")
}

main()