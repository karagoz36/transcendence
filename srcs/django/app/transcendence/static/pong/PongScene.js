// @ts-check
import * as THREE from "three";
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

export class PongScene {
    ASPECT_RATIO = 16 / 9;
    scene = new THREE.Scene()
    camera = new THREE.PerspectiveCamera(
        75,
        this.ASPECT_RATIO,
        0.1,
        1000,
    )
    renderer = new THREE.WebGLRenderer({"antialias": true});
    paddle1 = this.addPaddle(10, 0xff0000);
    paddle2 = this.addPaddle(-10, 0x0000ff);
    ball = this.addBall()
    controls = new OrbitControls(this.camera, this.renderer.domElement)
	score1 = 0;
	score2 = 0;

    constructor() {
        this.addLights()
        this.cameraControl()
        this.camera.position.z = 10;
        document.querySelector("#pong-container")?.appendChild(this.renderer.domElement);
        this.renderer.setAnimationLoop(() => {
            this.controls.update()
            this.renderer.render(this.scene, this.camera)
        });

        window.addEventListener("resize", this.onWindowResize.bind(this));
        this.onWindowResize();
    }

    // animateBallHit() {
    //     gsap.to(this.ball.scale, { x: 1.2, y: 1.2, duration: 0.2, yoyo: true, repeat: 1 });
    // }

    animateBallHit() {
        const scaleUp = new THREE.Vector3(1.3, 0.8, 1);
        const scaleDown = new THREE.Vector3(1, 1, 1);
    
        new THREE.VectorKeyframeTrack('.scale', [0, 0.1, 0.2], [
            scaleUp.x, scaleUp.y, scaleUp.z,
            scaleDown.x, scaleDown.y, scaleDown.z
        ]);
    }    

    cameraControl() {
		this.controls.enableZoom = false;
        this.controls.enablePan = false;
        this.controls.enablePan = false
        this.controls.mouseButtons = {
            RIGHT: THREE.MOUSE.ROTATE,
        }
    }

    addLights() {
        this.paddle1.castShadow = true
        this.paddle2.castShadow = true
        this.ball.castShadow = true
        const ambientLight = new THREE.AmbientLight(0xffffff, 1)
        this.scene.add(ambientLight);
    }

    addBall() {
        const geometry = new THREE.SphereGeometry(0.5);
        const material = new THREE.MeshStandardMaterial({ color: 0xffff00 });
        const neonMaterial = new THREE.MeshStandardMaterial({
            color: 0x00ffcc,
            emissive: 0x00ffcc,
            emissiveIntensity: 2,
        });
        const ball = new THREE.Mesh(geometry, neonMaterial);
        this.scene.add(ball);
        return ball;
    }

    /**
     * @param {number} position
     * @param {number} color
     */
    addPaddle(position, color) {
        const geometry = new THREE.BoxGeometry(-0.5, 3, 1);
        const material = new THREE.MeshStandardMaterial({ color });
        const neonMaterial = new THREE.MeshStandardMaterial({
            color,
            emissive: color,
            emissiveIntensity: 1.5,
        });
        const paddle = new THREE.Mesh(geometry, neonMaterial);
        paddle.position.x = position;
        this.scene.add(paddle);
        return paddle;
    }

    onWindowResize() {
        const height = window.innerWidth / this.ASPECT_RATIO;
        this.renderer.setSize(window.innerWidth, height, false);
    }
}