import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Trộm Xoài 3D - Cuộc Rượt Đuổi Đường Làng", page_icon="🥭", layout="centered")

html_code = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
    body { margin: 0; padding: 0; background-color: #1a1a2e; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; text-align: center; color: white; }
    #game-container {
        position: relative;
        width: 100%;
        max-width: 450px;
        height: 620px;
        margin: 10px auto;
        border: 4px solid #f1c40f;
        border-radius: 15px;
        overflow: hidden;
        background-color: #000;
        box-shadow: 0 10px 25px rgba(0,0,0,0.8);
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
        color: white; border: none; padding: 12px 20px;
        font-size: 16px; font-weight: bold; border-radius: 25px;
        cursor: pointer; box-shadow: 0 4px 8px rgba(0,0,0,0.4);
        margin: 4px; transition: transform 0.1s;
    }
    .btn:active { transform: scale(0.92); }
    .btn-boost { background: linear-gradient(135deg, #e74c3c, #c0392b); }
    
    .dialog-box {
        position: absolute; bottom: 15px; left: 5%; width: 90%;
        background: rgba(0,0,0,0.85); border: 2px solid #f1c40f;
        border-radius: 10px; padding: 12px; box-sizing: border-box;
    }

    #chaseCanvas { width: 100%; height: 100%; }
</style>
</head>
<body>

<div id="game-container">
    <!-- CẢNH 1: VƯỜN XOÀI (LÉN HÁI XOÀI) -->
    <div id="scene1" class="scene active" style="background-image: url('https://raw.githubusercontent.com/yenphitruong-2508/game-trom-xoai/main/btap2.jpg');">
        <div style="background: rgba(0,0,0,0.6); padding: 8px; font-weight: bold; font-size: 18px; color: #f1c40f;">
            🏡 VƯỜN XOÀI NHÀ BÀ CHỦ
        </div>
        
        <!-- Cây xoài keo trĩu quả -->
        <img src="https://raw.githubusercontent.com/yenphitruong-2508/game-trom-xoai/main/btap.jpg" style="position: absolute; top: 50px; right: 10px; width: 150px; height: 110px; border-radius: 10px; border: 2px solid #f1c40f; object-fit: cover;">
        
        <!-- Bé Masha -->
        <img id="masha-steal" src="https://raw.githubusercontent.com/yenphitruong-2508/game-trom-xoai/main/btap4.jpg" style="position: absolute; bottom: 110px; left: 20px; width: 110px; mix-blend-mode: multiply;">
        
        <!-- Chú chó đang nằm gãi tai -->
        <img id="dog-sleep" src="https://raw.githubusercontent.com/yenphitruong-2508/game-trom-xoai/main/btap5.jpg" style="position: absolute; bottom: 90px; right: 90px; width: 85px; mix-blend-mode: multiply; transition: transform 0.3s;">
        
        <!-- Bà chủ nhà -->
        <img id="granny-house" src="https://raw.githubusercontent.com/yenphitruong-2508/game-trom-xoai/main/btap3.jpg" style="position: absolute; top: 110px; left: 15px; width: 95px; display: none; mix-blend-mode: multiply;">

        <div class="dialog-box">
            <div id="status-text" style="color: #f1c40f; font-weight: bold; margin-bottom: 8px; font-size: 14px;">Bé Masha lén mò vào vườn... Chú chó đang nằm thiu thiu ngủ.</div>
            <button class="btn" onclick="stealMango()">🥭 Hái 1 quả xoài</button>
            <button id="run-btn" class="btn btn-boost" style="display:none;" onclick="startChase()">🏃 ÔM XOÀI BỨT TỐC CHẠY!</button>
        </div>
    </div>

    <!-- CẢNH 2: RƯỢT ĐUỔI TRÊN CON ĐƯỜNG LÀNG THỰC TẾ -->
    <div id="scene2" class="scene">
        <canvas id="chaseCanvas" width="400" height="600"></canvas>
        <div style="position: absolute; top: 10px; left: 10px; background: rgba(0,0,0,0.8); padding: 6px 14px; border-radius: 15px; text-align: left; font-size: 14px; border: 1px solid #f1c40f;">
            🥭 Xoài: <span id="mango-count" style="color:#f1c40f; font-weight:bold;">0</span><br>
            🏃 Quãng đường: <span id="dist-count" style="color:#2ecc71; font-weight:bold;">0</span>m
        </div>
        
        <div style="position: absolute; bottom: 12px; width: 100%; display: flex; justify-content: center; gap: 10px;">
            <button class="btn" onclick="moveLeft()">⬅️ Trái</button>
            <button class="btn btn-boost" onclick="useBoost()">⚡ TĂNG TỐC</button>
            <button class="btn" onclick="moveRight()">Phải ➡️</button>
        </div>
    </div>

    <!-- CẢNH KẾT THÚC -->
    <div id="scene-end" class="scene" style="background: #000; padding-top: 150px;">
        <h1 id="end-title" style="color:#e74c3c;">😭 BỊ BẮT RỒI!</h1>
        <p id="end-desc" style="font-size: 16px; padding: 0 20px; line-height: 1.5; color:#eee;"></p>
        <button class="btn" onclick="location.reload()">🔄 Chơi lại từ đầu</button>
    </div>
</div>

<script>
    let mangoes = 0;
    let dogAwake = false;
    let canvas = document.getElementById('chaseCanvas');
    let ctx = canvas.getContext('2d');
    let playerLane = 1;
    let distance = 0;
    let gap = 12;
    let gameInterval;
    let speed = 4;
    let roadY = 0;
    let obstacles = [];
    
    // Load hình ảnh
    let bgRoad = new Image(); bgRoad.src = 'https://raw.githubusercontent.com/yenphitruong-2508/game-trom-xoai/main/btap6.jpg';
    let imgMasha = new Image(); imgMasha.src = 'https://raw.githubusercontent.com/yenphitruong-2508/game-trom-xoai/main/btap4.jpg';
    let imgGranny = new Image(); imgGranny.src = 'https://raw.githubusercontent.com/yenphitruong-2508/game-trom-xoai/main/btap3.jpg';
    let imgDog = new Image(); imgDog.src = 'https://raw.githubusercontent.com/yenphitruong-2508/game-trom-xoai/main/btap5.jpg';

    function stealMango() {
        mangoes += Math.floor(Math.random() * 2) + 1;
        document.getElementById('status-text').innerHTML = "Bé Masha đã hái được <b>" + mangoes + "</b> quả xoài keo chín!";
        
        if (mangoes >= 3 && !dogAwake) {
            dogAwake = true;
            document.getElementById('dog-sleep').style.transform = "scale(1.2) rotate(15deg)";
            document.getElementById('granny-house').style.display = "block";
            document.getElementById('status-text').innerHTML = "🐕 <b>GÂU GÂU GÂU!</b> Chó sủa ầm ĩ! Bà chủ cầm chiếc dép xông ra quát lớn!";
            document.getElementById('run-btn').style.display = "inline-block";
        }
    }

    function startChase() {
        document.getElementById('scene1').classList.remove('active');
        document.getElementById('scene2').classList.add('active');
        document.getElementById('mango-count').innerText = mangoes;
        gameInterval = setInterval(updateGame, 40);
    }

    function moveLeft() { if(playerLane > 0) playerLane--; }
    function moveRight() { if(playerLane < 2) playerLane++; }
    function useBoost() {
        speed = 8;
        gap += 3;
        setTimeout(() => { speed = 4; }, 1200);
    }

    function updateGame() {
        distance += 0.3;
        document.getElementById('dist-count').innerText = Math.floor(distance);
        
        // Cuộn con đường btap6.jpg mượt mà
        roadY += speed * 2;
        if (roadY >= canvas.height) roadY = 0;
        
        ctx.drawImage(bgRoad, 0, roadY - canvas.height, canvas.width, canvas.height);
        ctx.drawImage(bgRoad, 0, roadY, canvas.width, canvas.height);
        
        let lanesX = [90, 200, 310];
        
        // Sinh chướng ngại vật ngẫu nhiên
        if (Math.random() < 0.08) {
            obstacles.push({ lane: Math.floor(Math.random() * 3), y: -50, type: Math.random() > 0.5 ? '🪨 Đá' : '🪵 Củi' });
        }
        
        ctx.font = "26px Arial";
        for (let i = 0; i < obstacles.length; i++) {
            let obs = obstacles[i];
            obs.y += speed * 1.8;
            ctx.fillText(obs.type, lanesX[obs.lane] - 15, obs.y);
            
            // Va chạm
            if (obs.y > 440 && obs.y < 510 && obs.lane === playerLane) {
                gap -= 4;
                mangoes = Math.max(0, mangoes - 1);
                document.getElementById('mango-count').innerText = mangoes;
                obstacles.splice(i, 1);
            }
        }
        
        obstacles = obstacles.filter(o => o.y < 650);

        // Vẽ Bé Masha
        ctx.drawImage(imgMasha, lanesX[playerLane] - 25, 460, 55, 70);
        
        // Vẽ Bà chủ nhà & Chó rượt theo phía sau
        let chaserY = 460 + (gap * 4);
        ctx.drawImage(imgGranny, lanesX[playerLane] - 25, Math.min(chaserY, 560), 50, 65);
        ctx.drawImage(imgDog, lanesX[playerLane] + 25, Math.min(chaserY + 10, 570), 40, 45);

        // Đụng chướng ngại vật liên tục bị bắt -> GameOver
        if (gap <= 0) {
            endGame();
        }
    }

    function endGame() {
        clearInterval(gameInterval);
        document.getElementById('scene2').classList.remove('active');
        document.getElementById('scene-end').classList.add('active');
        document.getElementById('end-desc').innerHTML = "Bà chủ cầm chiếc dép vụt trúng Masha! Bạn đã chạy được <b>" + Math.floor(distance) + "m</b> và giữ lại được <b>" + mangoes + " quả xoài</b>!";
    }
</script>

</body>
</html>
"""

components.html(html_code, height=640)
