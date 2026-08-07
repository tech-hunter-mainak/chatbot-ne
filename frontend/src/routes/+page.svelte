<script>
  // No external dependencies needed. All icons are inline SVGs for perfect replication.
</script>

<div class="flex h-screen bg-[#030303] text-gray-200 font-sans overflow-hidden selection:bg-purple-900 selection:text-white">
  
  <!-- SIDEBAR (Hidden on smaller screens, visible on md and up) -->
  <aside class="w-[280px] bg-[#09090b] border-r border-[#1f1f22] flex-col hidden md:flex z-20 shadow-2xl shadow-black">
    
    <!-- Logo & Top Actions -->
    <div class="p-4 flex items-center justify-between mt-2">
      <div class="flex items-center gap-3">
        <!-- WhispAI Logo Icon -->
        <div class="w-8 h-8 rounded-xl bg-gradient-to-br from-purple-400 via-fuchsia-500 to-purple-600 p-[1px]">
          <div class="w-full h-full bg-[#1a0f2e] rounded-xl flex items-center justify-center">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="url(#logo-grad)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <defs>
                <linearGradient id="logo-grad" x1="0" y1="0" x2="24" y2="24">
                  <stop offset="0%" stop-color="#c084fc" />
                  <stop offset="100%" stop-color="#e879f9" />
                </linearGradient>
              </defs>
              <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/>
              <circle cx="12" cy="12" r="3"/>
            </svg>
          </div>
        </div>
        <span class="font-semibold text-base tracking-wide text-white">WhispAI</span>
      </div>
      <div class="flex items-center gap-3 text-gray-400">
        <button class="hover:text-white transition-colors"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg></button>
        <button class="hover:text-white transition-colors"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><path d="M9 3v18"/></svg></button>
      </div>
    </div>

    <!-- New Chat Button -->
    <div class="px-4 py-2">
      <button class="w-full py-2.5 px-4 rounded-xl border border-purple-900/40 bg-gradient-to-r from-purple-900/10 to-transparent hover:border-purple-500/50 hover:bg-purple-900/20 flex items-center gap-2 text-sm text-fuchsia-300 transition-all duration-200">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z"/></svg>
        New Chat
      </button>
    </div>

    <!-- Sidebar Scrollable Area -->
    <div class="flex-1 overflow-y-auto px-4 py-4 space-y-7 scrollbar-thin scrollbar-thumb-gray-800 scrollbar-track-transparent">
      
      <!-- FEATURES -->
      <div>
        <h3 class="text-[10px] font-bold text-gray-500 mb-2 tracking-wider">FEATURES</h3>
        <ul class="space-y-[2px]">
          <li class="px-3 py-2 bg-[#16161a] rounded-lg text-sm flex items-center gap-3 text-white cursor-pointer border border-[#27272a]">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/></svg>
            AI Chat
          </li>
          <li class="px-3 py-2 text-gray-400 hover:bg-[#16161a] hover:text-white rounded-lg text-sm flex items-center gap-3 cursor-pointer transition-colors">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="16" height="18" x="4" y="3" rx="2"/><path d="M8 3v18"/><path d="M12 7h4"/><path d="M12 11h4"/><path d="M12 15h4"/></svg>
            Library
          </li>
        </ul>
      </div>

      <!-- TODAY -->
      <div>
        <h3 class="text-[10px] font-bold text-gray-500 mb-2 tracking-wider">TODAY</h3>
        <ul class="space-y-2.5 text-[13px] text-gray-400">
          <li class="truncate hover:text-white cursor-pointer transition-colors">Design a retro-themed dashboard</li>
          <li class="truncate hover:text-white cursor-pointer transition-colors">Create an 80s-inspired cityscape</li>
          <li class="truncate hover:text-white cursor-pointer transition-colors">Generate a retro digital watch</li>
          <li class="truncate hover:text-white cursor-pointer transition-colors">Illustrate a funky 70s living room w...</li>
          <li class="truncate hover:text-white cursor-pointer transition-colors">Render a retro computer UI with p...</li>
        </ul>
      </div>

      <!-- YESTERDAY -->
      <div>
        <h3 class="text-[10px] font-bold text-gray-500 mb-2 tracking-wider">YESTERDAY</h3>
        <ul class="space-y-2.5 text-[13px] text-gray-400">
          <li class="truncate hover:text-white cursor-pointer transition-colors">Retro style image generation with</li>
          <li class="truncate hover:text-white cursor-pointer transition-colors">Text for a business solution for a n...</li>
          <li class="truncate hover:text-white cursor-pointer transition-colors">Exporting files from the database</li>
        </ul>
      </div>
    </div>

    <!-- Upgrade Card -->
    <div class="p-4 pb-6 mt-auto">
      <div class="relative p-5 rounded-2xl overflow-hidden border border-[#27272a] group shadow-lg">
        <!-- Glow effects -->
        <div class="absolute inset-0 bg-gradient-to-t from-fuchsia-600/30 via-purple-900/10 to-transparent"></div>
        <div class="absolute bottom-0 left-1/2 -translate-x-1/2 w-24 h-12 bg-fuchsia-500/40 blur-[30px]"></div>
        
        <div class="relative z-10 flex flex-col items-center text-center">
          <!-- Avatars -->
          <div class="flex -space-x-3 mb-3">
            <img class="w-8 h-8 rounded-full border-[3px] border-[#101014] object-cover bg-gray-800" src="https://i.pravatar.cc/100?img=1" alt="User 1">
            <img class="w-9 h-9 rounded-full border-[3px] border-[#101014] object-cover z-10 -mt-0.5 bg-gray-700" src="https://i.pravatar.cc/100?img=11" alt="User 2">
            <img class="w-8 h-8 rounded-full border-[3px] border-[#101014] object-cover bg-gray-800" src="https://i.pravatar.cc/100?img=3" alt="User 3">
          </div>
          <h4 class="font-medium text-white mb-0.5 text-[15px]">Upgrade to Pro</h4>
          <p class="text-[11px] text-gray-400 mb-4 leading-tight">Unlock more power<br>and features</p>
          <button class="w-full bg-white text-black font-semibold py-2 rounded-xl text-[13px] flex items-center justify-center gap-1.5 hover:bg-gray-100 transition-colors shadow-[0_0_15px_rgba(255,255,255,0.3)]">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" stroke="none"><path d="M12 2l2.4 7.6 7.6 2.4-7.6 2.4L12 22l-2.4-7.6-7.6-2.4 7.6-2.4L12 2z"/></svg>
            Upgrade
          </button>
        </div>
      </div>
    </div>
  </aside>

  <!-- MAIN CONTENT -->
  <main class="flex-1 flex flex-col relative overflow-hidden bg-[#070709]">
    
    <!-- Giant Background Ambient Glow -->
    <div class="absolute top-[-10%] left-1/2 -translate-x-1/2 w-[700px] h-[500px] bg-fuchsia-900/15 blur-[120px] rounded-[100%] pointer-events-none z-0"></div>

    <!-- Top Navigation -->
    <header class="h-16 flex items-center justify-between px-6 z-10 relative mt-2">
      <!-- Left side: Dropdown -->
      <div class="flex items-center gap-2 cursor-pointer hover:text-white transition-colors text-sm font-medium text-gray-300">
        NodeAI-1
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg>
      </div>

      <!-- Right side: Links & Profile -->
      <div class="flex items-center gap-6">
        <nav class="hidden md:flex items-center gap-6 text-[13px] font-medium text-gray-400">
          <a href="#" class="text-white">Dashboard</a>
          <a href="#" class="hover:text-white transition-colors">Labs</a>
          <a href="#" class="hover:text-white transition-colors">Help & Support</a>
          <a href="#" class="hover:text-white transition-colors">Core</a>
        </nav>
        
        <div class="flex items-center gap-4 ml-2">
          <!-- Theme Toggle -->
          <button class="p-2 rounded-full bg-[#16161a] border border-[#27272a] text-gray-400 hover:text-white transition-colors">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/></svg>
          </button>
          <!-- User Avatar -->
          <img src="https://i.pravatar.cc/150?img=11" class="w-8 h-8 rounded-full border border-[#27272a] object-cover bg-gray-800" alt="Current User" />
        </div>
      </div>
    </header>

    <!-- Chat Area / Hero Section -->
    <div class="flex-1 overflow-y-auto z-10 relative flex flex-col items-center pt-[8vh] px-4 pb-12 w-full">
      
      <!-- Big Center Logo -->
      <div class="w-14 h-14 rounded-2xl bg-gradient-to-b from-[#2a1b38] to-[#1a1025] border border-fuchsia-900/30 flex items-center justify-center mb-8 shadow-[0_0_30px_rgba(192,132,252,0.15)] p-0.5">
         <div class="w-full h-full bg-[#110a18] rounded-xl flex items-center justify-center">
            <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="url(#center-logo-grad)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <defs>
                <linearGradient id="center-logo-grad" x1="0" y1="0" x2="24" y2="24">
                  <stop offset="0%" stop-color="#d946ef" />
                  <stop offset="100%" stop-color="#9333ea" />
                </linearGradient>
              </defs>
              <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/>
              <circle cx="12" cy="12" r="3" fill="#a855f7" />
            </svg>
         </div>
      </div>

      <!-- Welcome Text -->
      <h1 class="text-[26px] md:text-3xl font-medium mb-1.5 text-center text-gray-300/80">Good to see you!</h1>
      <h2 class="text-[32px] md:text-[40px] font-semibold mb-5 text-center text-gray-100 tracking-tight">How Can I Assist You?</h2>
      <p class="text-gray-400/80 text-center max-w-lg mb-10 text-[13px] md:text-sm">Quickly find answers, get assistance, and explore AI-<br class="hidden md:block">powered insights-all in one place</p>

      <!-- Input Interface -->
      <div class="w-full max-w-[700px] bg-[#101014] border border-[#27272a] rounded-2xl p-2.5 mb-10 shadow-lg">
        <input 
          type="text" 
          placeholder="Ask anything ..." 
          class="w-full bg-transparent border-none outline-none text-gray-200 px-3 py-3 text-[15px] placeholder-gray-500 mb-2" 
        />
        
        <div class="flex items-center justify-between px-1">
          <!-- Left Action Buttons -->
          <div class="flex items-center gap-2">
            <button class="flex items-center gap-2 bg-[#1a1a1f] hover:bg-[#27272a] text-gray-300 px-3 py-1.5 rounded-lg text-[13px] font-medium transition-colors border border-[#27272a]">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
              Search
            </button>
            <button class="flex items-center gap-2 bg-[#1a1a1f] hover:bg-[#27272a] text-gray-300 px-3 py-1.5 rounded-lg text-[13px] font-medium transition-colors border border-[#27272a]">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/></svg>
              Create Image
            </button>
            <button class="flex items-center justify-center w-[30px] h-[30px] bg-[#1a1a1f] hover:bg-[#27272a] text-gray-400 rounded-lg transition-colors border border-[#27272a]">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="1"/><circle cx="19" cy="12" r="1"/><circle cx="5" cy="12" r="1"/></svg>
            </button>
          </div>
          
          <!-- Right Action Buttons -->
          <div class="flex items-center gap-2">
            <button class="w-8 h-8 flex items-center justify-center text-gray-400 hover:text-white transition-colors bg-[#1a1a1f] rounded-lg border border-[#27272a]">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" x2="12" y1="19" y2="22"/></svg>
            </button>
            <button class="w-8 h-8 bg-white text-black rounded-full flex items-center justify-center hover:bg-gray-200 transition-colors shadow-md">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="m18 15-6-6-6 6"/></svg>
            </button>
          </div>
        </div>
      </div>

      <!-- Suggestions Grid -->
      <div class="w-full max-w-[700px]">
        <p class="text-[12px] text-gray-500 mb-4 px-1">Get started with an example below</p>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3.5">
          
          <!-- Card 1 -->
          <div class="bg-[#101014] border border-[#27272a] hover:border-gray-600 hover:bg-[#15151a] cursor-pointer rounded-xl p-5 transition-all duration-200 group flex flex-col justify-between min-h-[140px]">
            <div>
              <h3 class="font-medium text-gray-200 text-sm mb-1.5">Launch Your AI Assistant</h3>
              <p class="text-[13px] text-gray-500 leading-relaxed pr-2">Design an AI agent with custom skills and goals—tailored to your workflow and users.</p>
            </div>
            <div class="mt-4 flex items-center text-[12px] font-medium text-gray-400 group-hover:text-gray-200 transition-colors">
              Learn more <span class="ml-1 transition-transform group-hover:translate-x-0.5">→</span>
            </div>
          </div>
          
          <!-- Card 2 -->
          <div class="bg-[#101014] border border-[#27272a] hover:border-gray-600 hover:bg-[#15151a] cursor-pointer rounded-xl p-5 transition-all duration-200 group flex flex-col justify-between min-h-[140px]">
            <div>
              <h3 class="font-medium text-gray-200 text-sm mb-1.5">Fine-tune a model</h3>
              <p class="text-[13px] text-gray-500 leading-relaxed pr-2">Create and deploy a fine-tuned model from your own data.</p>
            </div>
            <div class="mt-4 flex items-center text-[12px] font-medium text-gray-400 group-hover:text-gray-200 transition-colors">
              Learn more <span class="ml-1 transition-transform group-hover:translate-x-0.5">→</span>
            </div>
          </div>
          
          <!-- Card 3 -->
          <div class="bg-[#101014] border border-[#27272a] hover:border-gray-600 hover:bg-[#15151a] cursor-pointer rounded-xl p-5 transition-all duration-200 group flex flex-col justify-between min-h-[140px]">
            <div>
              <h3 class="font-medium text-gray-200 text-sm mb-1.5">API Requests</h3>
              <p class="text-[13px] text-gray-500 leading-relaxed pr-2">Make your first Chat completion API requests.</p>
            </div>
            <div class="mt-4 flex items-center text-[12px] font-medium text-gray-400 group-hover:text-gray-200 transition-colors">
              Learn more <span class="ml-1 transition-transform group-hover:translate-x-0.5">→</span>
            </div>
          </div>
          
          <!-- Card 4 -->
          <div class="bg-[#101014] border border-[#27272a] hover:border-gray-600 hover:bg-[#15151a] cursor-pointer rounded-xl p-5 transition-all duration-200 group flex flex-col justify-between min-h-[140px]">
            <div>
              <h3 class="font-medium text-gray-200 text-sm mb-1.5">Download & Self-Deployment of models</h3>
              <p class="text-[13px] text-gray-500 leading-relaxed pr-2">Explore our market-leading open models.</p>
            </div>
            <div class="mt-4 flex items-center text-[12px] font-medium text-gray-400 group-hover:text-gray-200 transition-colors">
              Learn more <span class="ml-1 transition-transform group-hover:translate-x-0.5">→</span>
            </div>
          </div>

        </div>
      </div>
      
    </div>
  </main>
</div>