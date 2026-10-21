import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Trộm Xoài 3D Subway Surfers", page_icon="🥭", layout="centered")

html_3d_code = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
    body { margin: 0; overflow: hidden; background: #0f172a; font-family: 'Segoe UI', sans-serif; }
    #ui {
        position: absolute; top: 15px; left: 15px;
        color: #fff; font-size: 18px; font-weight: bold;
        text-shadow: 2px 2px 4px #000; z-index: 10;
        background: rgba(0,0,0,0.7); padding: 10px 20px; border-radius: 25px;
        border: 2px solid #f1c40f; display: none;
    }
    #start-screen {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background: linear-gradient(135deg, #1e293b, #0f172a); display: flex; flex-direction: column;
        justify-content: center; align-items: center; z-index: 20; color: white; text-align: center;
    }
    #msg {
        position: absolute; top: 35%; width: 100%; text-align: center;
        color: #ffeb3b; font-size: 26px; font-weight: bold;
        text-shadow: 3px 3px 6px #000; display: none; z-index: 10;
        background: rgba(0,0,0,0.9); padding: 25px 0; border-top: 3px solid #f1c40f; border-bottom: 3px solid #f1c40f;
    }
    .controls {
        position: absolute; bottom: 20px; width: 100%;
        display: none; justify-content: center; gap: 15px; z-index: 10;
    }
    .btn {
        background: linear-gradient(135deg, #f39c12, #e67e22);
        color: white; border: none; padding: 14px 28px;
        font-size: 18px; font-weight: bold; border-radius: 30px;
        cursor: pointer; box-shadow: 0 4px 15px rgba(0,0,0,0.6);
        transition: transform 0.1s;
    }
    .btn:active { transform: scale(0.95); }
    .btn-boost { background: linear-gradient(135deg, #e74c3c, #c0392b); }
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>

<!-- MÀN HÌNH CHỜ BẮT ĐẦU -->
<div id="start-screen">
    <h1 style="color: #f1c40f; text-shadow: 3px 3px 6px #000; font-size: 32px;">🥭 TRỘM XOÀI: CUỘC RƯỢT ĐUỔI 4D 🏃</h1>
    <p style="font-size: 16px; padding: 0 30px; line-height: 1.6; max-width: 400px;">
        Bé Masha hái xoài bị phát hiện! Không gian bao quanh sống động y hệt game rượt đuổi thực tế. Hãy né tránh chướng ngại vật thật khéo léo nhé!
    </p>
    <button class="btn btn-boost" onclick="startGame()">🚀 BẮT ĐẦU CHƠI NGAY</button>
</div>

<div id="ui">🥭 Xoài: <span id="score" style="color:#f1c40f;">0</span> | 🏃 Quãng đường: <span id="dist" style="color:#2ecc71;">0</span>m</div>
<div id="msg">
    <span id="end-text">😭 BỊ BẮT RỒI!</span><br><br>
    <button class="btn" onclick="resetGame()">🎮 CHƠI LẠI</button>
</div>

<div class="controls" id="game-controls">
    <button class="btn" onclick="moveLeft()">⬅️ TRÁI</button>
    <button class="btn btn-boost" onclick="jump()">🦘 NHẢY</button>
    <button class="btn" onclick="moveRight()">PHẢI ➡️</button>
</div>

<script>
    let scene, camera, renderer;
    let player, chaser;
    let lanes = [-2.2, 0, 2.2];
    let currentLane = 1;
    let isJumping = false, jumpSpeed = 0;
    let score = 0, distance = 0, speed = 0.4;
    let obstacles = [], mangoes = [], sceneryItems = [];
    let isGameStarted = false, isGameOver = false;

    // Load Texture hình ảnh từ GitHub
    const textureLoader = new THREE.TextureLoader();
    const texMasha = textureLoader.load('https://raw.githubusercontent.com/yenphitruong-2508/game-trom-xoai/main/btap4.jpg');
    const texGranny = textureLoader.load('https://raw.githubusercontent.com/yenphitruong-2508/game-trom-xoai/main/btap3.jpg');
    const texRoad = textureLoader.load('https://raw.githubusercontent.com/yenphitruong-2508/game-trom-xoai/main/btap6.jpg');
    const texHouse = textureLoader.load('https://raw.githubusercontent.com/yenphitruong-2508/game-trom-xoai/main/btap2.jpg');
    const texTree = textureLoader.load('https://raw.githubusercontent.com/yenphitruong-2508/game-trom-xoai/main/btap.jpg');

    function init() {
        scene = new THREE.Scene();
        scene.background = new THREE.Color(0x70a1ff);
        scene.fog = new THREE.FogExp2(0x70a1ff, 0.025);

        camera = new THREE.PerspectiveCamera(65, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.set(0, 3.2, 6.5);
        camera.rotation.x = -0.2;

        renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        // Ánh sáng môi trường 4D
        let ambientLight = new THREE.AmbientLight(0xffffff, 0.9);
        scene.add(ambientLight);
        let dirLight = new THREE.DirectionalLight(0xfffa65, 1.0);
        dirLight.position.set(10, 20, 10);
        scene.add(dirLight);

        // Mặt đường đất làng chính giữa
        let roadGeo = new THREE.PlaneGeometry(12, 300);
        let roadMat = new THREE.MeshPhongMaterial({ map: texRoad });
        texRoad.wrapS = THREE.RepeatWrapping;
        texRoad.wrapT = THREE.RepeatWrapping;
        texRoad.repeat.set(1, 30);
        let road = new THREE.Mesh(roadGeo, roadMat);
        road.rotation.x = -Math.PI / 2;
        road.position.z = -100;
        scene.add(road);

        // Tạo cảnh quan hai bên đường (Cây xoài & Nhà cửa bao quanh)
        for(let i = -120; i <= 20; i += 15) {
            createScenerySide(-7, i);
            createScenerySide(7, i);
        }

        // Nhân vật Bé Masha
        let matMasha = new THREE.SpriteMaterial({ map: texMasha });
        player = new THREE.Sprite(matMasha);
        player.scale.set(1.4, 2.0, 1);
        player.position.set(lanes[currentLane], 1.0, 0);
        scene.add(player);

        // Bà chủ nhà rượt đuổi phía sau
        let matGranny = new THREE.SpriteMaterial({ map: texGranny });
        chaser = new THREE.Sprite(matGranny);
        chaser.scale.set(1.6, 2.2, 1);
        chaser.position.set(lanes[currentLane], 1.1, 3.5);
        scene.add(chaser);

        window.addEventListener('keydown', (e) => {
            if (!isGameStarted) return;
            if (e.key === 'ArrowLeft') moveLeft();
            if (e.key === 'ArrowRight') moveRight();
            if (e.key === 'ArrowUp' || e.key === ' ') jump();
        });

        renderer.render(scene, camera);
    }

    function createScenerySide(xPos, zPos) {
        let mat = Math.random() > 0.5 ? new THREE.SpriteMaterial({ map: texTree }) : new THREE.SpriteMaterial({ map: texHouse });
        let obj = new THREE.Sprite(mat);
        obj.scale.set(4, 4, 1);
        obj.position.set(xPos, 2, zPos);
        scene.add(obj);
        sceneryItems.push(obj);
    }

    function startGame() {
        isGameStarted = true;
        document.getElementById('start-screen').style.display = 'none';
        document.getElementById('ui').style.display = 'block';
        document.getElementById('game-controls').style.display = 'flex';
        animate();
    }

    function moveLeft() { if (currentLane > 0 && !isGameOver) currentLane--; }
    function moveRight() { if (currentLane < 2 && !isGameOver) currentLane++; }
    function jump() {
        if (!isJumping && !isGameOver) {
            isJumping = true;
            jumpSpeed = 0.25;
        }
    }

    function spawnObjects() {
        if (Math.random() < 0.045) {
            let laneIndex = Math.floor(Math.random() * 3);
            let obsGeo = new THREE.BoxGeometry(1.3, 0.9, 1);
            let obsMat = new THREE.MeshPhongMaterial({ color: 0x8d6e63, shininess: 50 });
            let obs = new THREE.Mesh(obsGeo, obsMat);
            obs.position.set(lanes[laneIndex], 0.45, -70);
            scene.add(obs);
            obstacles.push(obs);
        }

        if (Math.random() < 0.08) {
            let laneIndex = Math.floor(Math.random() * 3);
            let mangoGeo = new THREE.SphereGeometry(0.4, 16, 16);
            let mangoMat = new THREE.MeshPhongMaterial({ color: 0xffd54f, emissive: 0x332200 });
            let mango = new THREE.Mesh(mangoGeo, mangoMat);
            mango.position.set(lanes[laneIndex], 1.2, -70);
            scene.add(mango);
            mangoes.push(mango);
        }
    }

    function animate() {
        if (isGameOver || !isGameStarted) return;
        requestAnimationFrame(animate);

        distance += 0.25;
        document.getElementById('dist').innerText = Math.floor(distance);

        // Hiệu ứng cuốn cảnh đường và phong cảnh xung quanh
        texRoad.offset.y -= 0.025;

        for(let item of sceneryItems) {
            item.position.z += speed;
            if(item.position.z > 15) item.position.z = -120;
        }

        // Di chuyển mượt nhân vật
        player.position.x += (lanes[currentLane] - player.position.x) * 0.25;
        chaser.position.x += (player.position.x - chaser.position.x) * 0.12;

        // Hiệu ứng nhảy
        if (isJumping) {
            player.position.y += jumpSpeed;
            jumpSpeed -= 0.016;
            if (player.position.y <= 1.0) {
                player.position.y = 1.0;
                isJumping = false;
            }
        }

        spawnObjects();

        // Xử lý chướng ngại vật
        for (let i = obstacles.length - 1; i >= 0; i--) {
            let obs = obstacles[i];
            obs.position.z += speed;

            if (Math.abs(obs.position.z - player.position.z) < 0.7 &&
                Math.abs(obs.position.x - player.position.x) < 0.65 &&
                player.position.y < 1.2) {
                endGame();
            }

            if (obs.position.z > 10) {
                scene.remove(obs);
                obstacles.splice(i, 1);
            }
        }

        // Xử lý ăn xoài
        for (let i = mangoes.length - 1; i >= 0; i--) {
            let m = mangoes[i];
            m.position.z += speed;
            m.rotation.y += 0.08;

            if (Math.abs(m.position.z - player.position.z) < 0.7 &&
                Math.abs(m.position.x - player.position.x) < 0.65) {
                score++;
                document.getElementById('score').innerText = score;
                scene.remove(m);
                mangoes.splice(i, 1);
            }

            if (m.position.z > 10) {
                scene.remove(m);
                mangoes.splice(i, 1);
            }
        }

        renderer.render(scene, camera);
    }

    function endGame() {
        isGameOver = true;
        document.getElementById('msg').style.display = 'block';
        document.getElementById('end-text').innerHTML = "😭 BỊ BẮT RỒI!<br>Bạn đã chạy được " + Math.floor(distance) + "m và hái được " + score + " quả xoài!";
    }

    function resetGame() {
        location.reload();
    }

    init();
</script>
</body>
</html>
"""

components.html(html_3d_code, height=650)
