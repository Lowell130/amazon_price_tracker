<template>
  <BaseModal :show="show" @close="$emit('close')">
    <div class="text-center">
      <!-- Icon Container -->
      <div 
        class="mx-auto mb-6 flex h-24 w-24 items-center justify-center rounded-[2.5rem] bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-900/40 dark:to-indigo-900/40 text-blue-600 dark:text-blue-400 shadow-xl shadow-blue-500/10 ring-4 ring-white dark:ring-gray-800"
      >
        <template v-if="loading">
          <svg class="h-12 w-12 animate-spin-slow" viewBox="0 0 24 24" fill="none">
            <circle class="opacity-10" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="3"></circle>
            <path class="opacity-90" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
        </template>
        <template v-else>
          <svg class="h-12 w-12 drop-shadow-sm" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
        </template>
      </div>

      <!-- Text Content -->
      <h3 class="mb-2 text-2xl font-black tracking-tight text-gray-900 dark:text-white">
        {{ loading ? loadingTitle : title }}
      </h3>
      <p class="mb-8 text-gray-500 dark:text-gray-400 font-medium px-4">
        {{ loading ? loadingMessage : message }}
      </p>

      <!-- Action Buttons -->
      <div v-if="!loading" class="flex flex-col sm:flex-row gap-3 justify-center px-4">
        <button
          @click="$emit('confirm')"
          class="flex-1 px-6 py-3.5 bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-black rounded-2xl shadow-lg hover:shadow-blue-500/30 hover:-translate-y-0.5 active:translate-y-0 transition-all uppercase tracking-widest text-xs"
        >
          {{ confirmText }}
        </button>
        <button
          @click="$emit('close')"
          class="flex-1 px-6 py-3.5 bg-gray-100 dark:bg-gray-700/50 text-gray-500 dark:text-gray-400 font-black rounded-2xl hover:bg-gray-200 dark:hover:bg-gray-700 transition-all uppercase tracking-widest text-xs"
        >
          Annulla
        </button>
      </div>
    </div>
  </BaseModal>
</template>

<script>
import BaseModal from "./BaseModal.vue";

export default {
  name: "ActionConfirmModal",
  components: { BaseModal },
  props: {
    show: { type: Boolean, required: true },
    loading: { type: Boolean, default: false },
    title: { type: String, default: "Conferma Azione" },
    message: { type: String, default: "Sei sicuro di voler procedere?" },
    loadingTitle: { type: String, default: "Elaborazione in corso..." },
    loadingMessage: { type: String, default: "Caricamento, attendere prego." },
    confirmText: { type: String, default: "Conferma" }
  },
  emits: ['close', 'confirm']
};
</script>

<style scoped>
@keyframes spin-slow {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.animate-spin-slow {
  animation: spin-slow 3s linear infinite;
}
</style>
