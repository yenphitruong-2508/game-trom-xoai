import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Trộm Xoài Rượt Đuổi 3D", page_icon="🥭", layout="centered")

html_code = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        text-align: center;
        background-color: #1a1a2e;
        color: white;
        margin: 0;
        padding: 5px;
    }
    #game-container {
        position: relative;
        width: 100%;
        max-width: 450px;
        height: 620px;
        margin: 0 auto;
        border: 4px solid #f1c40f;
        border-radius: 15px;
        overflow: hidden;
        background-color: #16213e;
        box-shadow: 0 10px 25px rgba(0,0,0,0.7);
    }
    .scene {
        position: absolute;
        width: 100%;
        height: 100%;
        top: 0;
        left: 0;
        display: none;
        background-size: cover;
        background-position: center;
    }
    .active { display: block; }
    
    .btn {
        background: linear-gradient(135deg, #f39c12, #e67e22);
        color: white;
        border: none;
        padding: 12px 20px;
        font-size: 16px;
        font-weight: bold;
        border-radius: 25px;
        cursor: pointer;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        margin: 4px;
        transition: transform 0.1s;
    }
    .btn:active { transform: scale(0.92); }
    .btn-boost { background: linear-gradient(135deg, #e74c3c, #c0392b); }
    
    .character {
        position: absolute;
        transition: all 0.2s ease;
    }
    
    .dialog-box {
        position: absolute;
        bottom: 15px;
        left: 5%;
        width: 90%;
        background: rgba(0,0,0,0.85);
        border: 2px solid #f1c40f;
        border-radius: 10px;
        padding: 10px;
        box-sizing: border-box;
    }

    #chaseCanvas {
        width: 100%;
        height: 100%;
    }
</style>
</head>
<body>

<div id="game-container">
    <!-- CẢNH 1: VƯỜN XOÀI NHÀ BÀ CHỦ -->
    <div id="scene1" class="scene active" style="background-image: url('https://raw.githubusercontent.com/yenphitruong-2508/game-trom-xoai/main/btap2.jpg');">
        <div style="background: rgba(0,0,0,0.6); padding: 8px; font-weight: bold; font-size: 18px; color: #f1c40f;">
            🏡 VƯỜN XOÀI NHÀ BÀ CHỦ
        </div>
        
        <!-- Cây xoài keo -->
        <img src="https://raw.githubusercontent.com/yenphitruong-2508/game-trom-xoai/main/btap.jpg" style="position: absolute; top: 45px; right: 10px; width: 150px; height: 110px; border-radius: 10px; border: 2px solid yellow; object-fit: cover;">
        
        <!-- Bé Masha -->
        <img id="masha-steal" src="https://raw.githubusercontent.com/yenphitruong-2508/game-trom-xoai/main/btap4.jpg" class="character" style="bottom: 110px; left: 20px; width: 100px; border-radius: 10px;">
        
        <!-- Chú chó nằm gãi tai -->
        <img id="dog-sleep" src="https://raw.githubusercontent.com/yenphitruong-2508/game-trom-xoai/main/btap5.jpg" class="character" style="bottom: 90px; right: 100px; width: 80px; border-radius: 10px;">
        
        <!-- Bà chủ nhà -->
        <img id="granny-house" src="https://raw.githubusercontent.com/yenphitruong-2508/game-trom-xoai/main/btap3.jpg" class="character" style="top: 110px; left: 15px; width: 90px; display: none; border-radius: 10px; border: 3px solid red;">

        <div class="dialog-box">
            <div id="status-text" style="color: #f1c40f; font-weight: bold; margin-bottom: 8px; font-size: 14px;">Bé Masha lén mò vào vườn... Chú chó đang thiu thiu ngủ.</div>
            <button class="btn" onclick="stealMango()">🥭 Hái 1 quả xoài</button>
            <button id="run-btn" class="btn btn-boost" style="display:none;" onclick="startChase()">🏃 ÔM XOÀI BỨT TỐC CHẠY!</button>
        </div>
    </div>

    <!-- CẢNH 2: RƯỢT ĐUỔI TRÊN ĐƯỜNG LÀNG (SUBWAY SURFERS STYLE) -->
    <div id="scene2" class="scene">
        <canvas id="chaseCanvas" width="400" height="600"></canvas>
        <div style="position: absolute; top: 10px; left: 10px; background: rgba(0,0,0,0.8); padding: 6px 12px; border-radius: 15px; text-align: left; font-size: 14px; border: 1px solid #f1c40f;">
            🥭 Xoài: <span id="mango-count" style="color:#f1c40f; font-weight:bold;">0</span><br>
            🏃 Quãng đường: <span id="dist-count" style="color:#2ecc71; font-weight:bold;">0</span>/100m
        </div>
        
        <div style="position: absolute; bottom: 12px; width: 100%; display: flex; justify-content: center; gap: 8px;">
            <button class="btn" onclick="moveLeft()">⬅️ Trái</button>
            <button class="btn btn-boost" onclick="useBoost()">⚡ TĂNG TỐC</button>
            <button class="btn" onclick="moveRight()">Phải ➡️</button>
        </div>
    </div>

    <!-- CẢNH KẾT THÚC -->
    <div id="scene-end" class="scene" style="background: #000; padding-top: 140px;">
        <h1 id="end-title">GAME OVER</h1>
        <p id="end-desc" style="font-size: 16px; padding: 0 20px; line-height: 1.5;"></p>
        <button class="btn" onclick="location.reload()">🔄 Chơi lại từ đầu</button>
    </div>
</div>

<script>
    // Audio Synthesizer via Web Audio API
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

    function playSound(type) {
        if (audioCtx.state === 'suspended') {
            audioCtx.resume();
        }
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.connect(gain);
        gain.connect(audioCtx.destination);

        if (type === 'pluck') {
            osc.frequency.setValueAtTime(400, audioCtx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(800, audioCtx.currentTime + 0.1);
            gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.1);
            osc.start(); osc.stop(audioCtx.currentTime + 0.1);
        } else if (type === 'bark') {
            osc.type = 'sawtooth';
            osc.frequency.setValueAtTime(150, audioCtx.currentTime);
            osc.frequency.linearRampToValueAtTime(80, audioCtx.currentTime + 0.15);
            gain.gain.setValueAtTime(0.4, audioCtx.currentTime);
            gain.gain.linearRampToValueAtTime(0.01, audioCtx.currentTime + 0.15);
            osc.start(); osc.stop(audioCtx.currentTime + 0.15);
        } else if (type === 'boost') {
            osc.type = 'triangle';
            osc.frequency.setValueAtTime(300, audioCtx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(1200, audioCtx.currentTime + 0.4);
            gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.4);
            osc.start(); osc.stop(audioCtx.currentTime + 0.4);
        } else if (type === 'hit') {
            osc.type = 'square';
            osc.frequency.setValueAtTime(100, audioCtx.currentTime);
            osc.frequency.linearRampToValueAtTime(40, audioCtx.currentTime + 0.2);
            gain.gain.setValueAtTime(0.5, audioCtx.currentTime);
            gain.gain.linearRampToValueAtTime(0.01, audioCtx.currentTime + 0.2);
            osc.start(); osc.stop(audioCtx.currentTime + 0.2);
        }
    }

    let mangoes = 0;
    let dogAwake = false;
    let canvas = document.getElementById('chaseCanvas');
    let ctx = canvas.getContext('2d');
    let playerLane = 1;
    let distance = 0;
    let gap = 15;
    let gameInterval;
    let speed = 3;
    let obstacles = [];
    
    // Load ảnh từ kho GitHub của bạn
    let bgRoad = new Image(); bgRoad.src = 'https://raw.githubusercontent.com/yenphitruong-2508/game-trom-xoai/main/btap6.jpg';
    let imgMasha = new Image(); imgMasha.src = 'https://raw.githubusercontent.com/yenphitruong-2508/game-trom-xoai/main/btap4.jpg';
    let imgGranny = new Image(); imgGranny.src = 'https://raw.githubusercontent.com/yenphitruong-2508/game-trom-xoai/main/btap3.jpg';

    function stealMango() {
        playSound('pluck');
        mangoes += Math.floor(Math.random() * 2) + 1;
        document.getElementById('status-text').innerHTML = "Bé Masha đã hái được <b>" + mangoes + "</b> quả xoài keo chín!";
        
        if (mangoes >= 3 && !dogAwake) {
            dogAwake = true;
            playSound('bark');
            document.getElementById('dog-sleep').style.transform = "scale(1.2) rotate(10deg)";
            document.getElementById('granny-house').style.display = "block";
            document.getElementById('status-text').innerHTML = "🐕 <b>GÂU GÂU GÂU!</b> Chó sủa ầm ĩ! Bà chủ cầm chiếc dép thần thánh xông ra quát!";
            document.getElementById('run-btn').style.display = "inline-block";
        }
    }

    function startChase() {
        playSound('boost');
        document.getElementById('scene1').classList.remove('active');
        document.getElementById('scene2').classList.add('active');
        document.getElementById('mango-count').innerText = mangoes;
        gameInterval = setInterval(updateGame, 50);
    }

    function moveLeft() { if(playerLane > 0) { playerLane--; playSound('pluck'); } }
    function moveRight() { if(playerLane < 2) { playerLane++; playSound('pluck'); } }
    function useBoost() {
        playSound('boost');
        speed = 8;
        gap += 4;
        setTimeout(() => { speed = 3; }, 1200);
    }

    function updateGame() {
        distance += 0.5;
        document.getElementById('dist-count').innerText = Math.floor(distance);
        
        if (Math.random() < 0.09) {
            obstacles.push({ lane: Math.floor(Math.random() * 3), y: -50, type: Math.random() > 0.5 ? '🗿 Đá' : '🪵 Củi' });
        }
        
        ctx.drawImage(bgRoad, 0, 0, canvas.width, canvas.height);
        let lanesX = [80, 180, 280];
        
        ctx.font = "28px Arial";
        for (let i = 0; i < obstacles.length; i++) {
            let obs = obstacles[i];
            obs.y += speed * 2.5;
            ctx.fillText(obs.type, lanesX[obs.lane] - 15, obs.y);
            
            if (obs.y > 450 && obs.y < 530 && obs.lane === playerLane) {
                playSound('hit');
                gap -= 4;
                mangoes = Math.max(0, mangoes - 1);
                document.getElementById('mango-count').innerText = mangoes;
                obstacles.splice(i, 1);
            }
        }
        
        obstacles = obstacles.filter(o => o.y < 650);

        // Hiệu ứng Bé Masha chạy né 3 làn đường
        ctx.drawImage(imgMasha, lanesX[playerLane] - 25, 470, 50, 65);
        
        // Hiệu ứng Bà chủ rượt theo sau
        let chaserY = 540 + (gap * 3.5);
        ctx.drawImage(imgGranny, lanesX[playerLane] - 25, Math.min(chaserY, 560), 45, 60);

        if (gap <= 0) {
            endGame(false);
        } else if (distance >= 100) {
            endGame(true);
        }
    }

    function endGame(isWin) {
        clearInterval(gameInterval);
        document.getElementById('scene2').classList.remove('active');
        document.getElementById('scene-end').classList.add('active');
        
        if (isWin) {
            playSound('boost');
            document.getElementById('end-title').innerHTML = "🎉 THẮNG RỰC RỠ!";
            document.getElementById('end-title').style.color = "#2ecc71";
            document.getElementById('end-desc').innerHTML = "Bé Masha đã ôm trọn <b>" + mangoes + " quả xoài</b> chạy thoát về xóm!";
        } else {
            playSound('hit');
            document.getElementById('end-title').innerHTML = "😭 BỊ BẮT RỒI!";
            document.getElementById('end-title').style.color = "#e74c3c";
            document.getElementById('end-desc').innerHTML = "Bà chủ cầm chiếc chiếc dép thần thánh vụt trúng Masha! Rơi mất sạch xoài!";
        }
    }
</script>

</body>
</html>
"""

components.html(html_code, height=640)
