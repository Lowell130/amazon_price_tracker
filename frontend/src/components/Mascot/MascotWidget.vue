<template>
  <div 
    v-if="isVisible && isAdmin"
    class="fixed z-[9999] hide-on-mobile transition-all duration-500"
    :style="widgetStyle"
    @pointerdown="startDrag"
  >
    <!-- Bubble Speech (Moved to the LEFT & Slightly HIGHER) -->
    <transition name="fade">
      <div 
        v-if="showMessage && mascot" 
        class="absolute -top-12 w-[380px] rounded-[1.5rem] shadow-[0_20px_50px_rgba(0,0,0,0.15)] border pointer-events-auto overflow-hidden transition-all duration-300"
        :class="[
          isAngry ? 'bg-slate-900 border-red-500/50 text-white shadow-red-500/10' : 'bg-white dark:bg-gray-800 border-gray-100 dark:border-gray-700 text-gray-700 dark:text-gray-200',
          bubbleOnRight ? 'left-full ml-6 animate-slide-right' : 'right-full mr-6 animate-slide-left'
        ]"
        @pointerdown.stop
      >
        <!-- Message Content -->
        <!-- Close Button (X) -->
        <button 
          @click="closeBubble" 
          class="absolute top-4 right-4 text-gray-300 dark:text-gray-500 hover:text-red-400 dark:hover:text-red-500 transition-colors z-10"
          title="Chiudi"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
        <div class="px-7 py-6">
          <p class="text-[14px] font-medium leading-relaxed" :class="isAngry ? 'text-red-100' : 'mb-6'">
            {{ isAngry ? "Grrr! Mi hai stufato con tutti questi clic! Lasciami in pace un attimo, miao!" : currentMessage }}
          </p>
          
          <!-- Chat Input (Hidden when angry) -->
          <div v-if="isTalking && !isAngry" class="mt-4 border-t border-gray-50 dark:border-gray-700 pt-5 animate-fade-in">
            <input 
              ref="chatInput"
              v-model="userMessage" 
              @keyup.enter="sendMessage"
              :disabled="loadingChat"
              placeholder="Scrivi qui..."
              class="w-full bg-gray-50 dark:bg-gray-900 border-none rounded-xl px-4 py-3 text-sm focus:ring-2 focus:ring-blue-500/30 transition-all outline-none"
            />
            <div class="flex justify-end mt-3">
              <span v-if="loadingChat" class="text-[9px] text-gray-400 animate-pulse font-bold uppercase tracking-widest">Pricey sta scrivendo...</span>
              <button 
                v-else
                @click="sendMessage"
                class="text-[11px] font-black text-blue-600 dark:text-blue-400 uppercase tracking-widest hover:translate-x-1 transition-transform"
              >
                Invia
              </button>
            </div>
          </div>

          <!-- Interaction Buttons (Fixed Alignment) -->
          <div v-else-if="!isAngry" class="flex flex-col gap-4 mt-2 pt-2 border-t border-gray-50 dark:border-gray-700/50">
            <!-- Direct Actions Row -->
            <div class="flex items-center justify-around py-1">
              <button @click="interact('pet')" :disabled="loading" class="flex flex-col items-center gap-1 group/btn transition-transform hover:scale-110">
                <span class="text-xl">🖐️</span>
                <span class="text-[9px] font-bold text-gray-500 uppercase tracking-tighter">Accarezza</span>
              </button>
              <button @click="interact('feed')" :disabled="loading" class="flex flex-col items-center gap-1 group/btn transition-transform hover:scale-110">
                <span class="text-xl">🍗</span>
                <span class="text-[9px] font-bold text-gray-500 uppercase tracking-tighter">Nutri</span>
              </button>
              <div class="w-px h-8 bg-gray-100 dark:bg-gray-700 mx-2"></div>
              <button @click="openChat" class="flex flex-col items-center gap-1 group/btn transition-transform hover:scale-110">
                <span class="text-xl">💬</span>
                <span class="text-[9px] font-bold text-blue-500 uppercase tracking-tighter">Parla</span>
              </button>
            </div>
            
            <div class="flex justify-center">
               <button @click="closeBubble" class="text-[9px] font-black text-gray-300 dark:text-gray-500 uppercase tracking-widest hover:text-red-400 transition-colors whitespace-nowrap">
                Nascondi il gatto
              </button>
            </div>
          </div>
        </div>
        
        <!-- Triangle pointer (Moved to the RIGHT side) -->
        <div class="absolute top-8 w-5 h-5 border-t border-r transform rotate-45"
          :class="[
            isAngry ? 'bg-slate-900 border-red-500/50' : 'bg-white dark:bg-gray-800 border-gray-100 dark:border-gray-700',
            bubbleOnRight ? '-left-2 border-l border-b border-t-0 border-r-0' : '-right-2'
          ]"
        ></div>
      </div>
    </transition>

    <!-- Mascot Container -->
    <div 
      class="relative cursor-grab active:cursor-grabbing group"
      :class="{ 'dragging': dragging }"
      @mouseenter="handlePetting"
      @mousemove="handlePetting"
      @mouseleave="hovering = false"
      style="touch-action: none;"
      draggable="false"
    >
      <!-- XP Tooltip -->
      <div v-if="mascot" class="absolute -top-14 left-1/2 -translate-x-1/2 bg-slate-900/90 backdrop-blur-md text-white text-[10px] font-black px-4 py-2 rounded-2xl opacity-0 group-hover:opacity-100 transition-all duration-300 whitespace-nowrap shadow-2xl scale-95 group-hover:scale-100 pointer-events-none">
        <div class="flex justify-between items-center gap-4 mb-1.5">
          <span>LV.{{ mascot.level }}</span>
          <span class="opacity-60">{{ mascot.xp }}/{{ mascot.next_level_xp }} XP</span>
        </div>
        <div class="w-32 h-1.5 bg-white/10 rounded-full overflow-hidden">
          <div class="h-full bg-gradient-to-r from-yellow-400 to-orange-500" :style="{ width: (mascot.xp / mascot.next_level_xp * 100) + '%' }"></div>
        </div>
      </div>

      <!-- Professional Mascot Image (Active/Sleeping Toggle) -->
      <div class="w-28 h-28 sm:w-32 sm:h-32 mascot-image-wrapper" :class="[mascot?.mood, { bouncing: bubbleBouncing }]">
        <img 
          ref="mascotImg"
          :src="mascotSrc" 
          alt="Pricey Mascot" 
          class="w-full h-full object-contain mascot-img drop-shadow-xl"
          @load="processImage"
          v-show="imageProcessed"
        />
        <!-- Loading state for image processing -->
        <div v-if="!imageProcessed" class="w-full h-full flex items-center justify-center">
           <div class="w-8 h-8 border-2 border-orange-500 border-t-transparent rounded-full animate-spin"></div>
        </div>

        <!-- Mood FX -->
        <div v-if="mascot?.mood === 'excited'" class="absolute -top-4 -right-2">
          <span class="animate-bounce inline-flex h-4 w-4 rounded-full bg-yellow-400 opacity-75"></span>
        </div>
        
        <!-- Zzz (Only when asleep/bubble hidden) -->
        <div v-if="!showMessage && mascot?.mood === 'sleepy' && !dragging && !hovering" class="absolute -top-0 right-4 z-particles">
          <span class="zzz z1">Z</span>
          <span class="zzz z2">z</span>
          <span class="zzz z3">z</span>
        </div>



        <!-- Floating Hearts -->
        <transition-group name="heart" tag="div" class="absolute inset-0 pointer-events-none">
          <div 
            v-for="heart in hearts" 
            :key="heart.id" 
            class="heart-float"
            :style="{ left: heart.x + '%', bottom: heart.y + '%' }"
          >
            <svg viewBox="0 0 32 32" class="w-4 h-4 text-red-500 fill-current">
              <path d="M16 28.5L14.5 27.1C9.2 22.3 5.7 19.3 5.7 15.5C5.7 12.4 8.1 10 11.2 10C13 10 14.7 10.8 15.8 12.1C16.9 10.8 18.6 10 20.4 10C23.5 10 25.9 12.4 25.9 15.5C25.9 19.3 22.4 22.3 17.1 27.1L15.6 28.5H16Z" />
            </svg>
          </div>
        </transition-group>

        <!-- Falling Kibble Animation -->
        <transition-group name="kibble" tag="div" class="absolute inset-0 pointer-events-none">
          <div 
            v-for="k in kibbles" 
            :key="k.id" 
            class="kibble-drop"
            :style="{ left: k.x + '%', animationDelay: k.delay + 's' }"
          >
            🟤
          </div>
        </transition-group>
      </div>

      <!-- DEBUG OVERLAY (Visible when showDebug = true) -->
      <div v-if="showDebug" class="absolute -bottom-24 left-1/2 -translate-x-1/2 bg-black/80 backdrop-blur-md text-[9px] text-green-400 p-3 rounded-lg font-mono border border-green-500/20 whitespace-nowrap shadow-2xl z-[10000] pointer-events-none">
        <div class="flex flex-col gap-1">
          <div class="flex justify-between gap-4"><span>STATE:</span> <span class="text-white">{{ debugState }}</span></div>
          <div class="flex justify-between gap-4"><span>SILENCE:</span> <span class="text-white">{{ silenceSecondsLeft }}s</span></div>
          <div class="flex justify-between gap-4"><span>CLICKS:</span> <span class="text-white">{{ clickData.count }}/5</span></div>
          <div class="flex justify-between gap-4"><span>SCHEDULE:</span> <span class="text-white">{{ isNightTime() ? 'NIGHT' : 'DAY' }}</span></div>
          <div class="flex justify-between gap-4"><span>MOOD:</span> <span class="text-white">{{ mascot?.mood || 'null' }}</span></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { jwtDecode } from "jwt-decode";

