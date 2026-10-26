import os
import json
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

GAMES = [
    {"name":"Roblox","category":"Adventure","description":"Explore millions of experiences and create your own adventures.","image":"https://images.unsplash.com/photo-1612287230202-1ff1d85d1bdf?auto=format&fit=crop&w=900&q=85","url":"https://www.roblox.com/","tag":"POPULAR","color":"#ff4f91",
     "objective":"Roblox is a platform containing millions of player-made games, called experiences. Each experience has its own goal.",
     "how":"1. Create or sign in to an account. 2. Browse experiences and choose one. 3. Press Play. 4. Follow that experience's instructions and controls.",
     "controls":"On PC, many experiences use WASD to move, Space to jump, and the mouse to look around, but controls vary by experience. Mobile games use on-screen controls.",
     "tips":"Try beginner-friendly experiences, read the instructions, use the in-game settings, and never share your password or personal details."},
    {"name":"Minecraft","category":"Sandbox","description":"Build amazing worlds, explore caves, and survive together.","image":"https://images.unsplash.com/photo-1607513746994-51f730a44832?auto=format&fit=crop&w=900&q=85","url":"https://www.minecraft.net/","tag":"BUILD & EXPLORE","color":"#66e58c",
     "objective":"Minecraft is a sandbox game where you explore a block-based world, gather resources, craft items, build structures, and optionally survive against hostile mobs.",
     "how":"1. Choose Survival or Creative mode. 2. In Survival, collect wood first. 3. Craft basic tools and a crafting table. 4. Gather food and build shelter before night. 5. Explore, mine, craft, and build.",
     "controls":"Typical PC controls: WASD move, Space jump, mouse look, left-click break/attack, right-click place/use, E inventory. Controls can be changed in Settings.",
     "tips":"Make a bed when possible, carry food and torches, keep track of your base, and store valuable items safely."},
    {"name":"Fortnite","category":"Action","description":"Jump into action, explore islands, and compete with friends.","image":"https://images.unsplash.com/photo-1542751371-adc38448a05e?auto=format&fit=crop&w=900&q=85","url":"https://www.fortnite.com/","tag":"ACTION","color":"#a78bfa",
     "objective":"Fortnite includes several modes. In Battle Royale, players try to be the last player or team remaining while the safe area gets smaller.",
     "how":"1. Choose a mode. 2. Land in a place that suits your skill level. 3. Collect equipment and supplies. 4. Watch the storm circle and move to safety. 5. Work with your team and aim to complete the mode's objective.",
     "controls":"On PC, movement commonly uses WASD, Space to jump, and mouse buttons to aim and fire. Building and other actions depend on your key bindings and mode.",
     "tips":"Learn the map, avoid staying outside the safe zone, use cover, and practise aiming in suitable training modes."},
    {"name":"VALORANT","category":"Action","description":"Use strategy, teamwork, and special abilities in tactical matches.","image":"https://images.unsplash.com/photo-1542751371-6533f8b4b2c9?auto=format&fit=crop&w=900&q=85","url":"https://playvalorant.com/","tag":"COMPETITIVE","color":"#ff667e",
     "objective":"VALORANT is a tactical team shooter. Teams alternate between attacking and defending; attackers generally try to plant the Spike while defenders try to stop them or defuse it.",
     "how":"1. Choose an agent and learn their abilities. 2. Buy weapons and utility during the buy phase. 3. Communicate with teammates. 4. Use cover and check angles carefully. 5. Play the round objective rather than chasing every fight.",
     "controls":"Typical PC controls: WASD move, mouse aim, left-click fire, R reload, and number keys switch weapons. Ability keys depend on settings.",
     "tips":"Keep your crosshair near head height, stop moving before accurate shots, share useful information, and practise in the Range."},
    {"name":"Among Us","category":"Casual","description":"Work together, complete tasks, and discover the impostor.","image":"https://images.unsplash.com/photo-1493711662062-fa541adb3fc8?auto=format&fit=crop&w=900&q=85","url":"https://www.innersloth.com/games/among-us/","tag":"PLAY TOGETHER","color":"#ffd166",
     "objective":"Crewmates complete tasks and try to identify the Impostor. The Impostor tries to sabotage the crew and avoid being discovered.",
     "how":"1. Join a lobby. 2. If you are a Crewmate, complete the tasks shown on your list and report suspicious activity. 3. If you are the Impostor, use sabotage strategically and avoid drawing attention. 4. Discuss evidence and vote during meetings.",
     "controls":"Move with the keyboard or touch controls. Interact with tasks, report, and use meeting or sabotage buttons when available.",
     "tips":"Explain what you actually saw, listen to other players, and avoid accusing people without evidence."},
    {"name":"Rocket League","category":"Sports","description":"Drive rocket-powered cars and score spectacular goals.","image":"https://images.unsplash.com/photo-1511512578047-dfb367046420?auto=format&fit=crop&w=900&q=85","url":"https://www.rocketleague.com/","tag":"SPORTS","color":"#55d6ff",
     "objective":"Rocket League is football played with rocket-powered cars. Score more goals than the other team before time runs out.",
     "how":"1. Start with the tutorial. 2. Drive toward the ball and try to hit it toward the opponent's goal. 3. Collect boost pads when useful. 4. Return to defend when needed. 5. Coordinate rotations with teammates.",
     "controls":"Default controls vary by platform. The tutorial teaches driving, jumping, boosting, and camera control; you can customise bindings in Settings.",
     "tips":"Do not chase the ball all the time. Leave space for teammates, practise basic hits, and learn when to defend."},
    {"name":"Fall Guys","category":"Casual","description":"Race through colourful obstacle courses and wild challenges.","image":"https://images.unsplash.com/photo-1511882150382-421056c89033?auto=format&fit=crop&w=900&q=85","url":"https://www.fallguys.com/","tag":"PARTY GAME","color":"#ff9e70",
     "objective":"Fall Guys is a colourful obstacle-course party game. Qualify through rounds by reaching the finish or completing each round's goal.",
     "how":"1. Join a show. 2. Follow the course and avoid obstacles. 3. Jump, dive, and grab when the round requires it. 4. Reach the finish or meet the objective before the round ends.",
     "controls":"Movement, jump, dive, and grab controls depend on your platform and settings; check the in-game controls menu.",
     "tips":"Watch moving obstacles before crossing, avoid crowded edges, and focus on staying upright rather than taking risky shortcuts."},
    {"name":"Genshin Impact","category":"Adventure","description":"Discover a beautiful fantasy world full of quests and mysteries.","image":"https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=900&q=85","url":"https://genshin.hoyoverse.com/","tag":"FANTASY","color":"#7cddff",
     "objective":"Genshin Impact is an open-world action role-playing game. Explore Teyvat, complete quests, solve puzzles, and build a team of characters.",
     "how":"1. Follow the early quests and tutorials. 2. Explore and unlock waypoints. 3. Collect resources and upgrade characters and equipment. 4. Experiment with different elemental abilities. 5. Check quest markers for guidance.",
     "controls":"Movement, attack, jump, dodge, character switching, and abilities have platform-specific controls. The settings menu shows and allows changes to them.",
     "tips":"Learn elemental reactions, upgrade a small team first, use waypoints to travel, and check adventure-rank requirements for quests."},
    {"name":"PUBG: Battlegrounds","category":"Action","description":"Search for equipment, plan your strategy, and compete to survive.","image":"https://images.unsplash.com/photo-1493711662062-fa541adb3fc8?auto=format&fit=crop&w=900&q=85","url":"https://pubg.com/","tag":"SURVIVAL","color":"#ffbd69",
     "objective":"PUBG: Battlegrounds is a battle royale game where players or squads search for equipment and try to be the last survivors as the play zone shrinks.",
     "how":"1. Drop into the map. 2. Find weapons, protective gear, healing items, and supplies. 3. Watch the play zone and move toward safety. 4. Use cover and listen for audio clues. 5. Survive until the match ends.",
     "controls":"PC controls commonly use WASD for movement and mouse controls for aiming and firing. Check Settings for your platform's full layout.",
     "tips":"Choose fights carefully, keep an eye on the zone, use cover, and communicate with your squad."},
    {"name":"Brawl Stars","category":"Action","description":"Choose your brawler and jump into fast-paced battles.","image":"https://images.unsplash.com/photo-1560253023-3ec5d502959f?auto=format&fit=crop&w=900&q=85","url":"https://supercell.com/en/games/brawlstars/","tag":"QUICK MATCHES","color":"#ff6bcb",
     "objective":"Brawl Stars is a fast multiplayer action game with different modes, brawlers, and objectives such as collecting gems, scoring goals, or surviving.",
     "how":"1. Choose a brawler. 2. Check the mode objective. 3. Move, aim, and use attacks with the controls. 4. Work with your team when the mode is team-based. 5. Use your Super at a useful moment.",
     "controls":"On mobile, use the virtual joystick to move and the attack controls to aim or fire. Exact control options depend on settings.",
     "tips":"Learn your brawler's range and role, use walls for cover, and focus on the mode objective."},
    {"name":"Stardew Valley","category":"Sandbox","description":"Build a farm, grow crops, meet people, and explore the valley.","image":"https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=900&q=85","url":"https://www.stardewvalley.net/","tag":"RELAX & PLAY","color":"#91e6a1",
     "objective":"Stardew Valley is a relaxing farming role-playing game. Restore a farm, grow crops, raise animals, make friends, and explore nearby areas.",
     "how":"1. Clear a small area on your farm. 2. Plant and water seasonal seeds. 3. Sell harvests to earn money. 4. Upgrade tools and explore the town. 5. Keep an eye on the calendar and energy.",
     "controls":"Controls vary by platform. Use the in-game menu to see how to move, use tools, interact, and manage your inventory.",
     "tips":"Start with a manageable number of crops, water them daily, save some money for seeds, and check the season before planting."},
    {"name":"Trackmania","category":"Sports","description":"Race on creative tracks and challenge your driving skills.","image":"https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?auto=format&fit=crop&w=900&q=85","url":"https://www.trackmania.com/","tag":"RACING","color":"#ffd166",
     "objective":"Trackmania is a time-trial racing game. Drive through tracks, pass checkpoints, and aim for faster completion times and medals.",
     "how":"1. Select a track. 2. Follow the route and pass each checkpoint. 3. Learn turns and jumps. 4. Finish the track and compare your time. 5. Replay to improve your route and speed.",
     "controls":"Steering, acceleration, braking, and respawn controls vary by platform and key bindings. Check the controls menu before racing.",
     "tips":"Smooth steering often beats sudden corrections. Learn where to brake, use checkpoints, and repeat sections to improve."}
]

