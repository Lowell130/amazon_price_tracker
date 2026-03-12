<template>
  <div class="fixed top-6 right-6 z-[9999] flex flex-col gap-3 pointer-events-none">
    <transition-group 
      name="toast-list" 
      tag="div" 
      class="flex flex-col gap-3"
    >
      <div 
        v-for="toast in toasts" 
        :key="toast.id"
        class="pointer-events-auto flex items-center min-w-[300px] max-w-md p-4 rounded-2xl shadow-2xl backdrop-blur-xl border border-white/20 dark:border-gray-700/50 animate-slideIn"
        :class="[
          toast.type === 'success' ? 'bg-emerald-500/90 text-white' : 
          toast.type === 'error' ? 'bg-red-500/90 text-white' : 
          toast.type === 'warning' ? 'bg-amber-500/90 text-white' : 
          'bg-blue-600/90 text-white'
        ]"
      >
        <!-- Icon -->
        <div class="shrink-0 mr-3 p-2 bg-white/20 rounded-xl">
          <svg v-if="toast.type === 'success'" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
          </svg>
          <svg v-else-if="toast.type === 'error'" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12" />
          </svg>
          <svg v-else-if="toast.type === 'warning'" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
          <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>

        <!-- Content -->
        <div class="flex-1 text-sm font-bold tracking-tight">
          {{ toast.message }}
        </div>

        <!-- Close -->
        <button 
          @click="removeToast(toast.id)"
          class="ml-4 p-1 rounded-lg hover:bg-white/10 transition-colors"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </transition-group>
  </div>
</template>

<script>
import { useToast } from '@/store/toast'

export default {
  name: 'ToastNotification',
  setup() {
    const { toasts, removeToast } = useToast()
    return {
      toasts,
      removeToast
    }
  }
}
</script>

<style scoped>
.toast-list-enter-active,
.toast-list-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.toast-list-enter-from {
  opacity: 0;
  transform: translateX(40px) scale(0.9);
}

.toast-list-leave-to {
  opacity: 0;
  transform: scale(0.8);
}

@keyframes slideIn {
  from {
    transform: translateX(20px);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}
</style>
