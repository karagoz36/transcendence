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
	// Boundaries = [this.addBoundaries()];
    paddle1 = this.addPaddle(10, 0xff0000);
    paddle2 = this.addPaddle(-10, 0x0000ff);
    ball = this.addBall()
    controls = new OrbitControls(this.camera, this.renderer.domElement)
	score1 = 0;
	score2 = 0;

    constructor() {
        this.addLights()
        this.addShadow()
		this.addBoundaries()
        this.cameraControl()
        this.camera.position.z = 10;
        this.renderer.shadowMap.enabled = true;
        this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        document.querySelector("#pong-container")?.appendChild(this.renderer.domElement);
        this.renderer.setAnimationLoop(() => {
            this.controls.update()
            this.renderer.render(this.scene, this.camera)
        });
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
        const planeMaterial = new THREE.MeshBasicMaterial({ 
            color: 0x8c93ec,
            transparent: false 
        });
		const plane = new THREE.Mesh(planeBoundaries, planeMaterial);
	
		plane.position.z = -0.8;
        plane.receiveShadow = true;
        plane.castShadow = false;        
	
		this.scene.add(plane);
		return (plane);
	}

    addShadow() {
        const shadowPlaneGeometry = new THREE.PlaneGeometry(40, 40);
        const shadowPlaneMaterial = new THREE.ShadowMaterial({ opacity: 0.5 });  // Ombre douce
        const shadowPlane = new THREE.Mesh(shadowPlaneGeometry, shadowPlaneMaterial);
        shadowPlane.receiveShadow = true;
        this.scene.add(shadowPlane);
    }
	
    addBoundaries() {
        const radius = 0.4;
        const length = 20;
        const capSegments = 8;
        const radialSegments = 16;
    
        const boundGeometry = new THREE.CapsuleGeometry(radius, length, capSegments, radialSegments);
        // const boundMat = new THREE.MeshNormalMaterial();
        const boundMat = new THREE.MeshStandardMaterial({
            color: 0x8c93ec,
            emissive: 0x8c93ec,
            emissiveIntensity: 0.5,
            metalness: 2,
            roughness: 1,
            // transparent: false
        });
        const leftBound = new THREE.Mesh(boundGeometry, boundMat);
        leftBound.rotateZ(-Math.PI * 0.5) ;
        leftBound.position.y = -8.2;
        leftBound.position.z = 0.2;
        leftBound.castShadow = true;
    
        const rightBound = leftBound.clone();
        rightBound.position.y = 8.2;
        rightBound.castShadow = true;
    
        this.scene.add(leftBound, rightBound);
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
		const ambientLight = new THREE.AmbientLight(0xffffff, 0.3);
		const dirLight = new THREE.DirectionalLight(0xffffff, 1);
	
		dirLight.position.set(30, 20, 30);
        dirLight.target.position.set(0, 0, 0); 
		dirLight.castShadow = true;
        dirLight.shadow.mapSize.set(2048, 2048);
        dirLight.shadow.camera.near = 0.1;
        dirLight.shadow.camera.far = 100;
        dirLight.shadow.camera.left = -30;
        dirLight.shadow.camera.right = 30;
        dirLight.shadow.camera.top = 30;
        dirLight.shadow.camera.bottom = -30;
    
        dirLight.shadow.bias = 0.00;
	
		this.scene.add(dirLight, ambientLight);
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
        ball.castShadow = true;
        ball.receiveShadow = true;
        this.scene.add(ball);
        return ball;
    }

    /**
     * @param {number} position
     * @param {number} color
     */
    addPaddle(position, color) {
		const geometry = new THREE.CapsuleGeometry(0.25, 3, 20, 10);
        const material = new THREE.MeshStandardMaterial({ color });
        const neonMaterial = new THREE.MeshStandardMaterial({
            color,
            emissive: color,
            emissiveIntensity: 1.5,
        });
        const paddle = new THREE.Mesh(geometry, neonMaterial);
        paddle.position.x = position;
        paddle.castShadow = true;
        this.scene.add(paddle);
        return paddle;
    }

	onWindowResize = () => {
		const containerWidth = window.innerWidth;
		const containerHeight = window.innerHeight;
	
		const targetAspectRatio = this.ASPECT_RATIO;
		let width = containerWidth;
		let height = containerHeight;
	
		if (containerWidth / containerHeight > targetAspectRatio) {
			width = containerHeight * targetAspectRatio;
		} else {
			height = containerWidth / targetAspectRatio;
		}
	
		this.renderer.setSize(width, height);
	
		this.camera.aspect = width / height;
		this.camera.updateProjectionMatrix();
	
		const baseZoom = 20;
		this.camera.position.z = baseZoom / (this.camera.aspect);
	}
}