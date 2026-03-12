import { reactive } from 'vue';

const state = reactive({
  toasts: []
});

export const useToast = () => {
  const addToast = (message, type = 'info', duration = 3000) => {
    const id = Date.now();
    state.toasts.push({
      id,
      message,
      type,
      duration
    });

    setTimeout(() => {
      removeToast(id);
    }, duration);
  };

  const removeToast = (id) => {
    const index = state.toasts.findIndex(t => t.id === id);
    if (index !== -1) {
      state.toasts.splice(index, 1);
    }
  };

  const success = (message, duration) => addToast(message, 'success', duration);
  const error = (message, duration) => addToast(message, 'error', duration);
  const info = (message, duration) => addToast(message, 'info', duration);
  const warning = (message, duration) => addToast(message, 'warning', duration);

  return {
    toasts: state.toasts,
    addToast,
    removeToast,
    success,
    error,
    info,
    warning
  };
};
