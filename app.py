import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Trộm Xoài Rượt Đuổi 3D", page_icon="🥭", layout="centered")

html_3d_code = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
    body { margin: 0; overflow: hidden; background: #1a1a2e; font-family: 'Segoe UI', sans-serif; }
    #ui {
        position: absolute; top: 12px; left: 12px;
        color: #fff; font-size: 18px; font-weight: bold;
        text-shadow: 2px 2px 4px #000; z-index: 10;
        background: rgba(0,0,0,0.6); padding: 8px 16px; border-radius: 20px;
        border: 1px solid #f1c40f;
    }
    #msg {
        position: absolute; top: 35%; width: 100%; text-align: center;
        color: #ffeb3b; font-size: 28px; font-weight: bold;
        text-shadow: 3px 3px 6px #000; display: none; z-index: 10;
        background: rgba(0,0,0,0.85); padding: 20px 0;
    }
    .controls {
        position: absolute; bottom: 20px; width: 100%;
        display: flex; justify-content: center; gap: 12px; z-index: 10;
    }
    .btn {
        background: linear-gradient(135deg, #f39c12, #e67e22);
        color: white; border: none; padding: 12px 22px;
        font-size: 16px; font-weight: bold; border-radius: 25px;
        cursor: pointer; box-shadow: 0 4px 10px rgba(0,0,0,0.5);
    }
    .btn-boost { background: linear-gradient(135deg, #e74c3c, #c0392b); }
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>

<div id="ui">🥭 Xoài: <span id="score" style="color:#f1c40f;">0</span> | 🏃 Quãng đường: <span id="dist" style="color:#2ecc71;">0</span>/100m</div>
<div id="msg">
    <span id="end-text">BÀ CHỦ & CHÓ BẮT ĐƯỢC RỒI!</span><br><br>
    <button class="btn" onclick="resetGame()">🎮 CHƠI LẠI</button>
</div>

<div class="controls">
    <button class="btn" onclick="moveLeft()">⬅️ TRÁI</button>
    <button class="btn btn-boost" onclick="jump()">🦘 NHẢY / BOOST</button>
    <button class="btn" onclick="moveRight()">PHẢI ➡️</button>
</div>

<script>
    let scene, camera, renderer;
    let player, chaser, dog;
    let lanes = [-2, 0, 2];
    let currentLane = 1;
    let isJumping = false, jumpSpeed = 0;
    let score = 0, distance = 0, speed = 0.35;
    let obstacles = [], mangoes = [];
    let isGameOver = false;

    // Load Texture ảnh từ GitHub của bạn
    const textureLoader = new THREE.TextureLoader();
    const texMasha = textureLoader.load('https://raw.githubusercontent.com/yenphitruong-2508/game-trom-xoai/main/btap4.jpg');
    const texGranny = textureLoader.load('https://raw.githubusercontent.com/yenphitruong-2508/game-trom-xoai/main/btap3.jpg');
    const texDog = textureLoader.load('https://raw.githubusercontent.com/yenphitruong-2508/game-trom-xoai/main/btap5.jpg');
    const texRoad = textureLoader.load('https://raw.githubusercontent.com/yenphitruong-2508/game-trom-xoai/main/btap6.jpg');

    function init() {
        scene = new THREE.Scene();
        scene.background = new THREE.Color(0x87ceeb);
        scene.fog = new THREE.Fog(0x87ceeb, 15, 60);

        camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.set(0, 3.5, 7);
        camera.rotation.x = -0.25;

        renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        // Ánh sáng
        let light = new THREE.DirectionalLight(0xffffff, 1.2);
        light.position.set(5, 10, 7);
        scene.add(light);
        scene.add(new THREE.AmbientLight(0x888888));

        // Mặt đường đất làng
        let roadGeo = new THREE.PlaneGeometry(10, 200);
        let roadMat = new THREE.MeshPhongMaterial({ map: texRoad });
        texRoad.wrapS = THREE.RepeatWrapping;
        texRoad.wrapT = THREE.RepeatWrapping;
        texRoad.repeat.set(1, 20);
        let road = new THREE.Mesh(roadGeo, roadMat);
        road.rotation.x = -Math.PI / 2;
        road.position.z = -80;
        scene.add(road);

        // Tạo Sprite Nhân vật Bé Masha
        let matMasha = new THREE.SpriteMaterial({ map: texMasha });
        player = new THREE.Sprite(matMasha);
        player.scale.set(1.2, 1.8, 1);
        player.position.set(lanes[currentLane], 0.9, 0);
        scene.add(player);

        // Tạo Sprite Bà chủ nhà
        let matGranny = new THREE.SpriteMaterial({ map: texGranny });
        chaser = new THREE.Sprite(matGranny);
        chaser.scale.set(1.4, 2.0, 1);
        chaser.position.set(lanes[currentLane], 1.0, 3.2);
        scene.add(chaser);

        // Bắt sự kiện phím
        window.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowLeft') moveLeft();
            if (e.key === 'ArrowRight') moveRight();
            if (e.key === 'ArrowUp' || e.key === ' ') jump();
        });

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
            let obsGeo = new THREE.BoxGeometry(1.2, 0.8, 1);
            let obsMat = new THREE.MeshPhongMaterial({ color: 0x8d6e63 });
            let obs = new THREE.Mesh(obsGeo, obsMat);
            obs.position.set(lanes[laneIndex], 0.4, -60);
            scene.add(obs);
            obstacles.push(obs);
        }

        if (Math.random() < 0.07) {
            let laneIndex = Math.floor(Math.random() * 3);
            let mangoGeo = new THREE.SphereGeometry(0.35, 16, 16);
            let mangoMat = new THREE.MeshPhongMaterial({ color: 0xffd54f });
            let mango = new THREE.Mesh(mangoGeo, mangoMat);
            mango.position.set(lanes[laneIndex], 1.1, -60);
            scene.add(mango);
            mangoes.push(mango);
        }
    }

    function animate() {
        if (isGameOver) return;
        requestAnimationFrame(animate);

        distance += 0.2;
        document.getElementById('dist').innerText = Math.floor(distance);

        // Cuộn nền con đường
        texRoad.offset.y -= 0.02;

        // Di chuyển mượt nhân vật
        player.position.x += (lanes[currentLane] - player.position.x) * 0.2;
        chaser.position.x += (player.position.x - chaser.position.x) * 0.1;

        // Xử lý nhảy
        if (isJumping) {
            player.position.y += jumpSpeed;
            jumpSpeed -= 0.015;
            if (player.position.y <= 0.9) {
                player.position.y = 0.9;
                isJumping = false;
            }
        }

        // Sinh vật phẩm
        spawnObjects();

        // Di chuyển chướng ngại vật
        for (let i = obstacles.length - 1; i >= 0; i--) {
            let obs = obstacles[i];
            obs.position.z += speed;

            if (Math.abs(obs.position.z - player.position.z) < 0.7 &&
                Math.abs(obs.position.x - player.position.x) < 0.6 &&
                player.position.y < 1.1) {
                endGame(false);
            }

            if (obs.position.z > 10) {
                scene.remove(obs);
                obstacles.splice(i, 1);
            }
        }

        // Di chuyển & Ăn Xoài
        for (let i = mangoes.length - 1; i >= 0; i--) {
            let m = mangoes[i];
            m.position.z += speed;
            m.rotation.y += 0.05;

            if (Math.abs(m.position.z - player.position.z) < 0.7 &&
                Math.abs(m.position.x - player.position.x) < 0.6) {
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

        if (distance >= 100) {
            endGame(true);
        }

        renderer.render(scene, camera);
    }

    function endGame(isWin) {
        isGameOver = true;
        document.getElementById('msg').style.display = 'block';
        if (isWin) {
            document.getElementById('end-text').innerHTML = "🎉 THẮNG RỰC RỠ!<br>Bé Masha đã ôm xoài chạy thoát!";
            document.getElementById('end-text').style.color = "#2ecc71";
        } else {
            document.getElementById('end-text').innerHTML = "😭 BỊ BẮT RỒI!<br>Bà chủ đã dùng dép vụt trúng Masha!";
            document.getElementById('end-text').style.color = "#e74c3c";
        }
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
