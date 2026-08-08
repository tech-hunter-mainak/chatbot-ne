<script lang="ts">
  import { onMount } from 'svelte';

  type MessageRole = 'user' | 'bot';

  interface ChatMessage {
    id: number;
    role: MessageRole;
    content: string;
  }

  // Chat State Management
  let inputValue = $state('');
  let messages = $state<ChatMessage[]>([]);
  let isChatting = $state(false);
  let nextMessageId = 1;
  
  // Sidebar State Management
  let isSidebarOpen = $state(true);

  // Default languages to send to backend (can be dynamically bound to UI later)
  let currentUserLang = 'English';
  let currentDestLang = 'Assamese';

  onMount(() => {
    // Automatically close sidebar on mobile devices upon loading
    if (typeof window !== 'undefined' && window.innerWidth < 768) {
      isSidebarOpen = false;
    }
  });

  function addMessage(role: MessageRole, content: string) {
    messages = [...messages, { id: nextMessageId++, role, content }];
  }

  // UPDATED: Now makes an actual API call to FastAPI backend
  async function handleSend() {
    if (!inputValue.trim()) return;

    const userMessage = inputValue;
    addMessage('user', userMessage);
    inputValue = '';
    isChatting = true;

    try {
      const response = await fetch('http://127.0.0.1:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          query: userMessage,
          language: 'kha'
        })
      });

      if (!response.ok) {
        throw new Error(`Backend returned ${response.status}`);
      }

      const data = await response.json();

      console.log('Backend response:', data);

      addMessage('bot', data.answer);

    } catch (error) {
      console.error('Error communicating with backend:', error);

      addMessage(
        'bot',
        "Sorry, I couldn't connect to the server. Please ensure the backend is running."
      );
    }
  }

  function handleKeyDown(event: KeyboardEvent) {
    if (event.key === 'Enter') {
      handleSend();
    }
  }

  function startNewChat() {
    messages = [];
    isChatting = false;
    inputValue = '';
    
    if (typeof window !== 'undefined' && window.innerWidth < 768) {
      isSidebarOpen = false;
    }
  }

  function handleSuggestion(text: string) {
    inputValue = text;
    handleSend();
  }

  function loadMockHistory(title: string) {
    messages = [
      { id: nextMessageId++, role: 'user', content: `Can we talk about: ${title}?` },
      { id: nextMessageId++, role: 'bot', content: `Sure! Loading context for "${title}". How can I help you continue this discussion in a North Eastern language?` }
    ];
    isChatting = true;
    
    if (typeof window !== 'undefined' && window.innerWidth < 768) {
      isSidebarOpen = false;
    }
  }

  function comingSoon(feature: string) {
    alert(`${feature} feature will be integrated with the backend API soon!`);
  }
</script>

