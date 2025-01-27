import { PongScene } from "../pong/PongScene.js";
import BaseWebSocket from "../global/websockets.js";


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
        sendMoveCommand();
    });
    
    document.addEventListener("keyup", (event) => {
        delete keysPressed[event.key];
        sendMoveCommand();
    });
    
    function sendMoveCommand(key) {
        let directionP1 = null;
        let directionP2 = null;
        let player = null;
        
        if (keysPressed["w"] || keysPressed["W"]) {
            directionP2 = "up";
            // player = "p2";
        }
        if (keysPressed["s"] || keysPressed["S"]) {
            directionP2 = "down";
            // player = "p2";
        }
        
        if (keysPressed["ArrowUp"]) {
            directionP1 = "up";
            // player = "p1";
        }
        if (keysPressed["ArrowDown"]) {
            directionP1 = "down";
            // player = "p1";
        }
        
        if (directionP1 !== null) {
            window.localPongWebSocket.socket.send(JSON.stringify({ "type": "move", "direction": directionP1, "player": "p1" }));
        } else if (!keysPressed["ArrowUp"] && !keysPressed["ArrowDown"]) {
            window.localPongWebSocket.socket.send(JSON.stringify({ "type": "move", "direction": "none", "player": "p1" }));
        }
        
        if (directionP2 !== null) {
            window.localPongWebSocket.socket.send(JSON.stringify({ "type": "move", "direction": directionP2, "player": "p2" }));
        } else if (!keysPressed["w"] && !keysPressed["W"] && !keysPressed["s"] && !keysPressed["S"]) {
            window.localPongWebSocket.socket.send(JSON.stringify({ "type": "move", "direction": "none", "player": "p2" }));
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
        
const localButton = document.getElementById("submit");
if (localButton) {
    localButton.addEventListener("click", async () => {
            document.addEventListener("DOMContentLoaded", () => {
            const title = document.getElementById("title");
            title.remove();
            localButton.remove();
        });
        await initializeLocalMode();
    });
}