GUIDE_BY_NAME = {game["name"]: game for game in GAMES}

PAGE = r"""
<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="Discover games, learn how to play, and ask the GameVerse gaming helper questions.">
<title>GameVerse | Games, Guides & Gaming Assistant</title>
<style>
:root{--bg:#090b18;--panel:#14182b;--text:#f7f7ff;--muted:#a7afca;--pink:#ff4fd8;--blue:#5d7cff;--cyan:#46e7ff}
*{box-sizing:border-box;margin:0;padding:0}html{scroll-behavior:smooth}body{background:radial-gradient(ellipse at 15% 5%,#332064 0,transparent 32%),radial-gradient(ellipse at 90% 30%,#102e59 0,transparent 34%),var(--bg);color:var(--text);font-family:"Segoe UI",Arial,sans-serif;min-height:100vh}a{color:inherit;text-decoration:none}
header{position:sticky;top:0;z-index:10;background:rgba(9,11,24,.9);backdrop-filter:blur(18px);border-bottom:1px solid #ffffff19}.nav{max-width:1250px;margin:auto;padding:18px 24px;display:flex;align-items:center;justify-content:space-between;gap:20px}.logo{font-size:25px;font-weight:900;letter-spacing:-1px;white-space:nowrap}.logo span{background:linear-gradient(90deg,var(--pink),var(--cyan));color:transparent;background-clip:text;-webkit-background-clip:text}.nav-links{display:flex;gap:24px;color:var(--muted);font-size:14px}.nav-links a:hover{color:white}.nav-button{background:linear-gradient(110deg,var(--pink),var(--blue));padding:11px 17px;border-radius:12px;font-size:13px;font-weight:800;white-space:nowrap}
main{max-width:1250px;margin:auto;padding:0 24px 70px}.hero{position:relative;overflow:hidden;padding:68px 42px;margin-top:32px;border-radius:30px;border:1px solid #ffffff24;background:linear-gradient(110deg,rgba(33,24,75,.97),rgba(12,65,105,.9));box-shadow:0 25px 80px #1a2a7d33}.hero:after{content:"🎮";position:absolute;right:7%;top:17%;font-size:clamp(100px,17vw,210px);opacity:.8;transform:rotate(-12deg);filter:drop-shadow(0 0 35px #46e7ff70)}.eyebrow{color:var(--cyan);font-weight:800;font-size:12px;letter-spacing:3px;margin-bottom:18px}.hero h1{position:relative;z-index:1;max-width:700px;font-size:clamp(38px,6vw,68px);line-height:1.06;letter-spacing:-2px}.hero h1 span{background:linear-gradient(90deg,#ff77d9,#72e9ff);color:transparent;background-clip:text;-webkit-background-clip:text}.hero p{position:relative;z-index:1;max-width:550px;margin-top:20px;color:#d4d9f0;line-height:1.8}.hero-actions{position:relative;z-index:1;display:flex;flex-wrap:wrap;gap:12px;margin-top:25px}.primary-btn,.secondary-btn{display:inline-block;padding:14px 20px;border-radius:13px;font-weight:800;font-size:14px}.primary-btn{color:#090b18;background:linear-gradient(100deg,#ff79d8,#65e8ff)}.secondary-btn{border:1px solid #ffffff40;background:#ffffff0f}.stats{display:flex;flex-wrap:wrap;gap:35px;margin-top:30px;color:var(--muted);font-size:13px}.stats strong{display:block;color:white;font-size:22px;margin-bottom:4px}
.section-heading{display:flex;justify-content:space-between;align-items:end;gap:18px;margin:52px 0 22px}.section-heading h2{font-size:clamp(25px,4vw,34px);letter-spacing:-.8px}.section-heading p{color:var(--muted);margin-top:8px;font-size:14px}.search-box{display:flex;align-items:center;gap:10px;width:min(100%,390px);padding:14px 16px;background:#151a2e;border:1px solid #303750;border-radius:14px}.search-box input{width:100%;color:white;background:transparent;border:0;outline:0;font-size:14px}.search-box input::placeholder{color:#8d96b4}.filters{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:25px}.filter{color:#c0c7e0;border:1px solid #303750;background:#14182b;border-radius:999px;padding:10px 17px;cursor:pointer;font-size:13px;font-weight:700}.filter:hover,.filter.active{color:white;border-color:#8c78ff;background:linear-gradient(100deg,#6742b7,#315eaa)}
.game-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:22px}.game-card{overflow:hidden;min-width:0;border:1px solid #ffffff1c;background:linear-gradient(155deg,#1b2037,#111525);border-radius:20px;transition:transform .25s,border-color .25s}.game-card:hover{transform:translateY(-5px);border-color:#64dcff88;box-shadow:0 20px 40px #0005}.game-image{position:relative;height:175px;overflow:hidden;background:linear-gradient(135deg,#332064,#17617b)}.game-image img{width:100%;height:100%;object-fit:cover;display:block}.game-image:after{content:"";position:absolute;inset:0;background:linear-gradient(0deg,#0a0c1bc2,transparent 65%);pointer-events:none}.game-tag{position:absolute;top:13px;left:13px;z-index:1;background:#0a0c1bd9;border:1px solid #ffffff33;border-radius:7px;padding:7px 9px;font-size:9px;letter-spacing:1px;font-weight:900}.game-info{padding:18px}.game-meta{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:9px}.game-meta h3{font-size:20px}.category-label{color:#c8ceeb;background:#ffffff12;border-radius:7px;padding:5px 8px;font-size:10px;white-space:nowrap}.game-info p{color:var(--muted);font-size:13px;line-height:1.7;min-height:62px}.card-actions{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:15px}.play-btn,.guide-btn{display:block;padding:12px 8px;border-radius:11px;text-align:center;font-size:12px;font-weight:900;color:white;border:1px solid #ffffff25;background:linear-gradient(100deg,#6044b5,#315eaa);cursor:pointer}.guide-btn{background:#ffffff0a}.play-btn:hover,.guide-btn:hover{filter:brightness(1.25)}.no-results{display:none;text-align:center;padding:40px 15px;color:var(--muted);background:var(--panel);border-radius:18px}
.info-banner,.assistant-panel{margin-top:50px;padding:28px;border-radius:22px;border:1px solid #ffffff20;background:linear-gradient(110deg,#231943,#102d45)}.info-banner p{color:var(--muted);line-height:1.8;margin-top:10px}.assistant-panel{background:linear-gradient(140deg,#171b33,#122a42)}.assistant-panel>p{color:var(--muted);margin:10px 0 18px;line-height:1.7}.chat-box{background:#0b1020;border:1px solid #ffffff20;border-radius:16px;padding:14px;max-width:850px}.chat-log{height:220px;overflow:auto;display:flex;flex-direction:column;gap:10px;padding:4px 2px 12px}.bubble{max-width:90%;padding:11px 13px;border-radius:12px;line-height:1.55;font-size:13px;white-space:pre-wrap}.bubble.bot{align-self:flex-start;background:#1b2440;color:#edf1ff}.bubble.user{align-self:flex-end;background:#5140a5;color:white}.chat-form{display:flex;gap:8px}.chat-form input{flex:1;min-width:0;background:#151a2e;border:1px solid #3a4260;color:white;border-radius:10px;padding:12px;outline:none}.chat-form button{border:0;border-radius:10px;padding:0 17px;background:linear-gradient(100deg,#ff79d8,#65e8ff);font-weight:900;cursor:pointer}.chat-note{font-size:11px!important;color:#929dbb!important;margin-top:10px!important}.modal{position:fixed;inset:0;z-index:30;background:#03050bd9;display:none;align-items:center;justify-content:center;padding:18px}.modal.open{display:flex}.modal-card{width:min(900px,100%);max-height:90vh;overflow:auto;border:1px solid #ffffff2b;border-radius:22px;background:linear-gradient(145deg,#1b2038,#0e1425);box-shadow:0 25px 90px #0009}.modal-head{display:flex;justify-content:space-between;align-items:center;gap:15px;padding:20px 22px;border-bottom:1px solid #ffffff1c;position:sticky;top:0;background:#171c30;z-index:2}.modal-head h2{font-size:23px}.close-btn{border:1px solid #ffffff2e;background:#ffffff0d;color:white;border-radius:10px;padding:8px 12px;cursor:pointer}.guide-content{padding:22px;display:grid;grid-template-columns:1fr 1fr;gap:16px}.guide-section{padding:17px;border:1px solid #ffffff18;border-radius:15px;background:#ffffff06}.guide-section h3{color:#78eaff;font-size:15px;margin-bottom:10px}.guide-section p{color:#d3d9ef;font-size:13px;line-height:1.75;white-space:pre-line}.guide-chat{padding:0 22px 22px}.guide-chat h3{margin-bottom:10px}.guide-chat .chat-log{height:160px}.guide-chat .chat-box{max-width:none}
footer{border-top:1px solid #ffffff1a;padding:28px 24px;text-align:center;color:#9da5c2;font-size:12px;line-height:1.9}footer strong{color:white}
@media(max-width:900px){.game-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.hero:after{right:3%;opacity:.3}}
@media(max-width:600px){.nav{padding:15px}.logo{font-size:21px}.nav-links{display:none}main{padding:0 15px 45px}.hero{padding:40px 23px;margin-top:18px}.hero h1{letter-spacing:-1px}.hero:after{top:12%;right:0;opacity:.2}.section-heading{align-items:stretch;flex-direction:column}.search-box{width:100%}.game-grid{grid-template-columns:1fr}.game-image{height:205px}.game-info p{min-height:0}.stats{gap:22px}.guide-content{grid-template-columns:1fr}.chat-form button{padding:0 12px}}

.mini-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin-top:20px}
.mini-card{min-width:0;padding:18px;border:1px solid #ffffff20;border-radius:16px;background:#090f20}
.mini-card h3{font-size:18px;margin-bottom:8px}
.mini-card p{font-size:13px;line-height:1.6;color:var(--muted);min-height:48px;margin-bottom:10px}
.ttt-board{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:6px;max-width:240px;margin:14px auto}
.ttt-cell{aspect-ratio:1;border:1px solid #ffffff24;border-radius:10px;background:#1b2440;color:white;font-size:30px;font-weight:900;cursor:pointer}
.ttt-cell:hover{background:#303b61}
.mini-status{text-align:center;color:#d9e1ff;font-size:13px;min-height:24px;margin:10px 0}
.mini-button{display:block;width:100%;padding:10px;border:0;border-radius:10px;background:linear-gradient(100deg,#7049c7,#315eaa);color:white;font-weight:800;cursor:pointer}
.memory-board{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:6px;margin:14px 0}
.memory-card{aspect-ratio:1;border:1px solid #ffffff25;border-radius:9px;background:#202849;color:white;font-size:23px;cursor:pointer}
.memory-card.flipped,.memory-card.matched{background:#315b78;border-color:#67e8f9}
.memory-card.matched{cursor:default}
.reaction-pad{width:100%;min-height:125px;margin:14px 0;border:1px solid #ffffff28;border-radius:14px;background:#252c48;color:white;font-size:18px;font-weight:900;cursor:pointer}
.reaction-pad.waiting{background:#9b334f}
.reaction-pad.ready{background:#198754}
.online-links{display:flex;flex-wrap:wrap;gap:10px;margin-top:18px}
.online-links a{padding:12px 15px;border:1px solid #ffffff22;border-radius:11px;background:#0e1830;font-weight:800;font-size:13px}
.online-links a:hover{border-color:var(--cyan);background:#18284a}
@media(max-width:850px){.mini-grid{grid-template-columns:1fr 1fr}}
@media(max-width:600px){.mini-grid{grid-template-columns:1fr}.mini-card p{min-height:0}}

</style></head><body>
<header><nav class="nav"><a class="logo" href="#"><span>GAME</span>VERSE 🎮</a><div class="nav-links"><a href="#games">Discover</a><a href="#games" data-nav-category="Action">Action</a><a href="#games" data-nav-category="Adventure">Adventure</a><a href="#play-here">Play Here</a><a href="#assistant">AI Helper</a><a href="#about">About</a></div><a class="nav-button" href="#games">EXPLORE GAMES ↗</a></nav></header>
<main>
<section class="hero"><div class="eyebrow">DISCOVER • LEARN • PLAY</div><h1>Your gaming world, <span>explained.</span></h1><p>Discover games, learn the basics, explore beginner tips, and ask the GameVerse assistant for help with your next adventure.</p><div class="hero-actions"><a class="primary-btn" href="#games">🎮 Explore Games</a><a class="secondary-btn" href="#assistant">🤖 Ask GameVerse AI</a></div><div class="stats"><div><strong>{{ games|length }}+</strong>Featured games</div><div><strong>5</strong>Game categories</div><div><strong>📘</strong>Beginner guides</div></div></section>
<section id="games"><div class="section-heading"><div><h2>🔥 Explore the games</h2><p>Open a guide to learn the goal, controls, and beginner tips.</p></div><label class="search-box"><span>🔎</span><input id="search" type="search" placeholder="Search games..." autocomplete="off" aria-label="Search games"></label></div>
<div class="filters" aria-label="Game categories"><button class="filter active" data-category="All">✨ All Games</button><button class="filter" data-category="Action">⚔️ Action</button><button class="filter" data-category="Adventure">🌍 Adventure</button><button class="filter" data-category="Sandbox">🧱 Sandbox</button><button class="filter" data-category="Casual">🎉 Casual</button><button class="filter" data-category="Sports">🏎️ Sports</button></div>
<div class="game-grid" id="gameGrid">{% for game in games %}<article class="game-card" data-name="{{ game.name|lower }}" data-category="{{ game.category|lower }}" data-description="{{ game.description|lower }}"><div class="game-image"><img src="{{ game.image }}" alt="Gaming artwork for {{ game.name }}" loading="lazy" onerror="this.style.display='none'"><span class="game-tag" style="color:{{ game.color }}">{{ game.tag }}</span></div><div class="game-info"><div class="game-meta"><h3>{{ game.name }}</h3><span class="category-label">{{ game.category }}</span></div><p>{{ game.description }}</p><div class="card-actions"><button class="guide-btn" data-guide="{{ game.name }}">📘 HOW TO PLAY</button><a class="play-btn" href="{{ game.url }}" target="_blank" rel="noopener noreferrer">PLAY NOW ↗</a></div></div></article>{% endfor %}</div><div class="no-results" id="noResults"><h3>😕 No games found</h3><p style="margin-top:8px">Try another name or select a different category.</p></div></section>

<section class="info-banner" id="play-here">
  <h2>🕹️ Play Games Right Here</h2>
  <p>These mini-games run directly in your browser after GameVerse loads. No extra download is needed. Tic-Tac-Toe and Memory Match work offline after the page has loaded.</p>
  <div class="mini-grid">
    <article class="mini-card">
      <h3>⭕ Tic-Tac-Toe</h3>
      <p>Take turns with a friend. Get three symbols in a row, column, or diagonal to win.</p>
      <div class="ttt-board" id="tttBoard" aria-label="Tic-Tac-Toe board"></div>
      <div class="mini-status" id="tttStatus">X goes first.</div>
      <button class="mini-button" id="tttReset" type="button">New round</button>
    </article>
    <article class="mini-card">
      <h3>🧠 Memory Match</h3>
      <p>Flip two cards at a time and find every matching pair.</p>
      <div class="memory-board" id="memoryBoard"></div>
      <div class="mini-status" id="memoryStatus">Find all 6 pairs.</div>
      <button class="mini-button" id="memoryReset" type="button">Shuffle cards</button>
    </article>
    <article class="mini-card">
      <h3>⚡ Reaction Test</h3>
      <p>Press Start, wait for the panel to turn green, then tap it quickly.</p>
      <button class="reaction-pad" id="reactionPad" type="button">Press Start</button>
      <div class="mini-status" id="reactionStatus">Your reaction time will appear here.</div>
      <button class="mini-button" id="reactionStart" type="button">Start test</button>
    </article>
  </div>
</section>
<section class="info-banner" id="online-play">
  <h2>🌐 More Online Games</h2>
  <p>These links open other websites. They need an internet connection, and some games may require an account or have their own rules and privacy settings.</p>
  <div class="online-links">
    <a href="https://www.chess.com/play/computer" target="_blank" rel="noopener noreferrer">♟️ Play Chess ↗</a>
    <a href="https://skribbl.io/" target="_blank" rel="noopener noreferrer">✏️ Play Skribbl.io ↗</a>
    <a href="https://garticphone.com/" target="_blank" rel="noopener noreferrer">🎨 Play Gartic Phone ↗</a>
    <a href="https://www.crazygames.com/" target="_blank" rel="noopener noreferrer">🎮 Browse browser games ↗</a>
  </div>
  <p class="chat-note">These are third-party websites. GameVerse does not own or control them.</p>
</section>

<section class="assistant-panel" id="assistant"><h2>🤖 GameVerse AI Assistant</h2><p>Ask about game rules, beginner tips, controls, or which game might suit you. The built-in helper works without an API key; a real AI connection can be enabled later using a private server-side key.</p><div class="chat-box"><div class="chat-log" id="homeChatLog" aria-live="polite"><div class="bubble bot">Hi! I'm the GameVerse gaming helper. Ask me how to play a game, get beginner tips, or choose a game to try.</div></div><form class="chat-form" id="homeChatForm"><input id="homeChatInput" maxlength="500" placeholder="Ask a gaming question..." aria-label="Ask the GameVerse assistant" required><button type="submit">ASK ↗</button></form></div><p class="chat-note">Safety tip: don't share passwords, private details, or account information in chat.</p></section>
<section class="info-banner" id="about"><h2>💜 Welcome to GameVerse</h2><p>GameVerse is an independent gaming discovery and learning hub. Browse games, read beginner guides, and visit official game websites. Controls and features can vary by platform and updates, so check the game's own settings and help pages too.</p></section>
</main><footer><strong>GAMEVERSE 🎮</strong><br>Made with Python and Flask. Built for gamers.<br>Game names and trademarks belong to their respective owners. GameVerse is an independent fan-made directory.</footer>
<div class="modal" id="guideModal" role="dialog" aria-modal="true" aria-labelledby="guideTitle"><div class="modal-card"><div class="modal-head"><h2 id="guideTitle">Game guide</h2><button class="close-btn" id="closeGuide" aria-label="Close guide">✕ Close</button></div><div class="guide-content"><section class="guide-section"><h3>🎯 What is the goal?</h3><p id="guideObjective"></p></section><section class="guide-section"><h3>🕹️ How to play</h3><p id="guideHow"></p></section><section class="guide-section"><h3>⌨️ Controls</h3><p id="guideControls"></p></section><section class="guide-section"><h3>💡 Beginner tips</h3><p id="guideTips"></p></section></div><div class="guide-chat"><h3>🤖 Ask about <span id="guideGameName"></span></h3><div class="chat-box"><div class="chat-log" id="guideChatLog"><div class="bubble bot">Ask a question about this game and I'll help with the basics.</div></div><form class="chat-form" id="guideChatForm"><input id="guideChatInput" maxlength="500" placeholder="Ask about this game..." aria-label="Ask about this game" required><button type="submit">ASK ↗</button></form></div></div></div></div>
<script>
const games = {{ games|tojson }};
const searchInput=document.getElementById("search"), cards=[...document.querySelectorAll(".game-card")], filters=[...document.querySelectorAll(".filter")], noResults=document.getElementById("noResults");
let activeCategory="All", currentGuide=null;
function filterGames(){const q=searchInput.value.trim().toLowerCase();let count=0;cards.forEach(card=>{const cat=activeCategory==="All"||card.dataset.category===activeCategory.toLowerCase();const text=card.dataset.name+" "+card.dataset.description+" "+card.dataset.category;const show=cat&&text.includes(q);card.style.display=show?"":"none";if(show)count++});noResults.style.display=count===0?"block":"none"}
filters.forEach(b=>b.addEventListener("click",()=>{activeCategory=b.dataset.category;filters.forEach(x=>x.classList.toggle("active",x===b));filterGames()}));
searchInput.addEventListener("input",filterGames);
document.querySelectorAll("[data-nav-category]").forEach(a=>a.addEventListener("click",()=>{activeCategory=a.dataset.navCategory;filters.forEach(x=>x.classList.toggle("active",x.dataset.category===activeCategory));filterGames()}));
const modal=document.getElementById("guideModal");
function addBubble(log,text,who){const b=document.createElement("div");b.className="bubble "+who;b.textContent=text;log.appendChild(b);log.scrollTop=log.scrollHeight;return b}
function openGuide(name){currentGuide=games.find(g=>g.name===name);if(!currentGuide)return;document.getElementById("guideTitle").textContent=currentGuide.name+" — Game Guide";document.getElementById("guideGameName").textContent=currentGuide.name;document.getElementById("guideObjective").textContent=currentGuide.objective;document.getElementById("guideHow").textContent=currentGuide.how;document.getElementById("guideControls").textContent=currentGuide.controls;document.getElementById("guideTips").textContent=currentGuide.tips;const log=document.getElementById("guideChatLog");log.replaceChildren();addBubble(log,"Ask a question about "+name+". I can explain the goal, controls, and beginner tips.","bot");modal.classList.add("open");document.getElementById("guideChatInput").focus()}
document.querySelectorAll("[data-guide]").forEach(b=>b.addEventListener("click",()=>openGuide(b.dataset.guide)));
function closeGuide(){modal.classList.remove("open")}document.getElementById("closeGuide").addEventListener("click",closeGuide);modal.addEventListener("click",e=>{if(e.target===modal)closeGuide()});document.addEventListener("keydown",e=>{if(e.key==="Escape")closeGuide()});
async function askHelper(question,gameName,log){addBubble(log,question,"user");const pending=addBubble(log,"Thinking...","bot");try{const res=await fetch("/api/ask",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({question,game:gameName||""})});const data=await res.json();pending.textContent=data.answer||"Sorry, I couldn't answer that just now."}catch(e){pending.textContent="I couldn't reach the helper. Please check that GameVerse is running and try again."}log.scrollTop=log.scrollHeight}
document.getElementById("homeChatForm").addEventListener("submit",e=>{e.preventDefault();const input=document.getElementById("homeChatInput"),q=input.value.trim();if(!q)return;input.value="";askHelper(q,"",document.getElementById("homeChatLog"))});
document.getElementById("guideChatForm").addEventListener("submit",e=>{e.preventDefault();const input=document.getElementById("guideChatInput"),q=input.value.trim();if(!q||!currentGuide)return;input.value="";askHelper(q,currentGuide.name,document.getElementById("guideChatLog"))});

// Local browser mini-games: no accounts or API keys needed.
const tttBoard = document.getElementById("tttBoard");
const tttStatus = document.getElementById("tttStatus");
let tttCells = Array(9).fill("");
let tttTurn = "X";
let tttFinished = false;
const tttWins = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]];
function drawTicTacToe() {
  tttBoard.replaceChildren();
  tttCells.forEach((value, index) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "ttt-cell";
    button.textContent = value;
    button.setAttribute("aria-label", "Square " + (index + 1) + (value ? ": " + value : ""));
    button.disabled = Boolean(value) || tttFinished;
    button.addEventListener("click", () => {
      if (tttFinished || tttCells[index]) return;
      tttCells[index] = tttTurn;
      const winner = tttWins.some(line => line.every(i => tttCells[i] === tttTurn));
      if (winner) {
        tttStatus.textContent = tttTurn + " wins! Start a new round to play again.";
        tttFinished = true;
      } else if (tttCells.every(Boolean)) {
        tttStatus.textContent = "It's a draw! Start a new round.";
        tttFinished = true;
      } else {
        tttTurn = tttTurn === "X" ? "O" : "X";
        tttStatus.textContent = tttTurn + "'s turn.";
      }
      drawTicTacToe();
    });
    tttBoard.appendChild(button);
  });
}
function resetTicTacToe() {
  tttCells = Array(9).fill(""); tttTurn = "X"; tttFinished = false;
  tttStatus.textContent = "X goes first."; drawTicTacToe();
}
document.getElementById("tttReset").addEventListener("click", resetTicTacToe);
resetTicTacToe();

const memoryBoard = document.getElementById("memoryBoard");
const memoryStatus = document.getElementById("memoryStatus");
const memorySymbols = ["🍓","🚀","🐱","⚽","🌈","🎮"];
let memoryDeck = [], memoryOpen = [], memoryMatches = 0, memoryLock = false, memoryMoves = 0;
function resetMemory() {
  memoryDeck = [...memorySymbols, ...memorySymbols].sort(() => Math.random() - 0.5);
  memoryOpen = []; memoryMatches = 0; memoryMoves = 0; memoryLock = false;
  memoryStatus.textContent = "Find all 6 pairs.";
  renderMemory();
}
function renderMemory() {
  memoryBoard.replaceChildren();
  memoryDeck.forEach((symbol, index) => {
    const button = document.createElement("button");
    button.type = "button"; button.className = "memory-card";
    const isOpen = memoryOpen.includes(index);
    const isMatched = memoryDeck[index] === null;
    button.textContent = isOpen || isMatched ? (symbol || "✓") : "?";
    if (isOpen) button.classList.add("flipped");
    if (isMatched) { button.classList.add("matched"); button.textContent = "✓"; }
    button.setAttribute("aria-label", isOpen || isMatched ? "Revealed card" : "Hidden card");
    button.disabled = memoryLock || isOpen || isMatched;
    button.addEventListener("click", () => flipMemory(index));
    memoryBoard.appendChild(button);
  });
}
function flipMemory(index) {
  if (memoryLock || memoryOpen.includes(index) || memoryDeck[index] === null) return;
  memoryOpen.push(index); renderMemory();
  if (memoryOpen.length === 2) {
    memoryMoves++;
    const [a,b] = memoryOpen;
    if (memoryDeck[a] === memoryDeck[b]) {
      memoryDeck[a] = null; memoryDeck[b] = null;
      memoryMatches++; memoryOpen = [];
      memoryStatus.textContent = memoryMatches === 6 ? "You found every pair in " + memoryMoves + " moves!" : "Match found! Pairs: " + memoryMatches + "/6.";
      renderMemory();
    } else {
      memoryLock = true;
      memoryStatus.textContent = "Not a match. Try to remember their places!";
      setTimeout(() => { memoryOpen = []; memoryLock = false; renderMemory(); }, 750);
    }
  }
}
document.getElementById("memoryReset").addEventListener("click", resetMemory);
resetMemory();

const reactionPad = document.getElementById("reactionPad");
const reactionStatus = document.getElementById("reactionStatus");
const reactionStart = document.getElementById("reactionStart");
let reactionState = "idle", reactionTimer = null, reactionStartedAt = 0;
reactionPad.addEventListener("click", () => {
  if (reactionState === "waiting") {
    clearTimeout(reactionTimer); reactionState = "idle";
    reactionPad.className = "reaction-pad"; reactionPad.textContent = "Too soon! Press Start.";
    reactionStatus.textContent = "Wait for green next time."; return;
  }
  if (reactionState === "ready") {
    const ms = Math.round(performance.now() - reactionStartedAt);
    reactionState = "idle"; reactionPad.className = "reaction-pad";
    reactionPad.textContent = "Press Start"; reactionStatus.textContent = "Your reaction time: " + ms + " ms.";
  }
});
reactionStart.addEventListener("click", () => {
  clearTimeout(reactionTimer); reactionState = "waiting";
  reactionPad.className = "reaction-pad waiting"; reactionPad.textContent = "Wait for green...";
  reactionStatus.textContent = "Don't click yet!";
  reactionTimer = setTimeout(() => {
    if (reactionState !== "waiting") return;
    reactionState = "ready"; reactionStartedAt = performance.now();
    reactionPad.className = "reaction-pad ready"; reactionPad.textContent = "CLICK NOW!";
    reactionStatus.textContent = "Go!";
  }, 1200 + Math.random() * 2800);
});

</script></body></html>
"""

