import * as THREE from 'three';

// 背景星空球体半径
const BACKGROUND_STARS_RADIUS = 200;
// 地球球体的半径
const EARTH_RADIUS = 5;
// 太阳半径
const SUN_RADIUS = 1;
// 月球半径
const MOON_RADIUS = 0.5;
// 月球轨道半径const MOON_TRACK_RADIUS = EARTH_RADIUS * 2;
// 星星数量
const STARS_AMOUNT = 1000;
// 星星最小距离
const STARS_MIN_DISTANCE = 100;
// 星星最大距离
const STARS_MAX_DISTANCE = 200;

class AssetsLoader {
    private assets: { [key: string]: THREE.Texture } = {};

    load(assets: { type: string; name: string; path: string }[]) {
        const loader = new THREE.TextureLoader();
        let loadedCount = 0;
        assets.forEach((asset) => {
            interface AssetItem {
                type: string;
                name: string;
                path: string;
            }

            loader.load(asset.path, (texture: THREE.Texture) => {
                this.assets[asset.name] = texture;
                loadedCount++;
                if (loadedCount === assets.length) {
                    this.dispatchEvent({ type: 'onLoad' });
                }
            });
        });
    }

    getAssets(name: string): THREE.Texture | undefined {
        return this.assets[name];
    }

    private eventListeners: { [key: string]: () => void } = {};

    addEventListener(type: string, callback: () => void) {
        this.eventListeners[type] callback;
    }

    dispatchEvent(event: { type: string }) {
        if (this.eventListeners[event.type]) {
            this.eventListeners[event.type]();
        }
    }
}

class Earth {
    private scene: THREE.Scene;
    private camera: THREE.PerspectiveCamera;
    private renderer: THREE.WebGLRenderer;
    private assetsLoader: AssetsLoader;
    private clock: THREE.Clock;
    private sunPosition: THREE.Vector3;
    private moonPosition: THREE.Vector3;
    private earthMaterial: THREE.ShaderMaterial | undefined;
    private sunMesh: THREE.Mesh | undefined;
    private starMaterial: THREE.ShaderMaterial | undefined;

    constructor() {
        this.scene = new THREE.Scene();
        this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        this.renderer = new THREE.WebGLRenderer();
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(this.renderer.domElement);
        this.assetsLoader = new AssetsLoader();
        this.assetsLoader.load([
            {
                type: 'Texture',
                name: 'sun', // 太阳贴图
                path: '/images/earth/8k_sun.jpg',
            },
            {
                type: 'Texture',
                name: 'moon', // 月球贴图
                path: '/images/earth/8k_moon.jpg',
            },
            {
                type: 'Texture',
                name: 'stars', // 星空背景贴图
                path: '/images/earth/8k_stars_milky_way.jpg',
            },
            {
                type: 'Texture',
                name: 'dayTexture', // 白天贴图
                path: '/images/earth/8k_earth_daymap.jpg',
            },
            {
                type: 'Texture',
                name: 'nightTexture', // 夜晚贴图
                path: '/images/earth/8k_earth_nightmap.jpg',
            },
            {
                type: 'Texture',
                name: 'normalMap', // 法线贴图
                path: '/images/earth/8k_earth_normal_map.jpg',
            },
            {
                type: 'Texture',
                name: 'clouds', // 云层贴图
                path: '/images/earth/earth_clouds_2048.png',
            },
        ]);
        this.assetsLoader.addEventListener('onLoad', () => {
            this.initMesh();
        });
        this.clock = new THREE.Clock();
        this.sunPosition = new THREE.Vector3(20, 10, 0);
        this.moonPosition = new THREE.Vector3(0, MOON_TRACK_RADIUS, 0);
    }

    initMesh() {
        this.initEarth();
        this.initSun();
        this.initStarBackground();
        this.initMoon();
        this.initStars();
        this.animate();
    }

