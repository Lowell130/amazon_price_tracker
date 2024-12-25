<template>
    <button
      @click="toggleTheme"
      class="rounded focus:outline-none focus:ring-2 focus:ring-gray-300 dark:focus:ring-gray-600"
    >
      <svg
        v-if="isDarkMode"
        xmlns="http://www.w3.org/2000/svg"
        class="h-6 w-6 text-gray-300"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
        stroke-width="2"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          d="M12 3v1m0 16v1m8-8h1M4 12H3m15.364 6.364-.707.707M6.343 6.343l-.707-.707m12.728 0-.707.707M6.343 17.657l-.707-.707M12 5a7 7 0 0 1 0 14 7 7 0 0 1 0-14z"
        />
      </svg>
      <svg
      v-else class="w-6 h-6 text-gray-300 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
  <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 21a9 9 0 0 1-.5-17.986V3c-.354.966-.5 1.911-.5 3a9 9 0 0 0 9 9c.239 0 .254.018.488 0A9.004 9.004 0 0 1 12 21Z"/>
</svg>

    </button>
  </template>
  
  <script>
  export default {
    data() {
      return {
        isDarkMode: false,
      };
    },
    mounted() {
      // Load the initial theme from localStorage
      this.isDarkMode = localStorage.getItem('theme') === 'dark';
      if (this.isDarkMode) {
        document.documentElement.classList.add('dark');
      }
    },
    methods: {
      toggleTheme() {
        this.isDarkMode = !this.isDarkMode;
        const theme = this.isDarkMode ? 'dark' : 'light';
        localStorage.setItem('theme', theme);
        document.documentElement.classList.toggle('dark', this.isDarkMode);
      },
    },
  };
  </script>
  