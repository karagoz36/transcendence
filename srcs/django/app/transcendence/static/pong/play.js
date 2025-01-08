// @ts-check
import * as THREE from "./three.module.js";

const ASPECT_RATIO = 16/9

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(
    75,
    ASPECT_RATIO,
    0.1,
    1000,
);
camera.position.z = 10;

const renderer = new THREE.WebGLRenderer();
document.querySelector("#pong-container")?.appendChild(renderer.domElement);

/** @param {number} position */
function addPaddle(position) {
    const geometry = new THREE.BoxGeometry(0.5, 3, 1);
    const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
    const paddle = new THREE.Mesh(geometry, material);
    paddle.position.x = position;
    scene.add(paddle);
    return paddle;
}

const paddle1 = addPaddle(10);
const paddle2 = addPaddle(-10);

function animate() {
    renderer.render(scene, camera);
}

renderer.setAnimationLoop(animate);

function onWindowResize() {
    camera.aspect = ASPECT_RATIO;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

window.addEventListener("resize", onWindowResize);

onWindowResize()