import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Trộm Xoài 3D Subway Surfers", page_icon="🥭", layout="centered")

html_3d_code = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
    body { margin: 0; overflow: hidden; background: #2c3e50; font-family: 'Segoe UI', sans-serif; }
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
    <h1 style="color: #f1c40f; text-shadow: 3px 3px 6px #000; font-size: 30px;">🥭 TRỘM XOÀI: ĐƯỜNG LÀNG QUÊ 🏃</h1>
    <p style="font-size: 16px; padding: 0 30px; line-height: 1.6; max-width: 400px;">
        Bé Masha hái xoài bị phát hiện! Bà chủ và chú chó đang hung hãn đuổi theo phía sau trên con đường đá quen thuộc. Hãy né chướng ngại vật thật khéo léo nhé!
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
    let player, chaser, dog;
    let lanes = [-1.8, 0, 1.8];
    let currentLane = 1;
    let isJumping = false, jumpSpeed = 0;
    let score = 0, distance = 0, speed = 0.35;
    let obstacles = [], mangoes = [];
    let isGameStarted = false, isGameOver = false;

    // Load hình ảnh từ GitHub và bật chế độ trong suốt (Transparent) để cắt bỏ viền trắng
    const textureLoader = new THREE.TextureLoader();
    
    function loadTransparentTexture(url) {
        let tex = textureLoader.load(url);
        return tex;
    }

    const texMasha = loadTransparentTexture('https://raw.githubusercontent.com/yenphitruong-2508/game-trom-xoai/main/btap4.jpg');
    const texGranny = loadTransparentTexture('https://raw.githubusercontent.com/yenphitruong-2508/game-trom-xoai/main/btap3.jpg');
    const texDog = loadTransparentTexture('https://raw.githubusercontent.com/yenphitruong-2508/game-trom-xoai/main/btap5.jpg');
    const texRoad = textureLoader.load('https://raw.githubusercontent.com/yenphitruong-2508/game-trom-xoai/main/btap6.jpg');

    function init() {
        scene = new THREE.Scene();
        scene.background = new THREE.Color(0xa0d2eb);
        scene.fog = new THREE.FogExp2(0xa0d2eb, 0.02);

        camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.set(0, 3.0, 6.0);
        camera.rotation.x = -0.22;

        renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        let ambientLight = new THREE.AmbientLight(0xffffff, 1.0);
        scene.add(ambientLight);

        // Tạo mặt đường lấy từ ảnh btap6.jpg
        let roadGeo = new THREE.PlaneGeometry(10, 300);
        let roadMat = new THREE.MeshBasicMaterial({ map: texRoad });
        texRoad.wrapS = THREE.RepeatWrapping;
        texRoad.wrapT = THREE.RepeatWrapping;
        texRoad.repeat.set(1, 25);
        let road = new THREE.Mesh(roadGeo, roadMat);
        road.rotation.x = -Math.PI / 2;
        road.position.z = -100;
        scene.add(road);

        // Nhân vật Masha (Sprite trong suốt, cắt viền trắng)
        let matMasha = new THREE.SpriteMaterial({ map: texMasha, transparent: true, alphaTest: 0.1 });
        player = new THREE.Sprite(matMasha);
        player.scale.set(1.1, 1.6, 1);
        player.position.set(lanes[currentLane], 0.8, 0);
        scene.add(player);

        // Bà chủ nhà rượt đuổi phía sau
        let matGranny = new THREE.SpriteMaterial({ map: texGranny, transparent: true, alphaTest: 0.1 });
        chaser = new THREE.Sprite(matGranny);
        chaser.scale.set(1.3, 1.8, 1);
        chaser.position.set(lanes[currentLane], 0.9, 3.0);
        scene.add(chaser);

        // Chú chó chạy theo sau cùng bà chủ
        let matDog = new THREE.SpriteMaterial({ map: texDog, transparent: true, alphaTest: 0.1 });
        dog = new THREE.Sprite(matDog);
        dog.scale.set(0.9, 1.2, 1);
        dog.position.set(lanes[currentLane] + 0.8, 0.6, 2.8);
        scene.add(dog);

        window.addEventListener('keydown', (e) => {
            if (!isGameStarted) return;
            if (e.key === 'ArrowLeft') moveLeft();
            if (e.key === 'ArrowRight') moveRight();
            if (e.key === 'ArrowUp' || e.key === ' ') jump();
        });

        renderer.render(scene, camera);
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
            jumpSpeed = 0.22;
        }
    }

    function spawnObjects() {
        if (Math.random() < 0.04) {
            let laneIndex = Math.floor(Math.random() * 3);
            let obsGeo = new THREE.BoxGeometry(1.1, 0.7, 0.8);
            let obsMat = new THREE.MeshPhongMaterial({ color: 0x6d4c41 });
            let obs = new THREE.Mesh(obsGeo, obsMat);
            obs.position.set(lanes[laneIndex], 0.35, -60);
            scene.add(obs);
            obstacles.push(obs);
        }

        if (Math.random() < 0.07) {
            let laneIndex = Math.floor(Math.random() * 3);
            let mangoGeo = new THREE.SphereGeometry(0.35, 16, 16);
            let mangoMat = new THREE.MeshPhongMaterial({ color: 0xffd54f });
            let mango = new THREE.Mesh(mangoGeo, mangoMat);
            mango.position.set(lanes[laneIndex], 1.0, -60);
            scene.add(mango);
            mangoes.push(mango);
        }
    }

    function animate() {
        if (isGameOver || !isGameStarted) return;
        requestAnimationFrame(animate);

        distance += 0.2;
        document.getElementById('dist').innerText = Math.floor(distance);

        // Hiệu ứng cuộn đường đá trong ảnh
        texRoad.offset.y -= 0.02;

        // Di chuyển nhân vật mượt mà
        player.position.x += (lanes[currentLane] - player.position.x) * 0.25;
        chaser.position.x += (player.position.x - chaser.position.x) * 0.12;
        dog.position.x += (player.position.x + 0.7 - dog.position.x) * 0.12;

        // Xử lý nhảy
        if (isJumping) {
            player.position.y += jumpSpeed;
            jumpSpeed -= 0.015;
            if (player.position.y <= 0.8) {
                player.position.y = 0.8;
                isJumping = false;
            }
        }

        spawnObjects();

        // Va chạm chướng ngại vật
        for (let i = obstacles.length - 1; i >= 0; i--) {
            let obs = obstacles[i];
            obs.position.z += speed;

            if (Math.abs(obs.position.z - player.position.z) < 0.6 &&
                Math.abs(obs.position.x - player.position.x) < 0.5 &&
                player.position.y < 1.0) {
                endGame();
            }

            if (obs.position.z > 10) {
                scene.remove(obs);
                obstacles.splice(i, 1);
            }
        }

        // Ăn xoài
        for (let i = mangoes.length - 1; i >= 0; i--) {
            let m = mangoes[i];
            m.position.z += speed;
            m.rotation.y += 0.05;

            if (Math.abs(m.position.z - player.position.z) < 0.6 &&
                Math.abs(m.position.x - player.position.x) < 0.5) {
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
        
