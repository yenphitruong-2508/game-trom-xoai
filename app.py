import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Trộm Xoài 3D Subway Surfers", page_icon="🥭", layout="centered")

html_3d_code = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
    body { margin: 0; overflow: hidden; background: #000; font-family: sans-serif; }
    #ui {
        position: absolute; top: 10px; left: 10px;
        color: #fff; font-size: 20px; font-weight: bold;
        text-shadow: 2px 2px 4px #000; z-index: 10;
    }
    #msg {
        position: absolute; top: 40%; width: 100%; text-align: center;
        color: #ffeb3b; font-size: 32px; font-weight: bold;
        text-shadow: 3px 3px 6px #000; display: none; z-index: 10;
    }
    .controls {
        position: absolute; bottom: 20px; width: 100%;
        display: flex; justify-content: center; gap: 15px; z-index: 10;
    }
    .btn {
        background: #ff9800; color: white; border: none;
        padding: 12px 24px; font-size: 18px; font-weight: bold;
        border-radius: 30px; cursor: pointer; box-shadow: 0 4px 10px rgba(0,0,0,0.5);
    }
    .btn-boost { background: #f44336; }
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>

<div id="ui">🥭 Xoài: <span id="score">0</span> | 🏃 Quãng đường: <span id="dist">0</span>m</div>
<div id="msg">BÀ CHỦ & CHÓ BẮT ĐƯỢC RỒI!<br><br><button class="btn" onclick="resetGame()">🎮 CHƠI LẠI</button></div>

<div class="controls">
    <button class="btn" onclick="moveLeft()">⬅️ TRÁI</button>
    <button class="btn btn-boost" onclick="jump()">🦘 NHẢY</button>
    <button class="btn" onclick="moveRight()">PHẢI ➡️</button>
</div>

<script>
    let scene, camera, renderer;
    let player, chaser, dog;
    let lanes = [-2, 0, 2];
    let currentLane = 1;
    let isJumping = false, jumpSpeed = 0;
    let score = 0, distance = 0, speed = 0.3;
    let obstacles = [], mangoes = [];
    let isGameOver = false;

    function init() {
        scene = new THREE.Scene();
        scene.background = new THREE.Color(0x87ceeb);
        scene.fog = new THREE.Fog(0x87ceeb, 20, 80);

        camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.set(0, 4, 8);
        camera.rotation.x = -0.3;

        renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        // Ánh sáng
        let light = new THREE.DirectionalLight(0xffffff, 1);
        light.position.set(5, 10, 7);
        scene.add(light);
        scene.add(new THREE.AmbientLight(0x666666));

        // Con đường 3D
        let roadGeo = new THREE.PlaneGeometry(8, 200);
        let roadMat = new THREE.MeshPhongMaterial({ color: 0x555555 });
        let road = new THREE.Mesh(roadGeo, roadMat);
        road.rotation.x = -Math.PI / 2;
        road.position.z = -80;
        scene.add(road);

        // Đường ray / Làn đường
        for (let i = -2; i <= 2; i += 2) {
            let railGeo = new THREE.BoxGeometry(0.1, 0.1, 200);
            let railMat = new THREE.MeshBasicMaterial({ color: 0xaaaaaa });
            let rail = new THREE.Mesh(railGeo, railMat);
            rail.position.set(i, 0.05, -80);
            scene.add(rail);
        }

        // Nhân vật chính (Bé Masha - Khối 3D đại diện)
        let playerGeo = new THREE.BoxGeometry(0.8, 1.4, 0.8);
        let playerMat = new THREE.MeshPhongMaterial({ color: 0x9c27b0 }); // Màu tím áo Masha
        player = new THREE.Mesh(playerGeo, playerMat);
        player.position.set(lanes[currentLane], 0.7, 0);
        scene.add(player);

        // Bà chủ nhà đuổi theo sau
        let chaserGeo = new THREE.BoxGeometry(1, 1.6, 1);
        let chaserMat = new THREE.MeshPhongMaterial({ color: 0x2196f3 });
        chaser = new THREE.Mesh(chaserGeo, chaserMat);
        chaser.position.set(lanes[currentLane], 0.8, 3.5);
        scene.add(chaser);

        // Con chó chạy bên cạnh bà chủ
        let dogGeo = new THREE.BoxGeometry(0.6, 0.6, 0.9);
        let dogMat = new THREE.MeshPhongMaterial({ color: 0xff9800 });
        dog = new THREE.Mesh(dogGeo, dogMat);
        dog.position.set(lanes[currentLane] + 0.8, 0.3, 3.2);
        scene.add(dog);

        // Bắt sự kiện bàn phím
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
            jumpSpeed = 0.25;
        }
    }

    function spawnObjects() {
        if (Math.random() < 0.05) {
            let laneIndex = Math.floor(Math.random() * 3);
            let obsGeo = new THREE.BoxGeometry(1.2, 1, 1);
            let obsMat = new THREE.MeshPhongMaterial({ color: 0x795548 });
            let obs = new THREE.Mesh(obsGeo, obsMat);
            obs.position.set(lanes[laneIndex], 0.5, -60);
            scene.add(obs);
            obstacles.push(obs);
        }

        if (Math.random() < 0.08) {
            let laneIndex = Math.floor(Math.random() * 3);
            let mangoGeo = new THREE.SphereGeometry(0.3, 16, 16);
            let mangoMat = new THREE.MeshPhongMaterial({ color: 0xffeb3b });
            let mango = new THREE.Mesh(mangoGeo, mangoMat);
            mango.position.set(lanes[laneIndex], 1, -60);
            scene.add(mango);
            mangoes.push(mango);
        }
    }

    function animate() {
        if (isGameOver) return;
        requestAnimationFrame(animate);

        distance += 0.2;
        document.getElementById('dist').innerText = Math.floor(distance);

        // Cập nhật vị trí nhân vật (Di chuyển mượt giữa các làn)
        player.position.x += (lanes[currentLane] - player.position.x) * 0.2;
        chaser.position.x += (player.position.x - chaser.position.x) * 0.1;
        dog.position.x += (player.position.x + 0.8 - dog.position.x) * 0.1;

        // Xử lý Nhảy
        if (isJumping) {
            player.position.y += jumpSpeed;
            jumpSpeed -= 0.015;
            if (player.position.y <= 0.7) {
                player.position.y = 0.7;
                isJumping = false;
            }
        }

        // Camera đi theo nhân vật
        camera.position.x = player.position.x * 0.5;

        // Sinh chướng ngại vật & Xoài
        spawnObjects();

        // Di chuyển Chướng ngại vật
        for (let i = obstacles.length - 1; i >= 0; i--) {
            let obs = obstacles[i];
            obs.position.z += speed;

            // Va chạm Chướng ngại vật
            if (Math.abs(obs.position.z - player.position.z) < 0.8 &&
                Math.abs(obs.position.x - player.position.x) < 0.6 &&
                player.position.y < 1.0) {
                endGame();
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

            if (Math.abs(m.position.z - player.position.z) < 0.8 &&
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

        renderer.render(scene, camera);
    }

    function endGame() {
        isGameOver = true;
        document.getElementById('msg').style.display = 'block';
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