def local_answer(question, game_name=""):
    q = question.lower()
    game = GUIDE_BY_NAME.get(game_name)
    if game:
        if any(word in q for word in ["goal", "objective", "what is", "about", "meaning"]):
            return game["objective"]
        if any(word in q for word in ["how", "start", "begin", "play", "first"]):
            return game["how"]
        if any(word in q for word in ["control", "keyboard", "key", "button", "mobile"]):
            return game["controls"]
        if any(word in q for word in ["tip", "better", "improve", "beginner", "good at", "strategy"]):
            return game["tips"]
        return (f"Here's a quick guide for {game['name']}:\n\nGoal: {game['objective']}\n\nHow to play: {game['how']}\n\nBeginner tip: {game['tips']}\n\nAsk me specifically about the goal, controls, how to start, or tips.")
    if any(word in q for word in ["recommend", "which game", "what game", "suggest", "choose"]):
        return "For building and creativity, try Minecraft or Stardew Valley. For fast action, try Brawl Stars or Fortnite. For racing and sports, try Rocket League or Trackmania. For relaxed party fun, try Fall Guys or Among Us. Check each game's age rating and device requirements before playing."
    if "roblox" in q: return "Roblox is a platform with many different player-made experiences. Choose an experience, press Play, and follow its instructions. Controls differ between experiences. Never share your password or private details."
    if "minecraft" in q: return "In Minecraft, gather wood first, craft basic tools, collect food, and build shelter before night in Survival mode. Creative mode lets you build freely with resources available."
    if "fortnite" in q: return "Fortnite has several modes. In Battle Royale, collect equipment, watch the safe-zone circle, use cover, and work with your team. Try the tutorial or a practice mode to learn controls."
    if "valorant" in q: return "VALORANT is a tactical team shooter. Learn one agent, practise in the Range, keep your crosshair near head height, communicate with teammates, and focus on the round objective."
    return "I can help with the games listed on GameVerse: Roblox, Minecraft, Fortnite, VALORANT, Among Us, Rocket League, Fall Guys, Genshin Impact, PUBG: Battlegrounds, Brawl Stars, Stardew Valley, and Trackmania. Ask about a game's goal, how to start, controls, beginner tips, or ask for a game recommendation."

