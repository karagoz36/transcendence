// @ts-check
import { getPage, refreshScripts } from "../global/SPA.js"
import BaseWebSocket from "../global/websockets.js"

/**
 * @typedef {Object} PongSocketData
 * @property {string} [type]
 * @property {string} [friend]
 * @property {string} [html]
*/

/**
 * @readonly
 * @enum {number}
 */
const e_states = {
    INVITE_SENT: 0,
    INVITE_ACCEPTED: 1,
    LAUNCH_GAME: 2,
    IN_GAME: 3,
}

class PongSocket extends BaseWebSocket {
    /** @type {string} */
    opponent

	constructor() {
		super("pong")
		addEventListener("page-changed", () => {
			this.socket.onmessage = null
			this.socket.close()
		})
	}
    
    open() {
        const urlParams = new URLSearchParams(window.location.search) // @ts-ignore
        this.opponent = urlParams.get("opponent")
        if (!this.opponent) {
            this.opponent = ""
            return
        }
        this.socket.send(JSON.stringify({"type": "accept_invite", "opponent": this.opponent}))
    }

    /** @param {string} html */
    async launchGame(html) {
        const container = document.querySelector("#pong-container")
        if (!container) return
        container.innerHTML = html
        await refreshScripts(container, container, "#pong-container")
        this.state = e_states.IN_GAME
    }

    /** @param {MessageEvent} e */
    async receive(e) {
        console.log(e.data)
        /** @type {PongSocketData} */
        const json = JSON.parse(e.data)
    
        if (json.type == "invite_accepted" && this.state == e_states.IN_GAME)
            return this.socket.send(JSON.stringify({"type": "join_game"}))

        if (json.type == "invite_accepted" && this.opponent == json.friend)
            this.state = e_states.INVITE_ACCEPTED
        else if (json.type == "launch_game")
            this.state = e_states.LAUNCH_GAME

        switch (this.state) {
            case e_states.INVITE_ACCEPTED:
                this.socket.send(JSON.stringify({"type": "launch_game"}))
                break;
            case e_states.LAUNCH_GAME:
                if (!json.html) {
                    console.error(json)
                    throw new Error("expected html")
                }
                await this.launchGame(json.html)
                break
        }
    }
}

function main() {
    const websocket = new PongSocket()
}

main()