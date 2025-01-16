// @ts-check
import { getPage, refreshScripts } from "../global/SPA.js"
import BaseWebSocket from "../global/websockets.js"
import { PongScene } from "./PongScene.js"

/**
 * @typedef {Object} PongSocketData
 * @property {string} [type]
 * @property {string} [friend]
 * @property {string} [html]
 * @property {Object} [p1]
 * @property {Object} [p2]
 * @property {Object} [ball]
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
    /** @type {PongScene|null} */
    game = null
    direction = ""
    clickPressed = false

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

    getClickDir(y = 0) {
        /** @type {HTMLCanvasElement} */ // @ts-ignore
        const canvas = this.game.renderer.domElement
        const rect = canvas.getBoundingClientRect()
        const clickHeight = y - rect.top
        
        if (clickHeight > rect.height / 2)
            return "down"
        return "up"
    }
    
    /** @param {number|undefined} y */
    sendDirection(y) {
        if (y)
            this.direction = this.getClickDir(y)
        if (this.clickPressed && this.direction != "")
            this.socket.send(JSON.stringify({"type": "move", "direction": this.direction}))
    }

    initGame() {
        this.game = new PongScene()
        /** @type {HTMLCanvasElement} */
        const canvas = this.game.renderer.domElement
        
        canvas.addEventListener("mousedown", (e) => {
            if (e.buttons != 1) return
            this.clickPressed = true
            this.sendDirection(e.y)
        })
        
        canvas.addEventListener("touchstart", (e) => {
            this.clickPressed = true
            this.sendDirection(e.touches[0].clientY)
        })
        
        canvas.addEventListener("mousemove", (e) => {
            if (e.buttons != 1) return
            this.sendDirection(e.y)
        })
        
        canvas.addEventListener("touchmove", (e) => {
            e.preventDefault()
            this.sendDirection(e.touches[0].clientY)
        })
        
        canvas.addEventListener("mouseup", (e) => {
            this.clickPressed = false
            this.direction = ""
        })
        
        canvas.addEventListener("touchend", (e) => {
            this.clickPressed = false
            this.direction = ""
        })
        
        setInterval(this.sendDirection.bind(this), 1_000 / 60_000)
    }

    /** @param {string} html */
    launchGame(html) {
        const container = document.querySelector("#pong-container")
        if (!container) return
        container.innerHTML = html
        this.state = e_states.IN_GAME
        this.initGame()
    }

    /** @param {PongSocketData} json */
    updatePong(json) {
        if (!this.game)
            return
        this.game.paddle1.position.x = json.p1.x
        this.game.paddle1.position.y = json.p1.y
    
        this.game.paddle2.position.x = json.p2.x
        this.game.paddle2.position.y = json.p2.y
    
        this.game.ball.position.x = json.ball.x
        this.game.ball.position.y = json.ball.y
    }

    /** @param {MessageEvent} e */
    async receive(e) {
        /** @type {PongSocketData} */
        const json = JSON.parse(e.data)
        
        if (json.type == "game_over")
            return await getPage("/friends")

        if (json.type == "update_pong" && this.state == e_states.IN_GAME)
            return this.updatePong(json)

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
                this.launchGame(json.html)
                break
        }
    }
}

function main() {
    const websocket = new PongSocket()
}

main()