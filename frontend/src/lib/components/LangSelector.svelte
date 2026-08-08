<script lang="ts">
  import { languages } from '$lib/config/language';

  const { currentDestLang, onLanguageChange } = $props<{
    currentDestLang: string;
    onLanguageChange: (language: string) => void;
  }>();

  let showLanguageMenu = $state(false);
</script>

<div class="relative">
  <button
    onclick={() => showLanguageMenu = !showLanguageMenu}
    class="flex items-center gap-2 bg-[#1a1a1f] hover:bg-[#27272a] text-gray-300 px-3 py-1.5 rounded-lg text-[13px] font-medium transition-colors border border-[#27272a]"
  >
    🌐
    {currentDestLang}

    <svg
      width="12"
      height="12"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      stroke-width="2"
    >
      <path d="m6 9 6 6 6-6" />
    </svg>
  </button>

  {#if showLanguageMenu}
    <div
      class="absolute bottom-10 left-0 w-40 bg-[#16161a] border border-[#27272a] rounded-xl shadow-xl overflow-hidden z-50"
    >
      {#each languages as language}
        <button
          onclick={() => {
            onLanguageChange(language.name);
            showLanguageMenu = false;
          }}
          class="w-full text-left px-3 py-2 text-sm text-gray-300 hover:bg-[#27272a] hover:text-white transition-colors"
        >
          {language.name}
        </button>
      {/each}
    </div>
  {/if}
</div>