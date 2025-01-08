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

/** 
 * @param {number} position 
 * @param {number} color
 **/
function addPaddle(position, color) {
    const geometry = new THREE.BoxGeometry(0.5, 3, 1);
    const material = new THREE.MeshBasicMaterial({ color });
    const paddle = new THREE.Mesh(geometry, material);
    paddle.position.x = position;
    scene.add(paddle);
    return paddle;
}

const paddle1 = addPaddle(10, 0xff0000);
const paddle2 = addPaddle(-10, 0x0000ff);

function animate() {
    renderer.render(scene, camera);
}

renderer.setAnimationLoop(animate);

function onWindowResize() {
    camera.aspect = ASPECT_RATIO;
    camera.updateProjectionMatrix();
    const height = window.innerWidth / ASPECT_RATIO
    if (window.innerHeight > window.innerWidth) {
    }
    renderer.setSize(window.innerWidth, height, false);
}

window.addEventListener("resize", onWindowResize);

onWindowResize()