    initEarth() {
        const dayTexture = this.assetsLoader.getAssets('dayTexture');
        const nightTexture = this.assetsLoader.getAssets('nightTexture');
        if (dayTexture && nightTexture) {
            const earthMaterial = new THREE.ShaderMaterial({
                uniforms: {
                    dayTexture: { value: dayTexture },
                    nightTexture: { value: nightTexture },
                    sunPosition: { value: this.sunPosition },
                    transitionWidth: { value: 0.2 },
                },
                vertexShader: `
                  // 纹理坐标
                  varying vec2 vUv;
                  // 变换后的法线向量
                  varying vec3 vNormal;

                  void main(){
                      vUv=uv;
                      vNormal=normalize(normalMatrix*normal);
                      gl_Position= projectionMatrix * modelViewMatrix * vec4(position, 1.0);
                  }
                `,
                fragmentShader: `
                  #ifdef GL_ES
                  precision mediump float;
                  #endif

                  uniform sampler2D dayTexture;
                  uniform sampler2D nightTexture;
                  uniform vec3 sunPosition;
                  uniform float transitionWidth;

                  varying vec2 vUv;
                  varying vec3 vNormal;

                  void main(){
                      vec3 lightDir=normalize(sunPosition);
                      float dotProduct=dot(normalize(vNormal),lightDir);
                      float transitionCenter = 0.0; // 晨昏线
                      float transitionStart = transitionCenter - transitionWidth * 0.5;
                      float transitionEnd = transitionCenter + transitionWidth * 0.5;
                      float mixFactor = smoothstep(transitionStart, transitionEnd, dotProduct);
                      vec4 dayColor = texture2D(dayTexture, vUv);
                      vec4 nightColor = texture2D(nightTexture, vUv);
                      gl_FragColor = mix(nightColor, dayColor, mixFactor);
                  }
                `,
            });

            const earthGeometry = new THREE.SphereGeometry(EARTH_RADIUS, 128, 128);
            const earthMesh = new THREE.Mesh(earthGeometry, earthMaterial);
            earthMesh.position.set(0, 0, 0);
            this.scene.add(earthMesh);
            this.earthMaterial = earthMaterial;
        }
    }

    initSun() {
        const sunTexture = this.assetsLoader.getAssets('sun');
        if (sunTexture) {
            const sunGeometry = new THREE.SphereGeometry(SUN_RADIUS, 32, 32);
            const sunMaterial = new THREE.MeshBasicMaterial({
                map: sunTexture,
            });
            const sun = new THREE.Mesh(sunGeometry, sunMaterial);
            sun.position.copy(this.sunPosition);
            this.scene.add(sun);
            this.sunMesh = sun;
        }
    }

    rotateVector3ByRadian(vec3: THREE.Vector3, axis: THREE.Vector3, radian: number) {
        const matrix = new THREE.Matrix4();
        matrix.makeRotationAxis(axis.normalize(), radian);
        vec3.applyMatrix4(matrix);
    }

    initStarBackground() {
        const starsTexture = this.assetsLoader.getAssets('stars');
        if (starsTexture) {
            const sphereGeometry = new THREE.SphereGeometry(
                BACKGROUND_STARS_RADIUS,
                64,
                64
            );
            sphereGeometry.scale(-1, 1, 1);
            const sphereMaterial = new THREE.MeshBasicMaterial({
                map: starsTexture,
                side: THREE.DoubleSide,
            });
            const sphere = new THREE.Mesh(sphereGeometry, sphereMaterial);
            this.scene.add(sphere);
        }
    }

    initMoon() {
        const group = new THREE.Group();
        const trackGeo = new THREE.TorusGeometry(MOON_TRACK_RADIUS, 0.01, 64, 64);
        const trackMt = new THREE.MeshBasicMaterial({
            color: 0xffffff,
            transparent: true,
            opacity: 0.5,
        });
        const track = new THREE.Mesh(trackGeo, trackMt);
        group.add(track);
        const moonGeo = new THREE.SphereGeometry(MOON_RADIUS, 64, 64);
        const moonTexture = this.assetsLoader.getAssets('moon');
        const moonMt = new THREE.MeshBasicMaterial({
            map: moonTexture,
        });
        const moon = new THREE.Mesh(moonGeo, moonMt);
        moon.position.copy(this.moonPosition);
        group.add(moon);
        group.rotateX(THREE.MathUtils.degToRad(100));
        this.scene.add(group);
    }

