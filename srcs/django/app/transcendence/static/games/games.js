import { PongScene } from "../pong/PongScene.js";
import BaseWebSocket from "../global/websockets.js";

let gameInitialized = false;

async function initializeLocalMode() {
    if (window.localPongWebSocket) {
        window.localPongWebSocket.socket.close();
    }
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

            await new Promise(resolve => requestAnimationFrame(resolve)); 
            window.pongScene = new PongScene();

            requestAnimationFrame(() => {
                window.dispatchEvent(new Event("resize"));
            });

            setupKeyboardControls();
            gameInitialized = true;
        }
    });
    window.localPongWebSocket.socket.send(JSON.stringify({
        type: "launch_game"
    }));
}


function setupKeyboardControls() {
    let keysPressed = {};

    document.addEventListener("keydown", (event) => {
        keysPressed[event.key] = true;
    });

    document.addEventListener("keyup", (event) => {
        delete keysPressed[event.key];
    });

    setInterval(() => {
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

class LocalGameWebSocket extends BaseWebSocket {
    constructor() {
        super("pongsocket");
    }

    receive(e) {
        const data = JSON.parse(e.data);
        if (!window.pongScene || !gameInitialized) return;
        
        switch (data.type) {
            case "update_pong":
                window.pongScene.paddle1.position.y = data.p1.y;
                window.pongScene.paddle2.position.y = data.p2.y;
                window.pongScene.ball.position.x = data.ball.x;
                window.pongScene.ball.position.y = data.ball.y;
                break;
            case "game_over":
                break;
        }
    }
}

function setupGame() {
    const localButton = document.getElementById("submit");
    if (localButton) {
        localButton.addEventListener("click", async () => {
            const title = document.getElementById("title");
            if (title) title.remove();
            localButton.remove();
            
            try {
                await initializeLocalMode();
            } catch (error) {
                console.error("Erreur lors de l'initialisation:", error);
            }
        });
    }
}

setupGame();