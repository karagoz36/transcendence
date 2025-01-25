import { PongScene } from "../pong/PongScene.js";
import BaseWebSocket from "../global/websockets.js";

document.addEventListener("DOMContentLoaded", () => {
    const localButton = document.getElementById("submit");

    if (localButton) {
        localButton.addEventListener("click", async () => {
            console.log("Submit button clicked. Initializing Local Game Mode...");
            const title = document.getElementById("title");
			title.remove();
			localButton.remove();
			await initializeLocalMode();
        });
    }
});

async function initializeLocalMode() {
    console.log("Initializing Local Game Mode...");

    if (window.localPongWebSocket) {
        console.log("Closing existing LocalGame WebSocket...");
        window.localPongWebSocket.socket.close();
    }

    window.localPongWebSocket = new LocalGameWebSocket();

    window.pongScene = new PongScene();

    await waitForWebSocketOpen(window.localPongWebSocket.socket);

    console.log("WebSocket connection ready! Starting game...");
    window.localPongWebSocket.socket.send(JSON.stringify({ "type": "start_game" }));
    setupKeyboardControls();
}

function setupKeyboardControls() {
    const paddleSpeed = 0.5;
    let keysPressed = {};

    document.addEventListener("keydown", (event) => {
        keysPressed[event.key] = true;
    });

    document.addEventListener("keyup", (event) => {
        keysPressed[event.key] = false;
    });

    function movePaddles() {
        if (!window.pongScene) return;

        if (keysPressed["w"] || keysPressed["W"]) {
            window.pongScene.paddle1.position.y = Math.min(window.pongScene.paddle1.position.y + paddleSpeed, 7);
        }
        if (keysPressed["s"] || keysPressed["S"]) {
            window.pongScene.paddle1.position.y = Math.max(window.pongScene.paddle1.position.y - paddleSpeed, -7);
        }

        if (keysPressed["ArrowUp"]) {
            window.pongScene.paddle2.position.y = Math.min(window.pongScene.paddle2.position.y + paddleSpeed, 7);
        }
        if (keysPressed["ArrowDown"]) {
            window.pongScene.paddle2.position.y = Math.max(window.pongScene.paddle2.position.y - paddleSpeed, -7);
        }

        requestAnimationFrame(movePaddles);
    }

    movePaddles();
	gameLoop();
}

/**
 * Attendre que le WebSocket soit ouvert avant d'envoyer des messages.
 * @param {WebSocket} socket
 * @returns {Promise<void>}
 */
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

    /** @param {MessageEvent} e */
    receive(e) {
        const data = JSON.parse(e.data);
        console.log("WebSocket message received:", data);

        if (!window.pongScene) return;

        switch (data.type) {
            case "update_pong":
                window.pongScene.paddle1.position.y = data.p1.y;
                window.pongScene.paddle2.position.y = data.p2.y;
                window.pongScene.ball.position.x = data.ball.x;
                window.pongScene.ball.position.y = data.ball.y;
                break;
            
            case "game_over":
                console.log("Game Over!");
                break;
        }
    }
}

function gameLoop() {
    if (!window.pongScene) return;

    let ballSpeedX = 0.2;
    let ballSpeedY = 0.1;

    setInterval(() => {
        if (!window.pongScene) return;

        window.pongScene.ball.position.x += ballSpeedX;
        window.pongScene.ball.position.y += ballSpeedY;

        if (window.pongScene.ball.position.y > 7 || window.pongScene.ball.position.y < -7) {
            ballSpeedY *= -1;
        }
    }, 16);
}
