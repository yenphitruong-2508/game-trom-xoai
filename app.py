import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Trộm xoài nhà bà hàng xóm", page_icon="🥭", layout="wide")

html_code = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
    body { margin: 0; padding: 0; overflow: hidden; background: #0b0f19; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; text-align: center; color: white; user-select: none; }
    #game-container {
        position: relative;
        width: 100%;
        max-width: 960px;
        height: 540px;
        margin: 10px auto;
        border: 4px solid #f1c40f;
        border-radius: 16px;
        overflow: hidden;
        background-color: #000;
        box-shadow: 0 12px 35px rgba(0,0,0,0.9);
    }
    .scene {
        position: absolute;
        width: 100%;
        height: 100%;
        top: 0; left: 0;
        display: none;
        background-size: cover;
        background-position: center;
    }
    .active { display: block; }
    
    .btn {
        background: linear-gradient(135deg, #f39c12, #e67e22);
        color: white; border: none; padding: 14px 32px;
        font-size: 18px; font-weight: bold; border-radius: 30px;
        cursor: pointer; box-shadow: 0 4px 12px rgba(0,0,0,0.5);
        margin: 4px; transition: transform 0.1s, background 0.2s;
    }
    .btn:active { transform: scale(0.92); }
    
    .dialog-box {
        position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%); width: 75%;
        background: rgba(0,0,0,0.85); border: 2px solid #f1c40f;
        border-radius: 12px; padding: 15px; box-sizing: border-box;
    }

    /* Hiệu ứng tách viền trắng giữ nguyên màu nhân vật bằng CSS mix-blend-mode */
    .sprite-img {
        mix-blend-mode: multiply;
        filter: contrast(110%) brightness(105%);
    }

    #chase3d { width: 100%; height: 100%; }
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>

<div id="game-container">
    <!-- CẢNH 1: LÉN HÁI 8 QUẢ XOÀI Ở CÂY GÓC TRÁI -->
    <div id="scene1" class="scene active" style="background-image: url('https://raw.githubusercontent.com/yenphitruong-2508/game-trom-xoai/main/btap2.jpg');">
        <div style="background: rgba(0,0,0,0.6); padding: 8px; font-weight: bold; font-size: 20px; color: #f1c40f;">
            🥭 TRỘM XOÀI NHÀ BÀ HÀNG XÓM
        </div>
        
        <!-- Chùm xoài tập trung trên cây góc trái -->
        <div id="mango-cluster" style="position: absolute; top: 80px; left: 100px; font-size: 26px; z-index: 3; text-shadow: 2px 2px 4px #000;">🥭🥭🥭🥭🥭🥭🥭🥭</div>
        
        <!-- Bé Masha trèo cây góc trái -->
        <img id="masha-climb" class="sprite-img" src="https://raw.githubusercontent.com/yenphitruong-2508/game-trom-xoai/main/btap4.jpg" style="position: absolute; top: 110px; left: 130px; width: 85px; z-index: 4; transition: transform 0.15s;">
        
        <!-- Chú chó nằm ngủ dưới gốc cây -->
        <img id="dog-sleep" class="sprite-img" src="https://raw.githubusercontent.com/yenphitruong-2508/game-trom-xoai/main/btap5.jpg" style="position: absolute; bottom: 100px; right: 180px; width: 95px; z-index: 4; transition: transform 0.3s;">
        
        <!-- Bà hàng xóm (Ẩn ban đầu, tự xông ra khi đủ 8 quả) -->
        <img id="granny-appear" class="sprite-img" src="https://raw.githubusercontent.com/yenphitruong-2508/game-trom-xoai/main/btap3.jpg" style="position: absolute; bottom: 90px; left: 60px; width: 110px; display: none; z-index: 4;">

        <div class="dialog-box">
            <div id="status-text" style="color: #f1c40f; font-weight: bold; margin-bottom: 10px; font-size: 18px;">
                Đã hái: <span id="picked-count" style="color:#2ecc71;">0</span> / 8 quả xoài
            </div>
            <button id="pick-btn" class="btn" onclick="pickMango()">Hái xoài (đừng để bị phát hiện)</button>
        </div>
    </div>

    <!-- CẢNH 2: RƯỢT ĐUỔI 4D -->
    <div id="scene2" class="scene">
        <div id="chase3d"></div>
        <div style="position: absolute; top: 15px; left: 15px; background: rgba(0,0,0,0.8); padding: 8px 18px; border-radius: 20px; text-align: left; font-size: 15px; border: 2px solid #f1c40f; z-index: 10;">
            🥭 Xoài: <span id="mango-count" style="color:#f1c40f; font-weight:bold;">8</span> | 
            🏃 Quãng đường: <span id="dist-count" style="color:#2ecc71; font-weight:bold;">0</span>m
        </div>
        
        <div style="position: absolute; bottom: 15px; width: 100%; display: flex; justify-content: center; gap: 15px; z-index: 10;">
            <button class="btn" onclick="moveLeft()">⬅️ TRÁI</button>
            <button class="btn" style="background:#e74c3c;" onclick="jump()">🦘 NHẢY / NÉ</button>
            <button class="btn" onclick="moveRight()">PHẢI ➡️</button>
        </div>
    </div>

    <!-- CẢNH KẾT THÚC -->
    <div id="scene-end" class="scene" style="background: #000; padding-top: 130px;">
        <h1 style="color:#e74c3c; font-size: 32px;">😭 BỊ BẮT RỒI!</h1>
        <p id="end-desc" style="font-size: 18px; padding: 0 30px; line-height: 1.6; color:#eee;"></p>
        <button class="btn" onclick="location.reload()">🔄 Chơi lại từ đầu</button>
    </div>
