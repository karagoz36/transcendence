import { PongScene } from "../pong/PongScene.js";
import { getPage, refreshScripts } from "../global/SPA.js"

document.addEventListener("DOMContentLoaded", () => {
    const localButton = document.getElementById("submit");

    if (localButton) {
        localButton.addEventListener("click", () => {
            const zone = document.getElementById("group");
            const title = document.getElementById("title");
            zone.remove();
            title.remove();
            initializeLocalMode();
        });
    }
});

function initializeLocalMode() {
    const container = document.querySelector("#pong-container");

    if (!container) {
        console.error("Conteneur #pong-container introuvable. Impossible de démarrer le mode local.");
        return;
    }

    container.innerHTML = "";

    const pongScene = new PongScene();
    container.appendChild(pongScene.renderer.domElement);

    pongScene.ball.position.set(0, 0, 0);
    let ballVelocity = { x: 0.1, y: 0.1 };

    const keysPressed = {
        paddle1Up: false,
        paddle1Down: false,
        paddle2Up: false,
        paddle2Down: false,
    };

    const paddleSpeed = 0.2;

    document.addEventListener("keydown", (e) => {
        if (e.key === "w") keysPressed.paddle1Up = true;
        if (e.key === "s") keysPressed.paddle1Down = true;
        if (e.key === "ArrowUp") keysPressed.paddle2Up = true;
        if (e.key === "ArrowDown") keysPressed.paddle2Down = true;
    });

    document.addEventListener("keyup", (e) => {
        if (e.key === "w") keysPressed.paddle1Up = false;
        if (e.key === "s") keysPressed.paddle1Down = false;
        if (e.key === "ArrowUp") keysPressed.paddle2Up = false;
        if (e.key === "ArrowDown") keysPressed.paddle2Down = false;
    });

    function updateGame() {
        if (keysPressed.paddle1Up) pongScene.paddle1.position.y += paddleSpeed;
        if (keysPressed.paddle1Down) pongScene.paddle1.position.y -= paddleSpeed;
        if (keysPressed.paddle2Up) pongScene.paddle2.position.y += paddleSpeed;
        if (keysPressed.paddle2Down) pongScene.paddle2.position.y -= paddleSpeed;

        pongScene.paddle1.position.y = Math.max(
            Math.min(pongScene.paddle1.position.y, 4.5),
            -4.5
        );
        pongScene.paddle2.position.y = Math.max(
            Math.min(pongScene.paddle2.position.y, 4.5),
            -4.5
        );

        pongScene.ball.position.x += ballVelocity.x;
        pongScene.ball.position.y += ballVelocity.y;

        if (pongScene.ball.position.y >= 5 || pongScene.ball.position.y <= -5) {
            ballVelocity.y *= -1;
        }

        if (
            pongScene.ball.position.x <= pongScene.paddle1.position.x + 0.5 &&
            pongScene.ball.position.x >= pongScene.paddle1.position.x &&
            pongScene.ball.position.y >= pongScene.paddle1.position.y - 1.5 &&
            pongScene.ball.position.y <= pongScene.paddle1.position.y + 1.5
        ) {
            ballVelocity.x *= -1;
        }

        if (
            pongScene.ball.position.x >= pongScene.paddle2.position.x - 0.5 &&
            pongScene.ball.position.x <= pongScene.paddle2.position.x &&
            pongScene.ball.position.y >= pongScene.paddle2.position.y - 1.5 &&
            pongScene.ball.position.y <= pongScene.paddle2.position.y + 1.5
        ) {
            ballVelocity.x *= -1;
        }

        if (pongScene.ball.position.x < -10) {
            resetBall();
            console.log("Joueur 2 marque !");
        } else if (pongScene.ball.position.x > 10) {
            resetBall();
            console.log("Joueur 1 marque !");
        }
    }

    function resetBall() {
        pongScene.ball.position.set(0, 0, 0);
        ballVelocity.x *= -1;
    }

    function animate() {
        updateGame();
        pongScene.renderer.render(pongScene.scene, pongScene.camera);
        requestAnimationFrame(animate);
    }

    animate();
}
