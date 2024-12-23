// @ts-check
import {getPage} from "../global/SPA.js"
import BaseWebSocket from "../global/websockets.js";

class MessagesHandler extends BaseWebSocket {
	/** @param {string} url */
	constructor(url) {
		super(url)
		addEventListener("page-changed", () => this.socket?.close())
	}

    /** @param {MessageEvent} e */
	receive(e) {
		/** @type {HTMLDivElement} */ // @ts-ignore
		const messageContainer = document.querySelector("#messages-container")
		const div = document.createElement("div")
		div.innerHTML = e.data
		messageContainer.appendChild(div)
	}
}

function main() {
	const notif = new MessagesHandler("messages")
}

main()