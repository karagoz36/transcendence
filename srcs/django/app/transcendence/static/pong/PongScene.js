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
	backGround = this.addTexturedGridBackground();
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
		
        // window.addEventListener("resize", this.onWindowResize.bind(this));
        window.addEventListener("resize", this.onWindowResize);
        this.onWindowResize();
    }
     
 
	addTexturedGridBackground() {
		const boundaries = new THREE.Vector2(20, 20);
		const planeBoundaries = new THREE.PlaneGeometry(boundaries.x * 2, boundaries.y * 2, boundaries.x * 2, boundaries.y * 2);
		planeBoundaries.rotateZ(-Math.PI * 0.5);
	
		// const planeMaterial = new THREE.MeshBasicMaterial({ 
		// 	color: 0x2222ff,
		// 	wireframe: true,
		// 	transparent: true, 
		// 	opacity: 0.5
		// });
		const planeMaterial = new THREE.MeshBasicMaterial({wireframe: true});
		const plane = new THREE.Mesh(planeBoundaries, planeMaterial);
	
		plane.position.z = -0.8;
	
		this.scene.add(plane);
		return (plane);
	}
	

    animateBallHit() {
        const particleCount = 50;
        const particles = new THREE.BufferGeometry();
        const positions = new Float32Array(particleCount * 3);
    
        for (let i = 0; i < particleCount; i++) {
            positions[i * 3] = (Math.random() - 0.5) * 0.5
            positions[i * 3 + 1] = (Math.random() - 0.5) * 0.5
            positions[i * 3 + 2] = (Math.random() - 0.5) * 0.5
        }
    
        particles.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    
        const particleMaterial = new THREE.PointsMaterial({
            color: 0xffcc00,
            size: 0.12,
            transparent: true,
            opacity: 1,
        });
    
        const particleSystem = new THREE.Points(particles, particleMaterial);
        particleSystem.position.copy(this.ball.position); 
    
        this.scene.add(particleSystem);
    
        const animateParticles = () => {
            const positions = particles.attributes.position.array;
            for (let i = 0; i < particleCount; i++) {
                positions[i * 3] *= 1.1;
                positions[i * 3 + 1] *= 1.1;
                positions[i * 3 + 2] *= 1.1;
            }
            particles.attributes.position.needsUpdate = true;
        };
    
        setTimeout(() => {
            this.scene.remove(particleSystem);
        }, 500);
    
        const interval = setInterval(() => {
            animateParticles();
        }, 50);
    
        setTimeout(() => {
            clearInterval(interval);
        }, 500);     
    }    

    cameraControl() {
		this.controls.enableZoom = false;
        this.controls.enablePan = false;
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

    // onWindowResize() {
    //     const height = window.innerWidth / this.ASPECT_RATIO;
    //     this.renderer.setSize(window.innerWidth, height, false);
    // }
	onWindowResize = () => {
		var width = window.innerWidth;
		var height = window.innerHeight;
		this.renderer.setSize( width, height );
		this.camera.aspect = width / height;
		this.camera.updateProjectionMatrix();

		// // Mise à jour du ratio d'aspect
		// this.ASPECT_RATIO = width / height;
		// this.camera.aspect = this.ASPECT_RATIO;
		// this.camera.updateProjectionMatrix();
	
		// // Ajuster la taille du rendu
		// this.renderer.setSize(width, height);
		// this.renderer.setPixelRatio(window.devicePixelRatio);
	
		// // // Ajuster dynamiquement la taille du fond pour qu'il remplisse l'écran
		// // if (this.backGround) {
		// // 	const scaleX = this.camera.aspect * 20; // Ajuster la largeur
		// // 	const scaleY = 20; // Hauteur fixe
		// // 	this.backGround.scale.set(scaleX, scaleY, 1);
		// // }
		// const baseZoom = 20;  // Valeur de base (correspond à la position actuelle)
		// this.camera.position.z = baseZoom / this.ASPECT_RATIO; 
	}
	
}