def ai_answer(question, game_name=""):
    # Optional real AI connection. Keep OPENAI_API_KEY on the server only.
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return local_answer(question, game_name)
    game = GUIDE_BY_NAME.get(game_name)
    context = ""
    if game:
        context = (
            f"\nGame guide facts for {game['name']}:\n"
            f"Goal: {game['objective']}\nHow to play: {game['how']}\n"
            f"Controls: {game['controls']}\nTips: {game['tips']}\n"
        )
    payload = {
        "model": os.environ.get("OPENAI_MODEL", "gpt-4.1-mini"),
        "messages": [
            {"role": "system", "content": "You are GameVerse, a friendly gaming helper. Give clear, age-appropriate advice about games, controls, beginner strategies, and recommendations. Do not ask for passwords or personal information. If unsure about a current game update, say so. Keep answers concise. Use the provided guide facts when relevant." + context},
            {"role": "user", "content": question}
        ],
        "max_tokens": 350
    }
    req = Request("https://api.openai.com/v1/chat/completions",
                  data=json.dumps(payload).encode("utf-8"),
                  headers={"Authorization": "Bearer " + api_key,
                           "Content-Type": "application/json"},
                  method="POST")
    try:
        with urlopen(req, timeout=20) as response:
            data = json.loads(response.read().decode("utf-8"))
        return data["choices"][0]["message"]["content"].strip()
    except (HTTPError, URLError, TimeoutError, KeyError, ValueError):
        app.logger.exception("AI service request failed")
        return "The AI service is unavailable right now. Please try again later. Your built-in gaming helper is available when no AI key is configured."

@app.route("/")
def home():
    return render_template_string(PAGE, games=GAMES)

@app.route("/api/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True) or {}
    question = str(data.get("question", "")).strip()[:500]
    game_name = str(data.get("game", "")).strip()[:100]
    if not question:
        return jsonify({"answer": "Type a question first."}), 400
    if game_name and game_name not in GUIDE_BY_NAME:
        game_name = ""
    return jsonify({"answer": ai_answer(question, game_name)})

if __name__ == "__main__":
    # debug=False is safer for normal use and works with a launcher.
    app.run(debug=False)
