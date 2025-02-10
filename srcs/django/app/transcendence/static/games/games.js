import { PongScene } from "../pong/PongScene.js";
import BaseWebSocket from "../global/websockets.js";
import { getPage, refreshScripts } from "../global/SPA.js"

let gameInitialized = false;
let keyboardControlInterval = null;
let pageCheckInterval = null;

document.addEventListener("keydown", function(event) {
    const keysToBlock = ["ArrowUp", "ArrowDown", "w", "W", "s", "S"];
    
    if (keysToBlock.includes(event.key)) {
        event.preventDefault();
    }
});


async function initializeLocalMode() {
    await cleanupGame();
    
    window.localPongWebSocket = new LocalGameWebSocket();
    await waitForWebSocketOpen(window.localPongWebSocket.socket);

    window.localPongWebSocket.socket.addEventListener("message", async (event) => {
        const data = JSON.parse(event.data);

        if (data.type === "launch_game" && data.html) {
            const container = document.querySelector("#pong-container");
            if (!container) {
                console.error("Erreur: #pong-container introuvable");
                return;
            }
            
            container.innerHTML = data.html;
            resetScoreDisplay();

            await new Promise(resolve => requestAnimationFrame(resolve)); 
            window.pongScene = new PongScene();

            requestAnimationFrame(() => {
                window.dispatchEvent(new Event("resize"));
            });

            setupKeyboardControls();
            gameInitialized = true;
			if (!pageCheckInterval) {
                pageCheckInterval = setInterval(checkPage, 500);
            }
        }
    });
    window.localPongWebSocket.socket.send(JSON.stringify({
        type: "launch_game"
    }));
}

function resetScoreDisplay() {
    const playerScoreElement = document.querySelector("#player-score");
    const opponentScoreElement = document.querySelector("#opponent-score");
    if (playerScoreElement && opponentScoreElement) {
        playerScoreElement.textContent = "0";
        opponentScoreElement.textContent = "0";
    }
}

async function cleanupGame() {
    if (keyboardControlInterval) {
        clearInterval(keyboardControlInterval);
        keyboardControlInterval = null;
    }

    if (pageCheckInterval) {
        clearInterval(pageCheckInterval);
        pageCheckInterval = null;
    }
    if (window.pongScene) {
        window.pongScene = null;
    }

    if (window.localPongWebSocket) {
        if (window.localPongWebSocket.socket.readyState === WebSocket.OPEN) {
            window.localPongWebSocket.socket.close();
            await new Promise(resolve => setTimeout(resolve, 100));
        }
        window.localPongWebSocket = null;
    }

    gameInitialized = false;
}

function setupKeyboardControls() {
    let keysPressed = {};

    document.addEventListener("keydown", (event) => {
        keysPressed[event.key] = true;
    });

    document.addEventListener("keyup", (event) => {
        delete keysPressed[event.key];
    });

    keyboardControlInterval = setInterval(() => {
        if (!gameInitialized || !window.pongScene) return;

        let directionP1 = null;
        let directionP2 = null;

        if (keysPressed["w"] || keysPressed["W"]) {
            directionP2 = "up";
        }
        if (keysPressed["s"] || keysPressed["S"]) {
            directionP2 = "down";
        }
        if (keysPressed["ArrowUp"]) {
            directionP1 = "up";
        }
        if (keysPressed["ArrowDown"]) {
            directionP1 = "down";
        }

        if (window.localPongWebSocket && window.localPongWebSocket.socket.readyState === WebSocket.OPEN) {
            if (directionP1 !== null) {
                window.localPongWebSocket.socket.send(JSON.stringify({
                    "type": "move",
                    "direction": directionP1,
                    "player": "p1"
                }));
            } else {
                window.localPongWebSocket.socket.send(JSON.stringify({
                    "type": "move",
                    "direction": "none",
                    "player": "p1"
                }));
            }

            if (directionP2 !== null) {
                window.localPongWebSocket.socket.send(JSON.stringify({
                    "type": "move",
                    "direction": directionP2,
                    "player": "p2"
                }));
            } else {
                window.localPongWebSocket.socket.send(JSON.stringify({
                    "type": "move",
                    "direction": "none",
                    "player": "p2"
                }));
            }
        }
    }, 50);
}

function waitForWebSocketOpen(socket) {
    return new Promise((resolve) => {
        if (socket.readyState === WebSocket.OPEN) {
            resolve();
        } else {
            socket.addEventListener("open", () => resolve(), { once: true });
        }
    });
}

function checkPage() {
	let page = window.location.pathname;
	if (page !== "/games/") {
		if (window.localPongWebSocket && window.localPongWebSocket.socket && window.localPongWebSocket.socket.readyState === WebSocket.OPEN) {
			window.localPongWebSocket.socket.send(JSON.stringify({ type: "player_exit" }));
			window.localPongWebSocket.socket.close();
		} else {
			console.warn("⚠️ Impossible d'envoyer player_exit : WebSocket déjà fermé ou inexistant.");
		}
		
		cleanupGame();
	}
}

class LocalGameWebSocket extends BaseWebSocket {
    constructor() {
        super("pongsocket");
    }

    receive(e) {
        const data = JSON.parse(e.data);
        if (!window.pongScene || !gameInitialized) return;
		console.table(data);

		switch (data.type) {
            case "hitBall":
                window.pongScene.animateBallHit();
                break;
            case "update_pong":
                window.pongScene.paddle1.position.y = data.p1.y;
                window.pongScene.paddle2.position.y = data.p2.y;
                window.pongScene.ball.position.x = data.ball.x;
                window.pongScene.ball.position.y = data.ball.y;
                const playerScoreElement = document.querySelector("#player-score");
                const opponentScoreElement = document.querySelector("#opponent-score");
                if (playerScoreElement && opponentScoreElement) {
                    playerScoreElement.textContent = data.score.p1;
                    opponentScoreElement.textContent = data.score.p2;
                }
                break;
            case "game_over":
                cleanupGame().then(() => getPage("/games"));
                break;
			default:
				break;
        }
    }
}

function setupGame() {
    const localButton = document.getElementById("multiplayer");
    if (localButton) {
        localButton.addEventListener("click", async () => {
            const title = document.getElementById("title");
            if (title) title.remove();
            localButton.remove();
            const section = document.getElementById("section");
            if (section) section.remove();
            try {
                await initializeLocalMode();
            } catch (error) {
                console.error("Erreur lors de l'initialisation:", error);
            }
        });
    }

    const tournamentButton = document.getElementById("tournament");
    if (tournamentButton) {
        tournamentButton.addEventListener("click", () => {
            getPage("/tournament/create/");
        });
    }

    const friendsButton = document.getElementById("friends");
    if (friendsButton) {
        friendsButton.addEventListener("click", () => {
            getPage("/friends/");
        });
    }
}

setupGame();
