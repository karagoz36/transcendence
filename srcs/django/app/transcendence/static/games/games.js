import { PongScene } from "../pong/PongScene.js";
import BaseWebSocket from "../global/websockets.js";

document.addEventListener("DOMContentLoaded", () => {
    const localButton = document.getElementById("submit");

    if (localButton) {
        localButton.addEventListener("click", async () => {
            const title = document.getElementById("title");
            title.remove();
            localButton.remove();
            await initializeLocalMode();
        });
    }
});

async function initializeLocalMode() {
    if (window.localPongWebSocket) {
        window.localPongWebSocket.socket.close();
    }

    window.localPongWebSocket = new LocalGameWebSocket();
    window.pongScene = new PongScene();

    await waitForWebSocketOpen(window.localPongWebSocket.socket);

    setupKeyboardControls();
}

function setupKeyboardControls() {
    let keysPressed = {};

    document.addEventListener("keydown", (event) => {
        keysPressed[event.key] = true;
        sendMoveCommand(event.key);
    });

    document.addEventListener("keyup", (event) => {
        keysPressed[event.key] = false;
        sendMoveCommand(null);
    });

    function sendMoveCommand(key) {
        let direction = null;
        let player = null;

        if (key === "w" || key === "W") {
            direction = "up";
            player = "p1";
        }
        if (key === "s" || key === "S") {
            direction = "down";
            player = "p1";
        }

        if (key === "ArrowUp") {
            direction = "up";
            player = "p2";
        }
        if (key === "ArrowDown") {
            direction = "down";
            player = "p2";
        }

        if (direction && player) {
            console.log(`🎮 Sending move: ${player} -> ${direction}`);
            window.localPongWebSocket.socket.send(JSON.stringify({ "type": "move", "direction": direction, "player": player }));
        }
    }
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
        if (!window.pongScene) return;

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