export default {
  name: "MascotWidget",
  data() {
    return {
      mascot: null,
      showMessage: false,
      loading: false,
      loadingChat: false,
      isTalking: false,
      userMessage: "",
      chatResponse: "",
      drillingDown: false,

      dragging: false,
      hovering: false,
      imageProcessed: false,
      isAngry: false,
      isYawning: false,
      isStretching: false,
      isAdmin: false,
      showDebug: true,
      lastSeenScrapeTime: localStorage.getItem('mascot_last_scrape_time') || null,
      scrapeReportMessage: null,
      hearts: [],
      kibbles: [],
      nextHeartId: 0,
      nextKibbleId: 0,
      bubbleBouncing: false,
      prevStats: null,
      clickData: { count: 0, lastTime: 0 },
      isVisible: localStorage.getItem('mascot_enabled') !== 'false',
      position: {
        x: window.innerWidth - 180,
        y: window.innerHeight - 180
      },
      touchStartPos: { x: 0, y: 0 }, // For distinguishing click vs drag
      offset: { x: 0, y: 0 }
    };
  },
  computed: {
    mascotSrc() {
      // Angry takes priority
      if (this.isAngry) {
        return require('@/assets/mascot_angry.png');
      }
      // Yawning or Stretching during transitions
      if (this.isYawning) {
        return require('@/assets/mascot_yawning.png');
      }
      if (this.isStretching) {
        return require('@/assets/mascot_stretching.png');
      }
      // Use sleeping image when bubble is closed
      if (!this.showMessage) {
        return require('@/assets/mascot_sleeping.png');
      }
      return require('@/assets/mascot.png');
    },
    bubbleOnRight() {
      // Se il gatto è nella metà sinistra dello schermo, sposta la bolla a destra
      return this.position.x < window.innerWidth / 2;
    },
    currentMessage() {
      if (this.scrapeReportMessage) return this.scrapeReportMessage;
      return this.chatResponse || (this.mascot ? this.mascot.message : "");
    },
    widgetStyle() {
      return {
        left: `${this.position.x}px`,
        top: `${this.position.y}px`,
        transition: this.dragging ? 'none' : 'all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275)'
      };
    },
    debugState() {
      if (this.isAngry) return 'ANGRY 💢';
      if (this.isYawning) return 'YAWNING 🥱';
      if (this.isStretching) return 'STRETCHING 🧘‍♂️';
      if (!this.showMessage) return 'SLEEPING 💤';
      return 'ACTIVE 🐱';
    },
    silenceSecondsLeft() {
      const silencedUntil = sessionStorage.getItem('mascot_silenced_until');
      if (!silencedUntil) return 0;
      const left = Math.ceil((parseInt(silencedUntil) - Date.now()) / 1000);
      return Math.max(0, left);
    }
  },
  watch: {
    mascotSrc() {
      this.imageProcessed = false;
    },
    showMessage(newVal, oldVal) {
      // Trigger yawning when waking up (not if already angry)
      if (newVal === true && oldVal === false && !this.isAngry) {
        console.log("%c [Pricey] Waking up with a yawn... 🥱", "color: #fbbf24; font-weight: bold;");
        this.isYawning = true;
        setTimeout(() => {
          this.isYawning = false;
          console.log("%c [Pricey] Fully awake now! 🐱", "color: #10b981; font-weight: bold;");
        }, 3500); // 3.5s yawn
      }
    }
  },
  async mounted() {
    const savedPos = localStorage.getItem('mascot_position');
    if (savedPos) {
      try {
        const parsed = JSON.parse(savedPos);
        this.position.x = Math.max(20, Math.min(parsed.x, window.innerWidth - 120));
        this.position.y = Math.max(20, Math.min(parsed.y, window.innerHeight - 150));
      } catch (e) { console.error(e); }
    }

    window.addEventListener('pointermove', this.onDrag);
    window.addEventListener('pointerup', this.stopDrag);
    window.addEventListener('resize', this.keepInBounds);
    window.addEventListener('mascot-settings-changed', this.updateVisibility);
    window.addEventListener('auth-state-changed', this.checkAdminStatus);
    
    // Initial check
    this.checkAdminStatus();

    if (this.isVisible && this.isAdmin) {
      await this.fetchMascot();
      // Show bubble only if alert/active conditions are met
      if (!this.isSilenced() && !this.isNightTime()) {
        setTimeout(() => { if (!this.isSilenced() && !this.isNightTime()) this.showMessage = true; }, 2000);
      }
    }
    
    this.fetchInterval = setInterval(this.fetchMascot, 300000);
    this.idleInterval = setInterval(this.triggerIdle, 15000);
    this.inactivityInterval = setInterval(this.handleInactivity, 60000); // Check for stretching every minute
  },
  beforeUnmount() {
    window.removeEventListener('pointermove', this.onDrag);
    window.removeEventListener('pointerup', this.stopDrag);
    window.removeEventListener('resize', this.keepInBounds);
    window.removeEventListener('mascot-settings-changed', this.updateVisibility);
    window.removeEventListener('auth-state-changed', this.checkAdminStatus);
    
    if (this.fetchInterval) clearInterval(this.fetchInterval);
    if (this.idleInterval) clearInterval(this.idleInterval);
    if (this.inactivityInterval) clearInterval(this.inactivityInterval);
  },
  methods: {
    updateVisibility() {
      this.isVisible = localStorage.getItem('mascot_enabled') !== 'false';
      if (this.isVisible && this.isAdmin && !this.mascot) {
        this.fetchMascot();
      }
    },
    checkAdminStatus() {
      const token = localStorage.getItem('token');
      console.log("%c [Pricey Debug] Checking Auth... Token exists:", "color: #3b82f6;", !!token);
      
      if (!token) {
        this.isAdmin = false;
        return;
      }
      try {
        const decoded = jwtDecode(token);
        const now = Math.floor(Date.now() / 1000);
        this.isAdmin = (decoded.admin === true) && (decoded.exp > now);
        console.log("%c [Pricey Debug] Decoded Token:", "color: #3b82f6;", { 
          isAdmin: this.isAdmin, 
          rawAdmin: decoded.admin,
          expired: decoded.exp <= now 
        });
      } catch (e) {
        console.error("[Pricey Debug] JWT Decode Error:", e);
        this.isAdmin = false;
      }
    },
    async fetchMascot() {
      try {
        const token = localStorage.getItem('token');
        // Robust token check
        if (!token || token === 'null' || token === 'undefined' || !this.isVisible) {
           if (this.showMessage) this.showMessage = false;
           return;
        }

        // Logic check: don't fetch if silenced/night unless already talking
        // REMOVED binary check that prevented fetching while silenced/night
        // We want data even if Pricey is sleeping!
        
        
        const response = await axios.get(`${process.env.VUE_APP_API_BASE_URL}/mascot`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        
        // Smart Awakening logic: Detect traffic bursts
        if (this.mascot && response.data) {
           const curStats = response.data.stats || {};
           const oldStats = this.prevStats || {};
           if (curStats.visits > oldStats.visits * 1.2 && !this.showMessage) {
              console.log("%c [Pricey] Noticed a traffic spike! Surprised and waking up! 🚀", "color: #f59e0b; font-weight: bold;");
              this.wakeUp();
           }
           this.prevStats = curStats;
        }

        // Detect new scrape results
        if (response.data.last_scrape_data) {
           const scrape = response.data.last_scrape_data;
           const isNew = !this.lastSeenScrapeTime || (new Date(scrape.timestamp) > new Date(this.lastSeenScrapeTime));
           
           // Only react if scrape was finished recently (last 10 mins) and it's new
           const wasRecent = (new Date() - new Date(scrape.timestamp)) < (10 * 60 * 1000);
           
           if (isNew && wasRecent) {
              console.log("%c [Pricey] Scraping results detected! Waking up with the news! 🐱📰", "color: #8b5cf6; font-weight: bold;");
              this.handleNewScrapeReport(scrape);
           }
        }

        if (!this.isTalking) {
           this.mascot = response.data;
           
           // AGENTIC PROACTIVE LOGIC
           const proactive = response.data.proactive_alert;
           if (proactive && proactive !== this.chatResponse) {
              console.log("%c [Pricey Agent] INCOMING PROACTIVE INSIGHT! 🐾🧠", "color: #3b82f6; font-weight: bold;");
              this.chatResponse = proactive;
              if (!this.showMessage) {
                 this.wakeUp(); // Proactive Auto-Wake!
              }
              // Bounce the bubble to attract attention
              this.bubbleBouncing = true;
              setTimeout(() => { this.bubbleBouncing = false; }, 8000);
           }
        }
      } catch (error) {
        if (error.response && error.response.status === 401) {
          // If unauthorized, just mark as non-admin for this check
          // DO NOT set isVisible = false as it would override user preference
          this.isAdmin = false;
          this.showMessage = false;
          console.log("%c [Pricey] Session expired or unauthorized. Hiding.", "color: #ef4444;");
        } else {
          console.error("Error fetching mascot:", error);
        }
      }
    },
    async sendMessage() {
      if (!this.userMessage.trim() || this.loadingChat) return;
      this.loadingChat = true;
      try {
        const token = localStorage.getItem('token');
        const response = await axios.post(`${process.env.VUE_APP_API_BASE_URL}/mascot/chat`, {
          message: this.userMessage
        }, {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.chatResponse = response.data.response;
        this.userMessage = "";
        this.isTalking = false; // Ritorna alla modalità con i tasti Nascondi/Parla
        this.fetchMascot();
      } catch (error) {
        console.error("Error sending message:", error);
        this.chatResponse = "Scusa miao, ho dei problemi di connessione...";
      } finally {
        this.loadingChat = false;
      }
    },
    processImage() {
      const img = this.$refs.mascotImg;
      if (!img || this.imageProcessed) return;

      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');
      canvas.width = img.naturalWidth;
      canvas.height = img.naturalHeight;

      ctx.drawImage(img, 0, 0);

      const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
      const data = imageData.data;

      // Make pixels with color close to white transparent
      for (let i = 0; i < data.length; i += 4) {
        const r = data[i];
        const g = data[i + 1];
        const b = data[i + 2];
        
        // Threshold for "white" - adjust if needed
        if (r > 240 && g > 240 && b > 240) {
          data[i + 3] = 0; // Set alpha to 0
        }
      }

      ctx.putImageData(imageData, 0, 0);
      img.src = canvas.toDataURL();
      this.imageProcessed = true;
    },
    openChat() {
      this.isTalking = true;
      this.chatResponse = ""; // Pulisce la vecchia risposta solo quando inizi a parlare di nuovo
      this.$nextTick(() => {
        if (this.$refs.chatInput) this.$refs.chatInput.focus();
      });
    },
    closeBubble() {
      console.log("%c [Pricey] Going to sleep (Hidden by user) 💤", "color: #60a5fa; font-weight: bold;");
      this.showMessage = false;
      this.isTalking = false;
      this.chatResponse = "";
      
      // Silence for 30 minutes (persist in sessionStorage)
      const silenceUntil = Date.now() + (30 * 60 * 1000);
      sessionStorage.setItem('mascot_silenced_until', silenceUntil);
      
      setTimeout(() => {
        if (!this.dragging && this.isVisible && !this.isSilenced()) {
          console.log("%c [Pricey] Silence timeout over, waking up automatically 🐱", "color: #10b981; font-weight: bold;");
          this.showMessage = true;
        }
      }, 30 * 60 * 1000);
    },
    isSilenced() {
      const silencedUntil = sessionStorage.getItem('mascot_silenced_until');
      if (!silencedUntil) return false;
      return Date.now() < parseInt(silencedUntil);
    },
    startDrag(e) {
      if (e.button !== 0 && e.pointerType === 'mouse') return; // Only left click for mouse
      e.preventDefault();
      
      // Track clicks for anger logic
      this.handleMascotClick();
      
      this.dragging = true;
      this.touchStartPos = { x: e.clientX, y: e.clientY };
      this.offset.x = e.clientX - this.position.x;
      this.offset.y = e.clientY - this.position.y;
      
      // Capture the pointer to ensure we get the 'up' event even outside window
      if (e.target.setPointerCapture) {
        e.target.setPointerCapture(e.pointerId);
      }
    },
    onDrag(e) {
      if (!this.dragging) return;
      this.position.x = e.clientX - this.offset.x;
      this.position.y = e.clientY - this.offset.y;
    },
    stopDrag(e) {
      if (!this.dragging) return;
      this.dragging = false;

      // Distinguish click from drag
      const dist = Math.sqrt(
        Math.pow(e.clientX - this.touchStartPos.x, 2) + 
        Math.pow(e.clientY - this.touchStartPos.y, 2)
      );

      // If moved less than 5px, it's a click: WAKE UP!
      if (dist < 5) {
        this.wakeUp();
      }
      
      // Release capture from the element that started the drag
      const el = document.querySelector('.cursor-grabbing') || e.target;
      if (el && el.releasePointerCapture && e.pointerId !== undefined) {
        try {
          el.releasePointerCapture(e.pointerId);
        } catch (err) { /* ignore */ }
      }

      localStorage.setItem('mascot_position', JSON.stringify(this.position));
    },
    handleMascotClick() {
      const now = Date.now();
      if (now - this.clickData.lastTime < 3000) {
        this.clickData.count++;
      } else {
        this.clickData.count = 1;
      }
      this.clickData.lastTime = now;

      // Don't get angry if we just woke him up (give him some grace)
      if (this.clickData.count >= 5 && !this.isAngry && !this.isYawning) {
        this.becomeAngry();
      }
    },
    wakeUp() {
      console.log("%c [Pricey] Manual wake up requested! 🐾", "color: #f472b6; font-weight: bold;");
      // Clear any session silence
      sessionStorage.removeItem('mascot_silenced_until');
      
      // Wake up only if not already showing or yawning
      if (!this.showMessage && !this.isYawning) {
        this.showMessage = true;
      }
    },
    isNightTime() {
      const hour = new Date().getHours();
      const night = hour >= 23 || hour < 8; // Night sleep 23:00 to 08:00
      if (night && !this.showMessage) {
        // Only log once to avoid cluttering in interval
        // console.log("%c [Pricey] Respecting night schedule (Sleeping) 💤", "color: #818cf8;");
      }
      return night;
    },
    becomeAngry() {
      console.log("%c [Pricey] GRRR! I'm getting ANGRY! 💢", "color: #ef4444; font-weight: bold; font-size: 1.2em;");
      this.isAngry = true;
      this.showMessage = true;
      this.isTalking = false;
      
      // Reset after 10 seconds
      setTimeout(() => {
        console.log("%c [Pricey] Cooling down... feeling better now. 🐱", "color: #6ee7b7;");
        this.isAngry = false;
        this.clickData.count = 0;
        // Optionally close bubble if it was closed before
        const wasSilenced = this.isSilenced();
        if (wasSilenced) this.showMessage = false;
      }, 10000);
    },
    keepInBounds() {
      this.position.x = Math.max(10, Math.min(this.position.x, window.innerWidth - 120));
      this.position.y = Math.max(10, Math.min(this.position.y, window.innerHeight - 150));
    },
    triggerIdle() {
      if (this.dragging || this.isTalking || Math.random() > 0.3 || !this.isVisible) return;
      
      // If sleeping, maybe stretch
      if (!this.showMessage && Math.random() > 0.7) {
        this.stretch();
        return;
      }
    },
    stretch() {
      if (this.isStretching || this.isAngry || this.showMessage) return;
      console.log("%c [Pricey] Stretching pigramente... 🥱🧘‍♂️", "color: #fb7185;");
      this.isStretching = true;
      setTimeout(() => {
        this.isStretching = false;
      }, 4000);
    },
    handleInactivity() {
      // Periodic check while sleeping to show life
      if (!this.showMessage && !this.isStretching && !this.isAngry && Math.random() > 0.5) {
        this.stretch();
      }
    },
    spawnHeart() {
      if (this.hearts.length > 10) return;
      const id = this.nextHeartId++;
      this.hearts.push({
        id,
        x: 40 + Math.random() * 20,
        y: 60 + Math.random() * 20
      });
      setTimeout(() => {
        this.hearts = this.hearts.filter(h => h.id !== id);
      }, 2000);
    },
    handleNewScrapeReport(scrape) {
      this.lastSeenScrapeTime = scrape.timestamp;
      localStorage.setItem('mascot_last_scrape_time', scrape.timestamp);
      
      const emoji = scrape.drops_found > 0 ? "🚀💰" : "📋✅";
      const word = scrape.drops_found > 0 ? "FANTASTICO!" : "Fatto!";
      this.scrapeReportMessage = `${word} Miao! Ho finito di aggiornare ${scrape.updated_count} prodotti. Ho trovato ben ${scrape.drops_found} cali di prezzo! ${emoji}`;
      
      if (!this.showMessage) {
        this.wakeUp();
      }
      
      // Proactive attention: Bounce if major drops found (>1)
      if (scrape.drops_found > 1) {
         console.log("%c [Pricey] BOUNCING! Found multiple drops! 🐾🔥", "color: #ef4444; font-weight: bold;");
         this.isStretching = false; // Override stretch
         this.isYawning = false;
         this.bubbleBouncing = true;
         setTimeout(() => { this.bubbleBouncing = false; }, 5000);
      }

      // Clear report message after 30 seconds to return to normal passive thoughts
      setTimeout(() => {
        this.scrapeReportMessage = null;
      }, 30000);
    },
    async interact(action) {
      if (this.loading) return;
      this.loading = true;
      try {
        const token = localStorage.getItem('token');
        const response = await axios.post(`${process.env.VUE_APP_API_BASE_URL}/mascot/interact?action=${action}`, {}, {
          headers: { Authorization: `Bearer ${token}` }
        });
        
        this.chatResponse = response.data.message;
        
        if (action === 'feed') {
           this.spawnKibble();
        } else if (action === 'pet') {
           this.spawnHeart();
           this.spawnHeart();
        }
        
        this.fetchMascot(); // Update levels/XP
      } catch (err) {
        console.error("Interaction failed:", err);
      } finally {
        this.loading = false;
      }
    },
    spawnKibble() {
      for (let i = 0; i < 8; i++) {
        const id = this.nextKibbleId++;
        this.kibbles.push({
          id,
          x: 20 + Math.random() * 60,
          delay: Math.random() * 0.5
        });
        setTimeout(() => {
          this.kibbles = this.kibbles.filter(k => k.id !== id);
        }, 3000);
      }
    },
    handlePetting() {
      if (this.isAngry) return;
      this.spawnHeart();
    }
  }
};
</script>

<style scoped>
.mascot-image-wrapper {
  animation: breathe 4s ease-in-out infinite;
  transform-origin: bottom center;
  transition: transform 0.3s ease;
}

/* Purring vibration on hover */
.group:hover .mascot-image-wrapper:not(.dragging) {
  animation: breathe 4s ease-in-out infinite, purr 0.4s ease-in-out infinite;
}

.mascot-image-wrapper.bouncing {
  animation: jump 0.5s ease-in-out infinite alternate !important;
}

@keyframes jump {
  from { transform: translateY(0); }
  to { transform: translateY(-25px); }
}

@keyframes purr {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.02); }
}

.heart-float {
  position: absolute;
  animation: heart-up 2s ease-out forwards;
  opacity: 0;
}

@keyframes heart-up {
  0% { transform: translateY(0) scale(0.5); opacity: 0; }
  20% { opacity: 0.8; }
  100% { transform: translateY(-80px) scale(1.5) rotate(15deg); opacity: 0; }
}

.mascot-img {
  filter: contrast(105%) brightness(105%);
}

.dark .mascot-img {
  filter: drop-shadow(0 0 12px rgba(251, 191, 36, 0.4));
}

.dragging .mascot-image-wrapper {
  transform: scale(1.1) rotate(5deg);
  animation: squish 0.3s ease-out infinite alternate;
}

@keyframes breathe {
  0%, 100% { transform: translateY(0) scale(1); }
  50% { transform: translateY(-5px) scale(1.03); }
}

@keyframes squish {
  from { transform: scale(1.1, 0.9) rotate(5deg); }
  to { transform: scale(0.9, 1.1) rotate(5deg); }
}

.kibble-drop {
  position: absolute;
  top: -20px;
  animation: kibble-fall 2s ease-in forwards;
  font-size: 14px;
}

@keyframes kibble-fall {
  0% { transform: translateY(0) rotate(0deg); opacity: 1; }
  100% { transform: translateY(150px) rotate(360deg); opacity: 0; }
}

.fade-enter-active, .fade-leave-active { 
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); 
}
.fade-enter-from, .fade-leave-to { 
  opacity: 0; transform: translateX(20px) scale(0.95); 
}

