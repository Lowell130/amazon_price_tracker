<template>
  <div 
    class="skeleton-loading h-full w-full rounded-2xl"
    :class="[
      type === 'text' ? 'h-4 w-3/4 mb-3' : 
      type === 'title' ? 'h-8 w-1/2 mb-6' : 
      type === 'avatar' ? 'h-12 w-12 rounded-full' : 
      type === 'button' ? 'h-10 w-28' : 
      ''
    ]"
  ></div>
</template>

<script>
export default {
  name: 'SkeletonLoader',
  props: {
    type: {
      type: String,
      default: 'card'
    }
  }
}
</script>

<style scoped>
.skeleton-loading {
  background: linear-gradient(
    90deg, 
    rgba(226, 232, 240, 0.5) 25%, 
    rgba(241, 245, 249, 0.8) 37%, 
    rgba(226, 232, 240, 0.5) 63%
  );
  background-size: 400% 100%;
  animation: skeleton-shimmer 1.4s ease infinite;
}

.dark .skeleton-loading {
  background: linear-gradient(
    90deg, 
    rgba(31, 41, 55, 0.5) 25%, 
    rgba(55, 65, 81, 0.8) 37%, 
    rgba(31, 41, 55, 0.5) 63%
  );
  background-size: 400% 100%;
}

@keyframes skeleton-shimmer {
  0% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}
</style>
