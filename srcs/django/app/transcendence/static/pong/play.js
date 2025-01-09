// @ts-check
import * as THREE from "./three.module.js";

export class PongGame {
    ASPECT_RATIO = 16 / 9;
    scene = new THREE.Scene()
    camera = new THREE.PerspectiveCamera(
        75,
        this.ASPECT_RATIO,
        0.1,
        1000,
    )
    renderer = new THREE.WebGLRenderer();
    paddle1 = this.addPaddle(10, 0xff0000);
    paddle2 = this.addPaddle(-10, 0x0000ff);
    ball = this.addBall()

    addBall() {
        const geometry = new THREE.SphereGeometry(0.5);
        const material = new THREE.MeshBasicMaterial({ color: 0xffff00 });
        const ball = new THREE.Mesh(geometry, material);
        this.scene.add(ball);
        return ball;
    }

    /**
     * @param {number} position
     * @param {number} color
     */
    addPaddle(position, color) {
        const geometry = new THREE.BoxGeometry(-0.5, 3, 1);
        const material = new THREE.MeshBasicMaterial({ color });
        const paddle = new THREE.Mesh(geometry, material);
        paddle.position.x = position;
        this.scene.add(paddle);
        return paddle;
    }

    onWindowResize() {
        const height = window.innerWidth / this.ASPECT_RATIO;
        this.renderer.setSize(window.innerWidth, height, false);
    }

    constructor() {
        this.camera.position.z = 10;
        document.querySelector("#pong-container")?.appendChild(this.renderer.domElement);
        this.renderer.setAnimationLoop(() => this.renderer.render(this.scene, this.camera));

        window.addEventListener("resize", this.onWindowResize.bind(this));
        this.onWindowResize();
    }
}