</div>

<script>
    let pickedMangoes = 0;

    // Phát âm thanh tiếng sủa và rượt đuổi
    function playSound(type) {
        try {
            let audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            let osc = audioCtx.createOscillator();
            let gain = audioCtx.createGain();
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            
            if (type === 'bark') {
                osc.type = 'sawtooth';
                osc.frequency.setValueAtTime(160, audioCtx.currentTime);
                osc.frequency.exponentialRampToValueAtTime(70, audioCtx.currentTime + 0.2);
                gain.gain.setValueAtTime(0.4, audioCtx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.22);
                osc.start();
                osc.stop(audioCtx.currentTime + 0.22);
            } else if (type === 'chase') {
                osc.type = 'triangle';
                osc.frequency.setValueAtTime(280, audioCtx.currentTime);
                osc.frequency.linearRampToValueAtTime(480, audioCtx.currentTime + 0.3);
                gain.gain.setValueAtTime(0.25, audioCtx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.32);
                osc.start();
                osc.stop(audioCtx.currentTime + 0.32);
            }
        } catch(e) {}
    }

    function pickMango() {
        if (pickedMangoes >= 8) return;
        
        pickedMangoes++;
        document.getElementById('picked-count').innerText = pickedMangoes;
        
        // Hiệu ứng nhún trèo cây khi bấm
        let masha = document.getElementById('masha-climb');
        masha.style.transform = "translateY(-12px) scale(1.08)";
        setTimeout(() => { masha.style.transform = "translateY(0) scale(1)"; }, 120);

        // Giảm dần các quả xoài trên cây ở góc trái
        let mangoIcons = "🥭".repeat(Math.max(0, 8 - pickedMangoes));
        document.getElementById('mango-cluster').innerText = mangoIcons;

        if (pickedMangoes < 8) {
            document.getElementById('status-text').innerHTML = "Đã hái: <span style='color:#2ecc71;'>" + pickedMangoes + "</span> / 8 quả xoài";
        } else {
            // Đủ 8 quả -> Phát tiếng sủa, bà hàng xóm chạy ra và tự động chuyển cảnh rượt đuổi
            playSound('bark');
            document.getElementById('status-text').innerHTML = "🐕 <b style='color:#e74c3c;'>GÂU GÂU!</b> Chó sủa ầm ĩ! Bà hàng xóm xông ra đuổi bắt!";
            document.getElementById('pick-btn').style.display = 'none';
            document.getElementById('dog-sleep').style.transform = "scale(1.25) rotate(18deg)";
            document.getElementById('granny-appear').style.display = "block";
            
            setTimeout(() => {
                playSound('chase');
                start4DChase();
            }, 1400);
        }
    }

    // KHÔNG GIAN 4D THREE.JS RƯỢT ĐUỔI
    let scene, camera, renderer;
    let player, chaser, dog;
    let lanes = [-2.0, 0, 2.0];
    let currentLane = 1;
    let isJumping = false, jumpSpeed = 0;
    let distance = 0, speed = 0.42;
    let obstacles = [];
    let isGameOver = false;

    const textureLoader = new THREE.TextureLoader();
    const texMasha = textureLoader.load('https://raw.githubusercontent.com/yenphitruong-2508/game-trom-xoai/main/btap4.jpg');
    const texGranny = textureLoader.load('https://raw.githubusercontent.com/yenphitruong-2508/game-trom-xoai/main/btap3.jpg');
    const texDog = textureLoader.load('https://raw.githubusercontent.com/yenphitruong-2508/game-trom-xoai/main/btap5.jpg');
    const texVillageBg = textureLoader.load('https://raw.githubusercontent.com/yenphitruong-2508/game-trom-xoai/main/btap6.jpg');

    function start4DChase() {
        document.getElementById('scene1').classList.remove('active');
        document.getElementById('scene2').classList.add('active');
        document.getElementById('mango-count').innerText = pickedMangoes;
        init4D();
    }

    function init4D() {
        let container = document.getElementById('chase3d');
        scene = new THREE.Scene();
        scene.background = texVillageBg;

        camera = new THREE.PerspectiveCamera(60, container.clientWidth / container.clientHeight, 0.1, 1000);
        camera.position.set(0, 3.0, 6.2);
        camera.rotation.x = -0.22;

        renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(container.clientWidth, container.clientHeight);
        container.appendChild(renderer.domElement);

        let ambientLight = new THREE.AmbientLight(0xffffff, 1.2);
        scene.add(ambientLight);

        // Mặt đường chạy chính giữa màu xám
        let roadGeo = new THREE.PlaneGeometry(8.5, 300);
        let roadMat = new THREE.MeshBasicMaterial({ color: 0x6e6e6e });
        let road = new THREE.Mesh(roadGeo, roadMat);
        road.rotation.x = -Math.PI / 2;
        road.position.z = -100;
        scene.add(road);

        // Tạo Sprite nhân vật với alphaTest
        let matMasha = new THREE.SpriteMaterial({ map: texMasha, transparent: true, alphaTest: 0.2 });
        player = new THREE.Sprite(matMasha);
        player.scale.set(1.3, 1.8, 1);
        player.position.set(lanes[currentLane], 0.9, 0);
        scene.add(player);

        let matGranny = new THREE.SpriteMaterial({ map: texGranny, transparent: true, alphaTest: 0.2 });
        chaser = new THREE.Sprite(matGranny);
        chaser.scale.set(1.5, 2.0, 1);
        chaser.position.set(lanes[currentLane], 1.0, 3.2);
        scene.add(chaser);

        let matDog = new THREE.SpriteMaterial({ map: texDog, transparent: true, alphaTest: 0.2 });
        dog = new THREE.Sprite(matDog);
        dog.scale.set(1.0, 1.3, 1);
        dog.position.set(lanes[currentLane] + 0.8, 0.65, 3.0);
        scene.add(dog);

        window.addEventListener('keydown', (e) => {
            if (isGameOver) return;
            if (e.key === 'ArrowLeft') moveLeft();
            if (e.key === 'ArrowRight') moveRight();
            if (e.key === 'ArrowUp' || e.key === ' ') jump();
        });

        animate4D();
    }

    function moveLeft() { if (currentLane > 0 && !isGameOver) currentLane--; }
    function moveRight() { if (currentLane < 2 && !isGameOver) currentLane++; }
    function jump() {
        if (!isJumping && !isGameOver) {
            isJumping = true;
            jumpSpeed = 0.23;
        }
    }

    // Chướng ngại vật: Cục đá, viên gạch, bụi cỏ, khúc gỗ
    const obsTypes = ['🪨 Cục đá', '🧱 Viên gạch', '🌿 Bụi cỏ', '🪵 Khúc gỗ'];

    function spawnObstacles() {
        if (Math.random() < 0.045) {
            let laneIndex = Math.floor(Math.random() * 3);
            let chosenObs = obsTypes[Math.floor(Math.random() * obsTypes.length)];
            let obsGeo = new THREE.BoxGeometry(1.2, 0.7, 0.9);
            let obsMat = new THREE.MeshPhongMaterial({ color: chosenObs.includes('gạch') ? 0xb7410e : 0x555555 });
            let obs = new THREE.Mesh(obsGeo, obsMat);
            obs.position.set(lanes[laneIndex], 0.35, -65);
            scene.add(obs);
            obstacles.push(obs);
        }
    }

    function animate4D() {
        if (isGameOver) return;
        requestAnimationFrame(animate4D);

        distance += 0.25;
        document.getElementById('dist-count').innerText = Math.floor(distance);

        player.position.x += (lanes[currentLane] - player.position.x) * 0.25;
        chaser.position.x += (player.position.x - chaser.position.x) * 0.12;
        dog.position.x += (player.position.x + 0.7 - dog.position.x) * 0.12;

        if (isJumping) {
            player.position.y += jumpSpeed;
            jumpSpeed -= 0.015;
            if (player.position.y <= 0.9) {
                player.position.y = 0.9;
                isJumping = false;
            }
        }

        spawnObstacles();

        for (let i = obstacles.length - 1; i >= 0; i--) {
            let obs = obstacles[i];
            obs.position.z += speed;

            if (Math.abs(obs.position.z - player.position.z) < 0.65 &&
                Math.abs(obs.position.x - player.position.x) < 0.6 &&
                player.position.y < 1.1) {
                endGame();
            }

            if (obs.position.z > 10) {
                scene.remove(obs);
                obstacles.splice(i, 1);
            }
        }

        renderer.render(scene, camera);
    }

    function endGame() {
        isGameOver = true;
        document.getElementById('scene2').classList.remove('active');
        document.getElementById('scene-end').classList.add('active');
        document.getElementById('end-desc').innerHTML = "Bà hàng xóm cầm chiếc dép vụt trúng Masha do vướng chướng ngại vật! Bạn đã chạy được <b>" + Math.floor(distance) + "m</b> và ôm trọn <b>" + pickedMangoes + " quả xoài</b>!";
    }
</script>

</body>
</html>
"""

components.html(html_code, height=560)
