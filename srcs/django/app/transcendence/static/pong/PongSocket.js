// @ts-check
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
}

class PongSocket extends BaseWebSocket {
    /** @type {string} */
    opponent

	/** @param {string} url */
	constructor(url) {
		super(url)
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
    launchGame(html) {
        const container = document.querySelector("#pong-container")
        if (!container) return
        container.innerHTML = html
    }
    
    /** @param {MessageEvent} e */
    receive(e) {
        /** @type {PongSocketData} */
        const json = JSON.parse(e.data)

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
                this.launchGame(json.html)
                break
        }
    }
}

function main() {
    const websocket = new PongSocket("pong")
}

main()