@keyframes slideLeft {
  from { opacity: 0; transform: translateX(20px); }
  to { opacity: 1; transform: translateX(0); }
}

@keyframes slide-right {
  from { opacity: 0; transform: translateX(-20px) scale(0.95); }
  to { opacity: 1; transform: translateX(0) scale(1); }
}

.animate-slide-left {
  animation: slideLeft 0.4s ease-out;
}

.sleepy .mascot-image-wrapper { opacity: 0.85; animation-duration: 6s; }
.excited .mascot-image-wrapper { animation: bounce 0.6s infinite alternate; }
@keyframes bounce { from { transform: translateY(0); } to { transform: translateY(-15px); } }

.zzz {
  font-family: 'Arial', sans-serif;
  font-weight: 900;
  color: #fbbf24;
  opacity: 0;
  animation: zzz-float 3s infinite;
}
.z1 { animation-delay: 0s; font-size: 16px; }
.z2 { animation-delay: 1s; font-size: 12px; margin-left: 10px; }
.z3 { animation-delay: 2s; font-size: 10px; margin-left: 20px; }
@keyframes zzz-float {
  0% { transform: translate(0, 0); opacity: 0; }
  20% { opacity: 0.8; }
  100% { transform: translate(25px, -50px); opacity: 0; }
}



.animate-fade-in { animation: fadeIn 0.4s ease-out; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }

@media (max-width: 768px) {
  .hide-on-mobile { display: none; }
}
</style>
