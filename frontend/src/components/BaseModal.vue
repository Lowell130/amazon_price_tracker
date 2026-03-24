<template>
  <Transition name="fade">
    <div v-if="show" class="fixed inset-0 z-[60] flex items-center justify-center p-4 sm:p-6">
      <!-- Backdrop with blur -->
      <div 
        class="absolute inset-0 bg-gray-900/40 backdrop-blur-md transition-opacity"
        @click="$emit('close')"
      ></div>

      <!-- Modal Container -->
      <Transition name="scale">
        <div 
          v-if="show"
          class="relative w-full max-w-lg overflow-hidden rounded-3xl bg-white/80 dark:bg-gray-800/80 backdrop-blur-2xl shadow-2xl border border-white/20 dark:border-gray-700/30 transform transition-all"
        >
          <!-- Close button -->
          <button 
            @click="$emit('close')"
            class="absolute right-4 top-4 p-2 rounded-xl text-gray-400 hover:text-gray-600 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-gray-700/50 transition-colors z-10"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>

          <!-- Content slot -->
          <div class="p-6 sm:p-8">
            <slot></slot>
          </div>
        </div>
      </Transition>
    </div>
  </Transition>
</template>

<script>
export default {
  name: "BaseModal",
  props: {
    show: {
      type: Boolean,
      required: true
    }
  },
  emits: ['close']
};
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.scale-enter-active,
.scale-leave-active {
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.scale-enter-from {
  opacity: 0;
  transform: scale(0.9) translateY(20px);
}

.scale-leave-to {
  opacity: 0;
  transform: scale(0.95);
}
</style>
