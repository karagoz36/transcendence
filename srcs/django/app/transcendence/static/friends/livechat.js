// @ts-check
import {getPage} from "../global/SPA.js"
import BaseWebSocket from "../global/websockets.js";

class MessagesHandler extends BaseWebSocket {
    /** @param {MessageEvent} e */
	receive(e) {
		const data = JSON.parse(e.data)
	}
}


function main() {
	const notif = new MessagesHandler("messages")
}

main()