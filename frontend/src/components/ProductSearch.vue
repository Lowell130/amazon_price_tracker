<template>
    <section class="py-16">
      <div class="max-w-2xl mx-auto px-4">
       
        <form @submit.prevent="redirectToSearch">
          <div class="flex flex-col sm:flex-row items-center gap-4">
            <!-- Flowbite Input -->
            <input
              v-model="query"
              type="text"
              id="search-input"
              class="w-full rounded-lg border border-gray-300 text-gray-900 focus:ring-primary-600 focus:border-primary-600 p-3 text-base"
              placeholder="Cerca un prodotto..."
            />
  
            <!-- Flowbite Button -->
            <button
              type="submit"
              class="inline-flex items-center justify-center px-5 py-3 mr-3 text-base font-medium text-center text-white rounded-lg bg-primary-700 hover:bg-primary-800 focus:ring-4 focus:ring-primary-300 dark:focus:ring-primary-900"
            >
           CERCA
            </button>
          </div>
        </form>
      </div>
    </section>
  </template>
  
  <script>
  import { useRouter } from 'vue-router'
  
  export default {
    setup() {
      const router = useRouter()
      return { router }
    },
    data() {
      return {
        query: ''
      }
    },
    methods: {
      redirectToSearch() {
        if (this.query.trim().length > 0) {
          this.$router.push({ path: '/search', query: { query: this.query } })
        }
      }
    }
  }
  </script>
  