<div class="flex h-screen bg-[#030303] text-gray-200 font-sans overflow-hidden selection:bg-purple-900 selection:text-white relative">
  
  <!-- Mobile Sidebar Backdrop Overlay -->
  {#if isSidebarOpen}
    <div 
      class="fixed inset-0 bg-black/60 z-30 md:hidden backdrop-blur-sm transition-opacity" 
      on:click={() => isSidebarOpen = false}
      role="button"
      tabindex="0"
      aria-hidden="true"
    ></div>
  {/if}

  <!-- SIDEBAR -->
  <aside class="
    fixed md:relative z-40 inset-y-0 left-0 h-full bg-[#09090b] border-[#1f1f22] shadow-2xl shadow-black transition-all duration-300 ease-in-out overflow-hidden shrink-0
    {isSidebarOpen ? 'w-[280px] translate-x-0 border-r opacity-100' : 'w-[280px] -translate-x-full border-r md:w-0 md:translate-x-0 md:border-r-0 md:opacity-0'}
  ">
    <!-- Inner fixed-width container prevents text squishing during collapse animation -->
    <div class="w-[280px] h-full flex flex-col pb-4">
      <!-- Logo & Top Actions -->
      <div class="p-4 flex items-center justify-between mt-2">
        <div class="flex items-center gap-3">
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
        <div class="flex items-center gap-2 text-gray-400">
          <button on:click={() => comingSoon('Search Sidebar')} class="hover:text-white transition-colors p-1.5 rounded-lg hover:bg-[#16161a]" aria-label="Search">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
          </button>
          <button on:click={() => isSidebarOpen = false} class="hover:text-white transition-colors p-1.5 rounded-lg hover:bg-[#16161a]" aria-label="Close sidebar">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><path d="M9 3v18"/></svg>
          </button>
        </div>
      </div>

      <!-- New Chat Button -->
      <div class="px-4 py-2">
        <button on:click={startNewChat} class="w-full py-2.5 px-4 rounded-xl border border-purple-900/40 bg-gradient-to-r from-purple-900/10 to-transparent hover:border-purple-500/50 hover:bg-purple-900/20 flex items-center gap-2 text-sm text-fuchsia-300 transition-all duration-200">
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
            <li>
              <button on:click={startNewChat} class="w-full px-3 py-2 bg-[#16161a] rounded-lg text-sm flex items-center gap-3 text-white border border-[#27272a] text-left transition-colors">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/></svg>
                AI Chat
              </button>
            </li>
            <li>
              <button on:click={() => comingSoon('Library')} class="w-full px-3 py-2 text-gray-400 hover:bg-[#16161a] hover:text-white rounded-lg text-sm flex items-center gap-3 text-left transition-colors">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="16" height="18" x="4" y="3" rx="2"/><path d="M8 3v18"/><path d="M12 7h4"/><path d="M12 11h4"/><path d="M12 15h4"/></svg>
                Library
              </button>
            </li>
          </ul>
        </div>

        <!-- TODAY -->
        <div>
          <h3 class="text-[10px] font-bold text-gray-500 mb-2 tracking-wider">TODAY</h3>
          <ul class="space-y-1">
            <li><button on:click={() => loadMockHistory('Assamese grammar structure')} class="w-full text-left truncate py-1.5 text-[13px] text-gray-400 hover:text-white transition-colors">Assamese grammar structure</button></li>
            <li><button on:click={() => loadMockHistory('Translate to Bodo')} class="w-full text-left truncate py-1.5 text-[13px] text-gray-400 hover:text-white transition-colors">Translate English phrases to Bodo</button></li>
            <li><button on:click={() => loadMockHistory('Manipuri script history')} class="w-full text-left truncate py-1.5 text-[13px] text-gray-400 hover:text-white transition-colors">Manipuri script history</button></li>
          </ul>
        </div>

        <!-- YESTERDAY -->
        <div>
          <h3 class="text-[10px] font-bold text-gray-500 mb-2 tracking-wider">YESTERDAY</h3>
          <ul class="space-y-1">
            <li><button on:click={() => loadMockHistory('Khasi pronunciation guide')} class="w-full text-left truncate py-1.5 text-[13px] text-gray-400 hover:text-white transition-colors">Khasi pronunciation guide</button></li>
            <li><button on:click={() => loadMockHistory('Mizo vocabulary building')} class="w-full text-left truncate py-1.5 text-[13px] text-gray-400 hover:text-white transition-colors">Mizo vocabulary building</button></li>
          </ul>
        </div>
      </div>
    </div>
  </aside>

  <!-- MAIN CONTENT -->
  <main class="flex-1 flex flex-col relative overflow-hidden bg-[#070709] min-w-0">
    
    <!-- Giant Background Ambient Glow -->
    <div class="absolute top-[-10%] left-1/2 -translate-x-1/2 w-[700px] h-[500px] bg-fuchsia-900/15 blur-[120px] rounded-[100%] pointer-events-none z-0"></div>

    <!-- Top Navigation -->
    <header class="h-16 flex items-center justify-between px-6 z-10 relative mt-2 shrink-0">
      
      <!-- Left side header -->
      <div class="flex items-center gap-3">
        <!-- Sidebar Toggle Button (Shows when sidebar is closed) -->
        {#if !isSidebarOpen}
          <button on:click={() => isSidebarOpen = true} class="text-gray-400 hover:text-white transition-colors p-1.5 -ml-1.5 rounded-lg hover:bg-[#16161a] border border-transparent hover:border-[#27272a]" aria-label="Open sidebar">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><path d="M9 3v18"/></svg>
          </button>
        {/if}

        <button on:click={() => comingSoon('Model Selector')} class="flex items-center gap-2 hover:text-white transition-colors text-sm font-medium text-gray-300">
          NodeAI-1
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg>
        </button>
      </div>

      <!-- Right side header -->
      <div class="flex items-center gap-6">
        <nav class="hidden md:flex items-center gap-6 text-[13px] font-medium text-gray-400">
          <button on:click={startNewChat} class="text-white hover:text-white transition-colors">Dashboard</button>
          <button on:click={() => comingSoon('Labs')} class="hover:text-white transition-colors">Labs</button>
          <button on:click={() => comingSoon('Help')} class="hover:text-white transition-colors">Help & Support</button>
          <button on:click={() => comingSoon('Core')} class="hover:text-white transition-colors">Core</button>
        </nav>
        
        <div class="flex items-center gap-4 ml-2">
          <button on:click={() => comingSoon('Theme Toggle')} class="p-2 rounded-full bg-[#16161a] border border-[#27272a] text-gray-400 hover:text-white transition-colors" aria-label="Toggle Theme">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/></svg>
          </button>
          <button on:click={() => comingSoon('Profile Menu')} class="rounded-full overflow-hidden border border-[#27272a]">
            <img src="https://i.pravatar.cc/150?img=11" class="w-8 h-8 object-cover bg-gray-800 block" alt="Current User" />
          </button>
        </div>
      </div>
    </header>

    <!-- Scrollable Area -->
    <div class="flex-1 overflow-y-auto z-10 relative flex flex-col w-full scroll-smooth">
      
      {#if !isChatting}
        <!-- HERO SECTION (Centered content) -->
        <div class="flex-1 flex flex-col items-center pt-[10vh] px-4 w-full max-w-[750px] mx-auto pb-16">
          
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

          <h1 class="text-[26px] md:text-3xl font-medium mb-1.5 text-center text-gray-300/80">Good to see you!</h1>
          <h2 class="text-[32px] md:text-[40px] font-semibold mb-5 text-center text-gray-100 tracking-tight">How Can I Assist You?</h2>
          <p class="text-gray-400/80 text-center max-w-lg mb-10 text-[13px] md:text-sm">Explore North Eastern languages, translate phrases, and<br class="hidden md:block"> learn cultural insights—all in one place.</p>

          <!-- Input Box (Hero Flow) -->
          <div class="w-full max-w-[700px] bg-[#101014] border border-[#27272a] rounded-2xl p-2.5 mb-10 shadow-lg">
            <input 
              bind:value={inputValue}
              on:keydown={handleKeyDown}
              type="text" 
              placeholder="Ask me anything in or about North Eastern languages..." 
              class="w-full bg-transparent border-none outline-none text-gray-200 px-3 py-3 text-[15px] placeholder-gray-500 mb-2 focus:ring-0" 
            />
            <div class="flex items-center justify-between px-1">
              <div class="flex items-center gap-2">
                <button on:click={() => comingSoon('Web Search')} class="flex items-center gap-2 bg-[#1a1a1f] hover:bg-[#27272a] text-gray-300 px-3 py-1.5 rounded-lg text-[13px] font-medium transition-colors border border-[#27272a]">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
                  Search
                </button>
                <button on:click={() => comingSoon('Image Generation')} class="flex items-center gap-2 bg-[#1a1a1f] hover:bg-[#27272a] text-gray-300 px-3 py-1.5 rounded-lg text-[13px] font-medium transition-colors border border-[#27272a]">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/></svg>
                  Create Image
                </button>
                <button on:click={() => comingSoon('More Options')} class="flex items-center justify-center w-[30px] h-[30px] bg-[#1a1a1f] hover:bg-[#27272a] text-gray-400 rounded-lg transition-colors border border-[#27272a]">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="1"/><circle cx="19" cy="12" r="1"/><circle cx="5" cy="12" r="1"/></svg>
                </button>
              </div>
              <div class="flex items-center gap-2">
                <button on:click={() => comingSoon('Voice Input')} class="w-8 h-8 flex items-center justify-center text-gray-400 hover:text-white transition-colors bg-[#1a1a1f] rounded-lg border border-[#27272a]">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" x2="12" y1="19" y2="22"/></svg>
                </button>
                <button on:click={handleSend} disabled={!inputValue.trim()} class="w-8 h-8 {inputValue.trim() ? 'bg-white text-black hover:bg-gray-200' : 'bg-gray-700 text-gray-400'} rounded-full flex items-center justify-center transition-colors shadow-md">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="m18 15-6-6-6 6"/></svg>
                </button>
              </div>
            </div>
          </div>

          <!-- Suggestions Grid -->
          <div class="w-full max-w-[700px]">
            <p class="text-[12px] text-gray-500 mb-4 px-1 text-left">Get started with an example below</p>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-3.5">
              <button on:click={() => handleSuggestion("Teach me basic greetings in Assamese")} class="bg-[#101014] text-left border border-[#27272a] hover:border-gray-600 hover:bg-[#15151a] cursor-pointer rounded-xl p-5 transition-all duration-200 group flex flex-col justify-between min-h-[120px]">
                <div>
                  <h3 class="font-medium text-gray-200 text-sm mb-1.5">Learn Basic Greetings</h3>
                  <p class="text-[13px] text-gray-500 leading-relaxed pr-2">Learn how to say Hello and Thank you in Assamese.</p>
                </div>
                <div class="mt-4 flex items-center text-[12px] font-medium text-gray-400 group-hover:text-gray-200 transition-colors">
                  Try it <span class="ml-1 transition-transform group-hover:translate-x-0.5">→</span>
                </div>
              </button>
              
              <button on:click={() => handleSuggestion("Translate 'How are you' to Manipuri")} class="bg-[#101014] text-left border border-[#27272a] hover:border-gray-600 hover:bg-[#15151a] cursor-pointer rounded-xl p-5 transition-all duration-200 group flex flex-col justify-between min-h-[120px]">
                <div>
                  <h3 class="font-medium text-gray-200 text-sm mb-1.5">Quick Translation</h3>
                  <p class="text-[13px] text-gray-500 leading-relaxed pr-2">Translate common English phrases into Manipuri.</p>
                </div>
                <div class="mt-4 flex items-center text-[12px] font-medium text-gray-400 group-hover:text-gray-200 transition-colors">
                  Try it <span class="ml-1 transition-transform group-hover:translate-x-0.5">→</span>
                </div>
              </button>
              
              <button on:click={() => handleSuggestion("Explain the grammar structure of Mizo")} class="bg-[#101014] text-left border border-[#27272a] hover:border-gray-600 hover:bg-[#15151a] cursor-pointer rounded-xl p-5 transition-all duration-200 group flex flex-col justify-between min-h-[120px]">
                <div>
                  <h3 class="font-medium text-gray-200 text-sm mb-1.5">Mizo Grammar Rules</h3>
                  <p class="text-[13px] text-gray-500 leading-relaxed pr-2">Understand sentence structures and tones in Mizo.</p>
                </div>
                <div class="mt-4 flex items-center text-[12px] font-medium text-gray-400 group-hover:text-gray-200 transition-colors">
                  Try it <span class="ml-1 transition-transform group-hover:translate-x-0.5">→</span>
                </div>
              </button>
              
              <button on:click={() => handleSuggestion("Tell me a cultural story from the Bodo community")} class="bg-[#101014] text-left border border-[#27272a] hover:border-gray-600 hover:bg-[#15151a] cursor-pointer rounded-xl p-5 transition-all duration-200 group flex flex-col justify-between min-h-[120px]">
                <div>
                  <h3 class="font-medium text-gray-200 text-sm mb-1.5">Cultural Stories</h3>
                  <p class="text-[13px] text-gray-500 leading-relaxed pr-2">Discover folklore and traditions from the Bodo community.</p>
                </div>
                <div class="mt-4 flex items-center text-[12px] font-medium text-gray-400 group-hover:text-gray-200 transition-colors">
                  Try it <span class="ml-1 transition-transform group-hover:translate-x-0.5">→</span>
                </div>
              </button>
            </div>
          </div>
        </div>

      {:else}
        <!-- ACTIVE CHAT VIEW -->
        <div class="flex-1 w-full max-w-[750px] mx-auto p-4 flex flex-col gap-6 pb-40 mt-4">
          {#each messages as msg}
            {#if msg.role === 'user'}
              <div class="self-end bg-[#16161a] border border-[#27272a] text-white px-5 py-3.5 rounded-2xl max-w-[85%] text-[15px] shadow-sm">
                {msg.content}
              </div>
            {:else}
              <div class="self-start flex gap-4 max-w-[90%]">
                <div class="w-8 h-8 rounded-full bg-gradient-to-br from-purple-500 to-fuchsia-600 flex items-center justify-center shrink-0 mt-1">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/>
                    <circle cx="12" cy="12" r="3"/>
                  </svg>
                </div>
                <div class="text-gray-300 text-[15px] leading-relaxed pt-1.5">
                  {msg.content}
                </div>
              </div>
            {/if}
          {/each}
        </div>
      {/if}
    </div>

    <!-- STICKY INPUT CONTAINER (Only visible when chatting) -->
    {#if isChatting}
      <div class="absolute bottom-0 left-0 right-0 z-20 flex justify-center bg-gradient-to-t from-[#070709] via-[#070709] to-transparent pb-8 pt-12 px-4">
        <div class="w-full max-w-[700px] bg-[#101014] border border-[#27272a] rounded-2xl p-2.5 shadow-2xl">
          <input 
            bind:value={inputValue}
            on:keydown={handleKeyDown}
            type="text" 
            placeholder="Ask me anything in or about North Eastern languages..." 
            class="w-full bg-transparent border-none outline-none text-gray-200 px-3 py-3 text-[15px] placeholder-gray-500 mb-2 focus:ring-0" 
          />
          <div class="flex items-center justify-between px-1">
            <div class="flex items-center gap-2">
              <button on:click={() => comingSoon('Web Search')} class="flex items-center gap-2 bg-[#1a1a1f] hover:bg-[#27272a] text-gray-300 px-3 py-1.5 rounded-lg text-[13px] font-medium transition-colors border border-[#27272a]">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
                Search
              </button>
              <button on:click={() => comingSoon('Image Generation')} class="flex items-center gap-2 bg-[#1a1a1f] hover:bg-[#27272a] text-gray-300 px-3 py-1.5 rounded-lg text-[13px] font-medium transition-colors border border-[#27272a]">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/></svg>
                Create Image
              </button>
              <button on:click={() => comingSoon('More Options')} class="flex items-center justify-center w-[30px] h-[30px] bg-[#1a1a1f] hover:bg-[#27272a] text-gray-400 rounded-lg transition-colors border border-[#27272a]">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="1"/><circle cx="19" cy="12" r="1"/><circle cx="5" cy="12" r="1"/></svg>
              </button>
            </div>
            <div class="flex items-center gap-2">
              <button on:click={() => comingSoon('Voice Input')} class="w-8 h-8 flex items-center justify-center text-gray-400 hover:text-white transition-colors bg-[#1a1a1f] rounded-lg border border-[#27272a]">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" x2="12" y1="19" y2="22"/></svg>
              </button>
              <button on:click={handleSend} disabled={!inputValue.trim()} class="w-8 h-8 {inputValue.trim() ? 'bg-white text-black hover:bg-gray-200' : 'bg-gray-700 text-gray-400'} rounded-full flex items-center justify-center transition-colors shadow-md">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="m18 15-6-6-6 6"/></svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    {/if}

  </main>
</div>