    initStars() {
        const starGeometry = new THREE.BufferGeometry();
        const positions = new Float32Array(STARS_AMOUNT * 3);
        const colors = new Float32Array(STARS_AMOUNT * 3);
        const sizes = new Float32Array(STARS_AMOUNT);
        const phases = new Float32Array(STARS_AMOUNT);
        const frequencies = new Float32Array(STARS_AMOUNT);

        for (let i = 0; i < STARS_AMOUNT; i++) {
            const i3 = i * 3;
            const distance = this.getRandomInt(STARS_MIN_DISTANCE, STARS_MAX_DISTANCE);
            const theta = Math.random() * Math.PI * 2; // 方位角
            const phi = Math.acos(2 * Math.random() - 1); // 极角

            positions[i3] = distance * Math.sin(phi) * Math.cos(theta);
            positions[i3 + 1] = distance * Math.sin(phi) * Math.sin(theta);
            positions[i3 + 2] = distance * Math.cos(phi);

            const colorChoice = Math.random();
            if (colorChoice < 0.7) {
                colors[i3] = 1.0; // R
                colors[i3 + 1] = 0.9 + Math.random() * 0.1; // G
                colors[i3 + 2] = 0.8 + Math.random() * 0.2; // B
            } else if (colorChoice < 0.9) {
                colors[i3] = 0.4 + Math.random() * 0.3; // R
                colors[i3 + 1] = 0.6 + Math.random() * 0.3; // G
                colors[i3 + 2] = 1.0; // B
            } else {
                colors[i3] = 1.0; // R
                colors[i3 + 1] = 0.5 + Math.random() * 0.3; // G
                colors[i3 + 2] = 0.3 + Math.random() * 0.2; // B
            }

            sizes[i] = Math.random() * 2 + 0.5;
            frequencies[i] = Math.random() * 0.5 + 0.5;
            phases[i] = Math.random() * Math.PI * 2;
        }

        starGeometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        starGeometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
        starGeometry.setAttribute('size', new THREE.BufferAttribute(sizes, 1));
        starGeometry.setAttribute('phase', new THREE.BufferAttribute(phases, 1));
        starGeometry.setAttribute('frequency', new THREE.BufferAttribute(frequencies, 1));

        const starMaterial = new THREE.ShaderMaterial({
            uniforms: {
                time: { value: 0.0 },
            },
            vertexShader: `
              attribute float size;
              attribute vec3 color;
              attribute float phase;
              attribute float frequency;

              varying vec3 vColor;

              uniform float time;

              void main() {
                  vColor = color;
                  float blink = sin(time * frequency + phase) * 0.5 + 0.8;
                  float noise = sin(dot(position, vec3(12.9898, 78.233, 45.5432)) * 43758.5453) * 0.1;
                  float finalSize = size * (blink + noise);
                  vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);
                  gl_PointSize = finalSize * (300.0 / -mvPosition.z);
                  gl_Position = projectionMatrix * mvPosition;
              }
            `,
            fragmentShader: `
              #ifdef GL_ES
              precision mediump float;
              #endif

              varying vec3 vColor;

              void main() {
                  float distanceToCenter = length(gl_PointCoord - vec2(0.5));
                  if (distanceToCenter > 0.5) {
                      discard;
                  }
                  float alpha = 1.0 - smoothstep(0.0, 0.5, distanceToCenter);
                  gl_FragColor = vec4(vColor, alpha * 0.9);
              }
            `,
            transparent: true,
            blending: THREE.AdditiveBlending,
        });
        const stars = new THREE.Points(starGeometry, starMaterial);
        this.scene.add(stars);
        this.starMaterial = starMaterial;
    }

    render() {
        const elapsedTime = this.clock.getElapsedTime();
        this.rotateVector3ByRadian(
            this.sunPosition,
            new THREE.Vector3(0, 1, 0),
            0.0004
        );
        if (this.sunMesh) {
            this.sunMesh.position.copy(this.sunPosition);
            this.sunMesh.rotation.y += 0.002;
        }
        if (this.earthMaterial) {
            this.earthMaterial.uniforms.sunPosition.value.copy(this.sunPosition);
        }
        if (this.starMaterial) {
            this.starMaterial.uniforms.time.value = elapsedTime;
        }

        this.renderer.render(this.scene, this.camera);
    }

    animate() {
        requestAnimationFrame(() => this.animate());
        this.render();
    }

    private getRandomInt(min: number, max: number) {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    }
}

const earth = new Earth();
